import requests
import logging
from colorama import Fore, Style
import time
import random
import string
import hashlib

class CourseManager:
    def __init__(self, session, token):
        self.session = session
        self.token = token
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
            'token': token,
            'authToken': token,
            'siteId': '95',
            'Content-Type': 'application/json'
        }

    def get_course_directory(self, course_packet_id, scale=1):
        """获取培训课程目录"""
        url = 'https://www.baomi.org.cn/portal/main-api/v2/coursePacket/getCourseDirectoryList'
        params = {
            'scale': scale,
            'coursePacketId': course_packet_id
        }
        try:
            response = self.session.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"{Fore.RED}获取课程目录失败: {e}{Style.RESET_ALL}")
            return None

    def get_course_info(self, course_packet_id):
        """获取培训课程相关信息"""
        url = 'https://www.baomi.org.cn/portal/main-api/v2/coursePacket/getCoursePacket'
        params = {
            'coursePacketId': course_packet_id
        }
        try:
            response = self.session.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"{Fore.RED}获取课程信息失败: {e}{Style.RESET_ALL}")
            return None

    def get_course_resources(self, course_packet_id, directory_id):
        """获取指定目录下的单节课程列表"""
        url = 'https://www.baomi.org.cn/portal/main-api/v2/coursePacket/getCourseResourceList'
        params = {
            'coursePacketId': course_packet_id,
            'directoryId': directory_id,
            'token': self.token
        }
        try:
            response = self.session.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"{Fore.RED}获取课程资源列表失败: {e}{Style.RESET_ALL}")
            return None

    def get_resource_status(self, course_packet_id, resource_directory_id):
        """获取单节课程的相关数据和完成状态"""
        url = 'https://www.baomi.org.cn/portal/main-api/v2/coursePacket/getResourceUserStatistic'
        params = {
            'coursePacketId': course_packet_id,
            'resourceDirectoryId': resource_directory_id,
            'token': self.token
        }
        try:
            response = self.session.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"{Fore.RED}获取课程状态失败: {e}{Style.RESET_ALL}")
            return None

    def save_study_record(self, course_id, resource_id, resource_directory_id, resource_length,
                         study_length, study_time, start_time, resource_name, resource_type='1',
                         resource_lib_id='3'):
        """保存观看记录"""
        url = 'https://www.baomi.org.cn/portal/main-api/v2/studyTime/saveCoursePackage.do'
        params = {
            'courseId': course_id,
            'resourceId': resource_id,
            'resourceDirectoryId': resource_directory_id,
            'resourceLength': resource_length,
            'studyLength': study_length,
            'studyTime': study_time,
            'startTime': start_time,
            'resourceName': resource_name,
            'resourceType': resource_type,
            'resourceLibId': resource_lib_id,
            'token': self.token
        }
        try:
            response = self.session.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"{Fore.RED}保存观看记录失败: {e}{Style.RESET_ALL}")
            return None

    def get_course_progress(self, course_packet_id):
        """查询培训课程完成进度"""
        url = 'https://www.baomi.org.cn/portal/main-api/v2/coursePacket/getCourseUserStatistic'
        params = {
            'coursePacketId': course_packet_id,
            'token': self.token
        }
        try:
            response = self.session.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"{Fore.RED}获取课程进度失败: {e}{Style.RESET_ALL}")
            return None

    def _convert_time_to_seconds(self, time_str):
        """将时间字符串(HH:MM:SS)转换为秒数"""
        try:
            h, m, s = map(int, time_str.split(':'))
            return h * 3600 + m * 60 + s
        except Exception as e:
            logging.error(f"{Fore.RED}时间格式转换失败: {e}{Style.RESET_ALL}")
            return 0

    def generate_custom_random_id(self):
        """生成一个自定义的随机ID"""
        e = random.randint(1, 500)
        base_string = f"founder{e}"
        md5_hash_object = hashlib.md5()
        
        md5_hash_object.update(base_string.encode('utf-8'))
        random_id = md5_hash_object.hexdigest()
        return random_id

    def get_exam_info(self, course_packet_id):
        """获取考试信息"""
        url = 'https://www.baomi.org.cn/portal/main-api/v2/coursePacket/getCourseRelateExam'
        params = {
            'coursePacketId': course_packet_id,
            'token': self.token
        }
        try:
            response = self.session.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"{Fore.RED}获取考试信息失败: {e}{Style.RESET_ALL}")
            return None

    def get_exam_answers(self, exam_id,random_id):
        """获取考试试卷答案"""
        url = 'https://www.baomi.org.cn/portal/main-api/v2/activity/exam/getExamContentData.do'
        params = {
            'examId': exam_id,
            'randomId': random_id
        }
        try:
            response = self.session.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"{Fore.RED}获取试卷答案失败: {e}{Style.RESET_ALL}")
            return None

    def submit_exam_answers(self, exam_id, answers, start_date, random_id):
        """提交考试答案"""
        import json

        url = 'https://www.baomi.org.cn/portal/main-api/v2/activity/exam/saveExamResultJc.do'
        
        data = {
            'examId': exam_id,
            'examResult': json.dumps(answers),  # 将答案列表转换为JSON字符串
            'randomId': random_id,
            'startDate': start_date,
        }
        try:
            response = self.session.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"{Fore.RED}提交考试答案失败: {e}{Style.RESET_ALL}")
            return None

    def get_exam_result(self, exam_id):
        """获取考试成绩"""
        url = 'https://www.baomi.org.cn/portal/main-api/v2/activity/exam/getExamResultMaxScore.do'
        params = {
            'examId': exam_id,
            'token': self.token
        }
        try:
            response = self.session.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"{Fore.RED}获取考试成绩失败: {e}{Style.RESET_ALL}")
            return None

    def complete_exam(self, course_packet_id):
        """自动完成考试"""
        import time

        # 获取考试信息
        exam_info = self.get_exam_info(course_packet_id)
        if not exam_info or not exam_info.get('data'):
            logging.error(f"{Fore.RED}获取考试信息失败{Style.RESET_ALL}")
            return False
        print(f"{Fore.GREEN}获取考试信息成功{Style.RESET_ALL}")
        exam_id = exam_info['data'][0].get('examId')
        if not exam_id:
            logging.error(f"{Fore.RED}未找到考试ID{Style.RESET_ALL}")
            return False
        random_id = self.generate_custom_random_id()

        # 获取试卷答案
        exam_paper = self.get_exam_answers(exam_id,random_id)
        if not exam_paper or not exam_paper.get('data'):
            logging.error(f"{Fore.RED}获取试卷答案失败{Style.RESET_ALL}")
            return False
        print(f"{Fore.GREEN}获取试卷答案成功{Style.RESET_ALL}")
        # 获取新的randomId
        random_id = exam_paper['data'].get('randomId')
        # random_id = "820c25b96ac65f0200bde3264fb0dffc"

        if not random_id:
            logging.error(f"{Fore.RED}获取randomId失败{Style.RESET_ALL}")
            return False

        # 准备答案数据
        answers = []
        type_list = exam_paper['data'].get('typeList', [])
        for type_item in type_list:
            question_list = type_item.get('questionList', [])
            for question in question_list:
                # 获取正确答案
                correct_answer = question['answer']
                # 构造答案数据，完全按照示例格式
                answer_data = {
                    'parentId': '0',
                    'qstId': question['id'],
                    'resultFlag': 0,
                    'standardAnswer': correct_answer,
                    'subCount': 0,
                    'tqId': question['tqId'],
                    'userAnswer': correct_answer,  # 使用正确答案
                    'userScoreRate': '100%',  # 使用正确答案，得分率100%
                    'viewTypeId': type_item.get('type', 1)  # 题目类型
                }
                answers.append(answer_data)

        # 提交答案
        start_date = time.strftime("%Y-%m-%d %H:%M:%S")  # 获取当前时间并格式化为指定格式
        result = self.submit_exam_answers(exam_id, answers, start_date, random_id)

        if result and result.get('status') == 0:
            print(f"{Fore.GREEN}答案提交成功！{Style.RESET_ALL}")
            
            # 获取考试成绩
            print(f"{Fore.YELLOW}正在查询考试成绩...{Style.RESET_ALL}")
            time.sleep(2)  # 等待服务器处理成绩
            exam_result = self.get_exam_result(exam_id)
            
            if exam_result and exam_result.get('status') == 0 and exam_result.get('data'):
                data = exam_result['data']
                print(f"{Fore.GREEN}考试成绩查询成功！{Style.RESET_ALL}")
                print(f"{Fore.CYAN}考试名称: {data.get('exam_name', '未知')}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}考试成绩: {data.get('score', '未知')} 分{Style.RESET_ALL}")
                print(f"{Fore.CYAN}答题次数: {data.get('answerCount', '未知')} 次{Style.RESET_ALL}")
                print(f"{Fore.CYAN}提交时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(data.get('submit_date', 0))/1000))}{Style.RESET_ALL}")
                
                # 更新考试完成状态
                score = data.get('score', 100)
                self.finish_exam(course_packet_id, score)
            else:
                print(f"{Fore.YELLOW}考试成绩查询失败或暂未生成，使用默认分数更新考试状态{Style.RESET_ALL}")
                self.finish_exam(course_packet_id)
            
            return True
        else:
            print(f"{Fore.RED}答案提交失败！{result.get('message', '')}{Style.RESET_ALL}")
            return False

    def study_course(self, course_packet_id):
        """自动学习课程"""
        import time
        import urllib.parse

        # 获取课程目录
        directory = self.get_course_directory(course_packet_id)
        if not directory or not directory.get('data'):
            logging.error(f"{Fore.RED}获取课程目录失败{Style.RESET_ALL}")
            return False

        # 遍历每个章节
        for section in directory['data']:
            print(f"\n{Fore.YELLOW}开始学习章节: {section['name']}{Style.RESET_ALL}")
            
            # 遍历每个子目录（具体课程）
            for sub in section['subDirectory']:
                print(f"\n{Fore.CYAN}正在学习: {sub['name']}{Style.RESET_ALL}")
                
                # 获取课程资源列表
                resources = self.get_course_resources(course_packet_id, sub['SYS_UUID'])
                if not resources or not resources.get('data') or not resources['data'].get('listdata'):
                    logging.error(f"{Fore.RED}获取课程资源列表失败{Style.RESET_ALL}")
                    continue

                # 遍历每个资源
                for resource in resources['data']['listdata']:
                        resource_length = self._convert_time_to_seconds(resource['timeLength'])
                        current_time = int(time.time() * 1000)  # 转换为毫秒时间戳
                        
                        # 保存学习记录
                        result = self.save_study_record(
                            course_id=course_packet_id,
                            resource_id=resource['resourceID'],
                            resource_directory_id=resource['SYS_UUID'],
                            resource_length=resource_length,
                            study_length=resource_length,
                            study_time=resource_length,
                            start_time=current_time,
                            resource_name=urllib.parse.quote(resource['name']),
                            resource_type='1',
                            resource_lib_id='3'
                        )
                        
                        if result and result.get('status') == 0:
                            print(f"{Fore.GREEN}完成学习: {resource['name']}{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.RED}学习失败: {resource['name']}{Style.RESET_ALL}")
                        
                        # 添加适当的延时，避免请求过于频繁
                        time.sleep(2)

        return True

    def finish_exam(self, course_packet_id, exam_score=100):
        """更新考试完成状态"""
        url = f"https://www.baomi.org.cn/portal/main-api/v2/studyTime/updateCoursePackageExamInfo.do"
        params = {
            'courseId': course_packet_id,
            'orgId': '',
            'isExam': 1,
            'isCertificate': 0,
            'examResult': exam_score,
            'token': self.token
        }
        try:
            response = self.session.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            result = response.json()
            if result and result.get('status') == 0:
                print(f"{Fore.GREEN}考试状态更新成功！{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.RED}考试状态更新失败！{result.get('message', '')}{Style.RESET_ALL}")
                return False
        except Exception as e:
            logging.error(f"{Fore.RED}更新考试状态失败: {e}{Style.RESET_ALL}")
            return False