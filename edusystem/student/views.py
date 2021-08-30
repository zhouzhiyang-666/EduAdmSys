from django.shortcuts import render, HttpResponse, redirect
from student import models
from public.models import Course, TeaCrs, Score, Active, Spot
from django.http import JsonResponse
from django.db import transaction
# from django.db.models import F
import json
from utils.validateToken import check_token    # 用于token验证装饰器 每个请求必须token校验过关
week_option = {'Mon': '星期一', 'Tues': '星期二', 'Wed': '星期三', 'Thur': '星期四', 'Fri': '星期五'}
time_option = {'0': '第一节', '1': '第二节', '3': '第三节', '4': '第四节', '6': '第五节'}

def test(request):
    obj = models.Student.objects.all()[1]
    print(obj.stu_no,obj.stu_name,obj.stu_sex,obj.stu_gdu,obj.stu_bth,obj.stu_tel,obj.stu_pol)
    return HttpResponse('ok')
    pass


# 获取学生成绩
@check_token
def getScoreTable(request):
    # 学期过滤
    request_data = json.loads(request.body)
    # print(request_data)
    user_id = request.META.get('HTTP_USERID', 'none')
    term_no = request_data.get('term', 'none')
    if term_no == '0':
        score_list = Score.objects.filter(stu_no=user_id)
    else:
        score_list = Score.objects.filter(stu_no=user_id, tea_crs_no__term__term_no=term_no)
    # print(score_list)

    datas = []
    response = {
        'code': 1,
        'msg': user_id + '的学期成绩',
        'datas': datas
    }
    if not score_list:
        response['code'] = -1
        response['msg'] = '成绩尚未录入'
        return JsonResponse(response)
    for row in score_list:
        print(row.score)
        temp ={}
        temp['id'] = row.tea_crs_no.crs_no.crs_no
        temp['type'] = row.tea_crs_no.crs_no.crs_type
        temp['credit'] = row.tea_crs_no.crs_no.crs_cdt
        temp['hours'] = row.tea_crs_no.crs_no.crs_hours
        temp['name'] = row.tea_crs_no.crs_no.crs_name
        temp['score'] = row.score
        datas.append(temp)
    return JsonResponse(response)


# 获取个人信息
@check_token
def getSelfInfo(request):
    # 获取学生id
    stu_no = request.META.get('HTTP_USERID', 'none')

    stu_obj = models.Student.objects.filter(stu_no=stu_no).first()
    datas = []
    response = {
        'code': 1,
        'msg': '请求成功',
        'datas': datas
    }
    temp ={}
    # print(row.stu_no, row.stu_name, row.stu_sex, row.stu_gdu, row.stu_bth, row.stu_id, row.stu_tel,
    #       row.stu_pol, row.stu_dpt, row.stu_class, row.stu_sta, row.stu_pwd)
    # temp['courseno'] = str(row.crs_no)[2:]
    temp['id'] = stu_obj.stu_no
    temp['name'] = stu_obj.stu_name
    temp['sex'] = stu_obj.stu_sex
    temp['birth'] = stu_obj.stu_bth
    temp['political'] = stu_obj.stu_pol
    temp['classAndGrade'] = stu_obj.stu_class.class_grade + stu_obj.stu_class.class_name
    temp['status'] = stu_obj.stu_sta
    # 计算成绩
    score_list = []
    creditSum = 0
    score_set = Score.objects.filter(stu_no=stu_no)
    if score_set.exists():
        for item in score_set:
            score_temp = item.score
            if score_temp:
                score_list.append(score_temp)
                if score_temp >= 60:
                    creditSum += item.tea_crs_no.crs_no.crs_cdt
        if len(score_list) == 0:
            temp['all_credit'] = '0'
            temp['avg_grade'] = '0'
        else:
            temp['all_credit'] = creditSum
            temp['avg_grade'] = round(sum(score_list)/len(score_list), 3)
    else:
        temp['all_credit'] = '0'
        temp['avg_grade'] = '0'
    datas.append(temp)
    return JsonResponse(response)
    pass


# 获取所有选课信息
@check_token
def getNewCourseArrange(request):
    datas = []
    response = {
        'code': -1,
        'msg': '学生选课',
        'datas': datas
    }
    stu_no = request.META.get('HTTP_USERID', 'none')
    request_data = json.loads(request.body, encoding='utf-8')
    print(request_data)
    dpt_no = request_data.get('dptNo', 'none')  # 学院编号
    stu_grade = models.Student.objects.filter(stu_no=stu_no).first().stu_class.class_grade  # 学生年级

    # 获取当前选课是否开启
    active_obj = Active.objects.first()
    option = active_obj.option
    grade = active_obj.grade
    if option == 0 or grade != stu_grade and grade != '0':
        response['msg'] = '选课未开放'
        return JsonResponse(response)
    # 否则开启选课
    response['code'] = 1
    active_term = Active.objects.filter(id='active_term_no').first()
    term_no = active_term.name.term_no
    print('term_no---->', term_no, 'term_name---->', active_term.name.term_name)
    if dpt_no == 'none' or dpt_no == '0':
        active_course = TeaCrs.objects.filter(term__term_no=term_no, grade=stu_grade, is_public='1')
    else:
        active_course = TeaCrs.objects.filter(term__term_no=term_no, grade=stu_grade, crs_no__crs_dpt=dpt_no, is_public='1')

    for row in active_course:
        temp = {}
        # print(week_option[row.week], time_option[row.time])
        temp['teaCrsNo'] = row.tea_crs_no
        temp['courseno'] = row.crs_no.crs_no
        temp['type'] = row.crs_no.crs_type
        temp['courseName'] = row.crs_no.crs_name
        temp['credit'] = row.crs_no.crs_cdt
        temp['hours'] = row.crs_no.crs_hours
        temp['area'] = row.spot.spt_area
        temp['room'] = row.spot.spt_room
        temp['time'] = week_option[row.week] + '|' + time_option[row.time]
        temp['teacherName'] = row.tea_no.tea_name
        temp['selected'] = row.selected
        temp['total'] = row.total
        datas.append(temp)
        # print(temp)

    return JsonResponse(response)


# 选课
@check_token
def addSelectCourse(request):
    datas = []
    response = {
        'code': -1,
        'msg': 'none',
        'datas': datas
    }
    request_data = json.loads(request.body, encoding='utf-8')
    # {'teaCrsNo': 57, 'courseno': 10007, 'type': '专业必修',
    #  'courseName': '数据库原理', 'credit': 4, 'hours': 64,
    #  'area': '第一实验楼', 'room': '501', 'teacherName': '周老师',
    #  'selected': 0, 'total': 50}
    # 获取学生id
    stu_no = request.META.get('HTTP_USERID', 'none')
    print(stu_no,'选课',request_data.get('teaCrsNo', 'none'))

    active_obj = Active.objects.first()
    pick_channel_is_open = active_obj.option   # 选课通道标识
    active_term = active_obj.name      # 当前学期编号
    select_num = active_obj.select_num   # 最大选课数目，默认为3
    if pick_channel_is_open == 0:
        response['msg'] = '选课通道已关闭，无法选课，请联系相关工作人员'
        return JsonResponse(response)

    if stu_no == 'none':
        response['code'] = 0
        response['msg'] = '用户信息出错'
        return JsonResponse(response)

    # 获取课程信息
    tea_crs_no = request_data.get('teaCrsNo', 'none')

    # 判断是否已选该课程
    pick_course = Score.objects.filter(stu_no=stu_no, tea_crs_no=tea_crs_no).first()
    # print('选课-->已选课程：', pick_course)
    if pick_course:
        response['msg'] = '您已选择该课程'
        return JsonResponse(response)

    # 判断选课数目是否为三个内
    selected_course_list = Score.objects.filter(stu_no=stu_no, tea_crs_no__term=active_term)
    if len(selected_course_list) >= int(select_num):
        response['msg'] = '最多选择{}门课程'.format(str(select_num))
        return JsonResponse(response)

    tea_course_obj = TeaCrs.objects.filter(tea_crs_no=tea_crs_no).first()
    # 判断当前选课人数是否满，满了就退出
    if tea_course_obj.selected >= tea_course_obj.total:
        response['msg'] = '选课人数已满，请选择其他课程'
        return JsonResponse(response)

    # 判断课程时间是否冲突
    all_course = Score.objects.filter(stu_no=stu_no)
    time_list, week_list, term_list = [], [], []
    for row in all_course:
        # print(row.week,row.time)
        time_list.append(row.tea_crs_no.time)
        week_list.append(row.tea_crs_no.week)
    print(stu_no, '学生本人时间:', time_list, week_list)
    for index in range(0, len(time_list)):
        if tea_course_obj.time == time_list[index] and tea_course_obj.week == week_list[index]:
            response['msg'] = '上课时间冲突，请选择其他时间段的课程'
            return JsonResponse(response)

    try:
        with transaction.atomic():
            # 选课人数加1
            # print(tea_course_obj.time, tea_course_obj.week)
            tea_course_obj.selected += 1
            tea_course_obj.save(update_fields=['selected'])

            # 写入选课分数表
            tea_course_obj = TeaCrs.objects.filter(tea_crs_no=tea_crs_no).first()
            stu_obj = models.Student.objects.filter(stu_no=stu_no).first()
            Score.objects.create(stu_no=stu_obj, tea_crs_no=tea_course_obj)
    except Exception as e:
        print('**error_msg**:', e)
        response['code'] = -1
        response['msg'] = '选课失败'
        # print(tea_course_obj, spot_obj)
        return JsonResponse(response)
    else:
        response['code'] = 1
        response['msg'] = '选课成功'
        print(stu_no, '选课成功')
        # print(tea_course_obj, spot_obj)
        return JsonResponse(response)


# 退课
@check_token
def delSelectCourse(request):
    datas = []
    response = {
        'code': -1,
        'msg': '退课',
        'datas': datas
    }
    request_data = json.loads(request.body, encoding='utf-8')
    # {'teaCrsNo': 33, 'courseno': 10001, 'type': '专业必修',
    # 'courseName': '数据结构', 'credit': 4, 'hours': 64, 'area': '教学楼B区',
    #  'room': 'B10
    #  1', 'teacherName': '周老师', 'selected': 3, 'total': 40}
    active_obj = Active.objects.first()
    pick_channel_is_open = active_obj.option
    if pick_channel_is_open == 0:
        response['msg'] = '选课通道已关闭，无法退课，请联系相关工作人员'
        return JsonResponse(response)

    # 获取学生id
    stu_no = request.META.get('HTTP_USERID', 'none')
    # 获取课程信息
    tea_crs_no = request_data.get('teaCrsNo', 'none')

    if stu_no == 'none':
        response['code'] = 0
        response['msg'] = '用户信息出错'
        return JsonResponse(response)

    try:
        with transaction.atomic():
            # 判断是否已选该课程
            pick_course = Score.objects.filter(stu_no=stu_no,
                                               tea_crs_no=tea_crs_no,
                                               tea_crs_no__term=active_obj.name).delete()
            print('选课记录', pick_course[0] > 0)
            if pick_course[0] > 0:
                tea_course_obj = TeaCrs.objects.filter(tea_crs_no=tea_crs_no).first()
                tea_course_obj.selected -= 1
                print('退课成功！', tea_course_obj.save(update_fields=['selected']))
            else:
                print('yestttttttttttt')
                response['code'] = -1
                response['msg'] = '退课失败'
                return JsonResponse(response)
    except Exception as e:
        print('**error_msg**:', e)
        response['code'] = -1
        response['msg'] = '退课失败'
        return JsonResponse(response)
    else:
        response['code'] = 1
        response['msg'] = '退课成功'
        return JsonResponse(response)


# 获取本人选课信息
@check_token
def getSelectedCourseArrange(request):
    datas = []
    response = {
        'code': 1,
        'msg': '学生本人选课',
        'datas': datas
    }
    # 获取学生id
    stu_no = request.META.get('HTTP_USERID', 'none')

    active_obj = Active.objects.first()
    term_no = active_obj.name.term_no
    pick_course = Score.objects.filter(stu_no=stu_no,
                                       tea_crs_no__term__term_no=term_no,
                                       tea_crs_no__grade=active_obj.grade)

    if not pick_course:
        response['code'] = -1
        return JsonResponse(response)

    for row in pick_course:
        temp = {}
        temp['teaCrsNo'] = row.tea_crs_no.tea_crs_no
        temp['courseno'] = row.tea_crs_no.crs_no.crs_no
        temp['type'] = row.tea_crs_no.crs_no.crs_type
        temp['courseName'] = row.tea_crs_no.crs_no.crs_name
        temp['credit'] = row.tea_crs_no.crs_no.crs_cdt
        temp['hours'] = row.tea_crs_no.crs_no.crs_hours
        temp['area'] = row.tea_crs_no.spot.spt_area
        temp['room'] = row.tea_crs_no.spot.spt_room
        temp['time'] = week_option[row.tea_crs_no.week] + '|' + time_option[row.tea_crs_no.time]
        temp['teacherName'] = row.tea_crs_no.tea_no.tea_name
        temp['selected'] = row.tea_crs_no.selected
        temp['total'] = row.tea_crs_no.total
        datas.append(temp)
        # print('学生本人选课', temp)

    return JsonResponse(response)
