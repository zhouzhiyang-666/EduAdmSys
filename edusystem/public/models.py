from django.db import models
from datetime import datetime


# 验证码表
class CheckCode(models.Model):
    code_id = models.AutoField(primary_key=True)
    session_key = models.CharField(max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'tbl_checkcode'


# 学期表
class Term(models.Model):
    term_no = models.IntegerField(primary_key=True)
    term_name = models.CharField(max_length=20)

    class Meta:
        managed = True
        db_table = 'tbl_term'


# 科目表
class Course(models.Model):
    crs_no = models.IntegerField(primary_key=True)
    crs_name = models.CharField(max_length=20)
    crs_cdt = models.IntegerField()
    crs_hours = models.IntegerField()
    # crs_dpt = models.CharField(max_length=2)
    crs_dpt =models.ForeignKey('Department',
                               db_column='crs_dpt',
                               on_delete=models.CASCADE,
                               to_field='dpt_no',
                               )

    type_choices = [
        (1, '专业必修'),
        (1, '通识选修'),
        (1, '通识必修'),
    ]
    crs_type = models.CharField(
        max_length=4,
        choices=type_choices
    )


    class Meta:
        managed = True
        db_table = 'tbl_course'


# 班级表，会重复，所以使用tbl_calss
class TblClass(models.Model):
    class_no = models.CharField(max_length=8, primary_key=True)
    class_name = models.CharField(max_length=20)
    class_dpt = models.ForeignKey('Department',
                                  db_column='class_dpt',
                                  on_delete=models.CASCADE,
                                  to_field='dpt_no')
    class_grade = models.CharField(max_length=4)

    class Meta:
        managed = True
        db_table = 'tbl_class'


# 教区表
class Spot(models.Model):
    spt_no = models.CharField(max_length=4, primary_key=True)
    spt_area = models.CharField(max_length=20)
    area_choices = [
        (1, '教学楼A区'),
        (2, '教学楼B区'),
        (3, '第一实验楼'),
        (4, '第一操场'),
    ]
    spt_room = models.CharField(
        max_length=10,
        choices=area_choices
    )

    class Meta:
        managed = True
        db_table = 'tbl_spot'


# 当前学期和选课开启表
class Active(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.ForeignKey('Term',
                             db_column='name',
                             on_delete=models.CASCADE,
                             to_field='term_no')
    option = models.IntegerField()
    select_num = models.IntegerField()
    grade = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'tbl_active'


# 学院表
class Department(models.Model):
    dpt_no = models.CharField(max_length=2, primary_key=True)
    dpt_name = models.CharField(max_length=20)

    class Meta:
        managed = True
        db_table = 'tbl_department'


# 选课表
class TeaCrs(models.Model):
    tea_crs_no = models.AutoField(primary_key=True)
    tea_no = models.ForeignKey('teacher.Teacher',
                               db_column='tea_no',
                               on_delete=models.CASCADE,
                               to_field='tea_no')
    crs_no = models.ForeignKey('Course',
                               db_column='crs_no',
                               on_delete=models.CASCADE,
                               to_field='crs_no')
    term = models.ForeignKey('Term',
                             db_column='term',
                             on_delete=models.CASCADE,
                             to_field='term_no')
    time_choices = [
        ('0', '0'),
        ('1', '1'),
        ('3', '3'),
        ('4', '4'),
        ('6', '6'),
    ]
    time = models.CharField(
        choices=time_choices, max_length=2
    )
    spot = models.ForeignKey('Spot',
                             db_column='spot',
                             on_delete=models.CASCADE,
                             to_field='spt_no')
    week_choices = [
        (1, 'Mon'),
        (2, 'Tues'),
        (3, 'Wed'),
        (4, 'Thur'),
        (5, 'Fri'),
    ]
    week = models.CharField(
        max_length=5,
        choices=week_choices
    )
    selected = models.IntegerField()
    total = models.IntegerField()
    grade = models.CharField(max_length=4)
    is_public = models.CharField(max_length=1)

    class Meta:
        managed = True
        db_table = 'tbl_tea_crs'


# 日志表
class Logging(models.Model):
    id = models.BigIntegerField(primary_key=True)
    message = models.CharField(max_length=300)
    level_string = models.CharField(max_length=254)
    # created_time = models.DateTimeField(auto_now_add=True)  # default=datetime.now()
    created_time = models.DateTimeField(default=datetime.now())  # default=datetime.now()
    logger_name = models.CharField(max_length=300)

    class Meta:
        managed = True
        db_table = 'logging'


# 权限表
class Permission(models.Model):
    pid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'permission'
    pass


# 角色表
class Role(models.Model):
    rid = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'role'


# 用户角色表  user_role
class UserRole(models.Model):
    uid = models.ForeignKey('teacher.Teacher',
                            db_column='uid',
                            on_delete=models.CASCADE,
                            to_field='tea_no',
                            primary_key=True)
    rid = models.ForeignKey('Role',
                            db_column='rid',
                            on_delete=models.CASCADE,
                            to_field='rid')

    class Meta:
        managed = True
        unique_together = (("uid", "rid"),)
        db_table = 'user_role'


# 角色与权限关联表
class RoleToPermission(models.Model):
    rid = models.ForeignKey('Role',
                            db_column='rid',
                            on_delete=models.CASCADE,
                            to_field='rid')
    pid = models.ForeignKey('Permission',
                            db_column='pid',
                            on_delete=models.CASCADE,
                            to_field='pid')

    class Meta:
        managed = True
        db_table = 'role_permission'


# 分数表也为选课表
class Score(models.Model):
    stu_no = models.ForeignKey('student.Student',
                               db_column='stu_no',
                               on_delete=models.CASCADE,
                               to_field='stu_no',
                               primary_key=True)
    tea_crs_no = models.ForeignKey('TeaCrs',
                                   db_column='tea_crs_no',
                                   on_delete=models.CASCADE,
                                   to_field='tea_crs_no')
    score_pro = models.FloatField()
    score_end = models.FloatField()
    score = models.FloatField()

    class Meta:
        managed = True
        unique_together = (("stu_no", "tea_crs_no"),)
        db_table = 'tbl_score'
