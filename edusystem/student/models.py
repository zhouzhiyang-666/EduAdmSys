from django.db import models


class Student(models.Model):
    stu_no = models.CharField(max_length=10, primary_key=True)
    stu_name = models.CharField(max_length=30, null=False)
    sex_choices = [
        (1, '男'),
        (2, '女')
    ]
    stu_sex = models.CharField(
        max_length=1,
        choices=sex_choices,
        default=2,
        null=False
    )
    stu_gdu = models.CharField(max_length=30)
    stu_bth = models.DateField(null=False)
    stu_id = models.CharField(max_length=18, null=False)
    stu_tel = models.CharField(max_length=11, null=False)
    pol_chocies = [
        (1, '共青团员'),
        (2, '共产党员'),
        (3, '入党积极分子'),
        (4, '其他党派'),
        (5, '群众'),
    ]
    stu_pol = models.CharField(
        max_length=6,
        choices=pol_chocies,
        default=1,
        null=False
    )
    stu_dpt = models.ForeignKey('public.Department',
                                db_column='stu_dpt',
                                on_delete=models.CASCADE,
                                to_field='dpt_no')
    stu_class = models.ForeignKey('public.TblClass',
                                  db_column='stu_class',
                                  on_delete=models.CASCADE,
                                  to_field='class_no')
    sta_choices = [
        (1, '在校'),
        (2, '离校'),
    ]
    stu_sta = models.CharField(
        max_length=4,
        choices=sta_choices,
        null=False
    )
    stu_pwd = models.BinaryField()

    class Meta:
        managed = True
        db_table = 'tbl_student'

