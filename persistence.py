import atexit
import sqlite3
from dbtools import Dao


class Student:
    def __init__(self, grade, count):
        self.grade = grade
        self.count = count


class Classroom:
    def __init__(self, id, location, current_course_id, current_course_time_left):
        self.id = id
        self.location = location
        self.current_course_id = current_course_id
        self.current_course_time_left = current_course_time_left


class Course:
    def __init__(self, id, course_name, student, number_of_students, class_id, course_length):
        self.id = id
        self.course_name = course_name
        self.student = student
        self.number_of_students = number_of_students
        self.class_id = class_id
        self.course_length = course_length


# Repository - must call init() before use
class Repository(object):
    def __init__(self):
        self._conn = None
        self.students = None
        self.classrooms = None
        self.courses = None

    def init(self):
        self._conn = sqlite3.connect('schedule.db')
        self._conn.text_factory = str
        self.students = Dao(Student, self._conn)
        self.classrooms = Dao(Classroom, self._conn)
        self.courses = Dao(Course, self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        self._conn.executescript("""
            CREATE TABLE students (
                grade      TEXT         PRIMARY KEY,
                count    INTEGER        NOT NULL
            );

            CREATE TABLE classrooms (
                id                          INTEGER    PRIMARY KEY,
                location                    TEXT       NOT NULL,
                current_course_id           INTEGER    NOT NULL,
                current_course_time_left    INTEGER    NOT NULL
            );

            CREATE TABLE courses (
                id      INTEGER     PRIMARY KEY,
                course_name  TEXT     NOT NULL,
                student           TEXT     NOT NULL,
                number_of_students  INTEGER  NOT NULL,
                class_id INTEGER REFERENCES classrooms(id),
                course_length   INTEGER     NOT NULL
            );
        """)

    def printAllCurrentData(self):
        print('courses')
        for course in repo.courses.find_all():
            print('({}, \'{}\', \'{}\', {}, {}, {})'.format(course.id, course.course_name, course.student
                                                            , course.number_of_students, course.class_id,
                                                            course.course_length))
        print('classrooms')
        for classroom in repo.classrooms.find_all():
            print('({}, \'{}\', {}, {})'.format(classroom.id, classroom.location, classroom.current_course_id,
                                                classroom.current_course_time_left))
        print('students')
        for student in repo.students.find_all():
            print('(\'{}\', {})'.format(student.grade, student.count))


# FOREIGN KEY(student_id)     REFERENCES students(id),


# singleton
repo = Repository()
atexit.register(repo._close)
