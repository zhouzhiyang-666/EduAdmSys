from django.http import JsonResponse
from django.db.models import Q
import json
from django.views.decorators.http import require_GET, require_POST
from django_redis import get_redis_connection
from django.db import transaction
from utils.checkToken import Token
from utils.validateToken import check_token    # 用于token验证装饰器 每个请求必须token校验过关
from admin import models
from public.models import Department, TblClass, Course, TeaCrs, RoleToPermission,\
    Role, Permission, UserRole, Active, Term, Spot
from student.models import Student
from teacher.models import Teacher
from public.forms import StudentForm, TeacherForm
from utils.writeLogger import LoggerTool   # 日志管理
import pandas as pd
import os
system_logger = LoggerTool()
from edusystem.settings import logger
from utils.handleJsonResponse import handelFileError, handelResopnse


# 登录测试
@require_POST
def login(request):
    codeRedis = get_redis_connection('img_code')
    tokenRedis = get_redis_connection('default')
    # 去数据库查找有没有这个用户，有的话再存session
    # 解决娶不到字符串数据问题
    response = {
        'code': -1,
        'msg': 'None',
        'datas': {
            'userid': '',
            'superadmin': False
        }
    }

    if not request.body:
        response['msg'] = '请输入账号信息！'
        return JsonResponse(response)
    request_data = json.loads(request.body)
    username = request_data.get('user', 'default')
    password = request_data.get('passwd', 'default')
    checkcode = request_data.get('vcode', '0000')
    uuid = request.META.get('HTTP_UUID', 'none')  # 验证码需要用到
    # print(request_data)
    # code = sqlhelper.get_one('select * from public_session where ')
    # 校验验证码
    # Token.check_token(myRedis, uuid, checkcode)
    if not Token.check_token(codeRedis, uuid, checkcode.upper()):
        response['msg'] = '验证码错误'
        system_logger.error(request, "- 验证码错误 id:{}".format(str(username)))
        return JsonResponse(response)

    obj = UserRole.objects.filter(uid__tea_no=username, uid__tea_pwd=password.encode()).first()
    # obj = UserRole.objects.all().first()
    # print(obj.uid.tea_pwd)
    if not obj:
        response['msg'] = '账号或密码错误，请重新输入，或者没有权限'
        system_logger.info(request, "- 登录失败 id:{}".format(str(username)))
        return JsonResponse(response)
    print('我的密码:', password.encode(), '数据库密码', obj.uid.tea_pwd)
    # 生成token
    if obj.rid.rid == 'super_admin':    # 超级管理员
        response['datas']['perm'] = 2
        response['datas']['superadmin'] = True
    token = Token.create_token(username, password)
    tokenRedis.set(username, token, 86400)  # 缓存token，保存一天
    response['code'] = 1
    response['msg'] = '登录成功'
    response['datas']['userid'] = username
    response['datas']['username'] = obj.uid.tea_name
    response['datas']['token'] = token
    # print(Token.check_token(tokenRedis, username, token))
    system_logger.info(request, "- 登录成功 id:{}".format(str(username)))
    return JsonResponse(response)


# 获取学院信息
@check_token
def getDptName(request):
    datas = []
    response = {
        'code': 0,
        'msg': 'None',
        'datas': datas
    }
    dpt_list = Department.objects.all()
    if not dpt_list:
        response['code'] = -1
        return JsonResponse(response)
    response['code'] = 1
    for row in dpt_list:
        temp = {}
        temp['id'] = row.dpt_no
        temp['name'] = row.dpt_name
        datas.append(temp)
    return JsonResponse(response)


# 获取学生档案信息
@check_token
@require_POST
def getStuData(request):
    datas = []
    response = {
        'code': -1,
        'msg': 'None',
        'datas': datas
    }
    request_data = json.loads(request.body, encoding='utf-8')
    # {'dpt': '0', 'grade': 2017, 'classId': '20171101', 'page': 1, 'size': 10}
    dpt_no = request_data.get('dpt', 'none')
    grade = request_data.get('grade', 'none')
    class_no = request_data.get('classId', 'none')

    query_data = Q()
    query_data.connector = 'AND'
    if dpt_no != 'none' and dpt_no != '0':
        query_data.children.append(('stu_dpt__dpt_no', dpt_no))
    if grade != 'none' and grade != '0':
        query_data.children.append(('stu_class__class_grade', grade))
    if class_no != 'none' and class_no != '0':
        query_data.children.append(('stu_class', class_no))
    print(query_data)
    stu_list = Student.objects.filter(query_data)

    response['code'] = 1
    # 分页实现
    # page = request_data.get('page', 1)
    # size = request_data.get('size', 10)
    # start = (page-1) * size
    # end = page * size
    # total = len(stu_list)
    # if end > len(stu_list):
    #     end = len(stu_list)
    # print(start, end)
    # for row in stu_list[start:end]:

    for row in stu_list:
        temp = {}
        temp['id'] = row.stu_no
        temp['name'] = row.stu_name
        temp['status'] = row.stu_sta
        temp['sex'] = row.stu_sex
        temp['classAndGrade'] = row.stu_class.class_grade + row.stu_class.class_name   # 年级+班级 如2017文学一班
        temp['department'] = row.stu_dpt.dpt_name
        temp['dptNo'] = row.stu_dpt.dpt_no
        temp['idCard'] = row.stu_id
        temp['birth'] = row.stu_bth
        temp['political'] = row.stu_pol
        temp['graduate'] = row.stu_gdu
        temp['telephone'] = row.stu_tel
        temp['classId'] = row.stu_class.class_no
        datas.append(temp)
    # print(response)
    # response['total'] = total
    return JsonResponse(response)


# 获取所有班级信息
@check_token
def getAllClass(request):
    datas = []
    response = {
        'code': -1,
        'msg': 'None',
        'datas': datas
    }
    request_data = json.loads(request.body, encoding='utf-8')
    dpt_no = request_data.get('dpt', 'none')
    grade = request_data.get('grade', 'none')
    print(request_data)

    query_data = Q()
    query_data.connector = 'AND'
    if dpt_no != 'none' and dpt_no != '0':
        query_data.children.append(('class_dpt', dpt_no))
    if grade != 'none' and grade != '0':
        query_data.children.append(('class_grade', str(grade)))
    print(query_data)
    class_list = TblClass.objects.filter(query_data)
    if not class_list:
        return handelResopnse(-1, '没有查到班级数据', '')

    response['code'] = 1
    for row in class_list:
        temp = {}
        temp['classId'] = row.class_no
        temp['classFullName'] = row.class_grade + row.class_name
        temp['classGrade'] = row.class_grade
        temp['className'] = row.class_name
        temp['dptNo'] = row.class_dpt.dpt_no
        temp['dptName'] = row.class_dpt.dpt_name
        datas.append(temp)
    return JsonResponse(response)


# 修改学生信息
@check_token
@require_POST
def editStu(request):
    datas = []
    response = {
        'code': -1,
        'msg': 'None',
        'datas': datas
    }
    request_data = json.loads(request.body, encoding='utf-8')
    # {'id': '2018090302', 'name': '小王同学', 'sex': '男', 'graduate': '第一中学', 'birth': '1999-12-01',
    #  'idCard': '527133199912018453', 'political': '共青团员', 'telephone': '18011108917', 'department': '0',
    #  'dptNo': '08', 'classAndGrade': '20180803', 'status': '在校', 'pwd': '', 'classId': '20180803'}
    print(request_data)

    valid_form = StudentForm(request_data)
    if not valid_form.is_valid():
        response['msg'] = '输入不符合规则'
        return JsonResponse(response)
    response['code'] = 1
    stu_no = request_data.get('id', 'none').strip()
    stu_name = request_data.get('name', 'none').strip()
    stu_sex = request_data.get('sex', 'none').strip()
    stu_gdu = request_data.get('graduate', 'none').strip()
    stu_bth = request_data.get('birth', 'none').strip()
    stu_id = request_data.get('idCard', 'none').strip()
    stu_pol = request_data.get('political', 'none').strip()
    stu_tel = request_data.get('telephone', 'none').strip()
    stu_dpt = request_data.get('dptNo', 'none').strip()
    # stu_class = request_data.get('classId', 'none').strip()
    stu_class = request_data.get('classAndGrade', 'none').strip()
    stu_sta = request_data.get('status', 'none').strip()
    stu_pwd = request_data.get('pwd', 'none')

    dpt_obj = Department.objects.get(dpt_no=stu_dpt)
    class_obj = TblClass.objects.get(class_no=stu_class)
    stu_obj = Student.objects.get(stu_no=stu_no)

    stu_obj.stu_name = stu_name
    stu_obj.stu_sex = stu_sex
    stu_obj.stu_gdu = stu_gdu
    stu_obj.stu_bth = stu_bth
    stu_obj.stu_id = stu_id
    stu_obj.stu_pol = stu_pol
    stu_obj.stu_tel = stu_tel
    stu_obj.stu_dpt = dpt_obj
    stu_obj.stu_class = class_obj
    stu_obj.stu_sta = stu_sta
    if stu_pwd == '':
        stu_obj.save(update_fields=['stu_name', 'stu_sex', 'stu_gdu',
                                    'stu_bth', 'stu_id', 'stu_pol',
                                    'stu_tel', 'stu_dpt', 'stu_class', 'stu_sta'])
    else:
        stu_obj.stu_pwd = stu_pwd.encode()
        stu_obj.save(update_fields=['stu_name', 'stu_sex', 'stu_gdu',
                                    'stu_bth', 'stu_id', 'stu_pol',
                                    'stu_tel', 'stu_dpt', 'stu_class', 'stu_sta', 'stu_pwd'])
    return JsonResponse(response)


# 添加学生
# 修改学生信息
@check_token
@require_POST
def addStu(request):
    # 生成MD5
    import hashlib
    # import binascii
    myHash = hashlib.md5()
    datas = []
    response = {
        'code': 0,
        'msg': 'None',
        'datas': datas
    }
    request_data = json.loads(request.body, encoding='utf-8')

    valid_form = StudentForm(request_data)
    print(request_data)
    if not valid_form.is_valid():
        response['code'] = -1
        response['msg'] = '输入不符合规则'
        return JsonResponse(response)
    response['code'] = 1
    stu_no = request_data.get('id', 'none')
    stu_name = request_data.get('name', 'none')
    stu_sex = request_data.get('sex', 'none')
    stu_gdu = request_data.get('graduate', 'none')
    stu_bth = request_data.get('birth', 'none')
    stu_id = request_data.get('idCard', 'none')
    stu_pol = request_data.get('political', 'none')
    stu_tel = request_data.get('telephone', 'none')
    stu_dpt = request_data.get('dptNo', 'none')
    stu_class = request_data.get('classAndGrade', 'none')
    stu_sta = request_data.get('status', 'none')

    if Student.objects.filter(stu_no=stu_no).exists():
        print(Student.objects.filter(stu_no=stu_no).first())
        response['code'] = -1
        response['msg'] = '学生信息已存在,请检查输入内容'
        return JsonResponse(response)

    # 获取初始密码 为学生的学号
    myHash.update(stu_no.encode(encoding='ascii'))
    stu_pwd = myHash.hexdigest()
    #print('加密的数据', type(stu_pwd.encode(encoding='ascii')))
    stu_pwd = stu_pwd.encode(encoding='ascii')
    # stu_pwd = binascii.hexlify(stu_pwd)
    # print(stu_pwd)
    # binascii.hexlify(en_pwd)
    # stu_pwd = binascii.hexlify(stu_pwd.encode(encoding='ascii'))
    # print('转十六禁止--',stu_pwd)
    dpt_obj = Department.objects.filter(dpt_no=stu_dpt).first()
    class_obj = TblClass.objects.filter(class_no=stu_class).first()
    Student.objects.create(
        stu_no=stu_no,
        stu_name=stu_name,
        stu_sex=stu_sex,
        stu_gdu=stu_gdu,
        stu_bth=stu_bth,
        stu_id=stu_id,
        stu_pol=stu_pol,
        stu_tel=stu_tel,
        stu_dpt=dpt_obj,
        stu_class=class_obj,
        stu_sta=stu_sta,
        stu_pwd=b'5a228c96a65ba383632c1ee156ef4dd3'
    )
    """
       此处由于Django插入mysql的Blob字段数据出现编码等问题，所以及逆行了先插入密码数据，再更
       新为用户的账号为密码，解决了插入数据后，密码不是原来账号的问题!!!!!
    """
    Student.objects.filter(stu_no=stu_no).update(stu_pwd=stu_pwd)
    return JsonResponse(response)


# 删除学生
@check_token
@require_POST
def delStu(request):
    datas = []
    response = {
        'code': -1,
        'msg': 'None',
        'datas': datas
    }
    request_data = json.loads(request.body, encoding='utf-8')
    print(request_data)
    stu_no = request_data.get('id', 'none')
    result = Student.objects.filter(stu_no=stu_no).delete()
    print('删除数据成功：影响', result[0], '行', '操作的表：', result[1])
    # if obj[]
    response['code'] = 1
    response['msg'] = '删除成功'
    return JsonResponse(response)


# 批量删除学生
@check_token
@require_POST
def batchDelStu(request):
    datas = []
    response = {
        'code': -1,
        'msg': 'None',
        'datas': datas
    }
    request_data = json.loads(request.body, encoding='utf-8')
    # print(request_data)
    stuNo_list = request_data.get('ids', 'none')
    try:
        for stu_no in stuNo_list:
            Student.objects.filter(stu_no=stu_no).delete()
    except Exception:
        pass
    # if obj[]
    response['code'] = 1
    response['msg'] = '删除成功'
    return JsonResponse(response)


# 批量导入学生档案excel表
@check_token
def uploadStuFiles(request):
    response = {
        'code': 1,
        'msg': '批量导入学生档案',
        'datas': {}
    }
    # print(request.body.split(b'\r\n')[1].decode())
    request_bytesList = request.body.split(b'\r\n')
    # print(request_bytesList[1].decode().split(';')[2][11:-1])
    filename = request_bytesList[1].decode().split(';')[2][11:-1]
    file_name = './'+filename
    if os.path.exists(file_name):
        os.remove(file_name)
    with open(file_name, 'ab') as f:
        f.write(request_bytesList[4])

    # with open('./xxx.csv','r',errors='ignore') as f:
    #     csv_read = csv.reader(f)
    #     print(csv_read)
    #     for line in csv_read:
    #         print(line)
    head = ['id', 'name', 'sex', 'graduate', 'birth',
            'idCard', 'telephone', 'political', 'department',
            'classAndGrade', 'status', 'pass']
    def excel_one_line_to_list():
        df = pd.read_excel(file_name,
                           usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],   # 0,1,2分别指取的列数
                           names=None)  # 读取项目名称列,不要列名
        print(df)
        df_header = df.columns.to_list()
        df_li = df.values.tolist()
        result = []
        for s_li in df_li:
            result.append(s_li)
        return result, df_header
    try:
        data_list, df_headers = excel_one_line_to_list()
        print(df_headers)
        if len(df_headers) != len(head):
            return handelFileError(file_name, '上传学生档案信息出错', '文件格式不符合规范，请检查文件后再上传!')
        for i in range(len(head)):
            if i < len(df_headers) and df_headers[i] != head[i]:
                return handelFileError(file_name, '上传学生档案信息出错', '文件格式不符合规范，请检查文件后再上传!')

    except Exception as e:
        return handelFileError(file_name, '上传学生档案信息出错', e)

    totalNum = len(data_list)
    success = 0
    error_list = []
    for row in data_list:
        # [2018090301, '小王同学', '男', '第一中学', '1999-12-01', 527133199912018453, 18011108917, '共青团员', 8, 20180803, '在校']
        try:
            stu_no = str(row[0])
            dpt_no = str(row[8])
            dpt_no = '0' + dpt_no if len(dpt_no) == 1 else dpt_no

            class_obj = TblClass.objects.filter(class_no=str(row[9])).first()
            dpt_obj = Department.objects.filter(dpt_no=dpt_no).first()

            if Student.objects.filter(stu_no=stu_no).first() or not dpt_obj or not class_obj:
                # print(Student.objects.filter(stu_no=stu_no).first(), 222222)
                error_list.append(stu_no + '-' + row[1])
                continue
            with transaction.atomic():
                Student.objects.create(stu_no=stu_no,
                                       stu_name=row[1],
                                       stu_sex=row[2],
                                       stu_gdu=row[3],
                                       stu_bth=row[4],
                                       stu_id=str(row[5]),
                                       stu_tel=str(row[6]),
                                       stu_pol=row[7],
                                       stu_dpt=dpt_obj,
                                       stu_class=class_obj,
                                       stu_sta=row[10],
                                       stu_pwd=b'e10adc3949ba59abbe56e057f20f883e')
                Student.objects.filter(stu_no=stu_no).update(stu_pwd=b'e10adc3949ba59abbe56e057f20f883e')
                success += 1
            # 批量导入学生初始密码
            # 初始密码	b'e10adc3949ba59abbe56e057f20f883e'  123456
        except Exception:
            if len(row) >= 2:
                error_list.append(stu_no + '-' + row[1])

    datas = {}
    datas['success'] = success
    datas['totalNum'] = totalNum
    datas['failed'] = totalNum - success
    datas['errorList'] = error_list
    response['datas'] = datas
    os.remove('./'+filename)
    return JsonResponse(response)


# 获取老师档案信息
@check_token
@require_POST
def getTeaData(request):
    datas = []
    response = {
        'code': -1,
        'msg': 'None',
        'datas': datas
    }
    request_data = json.loads(request.body, encoding='utf-8')
    dpt_no = request_data.get('dpt', 'none')

    if dpt_no == '0':
        tea_list = Teacher.objects.all()
    else:
        tea_list = Teacher.objects.filter(tea_dpt=dpt_no)
    response['code'] = 1
    for row in tea_list:
        temp = {}
        temp['id'] = row.tea_no
        temp['name'] = row.tea_name
        temp['sex'] = row.tea_sex
        temp['department'] = row.tea_dpt.dpt_name
        temp['dptNo'] = row.tea_dpt.dpt_no
        temp['title'] = row.tea_title
        temp['idCard'] = row.tea_id
        temp['workTime'] = row.tea_wkt.split('至')
        temp['political'] = row.tea_pol
        temp['degree'] = row.tea_degree
        temp['telephone'] = row.tea_tel
        temp['birth'] = row.tea_birth
        datas.append(temp)
    # print(response)
    return JsonResponse(response)


# 修改老师信息
@check_token
@require_POST
def editTea(request):
    datas = []
    response = {
        'code': 0,
        'msg': 'None',
        'datas': datas
    }
    request_data = json.loads(request.body, encoding='utf-8')
    # {'id': '20011103', 'name': '李老师', 'sex': '男', 'birth': '1976-04-14',
    #  'degree': '博士', 'idCard': '510722197604147894',
    #  'telephone': '13811104563', 'political': '共产党员',
    #  'workTime': '2001 - 09至2002 - 10', 'department': '0', 'title': '教授', pwd:''}
    print(request_data)

    valid_form = TeacherForm(request_data)
    if not valid_form.is_valid():
        response['code'] = -1
        response['msg'] = '输入不符合规则'
        return JsonResponse(response)
    response['code'] = 1
    response['msg'] = '修改成功'
    tea_no = request_data.get('id', 'none')
    tea_name = request_data.get('name', 'none')
    tea_sex = request_data.get('sex', 'none')
    tea_birth = request_data.get('birth', 'none')
    tea_degree = request_data.get('degree', 'none')
    tea_id = request_data.get('idCard', 'none')
    tea_tel = request_data.get('telephone', 'none')
    tea_pol = request_data.get('political', 'none')
    tea_wkt = request_data.get('workTime', 'none')
    tea_dpt = request_data.get('department', 'none')
    tea_title = request_data.get('title', 'none')
    tea_pwd = request_data.get('pwd', 'none')
    if tea_pwd == '':
        Teacher.objects.filter(tea_no=tea_no).update(
            tea_name=tea_name,
            tea_sex=tea_sex,
            tea_birth=tea_birth,
            tea_degree=tea_degree,
            tea_id=tea_id,
            tea_tel=tea_tel,
            tea_pol=tea_pol,
            tea_wkt=tea_wkt,
            tea_dpt=tea_dpt,
            tea_title=tea_title
        )
    else:
        Teacher.objects.filter(tea_no=tea_no).update(
            tea_name=tea_name,
            tea_sex=tea_sex,
            tea_birth=tea_birth,
            tea_degree=tea_degree,
            tea_id=tea_id,
            tea_tel=tea_tel,
            tea_pol=tea_pol,
            tea_wkt=tea_wkt,
            tea_dpt=tea_dpt,
            tea_title=tea_title,
            tea_pwd=tea_pwd.encode()
        )
    return JsonResponse(response)


# 添加老师
@check_token
@require_POST
def addTea(request):
    # 生成MD5
    import hashlib
    # import binascii
    myHash = hashlib.md5()
    datas = []
    response = {
        'code': 0,
        'msg': 'None',
        'datas': datas
    }
    request_data = json.loads(request.body, encoding='utf-8')
    # print(request_data)
    valid_form = TeacherForm(request_data)
    if not valid_form.is_valid():
        response['code'] = -1
        response['msg'] = '输入不符合规则'
        return JsonResponse(response)

    tea_no = request_data.get('id', 'none')
    tea_name = request_data.get('name', 'none')
    tea_sex = request_data.get('sex', 'none')
    tea_birth = request_data.get('birth', 'none')
    tea_degree = request_data.get('degree', 'none')
    tea_id = request_data.get('idCard', 'none')
    tea_tel = request_data.get('telephone', 'none')
    tea_pol = request_data.get('political', 'none')
    tea_wkt = request_data.get('workTime', 'none')
    tea_dpt = request_data.get('department', 'none')
    tea_title = request_data.get('title', 'none')

    if Teacher.objects.filter(tea_no=tea_no).exists():
        print(Teacher.objects.filter(tea_no=tea_no).first())
        response['code'] = -1
        response['msg'] = '教师信息已存在,请检查输入内容'
        return JsonResponse(response)

    # 获取初始密码 为老师的工号
    myHash.update(tea_no.encode(encoding='ascii'))
    tea_pwd = myHash.hexdigest()
    # print('加密的数据', tea_pwd.encode(encoding='ascii'))
    tea_pwd = tea_pwd.encode(encoding='ascii')

    dpt_obj = Department.objects.filter(dpt_no=tea_dpt).first()
    Teacher.objects.create(
        tea_no=tea_no,
        tea_name=tea_name,
        tea_sex=tea_sex,
        tea_birth=tea_birth,
        tea_degree=tea_degree,
        tea_id=tea_id,
        tea_tel=tea_tel,
        tea_pol=tea_pol,
        tea_dpt=dpt_obj,
        tea_wkt=tea_wkt,
        tea_title=tea_title,
        tea_pwd=b'5a228c96a65ba383632c1ee156ef4dd3'
    )
    Teacher.objects.filter(tea_no=tea_no).update(tea_pwd=tea_pwd)
    response['code'] = 1
    return JsonResponse(response)


# 删除老师
@check_token
@require_POST
def delTea(request):
    datas = []
    response = {
        'code': -1,
        'msg': 'None',
        'datas': datas
    }
    request_data = json.loads(request.body, encoding='utf-8')
    print(request_data)
    tea_no = request_data.get('id', 'none')
    result = Teacher.objects.filter(tea_no=tea_no).delete()
    print('删除数据成功：影响', result[0], '行', '操作的表：', result[1])
    # if obj[]
    response['code'] = 1
    response['msg'] = '删除成功'
    return JsonResponse(response)


# 批量删除教师
@check_token
@require_POST
def batchDelTea(request):
    datas = []
    response = {
        'code': -1,
        'msg': 'None',
        'datas': datas
    }
    request_data = json.loads(request.body, encoding='utf-8')
    print(request_data)
    teaNo_list = request_data.get('ids', 'none')
    try:
        for tea_no in teaNo_list:
            Teacher.objects.filter(tea_no=tea_no).delete()
    except Exception:
        pass
    response['code'] = 1
    response['msg'] = '删除成功'
    return JsonResponse(response)


# 批量导入老师档案excel表
@check_token
def uploadTeaFiles(request):
    response = {
        'code': 1,
        'msg': '批量导入老师档案',
        'datas': {}
    }
    # print(request.body.split(b'\r\n')[1].decode())
    request_bytesList = request.body.split(b'\r\n')
    # print(request_bytesList[1].decode().split(';')[2][11:-1])
    filename = request_bytesList[1].decode().split(';')[2][11:-1]
    file_name = './'+filename
    if os.path.exists(file_name):
        os.remove(file_name)
    with open(file_name, 'ab') as f:
        f.write(request_bytesList[4])

    # with open('./xxx.csv','r',errors='ignore') as f:
    #     csv_read = csv.reader(f)
    #     print(csv_read)
    #     for line in csv_read:
    #         print(line)
    head = ['id', 'name', 'sex',
            'degree', 'title', 'birth', 'idCard',
            'telephone', 'political', 'department', 'workTime', 'pass']
    def excel_one_line_to_list():
        df = pd.read_excel(file_name,
                           usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],  # 0,1,2分别指取的列数
                           names=None)  # 读取项目名称列,不要列名
        print(df)
        df_header = df.columns.to_list()
        df_li = df.values.tolist()
        result = []
        for s_li in df_li:
            result.append(s_li)
        return result, df_header
    try:
        data_list, df_headers = excel_one_line_to_list()
        print(df_headers)
        if len(df_headers) != len(head):
            return handelFileError(file_name, '上传教师档案信息出错', '文件格式不符合规范，请检查文件后再上传!')
        for i in range(len(head)):
            if i < len(df_headers) and df_headers[i] != head[i]:
                return handelFileError(file_name, '上传教师档案信息出错', '文件格式不符合规范，请检查文件后再上传!')

    except Exception as e:
        return handelFileError(file_name, '上传教师档案信息出错', e)

    totalNum = len(data_list)
    success = 0
    error_list = []
    for row in data_list:
        # [20031103, '33老师', '男', '硕士', '教授', '1980-12-14', 435123198012145545, 15878547753, '其他党派', 11, '2003-09至今']
        try:
            dpt_no = str(row[9])
            dpt_no = '0' + dpt_no if len(dpt_no) == 1 else dpt_no
            dpt_obj = Department.objects.filter(dpt_no=dpt_no).first()
            tea_no = str(row[0])
            # 已存在则跳过
            if Teacher.objects.filter(tea_no=tea_no).first() or not dpt_obj:
                error_list.append(tea_no + '-' + row[1])
                continue
            with transaction.atomic():
                Teacher.objects.create(tea_no=tea_no,
                                       tea_name=row[1],
                                       tea_sex=row[2],
                                       tea_degree=row[3],
                                       tea_title=row[4],
                                       tea_birth=row[5],
                                       tea_id=str(row[6]),
                                       tea_tel=str(row[7]),
                                       tea_pol=row[8],
                                       tea_dpt=dpt_obj,
                                       tea_wkt=row[10],
                                       tea_pwd=b'e10adc3949ba59abbe56e057f20f883e')
                Teacher.objects.filter(tea_no=tea_no).update(tea_pwd=b'e10adc3949ba59abbe56e057f20f883e')
            success += 1
            # 初始密码	b'e10adc3949ba59abbe56e057f20f883e'  123456
        except Exception as e:
            if len(row) >= 2:
                error_list.append(tea_no + '-' + row[1])

    datas = {}
    datas['success'] = success
    datas['totalNum'] = totalNum
    datas['failed'] = totalNum - success
    datas['errorList'] = error_list
    response['datas'] = datas
    os.remove('./' + filename)
    return JsonResponse(response)


# 课程开设
# 获取学期课表
@check_token
@require_POST
def getCourseInfo(request):
    request_data = json.loads(request.body, encoding='utf-8')
    dpt_no = request_data.get('dpt', 'none')
    course_type = request_data.get('courseType', 'none')
    print(request_data)
    # 补上学生或者教室id查对应的课表
    # print(request_data)

    query_data = Q()
    query_data.connector = 'AND'
    if dpt_no != 'none' and dpt_no != '0':
        query_data.children.append(('crs_dpt', dpt_no))
    if course_type != 'none' and course_type != '-1':
        query_data.children.append(('crs_type', str(course_type)))
    course_list = Course.objects.filter(query_data)

    datas = []
    for row in course_list:
        temp = {}
        temp['id'] = str(row.crs_no)
        temp['name'] = row.crs_name
        temp['type'] = row.crs_type
        temp['dptNo'] = row.crs_dpt.dpt_no
        temp['department'] = row.crs_dpt.dpt_name
        temp['hours'] = row.crs_hours
        temp['credit'] = row.crs_cdt
        datas.append(temp)
    response = {
        'code': 1,
        'msg': '学期课表',
        'datas': datas
    }
    return JsonResponse(response)


# 添加课程
@check_token
@require_POST
def addCourse(request):
    datas = []
    response = {
        'code': -1,
        'msg': 'None',
        'datas': datas
    }
    request_data = json.loads(request.body, encoding='utf-8')
    print(request_data)
    # {'id': '', 'name': '地理文化', 'dptNo': '07', 'department': '', 'type': '通识选修', 'hours': '8', 'credit': '1'}
    # valid_form = TeacherForm(request_data)
    # if not valid_form.is_valid():
    #     response['msg'] = '输入不符合规则'
    #     return JsonResponse(response)

    crs_no = request_data.get('id', 'none')
    crs_name = request_data.get('name', 'none')
    crs_dpt = request_data.get('dptNo', 'none')
    crs_hours = int(request_data.get('hours', 'none'))
    crs_cdt = int(request_data.get('credit', 'none'))
    crs_type = request_data.get('type', 'none')

    # 获取学院
    dpt_obj = Department.objects.filter(dpt_no=crs_dpt).first()
    if not dpt_obj:
        response['msg'] = '没有该学院'
        return JsonResponse(response)

    if crs_no == '':
        Course.objects.create(
            crs_name=crs_name,
            crs_dpt=dpt_obj,
            crs_hours=crs_hours,
            crs_type=crs_type,
            crs_cdt=crs_cdt
        )
    else:
        Course.objects.create(
            crs_no=crs_no,
            crs_name=crs_name,
            crs_dpt=dpt_obj,
            crs_hours=crs_hours,
            crs_type=crs_type,
            crs_cdt=crs_cdt
        )
    response['code'] = 1
    response['msg'] = '数据写入成功'
    return JsonResponse(response)


# 编辑课程
@check_token
@require_POST
def editCourse(request):
    datas = []
    response = {
        'code': -1,
        'msg': 'None',
        'datas': datas
    }
    request_data = json.loads(request.body, encoding='utf-8')
    # print(request_data)
    # valid_form = TeacherForm(request_data)
    # if not valid_form.is_valid():
    #     response['msg'] = '输入不符合规则'
    #     return JsonResponse(response)

    crs_no = request_data.get('id', 'none')
    crs_name = request_data.get('name', 'none')
    crs_dpt = request_data.get('dptNo', 'none')
    crs_hours = int(request_data.get('hours', 'none'))
    crs_cdt = int(request_data.get('credit', 'none'))
    crs_type = request_data.get('type', 'none')

    # 获取学院
    dpt_obj = Department.objects.filter(dpt_no=crs_dpt).first()
    if not dpt_obj:
        response['msg'] = '没有该学院'
        return JsonResponse(response)

    course_obj = Course.objects.filter(crs_no=crs_no).first()
    if not course_obj:
        response['code'] = -1
        response['msg'] = '该课程不存在'
        return JsonResponse(response)
    else:
        course_obj.crs_name = crs_name
        course_obj.crs_hours = crs_hours
        course_obj.crs_cdt = crs_cdt
        course_obj.crs_dpt = dpt_obj
        course_obj.crs_type = crs_type
        course_obj.save(update_fields=['crs_name', 'crs_hours', 'crs_cdt',
                                       'crs_dpt', 'crs_type'])
    response['code'] = 1
    response['msg'] = '课程修改成功'
    return JsonResponse(response)


# 删除课程
@check_token
@require_POST
def delCourse(request):
    datas = []
    response = {
        'code': -1,
        'msg': 'None',
        'datas': datas
    }
    request_data = json.loads(request.body, encoding='utf-8')
    print(request_data)
    # valid_form = TeacherForm(request_data)
    # if not valid_form.is_valid():
    #     response['msg'] = '输入不符合规则'
    #     return JsonResponse(response)

    crs_no = request_data.get('id', 'none')
    result = Course.objects.filter(crs_no=crs_no).first().delete()

    print(result)
    response['code'] = 1
    response['msg'] = '成功删除课程'
    return JsonResponse(response)


# 批量删除课程
@check_token
@require_POST
def batchDelCourse(request):
    datas = []
    response = {
        'code': -1,
        'msg': 'None',
        'datas': datas
    }
    request_data = json.loads(request.body, encoding='utf-8')
    print(request_data)
    # valid_form = TeacherForm(request_data)
    # if not valid_form.is_valid():
    #     response['msg'] = '输入不符合规则'
    #     return JsonResponse(response)

    courseNo_list = request_data.get('ids', 'none')
    try:
        for crs_no in courseNo_list:
            Course.objects.filter(crs_no=crs_no).first().delete()
    except Exception:
        pass
    response['code'] = 1
    response['msg'] = '成功删除课程'
    return JsonResponse(response)


# 上传课程开设excel表
@check_token
def uploadCourse(request):
    response = {
        'code': 1,
        'msg': '批量导入课程',
        'datas': {}
    }

    # print(request.body.split(b'\r\n')[1].decode())
    request_bytesList = request.body.split(b'\r\n')
    # print(request_bytesList[1].decode().split(';')[2][11:-1])
    filename = request_bytesList[1].decode().split(';')[2][11:-1]
    file_name = './' + filename
    if os.path.exists(file_name):
        os.remove(file_name)
    with open(file_name, 'ab') as f:
        f.write(request_bytesList[4])

    head = ['name', 'credit', 'hours', 'department', 'type']
    def excel_one_line_to_list():
        df = pd.read_excel('./' + filename,
                           usecols=[0, 1, 2, 3, 4],  # 0,1,2分别指取的列数
                           names=None)  # 读取项目名称列,不要列名
        print(df)
        df_header = df.columns.to_list()
        df_li = df.values.tolist()
        result = []
        for s_li in df_li:
            result.append(s_li)
        return result, df_header
    try:
        data_list, df_headers = excel_one_line_to_list()
        print(df_headers)
        if len(df_headers) != len(head):
            return handelFileError(file_name, '上传课程信息出错', '文件格式不符合规范，请检查文件后再上传!')
        for i in range(len(head)):
            if i < len(df_headers) and df_headers[i] != head[i]:
                return handelFileError(file_name, '上传课程信息出错', '文件格式不符合规范，请检查文件后再上传!')

    except Exception as e:
        return handelFileError(file_name, '上传课程信息出错', e)

    totalNum = len(data_list)
    success = 0
    error_list = []
    for row in data_list:
        # 课程名   学分  学时  学院号   课程类型
        # ['形体学3', 4, 54, 11, '专业必修']
        try:
            dpt_no = row[3][:2]
            dpt_obj = Department.objects.filter(dpt_no=dpt_no).first()
            if not dpt_obj:
                continue
            Course.objects.create(crs_name=row[0],
                                  crs_cdt=row[1],
                                  crs_hours=row[2],
                                  crs_dpt=dpt_obj,
                                  crs_type=row[4])
            success += 1
        except Exception as e:
            if len(row) >= 1:
                error_list.append(row[0])

    datas = {}
    datas['success'] = success
    datas['totalNum'] = totalNum
    datas['failed'] = totalNum - success
    datas['errorList'] = error_list
    response['datas'] = datas
    os.remove('./' + filename)
    return JsonResponse(response)


# 获取选课课程信息
@check_token
@require_POST
def getCrsArrange(request):
    datas = []
    response = {
        'code': 1,
        'msg': '学期课表',
        'datas': datas
    }
    request_data = json.loads(request.body, encoding='utf-8')
    print(request_data)
    dpt_no = request_data.get('dpt', 'none')
    grade = str(request_data.get('grade', 'none'))
    term_no = request_data.get('term', 'none')
    # 补上学生或者教室id查对应的课表
    # term_no = '20201'
    # if dpt_no == '0' and grade == '0':
    #     pickCourse_list = TeaCrs.objects.filter(term__term_no=term_no, is_public='1')
    # else:
    #     pickCourse_list = TeaCrs.objects.filter(crs_no__crs_dpt=dpt_no, term__term_no=term_no, grade=grade, is_public='1')
    try:
        query_data = Q()
        query_data.connector = 'AND'
        if dpt_no != 'none' and dpt_no != '0':
            query_data.children.append(('crs_no__crs_dpt', dpt_no))
        if grade != 'none' and grade != '0':
            query_data.children.append(('grade', grade))
        if term_no != 'none' and term_no != '0':
            query_data.children.append(('term', term_no))
        query_data.children.append(('is_public', '1'))  # 选课课程的标识
        print(query_data)
        pickCourse_list = TeaCrs.objects.filter(query_data)

        for row in pickCourse_list:
            temp = {}
            temp['teaCrsNo'] = row.tea_crs_no
            temp['courseno'] = row.crs_no.crs_no
            temp['type'] = row.crs_no.crs_type
            temp['courseName'] = row.crs_no.crs_name
            temp['hours'] = row.crs_no.crs_hours
            temp['credit'] = row.crs_no.crs_cdt
            temp['area'] = row.spot.spt_area
            temp['room'] = row.spot.spt_room
            temp['spotNo'] = row.spot.spt_no
            temp['week'] = row.week
            temp['time'] = row.time
            temp['teacherno'] = row.tea_no.tea_no
            temp['teacherName'] = row.tea_no.tea_name
            temp['total'] = row.total
            temp['term'] = str(row.term.term_no)
            temp['grade'] = row.grade
            datas.append(temp)
        return JsonResponse(response)
    except Exception:
        response['code'] = -1
        response['msg'] = '网路异常'
        return JsonResponse(response)


# 是否加载选课按钮
@check_token
def loadButton(request):
    datas = {}
    response = {
        'code': 1,
        'msg': '加载选课按钮',
        'datas': datas
    }
    # 获取用户信息 判断是否为超级管理员
    user_id = request.META.get('HTTP_USERID', 'none')
    print(user_id)
    if user_id == 'none':
        response['code'] = 0
        response['msg'] = '用户登录过期，请重新登录'
        return JsonResponse(response)
    user_role = UserRole.objects.filter(uid=user_id).first()
    if not user_role:
        response['code'] = 0
        response['msg'] = '用户登录过期，请重新登录'
        return JsonResponse(response)
    # 判断是否为超级管理员
    role = user_role.rid.rid
    if role == 'admin':
        datas['isSuper'] = 0
    else:
        datas['isSuper'] = 1
    # 判断是否开启选课
    is_open = Active.objects.first().option
    if is_open == 0:
        datas['isOpen'] = 0
    else:
        datas['isOpen'] = 1
    return JsonResponse(response)


# 编辑选课更改老师部分
@check_token
@require_POST
def getTeaName(request):
    response = {
        'code': 1,
        'msg': '获取老师名字',
        'datas': {}
    }
    request_data = json.loads(request.body, encoding='utf-8')
    tea_no = request_data.get('teaNo', 'none')
    try:
        tea_name = Teacher.objects.filter(tea_no=tea_no).first().tea_name
        response['datas']['teacherName'] = tea_name
        return JsonResponse(response)
    except Exception:
        response['code'] = -1
        response['msg'] = '异常错误，请重试'
        return JsonResponse(response)


# 编辑选课更改课程部分
@check_token
@require_POST
def getCourseName(request):
    response = {
        'code': 1,
        'msg': '获取课程名字',
        'datas': {}
    }
    request_data = json.loads(request.body, encoding='utf-8')
    crs_no = request_data.get('courseno', 'none')
    try:
        crs_name = Course.objects.filter(crs_no=crs_no).first().crs_name
        response['datas']['courseName'] = crs_name
        return JsonResponse(response)
    except Exception:
        response['code'] = -1
        response['msg'] = '异常错误，请重试'
        return JsonResponse(response)


# 编辑选课信息
@check_token
@require_POST
def editCrsArrange(request):
    datas = {}
    response = {
        'code': 1,
        'msg': '编辑选课信息',
        'datas': datas
    }
    request_data = json.loads(request.body, encoding='utf-8')
    # {'teaCrsNo': 33, 'grade': 2018, 'term': '20212', 'teacherno': '20081101', 'courseno': 10001, 'area': '教学楼B区',
    #  'room': 'B101', 'week': 'Mon', 'time': '3', 'total': 40, 'teacherName': '666老师'}
    print(request_data)
    tea_crs_no = request_data.get('teaCrsNo', 'none')
    grade = request_data.get('grade', 'none')
    term = request_data.get('term', 'none')
    courseno = request_data.get('courseno', 'none')
    teacherno = request_data.get('teacherno', 'none')
    area = request_data.get('area', 'none')
    room = request_data.get('room', 'none')
    week = request_data.get('week', 'none')
    time = request_data.get('time', 'none')
    total = int(request_data.get('total', 'none'))
    try:
        with transaction.atomic():
            tea_crs_obj = TeaCrs.objects.filter(tea_crs_no=tea_crs_no).first()
            # if total < tea_crs_obj.total:   # 修改后的人数不能少于原来人数或者已选人数
            if total < tea_crs_obj.selected:  # 修改后的人数不能少于原来人数或者已选人数
                response['code'] = -1
                response['msg'] = '选课最大人数不符合规范，必须比原来的人数多'
                return JsonResponse(response)
            spot_obj = Spot.objects.filter(spt_no=room).first()
            print(spot_obj)
            term_obj = Term.objects.filter(term_no=int(term)).first()
            crs_obj = Course.objects.filter(crs_no=courseno).first()
            tea_obj = Teacher.objects.filter(tea_no=teacherno).first()
            if not spot_obj or not term_obj or not crs_obj or not tea_obj:
                response['code'] = -1
                response['msg'] = '数据出错'
                return JsonResponse(response)
            # print(spot_obj, term_obj, crs_obj, tea_obj)

            tea_crs_obj.tea_no = tea_obj
            tea_crs_obj.crs_no = crs_obj
            tea_crs_obj.term = term_obj
            tea_crs_obj.time = time
            tea_crs_obj.spot = spot_obj
            tea_crs_obj.week = week
            tea_crs_obj.total = total
            tea_crs_obj.grade = str(grade)
            tea_crs_obj.save(update_fields=['tea_no', 'crs_no', 'term', 'time', 'spot', 'week', 'total', 'grade'])
            return JsonResponse(response)
    except Exception:
        response['code'] = -1
        response['msg'] = '网络异常出错'
        return JsonResponse(response)


# 删除选课信息
@check_token
@require_POST
def delCrsArrange(request):
    datas = {}
    response = {
        'code': 1,
        'msg': '删除选课信息',
        'datas': datas
    }
    request_data = json.loads(request.body, encoding='utf-8')
    # print(request_data)
    tea_course_id = request_data.get('id', 'none')
    if tea_course_id == 'none' or tea_course_id == '':
        response['code'] = -1
        response['msg'] = '选课信息不存在，请刷新页面'
        return JsonResponse(response)
    # 删除该课程数据
    TeaCrs.objects.filter(tea_crs_no=tea_course_id).first().delete()
    return JsonResponse(response)


# 批量删除选课信息
@check_token
@require_POST
def batchDelCourseArrange(request):
    datas = {}
    response = {
        'code': 1,
        'msg': '删除选课信息',
        'datas': datas
    }
    request_data = json.loads(request.body, encoding='utf-8')
    # print(request_data)
    tea_crs_list = request_data.get('ids', 'none')
    if tea_crs_list == 'none' or tea_crs_list == []:
        response['code'] = -1
        response['msg'] = '选课信息不存在，请刷新页面'
        return JsonResponse(response)
    # 删除该课程数据
    try:
        for tea_crs_no in tea_crs_list:
            TeaCrs.objects.filter(tea_crs_no=tea_crs_no).first().delete()
    except Exception:
        pass
    return JsonResponse(response)


# 上传选排课excel表
@check_token
def uploadCourseArrange(request):
    response = {
        'code': 1,
        'msg': '选课信息导入',
        'datas': {}
    }

    # print(request.body.split(b'\r\n')[1].decode())
    request_bytesList = request.body.split(b'\r\n')
    # print(request_bytesList[1].decode().split(';')[2][11:-1])
    filename = request_bytesList[1].decode().split(';')[2][11:-1]
    file_name = './' + filename
    # print(filename)
    if os.path.exists(file_name):
        os.remove(file_name)
    with open(file_name, 'ab') as f:
        f.write(request_bytesList[4])

    # with open('./xxx.csv','r',errors='ignore') as f:
    #     csv_read = csv.reader(f)
    #     print(csv_read)
    #     for line in csv_read:
    #         print(line)
    head = ['teacherno', 'courseno', 'term', 'spot', 'time',
            'week', 'total', 'grade', 'is_public']
    def excel_one_line_to_list():
        df = pd.read_excel(file_name,
                           usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8],   # 0,1,2分别指取的列数
                           names=None)  # 读取项目名称列,不要列名
        print(df)
        df_header = df.columns.to_list()
        df_li = df.values.tolist()
        result = []
        for s_li in df_li:
            result.append(s_li)
        return result, df_header
    try:
        data_list, df_headers = excel_one_line_to_list()
        print(df_headers)
        if len(df_headers) != len(head):
            return handelFileError(file_name, '上传选课信息出错', '文件格式不符合规范，请检查文件后再上传!')
        for i in range(len(head)):
            if i < len(df_headers) and df_headers[i] != head[i]:
                return handelFileError(file_name, '上传选课信息出错', '文件格式不符合规范，请检查文件后再上传!')

    except Exception as e:
        return handelFileError(file_name, '上传选课信息出错', e)

    totalNum = len(data_list)
    success = 0
    error_list = []
    for row in data_list:
        try:
            # [教师编号, 课程编号, 学期编号, 上课地点, 上课时间, 星期几上课, 最大选课人数, 开课年级]
            # [20021103, 10004, '2021-2022第一学年-20212', '0102-教学楼A区-A102', 1, 'Mon', 30, 2018]
            # [20021103, 10004, '第二学年-20211', '0102-教学楼A区-A102', 1, 'Mon', 30, 2018]
            term_obj = Term.objects.filter(term_no=int(row[2][-5:])).first()
            course_obj = Course.objects.filter(crs_no=row[1]).first()
            spt_no = row[3][0:4]
            spot_obj = Spot.objects.filter(spt_no=spt_no).first()
            tea_obj = Teacher.objects.filter(tea_no=str(row[0])).first()
            # print(term_obj,course_obj,spt_no,spot_obj,tea_obj)
            if not term_obj or not course_obj or not spot_obj or not tea_obj:
                continue

            TeaCrs.objects.create(tea_no=tea_obj,
                                  crs_no=course_obj,
                                  term=term_obj,
                                  time=str(row[4]),
                                  spot=spot_obj,
                                  week=row[5],
                                  selected=0,
                                  total=row[6],
                                  grade=str(row[7]),
                                  is_public=str(row[8]))
            success += 1
        except Exception as e:
            if len(row) > 1:
                error_list.append(str(row[0]) + '-' + str(row[1]))
        # print(error_list)

    datas = {}
    datas['success'] = success
    datas['totalNum'] = totalNum
    datas['failed'] = totalNum - success
    datas['errorList'] = error_list
    response['datas'] = datas
    os.remove('./'+filename)
    return JsonResponse(response)


# 开启或关闭选课
@check_token
def openOrCloseStuSelect(request):
    response = {
        'code': 1,
        'msg': 'none',
        'datas': {}
    }
    request_data = json.loads(request.body, encoding='utf-8')
    # {'active': '20212'}
    term_no = request_data.get('active', 'none')
    grade = request_data.get('grade', 'none')
    # select_num = request_data.get('limitNum', 'none')  # 控制最大选课课程数
    print(request_data)
    option = Active.objects.first().option
    if option == 0:
        # grade = grade if grade
        # Active.objects.update(name=term_no, option=1, grade=grade)
        Active.objects.update(name=term_no, option=1, grade=str(grade))
        # Active.objects.update(name=term_no, select_num=int(select_num), option=1)
        print('*****开启选课******')
        response['msg'] = '开启选课'
    else:
        Active.objects.update(option=0)
        print('*****关闭选课******')
        response['msg'] = '关闭选课'
    return JsonResponse(response)


# 获取当前选课年级和学期
@check_token
def getActiveSelect(request):
    response = {
        'code': 1,
        'msg': 'none',
        'datas': {}
    }

    active_obj = Active.objects.first()
    option = active_obj.option
    print(active_obj.name.term_no,active_obj.grade)
    if option == 0:
        response['msg'] = '还没开始选课呢!'
    else:
        response['datas']['term'] = str(active_obj.name.term_no)
        response['datas']['grade'] = int(active_obj.grade)
        response['msg'] = '已经开启选课了'
    print(222222)
    return JsonResponse(response)


# 授权中心数据展示--权限数据
@check_token
def getRoleData(request):
    userRole_list = UserRole.objects.all()
    datas = []
    response = {
        'code': 1,
        'msg': '用户中心',
        'datas': datas
    }
    for row in userRole_list:
        temp = {}
        temp['uid'] = row.uid.tea_no
        temp['teaName'] = row.uid.tea_name
        temp['department'] = row.uid.tea_dpt.dpt_name
        temp['telephone'] = row.uid.tea_tel
        temp['name'] = row.rid.name
        datas.append(temp)
    # print(response)
    return JsonResponse(response)
    pass


# 添加管理员
@check_token
@require_POST
def addAdmin(request):
    datas = []
    response = {
        'code': -1,
        'msg': '添加管理员',
        'datas': datas
    }
    userid = request.META.get('HTTP_USERID', 'none')
    request_data = json.loads(request.body, encoding='utf-8')
    uid = request_data.get('uid', 'none')
    role_name = request_data.get('name', 'none')
    print(request_data)
    if uid == 'none' or role_name == 'none':
        response['msg'] = '没有输入用户'
        return JsonResponse(response)
    tea_obj = Teacher.objects.filter(tea_no=uid).first()
    role_obj = Role.objects.filter(rid=role_name).first()

    if not tea_obj:
        response['msg'] = '没有该老师的信息'
        return JsonResponse(response)
    if UserRole.objects.filter(uid=tea_obj).first():
        response['msg'] = '该老师的权限已存在'
        return JsonResponse(response)

    result = UserRole.objects.create(uid=tea_obj, rid=role_obj)
    response['code'] = 1
    system_logger.info(request, "- id:{0}添加管理员 id:{1}".format(str(userid), str(uid)))
    return JsonResponse(response)


# 删除管理员
@check_token
@require_POST
def delAdmin(request):
    datas = []
    response = {
        'code': -1,
        'msg': '删除管理员',
        'datas': datas
    }
    userid = request.META.get('HTTP_USERID', 'none')
    request_data = json.loads(request.body, encoding='utf-8')
    uid = request_data.get('id', 'none')
    if uid == 'none':
        response['msg'] = '网络出错，请重新操作'
        return JsonResponse(response)
    response['code'] = 1
    result = UserRole.objects.filter(uid=uid).delete()
    system_logger.info(request, "- id:{0}删除管理员 id:{1}".format(str(userid), str(uid)))
    return JsonResponse(response)


# 批量删除管理员
def batchDelAdm(request):
    datas = []
    response = {
        'code': -1,
        'msg': '删除管理员',
        'datas': datas
    }
    userid = request.META.get('HTTP_USERID', 'none')
    request_data = json.loads(request.body, encoding='utf-8')
    uid_list = request_data.get('ids', 'none')
    if uid_list == 'none':
        response['msg'] = '网络出错，请重新操作'
        return JsonResponse(response)

    for uid in uid_list:
        UserRole.objects.filter(uid=uid).delete()
    response['code'] = 1
    response['msg'] = '批量删除成功'
    system_logger.info(request, "- id:{0}批量删除管理员".format(str(userid)))
    return JsonResponse(response)


# 提升管理权限
@check_token
@require_POST
def upToSuperAdmin(request):
    datas = []
    response = {
        'code': -1,
        'msg': '提升到超级管理员',
        'datas': datas
    }
    userid = request.META.get('HTTP_USERID', 'none')
    request_data = json.loads(request.body, encoding='utf-8')
    print(request_data)
    uid = request_data.get('id', 'none')
    UserRole.objects.filter(uid=uid).update(rid='super_admin')
    response['code'] = 1
    system_logger.info(request, "- id:{0}设id:{1}为超级管理员".format(str(userid), str(uid)))
    return JsonResponse(response)


# 降低管理权限
@check_token
@require_POST
def upToAdmin(request):
    datas = []
    response = {
        'code': -1,
        'msg': '降权为管理员',
        'datas': datas
    }
    userid = request.META.get('HTTP_USERID', 'none')
    request_data = json.loads(request.body, encoding='utf-8')
    # {'id': '20030119'}
    uid = request_data.get('id', 'none')
    UserRole.objects.filter(uid=uid).update(rid='admin')
    response['code'] = 1
    system_logger.info(request, "- id:{0}设id:{1}为管理员".format(str(userid), str(uid)))
    return JsonResponse(response)


# 添加班级
def addClass(request):
    datas = []
    response = {
        'code': -1,
        'msg': '添加班级',
        'datas': datas
    }
    request_data = json.loads(request.body, encoding='utf-8')
    print(request_data)
    classId = request_data.get('classId', 'none')  # 01/02
    className = request_data.get('className', 'none')   # 'xxx班'
    dptNo = request_data.get('dptNo', 'none')   # '01'
    grade = request_data.get('classGrade', 0)   # 2015
    classId = str(grade) + dptNo + classId
    if classId == 'none' or className == 'none' or dptNo == 'none' or grade == 0:
        response['msg'] = '请重新检查输入是否有误'
        return JsonResponse(response)
    dpt_obj = Department.objects.filter(dpt_no=dptNo).first()
    if not dpt_obj:
        response['msg'] = '学院有误'
        return JsonResponse(response)
    TblClass.objects.create(class_no=classId, class_name=className, class_dpt=dpt_obj, class_grade=str(grade))
    response['code'] = 1
    return JsonResponse(response)


# 修改班级
def editClass(request):
    datas = []
    response = {
        'code': -1,
        'msg': '添加班级',
        'datas': datas
    }
    request_data = json.loads(request.body, encoding='utf-8')
    print(request_data)
    classId = request_data.get('classId', 'none')
    className = request_data.get('className', 'none')
    dptNo = request_data.get('dptNo', 'none')
    grade = request_data.get('classGrade', 0)
    if classId == 'none' or className == 'none' or dptNo == 'none' or grade == 0:
        response['msg'] = '请重新检查输入是否有误'
        return JsonResponse(response)
    class_obj = TblClass.objects.filter(class_no=classId).first()
    class_obj.class_name = className
    class_obj.dpt_no = dptNo
    class_obj.class_grade = str(grade)
    print(class_obj.class_grade)
    class_obj.save()

    response['code'] = 1
    return JsonResponse(response)


# 删除班级
def delClass(request):
    datas = []
    response = {
        'code': -1,
        'msg': '删除班级',
        'datas': datas
    }
    request_data = json.loads(request.body, encoding='utf-8')
    print(request_data)
    classId = request_data.get('classId', 'none')
    if classId == 'none':
        response['msg'] = '班级删除出错，请重试'
        return JsonResponse(response)

    TblClass.objects.filter(class_no=classId).delete()
    response['code'] = 1
    return JsonResponse(response)


# 批量删除班级
def batchDelClass(request):
    datas = []
    response = {
        'code': -1,
        'msg': '删除班级',
        'datas': datas
    }
    request_data = json.loads(request.body, encoding='utf-8')
    print(request_data)
    classId_list = request_data.get('ids', 'none')
    try:
        for class_no in classId_list:
            TblClass.objects.filter(class_no=class_no).delete()
    except Exception:
        pass
    response['code'] = 1
    response['msg'] = '删除成功'
    return JsonResponse(response)


# 批量导入班级
def uploadClass(request):
    response = {
        'code': 1,
        'msg': '导入班级',
        'datas': ''
    }

    # print(request.body.split(b'\r\n')[1].decode())
    request_bytesList = request.body.split(b'\r\n')
    # print(request_bytesList[1].decode().split(';')[2][11:-1])
    filename = request_bytesList[1].decode().split(';')[2][11:-1]
    file_name = './'+filename
    if os.path.exists(file_name):
        os.remove(file_name)
    with open(file_name, 'ab') as f:
        f.write(request_bytesList[4])

    # with open('./xxx.csv','r',errors='ignore') as f:
    #     csv_read = csv.reader(f)
    #     print(csv_read)
    #     for line in csv_read:
    #         print(line)
    head = ['class_no', 'class_name', 'class_dpt', 'class_grade']
    def excel_one_line_to_list():
        df = pd.read_excel(file_name,
                           usecols=[0, 1, 2, 3],  # 0,1,2分别指取的列数
                           names=None)  # 读取项目名称列,不要列名
        print(df)
        df_header = df.columns.to_list()
        df_li = df.values.tolist()
        result = []
        for s_li in df_li:
            result.append(s_li)
        return result, df_header
    try:
        data_list, df_headers = excel_one_line_to_list()
        print(df_headers)
        if len(df_headers) != len(head):
            return handelFileError(file_name, '上传班级信息出错', '文件格式不符合规范，请检查文件后再上传!')
        for i in range(len(head)):
            if i < len(df_headers) and df_headers[i] != head[i]:
                return handelFileError(file_name, '上传班级信息出错', '文件格式不符合规范，请检查文件后再上传!')
    except Exception as e:
        return handelFileError(file_name, '上传班级信息出错', e)

    totalNum = len(data_list)
    success = 0
    error_list = []

    for row in data_list:
        # 班级编号   名称  学院  年级
        # [20170103, '汉语言2班', '01-文学院', 2017]
        try:
            dpt_no = row[2][0:2]
            # 校验班级编号是否符合规则，是否已存在
            # print(str(row[0])[4:6], str(row[0])[0:4])
            if dpt_no != str(row[0])[4:6] or str(row[3]) != str(row[0])[0:4] or TblClass.objects.filter(class_no=str(row[0])).first():
                error_list.append(str(row[0]) + '-' + row[1])
                continue

            dpt_obj = Department.objects.filter(dpt_no=dpt_no).first()
            if not dpt_obj:
                error_list.append(str(row[0])+'-'+row[1])
                continue
            TblClass.objects.create(class_no=str(row[0]),
                                    class_name=row[1],
                                    class_dpt=dpt_obj,
                                    class_grade=str(row[3]))
            success += 1
        except Exception as e:
            if len(row) > 1:
                error_list.append(str(row[0])+str(row[1]))

    datas = {}
    datas['success'] = success
    datas['totalNum'] = totalNum
    datas['failed'] = totalNum - success
    datas['errorList'] = error_list
    response['datas'] = datas
    os.remove('./' + filename)
    return JsonResponse(response)


def test(request):
    import binascii
    obj = Student.objects.filter(stu_no='2017324120').first()
    print(obj.stu_pwd)
    en_pwd = obj.stu_pwd
    s_hex = binascii.hexlify(en_pwd)
    print(s_hex)
    response = {
        's': 1
    }
    Student.objects.filter(stu_no='2017324120').update(stu_pwd=b'5a228c96a65ba383632c1ee156ef4dd3')
    obj = Student.objects.filter(stu_no='2017324120').first()
    print(obj.stu_pwd)
    return JsonResponse(response)
