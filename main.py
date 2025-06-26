import requests
import time
import logging
import json 
import os
from colorama import init, Fore, Style
import login

# Initialize colorama
init()

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 凭证文件路径
CREDENTIALS_FILE = 'credentials.json'

# 创建会话
session = requests.Session()

def get_headers(token):
    """返回带有当前token的headers"""
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        'token': token,
        'authToken': token,
        'siteId': '95',
        'Content-Type': 'application/json'
    }

def save_credentials(loginName, passWord, token):
    """保存用户凭证到本地文件"""
    data = {
        'loginName': loginName,
        'passWord': passWord,
        'token': token,
        'timestamp': int(time.time())
    }
    
    with open(CREDENTIALS_FILE, 'w') as f:
        json.dump(data, f)
    logging.info(f"{Fore.GREEN}凭证已保存{Style.RESET_ALL}")

def load_credentials():
    """从本地文件加载用户凭证"""
    if not os.path.exists(CREDENTIALS_FILE):
        return None
    
    try:
        with open(CREDENTIALS_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"{Fore.RED}加载凭证失败: {e}{Style.RESET_ALL}")
        return None

# 检查登录情况
def check_login(token):
    """检查token是否有效，返回用户昵称或False。如果昵称为空则返回'未设定姓名'"""
    if not token:
        return False
        
    headers = get_headers(token)
    url = 'https://www.baomi.org.cn/portal/main-api/checkToken.do'
    try:
        response = session.get(url, headers=headers).json()
        result = response.get('result')
        if result:
            nickname = response['data'].get('nickName')
            if not nickname:
                return "未设定姓名"
            return nickname
    except Exception as e:
        logging.error(f"{Fore.RED}检查token失败: {e}{Style.RESET_ALL}")
    
    return False

def get_user_credentials():
    """获取用户凭证，优先使用保存的凭证，否则进行登录"""
    # 检查是否有保存的凭证
    saved_creds = load_credentials()
    
    if saved_creds:
        # 提示用户是否使用保存的凭证
        print(f"{Fore.YELLOW}发现保存的用户名: {saved_creds['loginName']}{Style.RESET_ALL}")
        use_saved = input(f"{Fore.CYAN}是否使用保存的凭证自动登录? (y/n): {Style.RESET_ALL}").lower() == 'y'
        
        if use_saved:
            # 验证保存的token
            token = saved_creds['token']
            if check_login(token):
                print(f"{Fore.GREEN}使用已保存的凭证登录成功{Style.RESET_ALL}")
                return saved_creds['loginName'], saved_creds['passWord'], token
            else:
                print(f"{Fore.YELLOW}保存的凭证已过期，需要重新登录{Style.RESET_ALL}")
    
    # 获取新凭证
    print(f"{Fore.CYAN}请输入新凭证进行登录{Style.RESET_ALL}")
    loginName = input(f"{Fore.CYAN}请输入用户名: {Style.RESET_ALL}")
    passWord = input(f"{Fore.CYAN}请输入密码: {Style.RESET_ALL}")
    
    # 执行登录
    try:
        token = login.login(loginName, passWord)
        print(f"{Fore.GREEN}登录成功获取到token!{Style.RESET_ALL}")
        
        # 自动保存凭证
        save_credentials(loginName, passWord, token)
        print(f"{Fore.GREEN}已自动保存凭证{Style.RESET_ALL}")
        
        return loginName, passWord, token
    except Exception as e:
        print(f"{Fore.RED}登录失败: {e}{Style.RESET_ALL}")
        return get_user_credentials()  # 递归调用直到登录成功

def display_course_menu():
    """显示课程管理菜单"""
    print(f"\n{Fore.CYAN}============ 课程管理菜单 ============{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}1. 查看课程目录{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}2. 查看课程进度{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}3. 开始学习课程{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}4. 完成课程考试{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}0. 退出程序{Style.RESET_ALL}")
    choice = input(f"\n{Fore.CYAN}请选择操作 (0-4): {Style.RESET_ALL}")
    return choice

def handle_course_menu(course_manager):
    """处理课程管理菜单选择"""
    while True:
        choice = display_course_menu()
        
        if choice == '0':
            print(f"\n{Fore.GREEN}感谢使用，再见！{Style.RESET_ALL}")
            break
        elif choice == '1':
            # 获取课程目录
            course_info = course_manager.get_course_info('21c7d935-dd53-49d2-a95f-dc0f3e14ced7')
            if course_info and course_info.get('data'):
                print(f"\n{Fore.GREEN}当前课程: {course_info['data']['name']}{Style.RESET_ALL}")
                print(f"课程说明: {course_info['data']['note']}")
                
                directory = course_manager.get_course_directory('21c7d935-dd53-49d2-a95f-dc0f3e14ced7')
                if directory and directory.get('data'):
                    print(f"\n{Fore.CYAN}课程目录:{Style.RESET_ALL}")
                    for section in directory['data']:
                        print(f"\n{Fore.YELLOW}{section['name']}{Style.RESET_ALL}")
                        for sub in section['subDirectory']:
                            print(f"  - {sub['name']}")
        elif choice == '2':
            # 查看课程进度
            progress = course_manager.get_course_progress('21c7d935-dd53-49d2-a95f-dc0f3e14ced7')
            if progress and progress.get('data'):
                data = progress['data']
                print(f"\n{Fore.CYAN}课程进度信息:{Style.RESET_ALL}")
                print(f"课程名称: {data['courseName']}")
                print(f"学习进度: {data['progressRate']*100:.1f}%")
                print(f"已学课程数: {data['studyResourceNum']}/{data['resourceSum']}")
                print(f"总学习时长: {data['totalStudyTime']}秒")
                print(f"是否完成: {'是' if data['isFinish'] else '否'}")
                print(f"是否获得证书: {'是' if data['isCertificate'] else '否'}")
        elif choice == '3':
            # 开始自动学习课程
            print(f"\n{Fore.CYAN}开始自动学习课程...{Style.RESET_ALL}")
            if course_manager.study_course('21c7d935-dd53-49d2-a95f-dc0f3e14ced7'):
                print(f"\n{Fore.GREEN}课程学习完成！{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}课程学习失败，请稍后重试{Style.RESET_ALL}")
        elif choice == '4':
            # 开始自动完成考试
            print(f"\n{Fore.CYAN}开始自动完成考试...{Style.RESET_ALL}")
            if course_manager.complete_exam('21c7d935-dd53-49d2-a95f-dc0f3e14ced7'):
                print(f"\n{Fore.GREEN}考试完成！{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}考试完成失败，请稍后重试{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}无效的选择，请重试{Style.RESET_ALL}")

if __name__ == '__main__':
    print(f"{Fore.CYAN}============ 保密教育登录程序 ============{Style.RESET_ALL}")
    loginName, passWord, token = get_user_credentials()
    
    # 验证登录状态
    nickname = check_login(token)
    if nickname:
        print(f"{Fore.GREEN}登录成功! 欢迎, {nickname}{Style.RESET_ALL}")
        # 初始化课程管理器
        from course import CourseManager
        course_manager = CourseManager(session, token)
        # 显示课程管理菜单
        handle_course_menu(course_manager)
    else:
        print(f"{Fore.RED}登录失败或token无效{Style.RESET_ALL}")
