import os
from edusystem.settings import logger
from django.http import JsonResponse
response = {
        'code': 1,
        'msg': '',
        'datas': {}
    }


def handelFileError(file, title, message):
    os.remove(file)
    logger.info(title + '- ' + str(message))
    response['code'] = -1
    response['msg'] = title + '- ' + str(message)
    return JsonResponse(response)


def handelResopnse(code, message, datas):
    response['code'] = code
    response['msg'] = message
    response['datas'] = datas
    return JsonResponse(response)
