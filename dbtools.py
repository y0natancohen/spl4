import inspect


def orm(cursor, dto_type):
    # the following line retrieve the argument names of the constructor
    args = inspect.getargspec(dto_type.__init__).args

    # the first argument of the constructor will be 'self', it does not correspond
    # to any database field, so we can ignore it.
    args = args[1:]

    # gets the names of the columns returned in the cursor
    col_names = [column[0] for column in cursor.description]

    # map them into the position of the corresponding constructor argument
    col_mapping = [col_names.index(arg) for arg in args]
    return [row_map(row, col_mapping, dto_type) for row in cursor.fetchall()]


def row_map(row, col_mapping, dto_type):
    ctor_args = [row[idx] for idx in col_mapping]
    return dto_type(*ctor_args)


# we can use our method above in order to start writing a generic Dao
# note that this class is not complete and we will add methods to it next
class Dao(object):
    def __init__(self, dto_type, conn):
        self._conn = conn
        self._dto_type = dto_type

        # dto_type is a class, its __name__ field contains a string representing the name of the class.
        self._table_name = dto_type.__name__.lower() + 's'

    def insert(self, dto_instance):
        ins_dict = vars(dto_instance)
        column_names = ','.join(ins_dict.keys())
        params = ins_dict.values()
        qmarks = ','.join(['?'] * len(ins_dict))
        stmt = 'INSERT INTO {} ({}) VALUES ({})' \
            .format(self._table_name, column_names, qmarks)
        self._conn.execute(stmt, tuple(params))

    def update(self, dto_instance):
        ins_dict = vars(dto_instance)
        # for key, value in ins_dict.items():
        #     value.replace(":", '=')
        # shitty code
        if ins_dict.get('id') is not None:
            pk = 'id'
            pkVal = '{}'.format(ins_dict.get(pk))
        else:
            pk = 'grade'
            pkVal = '\'{}\''.format(ins_dict.get(pk))

        column_names = '=?,'.join(ins_dict.keys())
        column_names += '=?'
        params = ins_dict.values()
        # qmarks = ','.join(['?'] * len(ins_dict))
        stmt = 'UPDATE {} SET {} WHERE {} = {}' \
            .format(self._table_name, column_names, pk, pkVal)
        self._conn.execute(stmt, tuple(params))

    # delete
    def delete(self, keyvals):
        column_names = keyvals.keys()
        params = keyvals.values()
        stmt = 'DELETE FROM {} WHERE {}' \
            .format(self._table_name, ' AND '.join([col + '=?' for col in column_names]))
        self._conn.execute(stmt, tuple(params))

    # find all
    def find_all(self):
        c = self._conn.cursor()
        c.execute('SELECT * FROM {}'.format(self._table_name))
        return orm(c, self._dto_type)

    # find by specific attributes
    def find(self, **keyvals):
        column_names = keyvals.keys()
        params = keyvals.values()

        stmt = 'SELECT * FROM {} WHERE {}' \
            .format(self._table_name, ' AND '.join([col + '=?' for col in column_names]))

        c = self._conn.cursor()
        c.execute(stmt, tuple(params))
        return orm(c, self._dto_type)
