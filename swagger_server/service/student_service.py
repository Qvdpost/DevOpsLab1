from swagger_server.db import students, grades

import random


def add(student=None):
    if not student:
        return 'error', 500

    if student.student_id is None:
        while students.retrieve((student_id := int(1000 * random.random()))):
            pass
        student.student_id = student_id

    if students.retrieve(student.student_id):
        return 'Student already exists', 409

    data = {
        'first_name': student.first_name,
        'last_name': student.last_name,
        '_id': student.student_id,
        'grade_records': [{'subject_name': grade.subject_name, 'grade': grade.grade} for grade in student.grade_records]
        if student.grade_records else []
    }

    doc_id = students.create(data)

    if doc_id != student.student_id:
        return 'error', 500

    return doc_id, 200


def get_by_id(student_id=None):
    if student_id is None:
        return 'error', 500

    student = students.retrieve(student_id)

    if not student:
        return 'Student not found', 404

    return student, 200


def update(student_id=None, gradeRecord=None):
    if student_id is None or gradeRecord is None:
        return 'error', 500

    if not (student := students.retrieve(student_id)):
        return 'not found', 404

    students.update("push", student_id,
                    {"grade_records": {"subject_name": gradeRecord.subject_name, "grade": gradeRecord.grade}})

    return students.retrieve(student_id), 200


def delete(student_id=None):
    if student_id is None:
        return 'error', 500

    if not (student := students.retrieve(student_id)):
        return 'not found', 404

    students.delete(student_id)

    return student, 200
