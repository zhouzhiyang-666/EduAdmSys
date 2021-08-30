from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from public import models
from teacher.models import Teacher
from student.models import Student
from admin.models import Admin
from edusystem.settings import logger    # 系统运行日志模块

import json

from utils.checkToken import Token    # token验证--验证码--模块
from django_redis import get_redis_connection
from utils.writeLogger import LoggerTool   # 日志管理
from utils.validateToken import check_token    # 用于token验证装饰器 每个请求必须token校验过关
tokenRedis = get_redis_connection('default')  # token的redis
codeRedis = get_redis_connection('img_code')   # 登录验证码redis
phoneCodeRedis = get_redis_connection('phone_code')  # 修改手机号验证码redis
system_logger = LoggerTool()

# 登录验证码模块
@require_GET
def checkcode(request):
    # 生成MD5
    import hashlib
    myHash = hashlib.md5()
    # 需要用到的模块
    from PIL import Image, ImageDraw, ImageFont
    import random
    from io import BytesIO
    import base64
    import time

    # 随机图片的颜色
    def get_random_color():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # 随机字符串
    def get_random_char():
        random_num = str(random.randint(0, 9))
        random_upper_alph = chr(random.randint(65, 90))
        random_lowwer_alph = chr(random.randint(97, 122))
        # 随机选择一个
        random_char = random.choice([random_num, random_lowwer_alph, random_upper_alph])

        return random_char

    # 创建一张图片
    image = Image.new(mode="RGB", size=(260, 40), color=get_random_color())
    # 获取一个画笔对象
    draw = ImageDraw.Draw(image, mode="RGB")
    # 获取一个文字对象，文字文件需要下载并引入这里，并设置字体大小
    font = ImageFont.truetype("../static/font/ARIALNI.TTF", 32)

    valid_code_str = ""
    # 随机生成5个字符串并写入图片中
    for i in range(1, 6):
        char = get_random_char()
        valid_code_str += char
        draw.text([i * 40, 5], char, get_random_color(), font=font)

    # width = 260
    # height = 40
    # for i in range(80):
    #     draw.point((random.randint(0,width),random.randint(0,height)),fill=get_random_color())
    #
    # for i in range(10):
    #     x1=random.randint(0,width)
    #     x2=random.randint(0,width)
    #     y1=random.randint(0,height)
    #     y2=random.randint(0,height)
    #     draw.line((x1,y1,x2,y2),fill=get_random_color())
    # for i in range(40):
    #     draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
    #     x = random.randint(0, width)
    #     y = random.randint(0, height)
    #     draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())

    f = BytesIO()
    image.save(f, "png")
    img_b64 = f.getvalue()
    # print(valid_code_str)

    # 将验证码存放在redis里
    uuid = str(time.time())
    myHash.update(uuid.encode(encoding='utf-8'))
    uuid = myHash.hexdigest()
    data = {
        'code': 1,
        'uuid': uuid,
        'data': base64.b64encode(img_b64).decode('utf8')
    }
    # 生成token
    codeRedis.set(uuid, valid_code_str.upper(), 60)  # 缓存token，保存60秒
    return JsonResponse(data)


# 忘记密码页面获取的验证码
def getResetPwdCode(request):
    response = {
        'code': 1,
        'msg': 'None',
        'datas': {
            'phoneCode': ''
        }
    }
    # 1 获取登录信息
    request_data = json.loads(request.body)
    user_id = request_data.get('userid', 'none')
    phone_number = request_data.get('phoneNumber', 'none')
    # print(request_data)

    if user_id == 'none' or phone_number == 'none':
        response['code'] = -1
        response['msg'] = '个人信息有误'
        return JsonResponse(response)

    userInfo_obj = Teacher.objects.filter(tea_no=user_id, tea_tel=phone_number).first()
    if not userInfo_obj:  # 不是老师账号
        userInfo_obj = Student.objects.filter(stu_no=user_id, stu_tel=phone_number).first()
    if not userInfo_obj:
        response['code'] = -1
        response['msg'] = '个人信息有误'
        return JsonResponse(response)

    # 生成MD5
    # import time
    import random
    # import hashlib
    # myHash = hashlib.md5()
    # codeKey = str(time.time())
    # myHash.update(codeKey.encode(encoding='utf-8'))
    # codeKey = myHash.hexdigest()

    # 随机字符串
    def get_random_char():
        random_num = str(random.randint(0, 9))
        random_upper_alph = chr(random.randint(65, 90))
        random_lowwer_alph = chr(random.randint(97, 122))
        # 随机选择一个
        random_char = random.choice([random_num, random_lowwer_alph, random_upper_alph])
        return random_char
    # 随机生成5个字符串并写入图片中
    phone_code_str = ""
    for i in range(1, 6):
        char = get_random_char()
        phone_code_str += char
    # 生成token
    phoneCodeRedis.set(user_id + '-' + phone_number, phone_code_str.upper(), 600)  # 缓存token，保存10分钟
    response['datas']['phoneCode'] = phone_code_str
    return JsonResponse(response)


# 通过登录页重置密码
def ResetPwdByInfo(request):
    response = {
        'code': 1,
        'msg': 'None',
        'datas': {
            'phoneCode': ''
        }
    }
    # 1 获取登录信息
    request_data = json.loads(request.body)
    user_id = request_data.get('user', 'none')
    phone_number = request_data.get('tel', 'none')
    vcode = request_data.get('vcode', 'none')
    password = request_data.get('pass', 'none')
    check_pass = request_data.get('checkPass', 'none')
    # print(request_data)

    if password == 'none' or check_pass == 'none' or password != check_pass:
        response['code'] = -1
        response['msg'] = '两次输入的密码不一样，请重新输入'
        return JsonResponse(response)

    if not Token.check_token(phoneCodeRedis, user_id + '-' + phone_number, vcode.upper()):
        response['code'] = -1
        print('验证码错误。。。。。。。。。。。。。。。。。。')
        response['msg'] = '验证码错误'
        return JsonResponse(response)

    userInfo_obj = Teacher.objects.filter(tea_no=str(user_id)).first()
    if userInfo_obj:  # 是老师账号
        userInfo_obj.tea_pwd = password.encode()
        userInfo_obj.save()
    else:
        userInfo_obj = Student.objects.filter(stu_no=str(user_id)).first()
        if userInfo_obj:   # 是学生账号
            userInfo_obj.stu_pwd = password.encode()
            userInfo_obj.save()
        else:     # 不是学生也不是老师，直接退出
            response['code'] = -1
            response['msg'] = '没有该用户，请重新输入个人信息'
            return JsonResponse(response)

    response['msg'] = '修改密码成功！'
    return JsonResponse(response)


# 校验token,手机验证码
@check_token
def getPhoneCode(request):
    # 生成MD5
    # import time
    import random
    # import hashlib
    # myHash = hashlib.md5()
    # codeKey = str(time.time())
    # myHash.update(codeKey.encode(encoding='utf-8'))
    # codeKey = myHash.hexdigest()

    # 随机字符串
    def get_random_char():
        random_num = str(random.randint(0, 9))
        random_upper_alph = chr(random.randint(65, 90))
        random_lowwer_alph = chr(random.randint(97, 122))
        # 随机选择一个
        random_char = random.choice([random_num, random_lowwer_alph, random_upper_alph])
        return random_char
    # 随机生成5个字符串并写入图片中
    phone_code_str = ""
    for i in range(1, 6):
        char = get_random_char()
        phone_code_str += char
    # 生成token
    phoneCodeRedis.set(phone_code_str, phone_code_str, 600)  # 缓存token，保存6分钟
    response = {
        'code': 1,
        'msg': 'None',
        'datas': {
            'phoneCode': phone_code_str
        }
    }
    return JsonResponse(response)


# 登录  学生或者老师
@require_POST
def login(request):
    # tokenRedis = get_redis_connection('default')
    # 去数据库查找有没有这个用户，有的话再存session
    # 解决娶不到字符串数据问题
    response = {
        'code': -1,
        'msg': 'None',
        'datas': {
            'userid': '',
            'token': '',
        }
    }
    if not request.body:
        response['msg'] = '请输入账号密码！！'
        return JsonResponse(response)
    # 1 获取登录信息
    request_data = json.loads(request.body)
    # {'user': 'sef', 'passwd': '38f0b4a9f8d7ef4915f3b77e7a8d0ef9', 'vcode': 'sefs', 'userType': '1'}
    user_id = request_data.get('user', 'deflt')
    password = request_data.get('passwd', 'deflt')
    checkcode = request_data.get('vcode', '0000')
    uuid = request.META.get('HTTP_UUID', 'none')  # 验证码需要用到
    user_type = request_data.get('userType', '0000')
    # import chardet
    # print(chardet.detect(password.encode()))
    # print('登录密码', password.encode())
    # 校验验证码
    # Token.check_token(myRedis, uuid, checkcode)
    # print(Token.get_token(userid))
    # print('输入的验证码---',checkcode.upper())
    if not Token.check_token(codeRedis, uuid, checkcode.upper()):
        response['msg'] = '验证码错误'
        system_logger.error(request, "- 验证码错误 id:{}".format(str(user_id)))
        return JsonResponse(response)

    # 3 校验用户登录信息
    if user_type == '1':
        user_obj = Student.objects.filter(stu_no=str(user_id), stu_pwd=password.encode()).first()
        if user_obj:
            response['code'] = 1
            username = user_obj.stu_name
    elif user_type == '2':
        user_obj = Teacher.objects.filter(tea_no=str(user_id), tea_pwd=password.encode()).first()
        if user_obj:
            response['code'] = 2
            username = user_obj.tea_name
    else:
        response['msg'] = '登录出错'
        system_logger.info(request, "- 登录出错 id:{}".format(str(user_id)))
        return JsonResponse(response)

    if not user_obj:
        response['msg'] = '用户名或密码错误'
        system_logger.info(request, "- 登录失败 id:{}".format(str(user_id)))
        return JsonResponse(response)

    # 生成token
    token = Token.create_token(user_id, password)
    tokenRedis.set(user_id, token, 86400)   # 缓存token，保存一天
    response['msg'] = '登录成功'
    response['datas']['userid'] = user_id
    response['datas']['token'] = token
    response['datas']['username'] = username
    # print(Token.check_token(tokenRedis, username, token))
    system_logger.info(request, "- 登录成功 id:{}".format(str(user_id)))
    return JsonResponse(response)



@check_token
def logout(request):
    # tokenRedis = get_redis_connection('default')
    # 去数据库查找有没有这个用户，有的话再存session
    # 解决娶不到字符串数据问题
    response = {
        'code': 0,
        'msg': 'None',
        'datas': {}
    }
    userid = request.META.get('HTTP_USERID', 'none')

    tokenRedis.delete(userid)
    response['code'] = 302
    response['msg'] = '退出登录成功!'
    system_logger.info(request, "- 退出登录 id:{}".format(str(userid)))
    return JsonResponse(response)


@check_token
def changePwd(request):
    response = {
        'code': -1,
        'msg': 'None',
    }
    # 获取用户信息
    userid = request.META.get('HTTP_USERID', 'none')
    request_data = json.loads(request.body, encoding='utf-8')
    old_pwd = request_data.get('oldPass', 'none')
    new_pwd = request_data.get('newPass', 'none')
    check_pwd = request_data.get('checkPass', 'none')

    if not request.body or userid == 'none':
        response['msg'] = '密码修改失败！'
        return JsonResponse(response)

    if new_pwd != check_pwd:
        response['msg'] = '两次输入密码不一致'
        return JsonResponse(response)
    print(request_data)

    tea_info = Teacher.objects.filter(tea_no=userid).first()
    stu_info = Student.objects.filter(stu_no=userid).first()
    adm_info = Admin.objects.filter(adm_name=userid).first()
    # print(old_pwd.encode(), adm_info.adm_pwd)
    # 读取数据库密码
    type = 0    # 处理类型 1老师  2学生  3 管理员
    if tea_info:
        user_pwd = tea_info.tea_pwd
        type = 1
    if stu_info:
        user_pwd = stu_info.stu_pwd
        type = 2
    if adm_info:
        user_pwd = adm_info.adm_pwd
        type = 3

    if old_pwd.encode() != user_pwd:
        response['code'] = 2
        response['msg'] = '旧密码错误'
        return JsonResponse(response)

    if type == 1:
        Teacher.objects.filter(tea_no=userid).update(tea_pwd=new_pwd.encode())
    if type == 2:
        Student.objects.filter(stu_no=userid).update(stu_pwd=new_pwd.encode())
    if type == 3:
        Admin.objects.filter(adm_name=userid).update(adm_pwd=new_pwd.encode())

    response['code'] = 1
    response['msg'] = '修改密码成功!!!'
    return JsonResponse(response)
    pass


# 获取路由
def getRoute(request):
    response = {
        'code': -1,
        'msg': 'None',
        'datas': {}
    }
    request_data = json.loads(request.body)
    print(request_data)
    return JsonResponse(response)


# 修改手机号
@check_token
@require_POST
def changePhone(request):
    response = {
        'code': -1,
        'msg': '修改手机号',
        'datas': {}
    }
    userid = request.META.get('HTTP_USERID')
    request_data = json.loads(request.body, encoding='utf-8')
    old_telephone = request_data.get('oldTel', 'none')
    telephone = request_data.get('telephone', 'none')
    phoneCode = request_data.get('phoneCode', 'none')
    print(request_data)

    # 校验验证码
    if not Token.check_token(phoneCodeRedis, phoneCode, phoneCode):
        response['msg'] = '验证码错误'
        return JsonResponse(response)

    try:
        selfInfo_obj = Student.objects.filter(stu_no=userid, stu_tel=old_telephone)
        print('stu', selfInfo_obj)
        if selfInfo_obj.stu_no:
            selfInfo_obj.update(stu_tel=telephone)
        print(111)
    except Exception as e:
        selfInfo_obj = Teacher.objects.filter(tea_no=userid, tea_tel=old_telephone)
        print('tea', selfInfo_obj)
        if selfInfo_obj.exists():
            selfInfo_obj.update(tea_tel=telephone)
            response['code'] = 1
            response['msg'] = '修改成功'
            return JsonResponse(response)
        if not selfInfo_obj:
            response['msg'] = '原手机号错误'
            return JsonResponse(response)
    else:
        response['code'] = 1
        response['msg'] = '修改成功'
        return JsonResponse(response)
    # finally:
    #     response['code'] = 1
    #     response['msg'] = '修改成功'
    #     return JsonResponse(response)


# 获取学期课表
@check_token
def getStuScore(request):
    score = models.Score.objects.all()
    datas = []
    for row in score:
        print(row.stu_no.stu_no, row.stu_no.stu_name, row.stu_no.stu_class.class_name, row.tea_crs_no.tea_no.tea_name, row.score_pro, row.score_end, row.score)

        temp = {}
        temp['index'] = '111111'
        temp['stuId'] = row.stu_no.stu_no
        temp['classAndGrade'] = row.stu_no.stu_class.class_name
        temp['stuName'] = row.stu_no.stu_name
        temp['score'] = row.score
        datas.append(temp)
    print('-------------------------------------')

    response = {
        'code': 1,
        'msg': 'xxx课表',
        'datas': datas
    }
    return HttpResponse(json.dumps(response))
    pass


# 获取学期课表
@check_token
def getTermCourse(request):
    if request.body:
        datas = []
        response = {
            'code': 1,
            'msg': '学期课表',
            'datas': datas
        }
        user_id = request.META.get('HTTP_USERID', 'none')

        request_data = json.loads(request.body, encoding='utf-8')
        print(request_data)
        print(user_id)
        term_no = request_data.get('term', 'none')
        user_type = request_data.get('userType', 'none')  # 用户类型  '1' 学生  '2' 教师   '3'管理员
        # 补上学生或者教室id查对应的课表
        # print(request_data)
        # if user_id == 'none' or user_id != 'admin':
        #     term_course = models.TeaCrs.objects.filter(term__term_no=term_no)
        # else:
        #     term_course = models.TeaCrs.objects.filter(term__term_no=term_no)
        try:
            if user_type == '1':
                if user_id == 'none' or user_id != 'admin':
                    term_score = models.Score.objects.filter(stu_no=user_id, tea_crs_no__term=term_no)
                else:
                    response['msg'] = '暂未排课'
                    return JsonResponse(response)
                for row in term_score:
                    temp = {}
                    coursename = row.tea_crs_no.crs_no.crs_name
                    teacher = row.tea_crs_no.tea_no.tea_name
                    location = row.tea_crs_no.spot.spt_area
                    location_room = row.tea_crs_no.spot.spt_room
                    temp['week'] = row.tea_crs_no.week
                    temp['time'] = row.tea_crs_no.time
                    temp['span'] = row.tea_crs_no.crs_no.crs_hours
                    temp['odd-even'] = 1
                    temp['info'] = coursename + '\n' + teacher + '\n' + location + location_room + '\n单双周'
                    datas.append(temp)
                return JsonResponse(response)
            else:
                if user_id == 'none' or user_id != 'admin':
                    term_course = models.TeaCrs.objects.filter(tea_no=user_id, term=term_no)
                else:
                    response['msg'] = '暂未排课'
                    return JsonResponse(response)
                for row in term_course:
                    print(row)
                    temp = {}
                    coursename = row.crs_no.crs_name
                    teacher = row.tea_no.tea_name
                    location = row.spot.spt_area
                    location_room = row.spot.spt_room
                    temp['week'] = row.week
                    temp['time'] = row.time
                    temp['span'] = row.crs_no.crs_hours
                    temp['odd-even'] = 1
                    temp['info'] = coursename + '\n' + teacher + '\n' + location + location_room + '\n单双周'
                    datas.append(temp)
                return JsonResponse(response)
        except Exception as e:
            print(e)
            return JsonResponse(response)


# 获取教室编号 RoomTable.vue
@check_token
def getRoomByArea(request):
    request_data = json.loads(request.body, encoding='utf-8')
    # print(request_data)
    area_list = models.Spot.objects.filter(spt_area=request_data.get('area', 'default'))
    datas = []
    for row in area_list:
        temp = {}
        temp['id'] = row.spt_no
        temp['room'] = row.spt_room
        print(row.spt_no, row.spt_area, row.spt_room)
        datas.append(temp)
    response = {
        'code': 1,
        'msg': '教室号',
        'datas': datas
    }
    return JsonResponse(response)


# 获取学期课表和教室课表  Termtable.vue
@check_token
def getRoomCourse(request):
    datas = []
    response = {
        'code': 1,
        'msg': '学期/教室课表',
        'datas': datas
    }
    if request.body:
        request_data = json.loads(request.body, encoding='utf-8')
        # print(request_data)
        if request_data.get('room', 'none') == 'none':  # 学期课表
            term_course = models.TeaCrs.objects.filter(term__term_no=request_data.get('term', 'none'))
        else:       # 教室课表
            term_course = models.TeaCrs.objects.filter(term__term_no=request_data.get('term', 'none'),
                                                       spot__spt_no=request_data.get('room', 'none')
                                                       )
    else:
        term_course = models.TeaCrs.objects.all()

    for row in term_course:
        print(row.tea_crs_no,
              row.tea_no.tea_name,
              row.crs_no.crs_name,
              row.term.term_name,
              row.time, row.spot.spt_area,
              row.week, row.selected, row.total, row.grade)
        temp = {}
        temp['week'] = row.week
        temp['time'] = row.time
        coursename = row.crs_no.crs_name
        teacher = row.tea_no.tea_name
        location = row.spot.spt_area
        location_room = row.spot.spt_room
        temp['span'] = row.crs_no.crs_hours
        temp['odd-even'] = 1
        temp['info'] = coursename + '\n' + teacher + '\n' + location + location_room + '\n单双周'
        datas.append(temp)

    return JsonResponse(response)


# 获取验证码模块
# token  V0rKjIoTnG2A-H3Ia7IjB7R-vS0y1NicGj2kNa3y


# 标准的学期课表返回
# def returnTremCourse(request):
#     if request.body:
#         request_data = json.loads(request.body)
#         # print(request_data)
#         term_course = models.TeaCrs.objects.filter(term__term_no=request_data.get('term'))
#     else:
#         term_course = models.TeaCrs.objects.all()
#
#     datas = []
#     for row in term_course:
#         print(row.tea_crs_no,
#               row.tea_no.tea_name,
#               row.crs_no.crs_name,
#               row.term.term_name,
#               row.time, row.spot.spt_area,
#               row.week, row.selected, row.total, row.grade)
#         temp = {}
#         temp['week'] = row.week
#         temp['time'] = row.time
#         temp['coursename'] = row.crs_no.crs_name
#         temp['teacher'] = row.tea_no.tea_name
#         temp['location'] = row.spot.spt_area
#         temp['span'] = row.crs_no.crs_hours
#         temp['odd-even'] = 1
#         temp['info'] = 'sfsfsefsf'
#         datas.append(temp)
#
#     response = {
#         'code': 1,
#         'msg': 'xxx授课课表',
#         'datas': datas
#     }
#     return HttpResponse(json.dumps(response))


# 测试ORM操作数据库数据
def test_term(request):
    obj = models.Term.objects.all()
    codes = models.CheckCode.objects.all()
    course = models.Course.objects.all()
    class_list = models.TblClass.objects.all()
    spot = models.Spot.objects.all()
    active = models.Active.objects.all().first()
    departments = models.Department.objects.all()
    pick_course = models.TeaCrs.objects.all()
    role = models.Role.objects.all()
    permission = models.Permission.objects.all()
    role_permission = models.RoleToPermission.objects.all()
    score = models.Score.objects.all()
    # for row in codes:
    #     print(row.session_key,row.session_data)
    # print('-------------------------------------')
    #
    # for row in obj:
    #     print(row.term_no,row.term_name)
    # print('-------------------------------------')
    #
    # 涉及外键的使用
    # datas = []
    # for row in course:
    #     temp ={}
    #     print(row.crs_no, row.crs_name, row.crs_cdt, row.crs_hours, row.crs_dpt.dpt_no, row.crs_type, row.crs_dpt.dpt_name ,row.teacrs__set)
    #     temp['courseno'] = str(row.crs_no)[2:]
    #     temp['crsname'] = row.crs_name
    #     temp['time'] = 'xxxx'
    #     temp['port'] = 'xxxx'
    #     temp['info'] = row.crs_type
    #     datas.append(temp)
    # print('-------------------------------------')
    #
    # for row in class_list:
    #     print(row.class_no,row.class_name,row.class_dpt,row.class_grade)
    # print('-------------------------------------')
    #
    # for row in spot:
    #     print(row.spt_no,row.spt_area,row.spt_room)
    # print('-------------------------------------')
    #
    # print(active.id, active.name)
    # print('-------------------------------------')
    #
    # for row in departments:
    #     print(row.dpt_no,row.dpt_name)
    # print('-------------------------------------')
    #
    datas = []
    for row in pick_course:
        print(row.tea_crs_no, row.tea_no.tea_name, row.crs_no.crs_name, row.term.term_name, row.time, row.spot.spt_area, row.week, row.selected, row.total, row.grade)
        temp ={}
        temp['courseno'] = str(row.crs_no.crs_no)[2:]
        temp['crsname'] = row.crs_no.crs_name
        temp['time'] = row.term.term_name
        temp['port'] = row.spot.spt_area
        temp['info'] = row.crs_no.crs_type
        datas.append(temp)
    print('-------------------------------------')

    # for row in role:
    #     print(row.rid,row.name)
    # print('-------------------------------------')
    #
    # for row in permission:
    #     print(row.pid, row.name, row.code, row.url)
    # print('-------------------------------------')
    #
    # for row in role_permission:
    #     print(row.rid, row.pid)
    # print('-------------------------------------')

    # for row in score:
    #     print(row.stu_no.stu_name, row.tea_crs_no, row.score_pro, row.score_end, row.score)
    # print('-------------------------------------')

    # 测试
    response = {
        'code': 1,
        'msg': 'xxx课表',
        'datas': datas
    }
    import json
    return HttpResponse(json.dumps(response))
    pass