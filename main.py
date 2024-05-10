import requests
import time
import logging
from concurrent.futures import ThreadPoolExecutor
import json 
import time
# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 读取配置文件
token =  # 请填写你的token
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'token': token,
    'Content-Type': 'application/json'
}

# 创建会话
session = requests.Session()

# 获取完成情况
def get_course_user_statistic(token):
    url = f"https://www.baomi.org.cn/portal/main-api/v2/coursePacket/getCourseUserStatistic?coursePacketId=78e6a04c-dd87-4794-8214-9de32be7cae1&token={token}"
    response = requests.get(url).json()
    gradeSum = response['data']['gradeSum']
    totalGrade = response['data']['totalGrade']
    if gradeSum == totalGrade:
        return True

# 获取课程时长
def view_resource_details(token, resource_directory_id):
    timestamp = int(time.time())
    url = 'http://www.baomi.org.cn/portal/api/v2/coursePacket/viewResourceDetails'
    post_data = {
        'token': token,
        'resourceDirectoryId': resource_directory_id,
        'timestamps': timestamp
    }
    try:
        response = session.get(url, params=post_data, headers=headers)
        response.raise_for_status()  # 检查响应状态码
        data = response.json()['data']
        resource_length = data['resourceLength']
        resource_id = data['resourceID']
        display_order = data['displayOrder']
        logging.info(f"正在刷: {data['name']}")
        return resource_length, resource_id, display_order
    except requests.exceptions.RequestException as e:
        logging.error(f"获取课程时长失败: {e}")
        return None, None, None

# 传递观看时间
def save_course_package(course_id, resource_id, resource_directory_id, resource_length, study_length, study_time, display_order, token):
    url = 'http://www.baomi.org.cn/portal/api/v2/studyTime/saveCoursePackage.do'
    timestamp = int(time.time())
    post_data = {
        'courseId': course_id,
        'resourceId': resource_id,
        'resourceDirectoryId': resource_directory_id,
        'resourceLength': resource_length,
        'studyLength': study_length,
        'studyTime': study_time,
        'startTime': timestamp - int(resource_length),
        'resourceType': 1,
        'resourceLibId': 3,
        'token': token,
        'studyResourceId': display_order,
        'timestamps': timestamp
    }
    try:
        response = session.get(url, params=post_data, headers=headers)
        response.raise_for_status()  # 检查响应状态码
        message = response.json()['message']
        logging.info(message)
    except requests.exceptions.RequestException as e:
        logging.error(f"保存课程包失败: {e}")

# 自动完成考试
def save_exam_result():
    url = "https://www.baomi.org.cn/portal/main-api/v2/activity/exam/saveExamResultJc.do"
    payload = json.dumps({
    "examId": "8ad5b4848f198e65018f332212c10004",
    "examResult": "[{\"parentId\":\"0\",\"qstId\":\"8ad59f838f196aef018f2887bcfc0100\",\"resultFlag\":0,\"standardAnswer\":\"D\",\"subCount\":0,\"tqId\":63,\"userAnswer\":\"D\",\"userScoreRate\":\"100%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad59f838f196aef018f28879ae10068\",\"resultFlag\":0,\"standardAnswer\":\"D\",\"subCount\":0,\"tqId\":25,\"userAnswer\":\"D\",\"userScoreRate\":\"100%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad59f838f196aef018f2887c355011c\",\"resultFlag\":0,\"standardAnswer\":\"B\",\"subCount\":0,\"tqId\":70,\"userAnswer\":\"B\",\"userScoreRate\":\"100%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad59f838f196aef018f2887a3d30090\",\"resultFlag\":0,\"standardAnswer\":\"B\",\"subCount\":0,\"tqId\":35,\"userAnswer\":\"C\",\"userScoreRate\":\"0%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad59f838f196aef018f2887cc5c0144\",\"resultFlag\":0,\"standardAnswer\":\"B\",\"subCount\":0,\"tqId\":80,\"userAnswer\":\"B\",\"userScoreRate\":\"100%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad59f838f196aef018f288787250010\",\"resultFlag\":0,\"standardAnswer\":\"D\",\"subCount\":0,\"tqId\":3,\"userAnswer\":\"C\",\"userScoreRate\":\"0%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad59f838f196aef018f28879106003c\",\"resultFlag\":0,\"standardAnswer\":\"C\",\"subCount\":0,\"tqId\":14,\"userAnswer\":\"B\",\"userScoreRate\":\"0%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad59f838f196aef018f2887adb200bc\",\"resultFlag\":0,\"standardAnswer\":\"A\",\"subCount\":0,\"tqId\":46,\"userAnswer\":\"A\",\"userScoreRate\":\"100%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad59f838f196aef018f2887c7d80130\",\"resultFlag\":0,\"standardAnswer\":\"C\",\"subCount\":0,\"tqId\":75,\"userAnswer\":\"C\",\"userScoreRate\":\"100%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad59f838f196aef018f288789da001c\",\"resultFlag\":0,\"standardAnswer\":\"A\",\"subCount\":0,\"tqId\":6,\"userAnswer\":\"A\",\"userScoreRate\":\"100%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad59f838f196aef018f2887b14900cc\",\"resultFlag\":0,\"standardAnswer\":\"D\",\"subCount\":0,\"tqId\":50,\"userAnswer\":\"D\",\"userScoreRate\":\"100%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad59f838f196aef018f28878f390034\",\"resultFlag\":0,\"standardAnswer\":\"D\",\"subCount\":0,\"tqId\":12,\"userAnswer\":\"D\",\"userScoreRate\":\"100%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad59f838f196aef018f2887accd00b8\",\"resultFlag\":0,\"standardAnswer\":\"B\",\"subCount\":0,\"tqId\":45,\"userAnswer\":\"B\",\"userScoreRate\":\"100%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad59f838f196aef018f288791eb0040\",\"resultFlag\":0,\"standardAnswer\":\"B\",\"subCount\":0,\"tqId\":15,\"userAnswer\":\"B\",\"userScoreRate\":\"100%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad59f838f196aef018f28879cac0070\",\"resultFlag\":0,\"standardAnswer\":\"D\",\"subCount\":0,\"tqId\":27,\"userAnswer\":\"D\",\"userScoreRate\":\"100%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad59f838f196aef018f2887cb750140\",\"resultFlag\":0,\"standardAnswer\":\"B\",\"subCount\":0,\"tqId\":79,\"userAnswer\":\"B\",\"userScoreRate\":\"100%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad59f838f196aef018f2887b79300e8\",\"resultFlag\":0,\"standardAnswer\":\"C\",\"subCount\":0,\"tqId\":57,\"userAnswer\":\"C\",\"userScoreRate\":\"100%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad59f838f196aef018f28879f5a007c\",\"resultFlag\":0,\"standardAnswer\":\"B\",\"subCount\":0,\"tqId\":30,\"userAnswer\":\"B\",\"userScoreRate\":\"100%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad59f838f196aef018f28878ba40024\",\"resultFlag\":0,\"standardAnswer\":\"D\",\"subCount\":0,\"tqId\":8,\"userAnswer\":\"D\",\"userScoreRate\":\"100%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad59f838f196aef018f2887b06200c8\",\"resultFlag\":0,\"standardAnswer\":\"D\",\"subCount\":0,\"tqId\":49,\"userAnswer\":\"D\",\"userScoreRate\":\"100%\",\"viewTypeId\":1},{\"parentId\":\"0\",\"qstId\":\"8ad59f838f196aef018f2887f09101e4\",\"resultFlag\":0,\"standardAnswer\":\"A\",\"subCount\":0,\"tqId\":120,\"userAnswer\":\"A\",\"userScoreRate\":\"100%\",\"viewTypeId\":3},{\"parentId\":\"0\",\"qstId\":\"8ad59f838f196aef018f2887dc9c018c\",\"resultFlag\":0,\"standardAnswer\":\"B\",\"subCount\":0,\"tqId\":98,\"userAnswer\":\"B\",\"userScoreRate\":\"100%\",\"viewTypeId\":3},{\"parentId\":\"0\",\"qstId\":\"8ad59f838f196aef018f2887e20c01a4\",\"resultFlag\":0,\"standardAnswer\":\"B\",\"subCount\":0,\"tqId\":104,\"userAnswer\":\"B\",\"userScoreRate\":\"100%\",\"viewTypeId\":3},{\"parentId\":\"0\",\"qstId\":\"8ad59f838f196aef018f2887ecee01d4\",\"resultFlag\":0,\"standardAnswer\":\"A\",\"subCount\":0,\"tqId\":116,\"userAnswer\":\"A\",\"userScoreRate\":\"100%\",\"viewTypeId\":3},{\"parentId\":\"0\",\"qstId\":\"8ad59f838f196aef018f2887eb1d01cc\",\"resultFlag\":0,\"standardAnswer\":\"B\",\"subCount\":0,\"tqId\":114,\"userAnswer\":\"B\",\"userScoreRate\":\"100%\",\"viewTypeId\":3}]",
    "startDate": "2024-05-10 16:14:22",
    "randomId": "dd98488d30f1fded7d3600c7f707b6fc"
    })
    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def finish_exam(course_packet_id):
    url = f"https://www.baomi.org.cn/portal/main-api/v2/studyTime/updateCoursePackageExamInfo.do?courseId={course_packet_id}&orgId=&isExam=1&isCertificate=0&examResult=100"
    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()  # 检查响应状态码
        message = response.json()['message']
        logging.info(message)
    except requests.exceptions.RequestException as e:
        logging.error(f"完成考试失败: {e}")

def process_video(course_packet_id, directory_id):
    timestamp = int(time.time())
    try:
        resource_directory_ids = session.get('http://www.baomi.org.cn/portal/api/v2/coursePacket/getCourseResourceList', params={'coursePacketId': course_packet_id, 'directoryId': directory_id, 'timestamps': timestamp}, headers=headers).json()['data']['listdata']
        for resource_info in resource_directory_ids:
            resource_directory_id = resource_info['SYS_UUID']
            directory_id = resource_info['directoryID']
            resource_length, resource_id, display_order = view_resource_details(token, resource_directory_id)
            if resource_length is not None:
                save_course_package(course_packet_id, resource_id, resource_directory_id, resource_length, 0, 180, display_order, token)
                save_course_package(course_packet_id, resource_id, resource_directory_id, resource_length, resource_length, resource_length, display_order, token)
    except requests.exceptions.RequestException as e:
        logging.error(f"处理视频失败: {e}")

if __name__ == '__main__':
    course_packet_id = '78e6a04c-dd87-4794-8214-9de32be7cae1'  # 2024年度保密教育线上培训 课程参数
    timestamp = int(time.time())

    try:
        directory_ids = session.get('http://www.baomi.org.cn/portal/api/v2/coursePacket/getCourseDirectoryList', params={'scale': 1, 'coursePacketId': course_packet_id, 'timestamps': timestamp}, headers=headers).json()['data']
        with ThreadPoolExecutor(max_workers=10) as executor:
            for directory in directory_ids:
                sub_directories = directory['subDirectory']
                for sub_dir in sub_directories:
                    executor.submit(process_video, course_packet_id, sub_dir['SYS_UUID'])
        print('视频观看完成, 开始考试...')
    except requests.exceptions.RequestException as e:
        logging.error(f"获取目录列表失败: {e}")
        
    while not get_course_user_statistic(token):
        time.sleep(10)
        save_exam_result()
        finish_exam(course_packet_id)
