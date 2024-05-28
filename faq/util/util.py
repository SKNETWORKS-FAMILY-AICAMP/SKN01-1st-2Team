# util.py
import selenium
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

### 드라이버 변경하기
chrome_driver_path = r'/usr/local/bin/chromedriver'

class User:
    def __init__(self):
        self.new_window = True
        self.options = Options()
        # detach True 옵션 안끄면 크롬창 계속 열려있으니 원치 않는다면 주석처리하세요(코드 여러번 돌리면 크롬창이 매우매우 많이 생성됩니다..)
        self.options.add_argument("--start-maximized")
        self.options.add_experimental_option("detach", True)
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.browser  = webdriver.Chrome(options=self.options)
        self.browser.maximize_window()
        self.scroll_pos = 0 
        # service = Service(chrome_driver_path) 버전 업데이트 되면서 필요없어짐

    def getBrowser(self, url='https://naver.com', new_window=True, option=None):  
        if new_window == False: # 기존 브라우저 모드
            print('디버깅 모드를 시작합니다.')
            time.sleep(2)
            option = self.options
            option.add_experimental_option('debuggerAddress','127.0.0.1:9222')
            
            # 디버거모드로 실행해보고 싶으면, 본인 랩탑 chrome.exe 경로 찾아서 변경하기 --> 파라미터 new_window=False
            # cmd = ['chrome.exe', '--remote-debugging-port=9222', '--user-data-dir="C:\\Program Files\\Google\\Chrome\\Temp"']
            # chrome_directory = 'C:\\Program Files\\Google\\Chrome\\Application'
            # subprocess.run(cmd, cwd=chrome_directory, shell=True)

        else:
            self.browser.get(url)
            
    # 해당 XPATH의 요소의 text 반환하는 함수
    def find_ele_text(self,user_xpath):
        text = self.browser.find_element(By.XPATH, user_xpath).text.strip()
        return text

    

    # item_name을 파라미터로 입력받아, 검색창에 입력하는 함수
    def search_keword(self,user_xpath, item_name):
        self.browser.find_element(By.XPATH, user_xpath).send_keys(item_name)
        
    # 버튼 클릭 함수 (모든 클릭해야 하는 부분에서 사용함)
    # 웹페이지 버튼의 role을 보면 link인 것이 있고 아닌 것이 있었음. 
    # -> 해당 부분에서 오류가나는가 싶어서 구글링해서 By.PARTIAL_LINK_TEXT 가져옴
    def click_button(self,button_xpath=None):
        try:
            self.browser.find_element(By.XPATH, button_xpath).click()
            print('버튼 클릭 성공')
        except Exception as e:
            print('By.XPATH로 클릭되지 않습니다. By.PARTIAL_LINK_TEXT로 접근합니다! ')
            time.sleep(2)
            try:
                totext = self.find_ele_text(button_xpath) # 버튼 이름 텍스트로 가져와서
                self.browser.find_element(By.PARTIAL_LINK_TEXT, totext).click() # By.PARTIAL_LINK_TEXT 안에 넣어줌
    
                print('성공!')
                if totext == None: # 텍스트 받아오기를 실패하면 직접 이름 입력
                    print('해당 버튼의 키워드(이름)를 추가로 입력하세요. --> click_button(XPATH, 버튼 이름)')
                    
            except Exception as e:
                print('문제발생!', type(e))

    # 스크롤 내려주는 함수 
    # 픽셀값이 0이면 최상단. pixel 파라미터값만큼 이동 (defualt는 500씩 이동하도록 설정)
    def scroll_down(self, pixel=500, init_pos=False): 
        try:
            if init_pos == True: # 새로운 탭으로 전환할 경우 스크롤 위치 픽셀값을 최상단으로 초기화하기 위해 지정
                self.scroll_pos = 0         

            self.browser.execute_script(f"window.scrollTo({self.scroll_pos}, {self.scroll_pos+pixel})") # (2) 해당위치에서 pixel만큼 이동하도록
            self.scroll_pos = self.scroll_pos + pixel # (1) 스크롤값이 계속 저장되어서 ----------------------↑
            print('스크롤 다운 성공')

        except Exception as e:
            print('스크롤 다운 실패') 
            print(e)   

    def close_connect(self): # 창이 닫히는 게 아닌 연결이 끊기는 것
        self.browser.close()
        print('finished.')
        print(' ')

    def change_window(self):
        self.browser.switch_to.window(self.browser.window_handles[-1]) # 가장 마지막에 열린 창으로 이동