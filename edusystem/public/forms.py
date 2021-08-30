"""
用于校验表单
"""
from django.forms import Form, fields


class StudentForm(Form):
    id = fields.CharField(max_length=10, required=True)
    name = fields.CharField(max_length=30, required=True)
    sex = fields.CharField(max_length=2, required=True)
    # graduate = fields.CharField(max_length=30)
    birth = fields.DateField(required=True)
    idCard = fields.CharField(max_length=18, required=True)
    political = fields.CharField(max_length=6, required=True)
    telephone = fields.CharField(max_length=11, required=True)
    dptNo = fields.CharField(max_length=2, required=True)
    classAndGrade = fields.CharField(max_length=24, required=True)
    status = fields.CharField(max_length=5, required=True)


class TeacherForm(Form):
    id = fields.CharField(max_length=8, required=True)
    name = fields.CharField(max_length=30, required=True)
    sex = fields.CharField(max_length=2, required=True)
    birth = fields.DateField(required=True)
    degree = fields.CharField(max_length=8, required=True)
    idCard = fields.CharField(max_length=18, required=True)
    telephone = fields.CharField(max_length=11, required=True)
    political = fields.CharField(max_length=6, required=True)
    workTime = fields.CharField(max_length=255)
    department = fields.CharField(max_length=2, required=True)
    title = fields.CharField(max_length=6)


# class CourseForm(Form):
#     name = fields.CharField(max_length=20)
#     dpt = fields.CharField(max_length=2)
#     hours = fields.IntegerField()
#     type = fields.CharField(max_length=10)
#     credit = fields.IntegerField()

