from django.http import JsonResponse,HttpResponse
from teacher import models
from public.models import TeaCrs, Score
from student.models import Student
from utils.validateToken import check_token    # 用于token验证装饰器 每个请求必须token校验过关
import json


@check_token
def course(request):
    tea_no = request.META.get('HTTP_USERID', 'none')
    if tea_no == 'none':
        course_list = TeaCrs.objects.all()
    else:
        course_list = TeaCrs.objects.filter(tea_no__tea_no=tea_no)
    datas = []
    for row in course_list:
        # print(row.tea_crs_no, row.tea_no.tea_name, row.crs_no.crs_name, row.term.term_name, row.time, row.spot.spt_area,
        #       row.week, row.selected, row.total, row.grade)
        temp = { }
        temp['courseno'] = str(row.crs_no.crs_no)
        temp['crsname'] = row.crs_no.crs_name
        temp['time'] = row.term.term_name
        temp['port'] = row.spot.spt_area + '-' + row.spot.spt_room
        temp['info'] = row.crs_no.crs_type
        datas.append(temp)
    # 测试
    response = {
        'code': 1,
        'msg': 'xxx课表',
        'datas': datas
    }
    return JsonResponse(response)


# 获取学生成绩信息
@check_token
def getStuScore(request):
    # if request.body:
    #     request_data = json.loads(request.body)
    #     print(request_data)
    #     score = Score.objects.all()
    # else:
    tea_no = request.META.get('HTTP_USERID', 'none')
    score = Score.objects.filter(tea_crs_no__tea_no__tea_no=tea_no)
    datas = []
    for row in score:
        # print(row.stu_no.stu_no, row.stu_no.stu_name, row.stu_no.stu_class.class_name, row.tea_crs_no.tea_no.tea_name, row.score_pro, row.score_end, row.score)
        temp = {}
        temp['teaCrsNo'] = row.tea_crs_no.tea_crs_no
        temp['stuId'] = row.stu_no.stu_no
        temp['courseName'] = row.tea_crs_no.crs_no.crs_name
        temp['classAndGrade'] = row.stu_no.stu_class.class_name
        temp['stuName'] = row.stu_no.stu_name
        temp['score'] = row.score
        datas.append(temp)

    response = {
        'code': 1,
        'msg': '教师所教学生信息',
        'datas': datas
    }
    return JsonResponse(response)


# 获取个人信息
@check_token
def getInfo(request):
    tea_no = request.META.get('HTTP_USERID', 'none')
    self_info = models.Teacher.objects.filter(tea_no=tea_no)
    datas = []
    for row in self_info:
        temp = {}
        temp['id'] = row.tea_no
        temp['name'] = row.tea_name
        temp['sex'] = row.tea_sex
        temp['tel'] = row.tea_tel
        temp['pol'] = row.tea_pol
        temp['title'] = row.tea_title
        temp['dpt'] = row.tea_dpt.dpt_name
        temp['degree'] = row.tea_degree
        temp['workTime'] = row.tea_wkt
        datas.append(temp)
    response = {
        'code': 1,
        'msg': 'xxx课表',
        'datas': datas
    }
    return JsonResponse(response)


# 获取学期授课科目
@check_token
def getCourse(request):
    if request.body:
        tea_no = request.META.get('HTTP_USERID', 'none')

        request_data = json.loads(request.body, encoding='utf-8')
        term_no = request_data.get('term', 'none')
        print(request_data, tea_no)
        if tea_no != 'none' and tea_no != 'admin':
            term_course = TeaCrs.objects.filter(term__term_no=term_no, tea_no=tea_no)


        datas = []
        for row in term_course:
            # print(row.tea_crs_no,
            #       row.tea_no.tea_name,
            #       row.crs_no.crs_name,
            #       row.term.term_name,
            #       row.time, row.spot.spt_area,
            #       row.week, row.selected, row.total, row.grade)
            temp = {}
            temp['name'] = row.crs_no.crs_name + '(' + row.grade + '级)'
            temp['id'] = row.crs_no.crs_no
            datas.append(temp)

        response = {
            'code': 1,
            'msg': '教师授课科目',
            'datas': datas
        }
        return JsonResponse(response)


"""
   查询学生模块接口
   请求参数：老师id，课程编号，学期编号
   返回参数：教师所教的学生信息
"""
@check_token
def getScoreData(request):
    if request.body:
        request_data = json.loads(request.body, encoding='utf-8')
        tea_no = request.META.get('HTTP_USERID', 'none')
        crs_no = request_data.get('crsId', 'none')
        # 补上学生或者教室id查对应的课表
        # print(request_data)
        datas = []
        response = {
            'code': 1,
            'msg': '学生信息',
            'datas': datas
        }
        if crs_no == 'none':
            response['msg'] = '没有该课程的学生'
            return JsonResponse(response)

        score = Score.objects.filter(tea_crs_no__crs_no__crs_no=crs_no,
                                     tea_crs_no__tea_no=tea_no)
        datas = []
        for row in score:
            temp = {}
            temp['teaCrsNo'] = row.tea_crs_no.tea_crs_no
            temp['stuId'] = row.stu_no.stu_no
            temp['courseName'] = row.tea_crs_no.crs_no.crs_name
            temp['classAndGrade'] = row.stu_no.stu_class.class_grade + row.stu_no.stu_class.class_name
            temp['stuName'] = row.stu_no.stu_name
            temp['score'] = row.score
            datas.append(temp)
        # print('-------------------------------------')

        response = {
            'code': 1,
            'msg': 'xxx课表',
            'datas': datas
        }
        return JsonResponse(response)


@check_token
def postScoreList(request):
    response = {
        'code': 1,
        'msg': '更改成绩',
        'datas': []
    }
    request_data = json.loads(request.body, encoding='utf-8')
    score_list = request_data.get('scoreList', 'none')
    print(score_list)
    # [{'teaCrsNo': 17, 'stuId': '2017110318', 'classAndGrade': '网路工程1', 'stuName': '雷同学', 'score': 89}]

    # try:
    for row in score_list:
        score = row.get('score', 'none')
        # print(score)
        if score == 'none':
            continue
        if score == '':
            score = None
        Score.objects.filter(stu_no=row.get('stuId', 'none'),
                             tea_crs_no=row.get('teaCrsNo', 'none')).update(score=float(score))
    # except:
    #     pass
    return JsonResponse(response)

