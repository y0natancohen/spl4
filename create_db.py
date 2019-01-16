import os
import sys

from persistence import Student, Classroom, Course, repo


def main(args):
    if not os.path.isfile('schedule.db'):
        repo.init()
        repo.create_tables()
        with open(args[1], 'r') as config_file_object:
            lines = config_file_object.readlines()
            for line in lines:
                splitedLine = line.split(',')
                lineIdentifier = splitedLine[0]
                if lineIdentifier is 'S':
                    repo.students.insert(Student(splitedLine[1].strip(), splitedLine[2].strip()))
                elif lineIdentifier is 'R':
                    repo.classrooms.insert(Classroom(splitedLine[1].strip(), splitedLine[2].strip(), 0, 0))
                else:
                    repo.courses.insert(Course(splitedLine[1].strip(), splitedLine[2].strip(), splitedLine[3].strip(),
                                               splitedLine[4].strip(), splitedLine[5].strip(), splitedLine[6].strip()))

        # print all tables before exit
        repo.printAllCurrentData()


if __name__ == '__main__':
    main(sys.argv)
