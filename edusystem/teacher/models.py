from django.db import models


class Teacher(models.Model):
    tea_no = models.CharField(max_length=8, primary_key=True)
    tea_name = models.CharField(max_length=30, null=False)
    sex_choices = [
        (1, '男'),
        (2, '女')
    ]
    tea_sex = models.CharField(
        max_length=1,
        choices=sex_choices,
        default=2,
        null=False
    )
    degree_choices = [
        (1, '本科'),
        (1, '硕士'),
        (1, '博士'),
        (1, '其他'),
    ]
    tea_degree = models.CharField(
        max_length=2,
        choices=degree_choices,
        default=1,
        null=False
    )
    title_choices = [
        (1, '教授'),
        (1, '副教授'),
        (1, '讲师'),
        (1, '助教'),
    ]
    tea_title = models.CharField(
        max_length=3,
        choices=title_choices,
        default=1,
    )
    tea_birth = models.DateField(null=False)
    tea_id = models.CharField(max_length=18, null=False)
    tea_tel = models.CharField(max_length=11, null=False)
    pol_chocies = [
        (1, '共青团员'),
        (2, '共产党员'),
        (3, '入党积极分子'),
        (4, '其他党派'),
        (5, '群众'),
    ]
    tea_pol = models.CharField(
        max_length=6,
        choices=pol_chocies,
        default=1,
        null=False
    )
    tea_dpt = models.ForeignKey('public.Department',
                                db_column='tea_dpt',
                                on_delete=models.CASCADE,
                                to_field='dpt_no')
    tea_wkt = models.CharField(max_length=255)
    tea_pwd = models.BinaryField()

    class Meta:
        managed = True
        db_table = 'tbl_teacher'
