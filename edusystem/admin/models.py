from django.db import models


class Admin(models.Model):
    adm_no = models.CharField(primary_key=True,max_length=11)
    adm_name = models.CharField(max_length=32)
    adm_pwd = models.BinaryField()

    class Meta:
        managed = True
        db_table = 'tbl_admin'
    pass



