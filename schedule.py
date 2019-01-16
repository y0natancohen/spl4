import os
from persistence import repo, printAllCurrentData


def main():
    repo.init()
    iteration_num = 0
    while os.path.isfile('schedule.db') and len(repo.courses.find_all()) > 0:
        assign_classes(iteration_num)
        printAllCurrentData()
        iteration_num += 1
        for classroom in get_sorted_classrooms():
            if has_course(classroom):
                classroom.current_course_time_left -= 1
                repo.classrooms.update(classroom)


def has_course(classroom):
    return classroom.current_course_time_left != 0 and classroom.current_course_id != 0


def _print_done(classroom, course, iteration_num):
    print('({}) {}: {} is done'.format(
        iteration_num, classroom.location, course.course_name))


def _print_occupied(classroom, current_course, iteration_num):
    print('({}) {}: occupied by {}'.format(
        iteration_num, classroom.location, current_course.course_name))


def _print_start(classroom, current_course, iteration_num):
    print('({}) {}: {} is schedule to start'.format(
        iteration_num, classroom.location, current_course.course_name))


def get_sorted_classrooms():
    return sorted(repo.classrooms.find_all(), key=lambda x: x.current_course_id)


def assign_classes(iter_num, second_time=False):
    assign_again = False
    for classroom in repo.classrooms.find_all():
        for course in repo.courses.find(class_id=classroom.id):

            if classroom.current_course_time_left == 0 and classroom.current_course_id == 0:  # free
                _put_class(classroom, course, iter_num)

            elif classroom.current_course_time_left == 0 and classroom.current_course_id != 0:  # finished
                assign_again = _remove_class(classroom, course, iter_num)

            elif classroom.current_course_id == course.id:  # occupied by this course
                if not second_time:
                    _print_occupied(classroom, course, iter_num)

    if assign_again:
        assign_classes(iter_num, second_time=True)


def _remove_class(classroom, course, it_num):
    _print_done(classroom, course, it_num)
    repo.courses.delete({'id': classroom.current_course_id})
    classroom.current_course_id = 0
    repo.classrooms.update(classroom)
    assign_again = True
    return assign_again


def _put_class(classroom, course, it_num):
    classroom.current_course_id = course.id
    classroom.current_course_time_left = course.course_length
    repo.classrooms.update(classroom)
    student = repo.students.find(grade=course.student)[0]
    student.count = student.count - course.number_of_students
    repo.students.update(student)
    _print_start(classroom, course, it_num)


if __name__ == '__main__':
    main()
