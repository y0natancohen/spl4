import os
import sys

from persistence import Student, Classroom, Course, repo, printAllCurrentData


def main(args):
    if not os.path.isfile('schedule.db'):
        repo.init()
        repo.create_tables()
        with open(args[1], 'r') as config_file_object:
            lines = config_file_object.readlines()
            for line in lines:
                splited_line = line.split(',')
                line_identifier = splited_line[0]
                if line_identifier is 'S':
                    repo.students.insert(Student(splited_line[1].strip(), splited_line[2].strip()))
                elif line_identifier is 'R':
                    repo.classrooms.insert(Classroom(splited_line[1].strip(), splited_line[2].strip(), 0, 0))
                else:
                    repo.courses.insert(Course(splited_line[1].strip(), splited_line[2].strip(), splited_line[3].strip(),
                                               splited_line[4].strip(), splited_line[5].strip(), splited_line[6].strip()))

        # print all tables before exit
        printAllCurrentData()


if __name__ == '__main__':
    main(sys.argv)
