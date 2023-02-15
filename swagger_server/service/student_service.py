from swagger_server.db import students, grades

import random


def add(student=None):
    if not student:
        return 'error', 500

    if not student.student_id:
        student.student_id = int(1000*random.random())

    if students.retrieve(student.student_id):
        return 'Student already exists', 409

    doc_id = students.create({
        'first_name': student.first_name,
        'last_name': student.last_name,
        '_id': student.student_id,
        'grades': [{'subject_name': grade.subject_name, 'grade': grade.grade} for grade in student.grade_records]
    })

    if doc_id != student.student_id:
        return 'error', 500

    return doc_id


def get_by_id(student_id=None, subject=None):
    if student_id is None:
        return 'error', 500

    student = students.retrieve(student_id)

    if not student:
        return 'Student not found', 404

    return student


def update(student_id=None, gradeRecord=None):
    if student_id is None or gradeRecord is None:
        return 'error', 500

    if not (student := students.retrieve(student_id)):
        return 'not found', 404

    students.update("push", student_id,
                    {"grades": {"subject_name": gradeRecord.subject_name, "grade": gradeRecord.grade}})

    return students.retrieve(student_id)


def delete(student_id=None):
    if student_id is None:
        return 'error', 500

    if not (student := students.retrieve(student_id)):
        return 'not found', 404

    students.delete(student_id)
    return student
