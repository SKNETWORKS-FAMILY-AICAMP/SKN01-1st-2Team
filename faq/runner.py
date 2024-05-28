# # runner.py
# import os
# import time
# import pandas as pd
# from util.util import User

# # 사이트 접속 -> 전기친환경 클릭 -> 개인 클릭 -> 페이지 번호 클릭
# if __name__ == "__main__":
#     user = User()
#     user.getBrowser("http://www.encar.com/", new_window=True)
#     time.sleep(2)
#     user.click_button('/html/body/div[1]/div[1]/ul[2]/li[3]/a')  # menu
#     user.click_button('/html/body/div[1]/div[1]/div[2]/div/div[2]/div[4]/ul/li[2]/a')  # faq
#     time.sleep(2)
    

#     q_lst = []
#     a_lst = []
    

#     for i in range(5):
#         try:
#             user.click_button(f"/html/body/div[1]/div[2]/div[1]/div/form/div[3]/span[2]/a[{i+1}]")
#             time.sleep(1)
#             try:
#                 for j in range(40):  # 제목이나 사이트 등 더 추가하고 싶다면 여기서 추가 입력
#                     if j%2 == 0:
#                         time.sleep(1)
#                         q = f"/html/body/div[1]/div[2]/div[1]/div/form/span/div/ul/li[{j+1}]"  # question
#                         q = user.find_ele_text(q)
#                         q_lst.append(q)
#                         print(q)
#                     else:
#                         user.click_button(f"/html/body/div[1]/div[2]/div[1]/div/form/span/div/ul/li[{j}]/a")
#                         time.sleep(1)
#                         a = f'/html/body/div[1]/div[2]/div[1]/div/form/span/div/ul/li[{j+1}]/div[@class="text"]'  # answer
#                         a = user.find_ele_text(a)
#                         a_lst.append(a)
#                         print(a)

#             except:
#                 pass

#                 print(f'------------ {i+1}페이지 finished!! -------------')
                
#         except:
#             pass
#     # q_lst = [q for q in q_lst if q.strip()]
#     # a_lst = [a for a in a_lst if a.strip()]
    
#     user.close_connect()
#     print(f"질문 {len(q_lst)}개가 저장되었습니다.")
#     print(f"답변 {len(a_lst)}개가 저장되었습니다.")

#     df = pd.DataFrame(
#         {"질문": q_lst, "답변": a_lst,}
#     )

#     # result 파일 경로 만들기
#     result_path = os.path.join(os.getcwd(), "result")
#     os.makedirs(result_path, exist_ok=True)
#     # csv로 저장
#     df.to_csv(os.path.join(result_path, "review_faq.csv"), index=False, encoding="utf-8")
#     print(f'#### "review_faq.csv"가 {result_path}에 저장되었습니다. ####')

# runner.py
import os
import time
import pandas as pd
from util.util import User
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    user = User()
    user.getBrowser("http://www.encar.com/", new_window=True)
    time.sleep(2)
    user.click_button('/html/body/div[1]/div[1]/ul[2]/li[3]/a')  # 메뉴 클릭
    user.click_button('/html/body/div[1]/div[1]/div[2]/div/div[2]/div[4]/ul/li[2]/a')  # FAQ 클릭
    time.sleep(2)
    
    q_lst = []
    a_lst = []
    
    for i in range(5):
        try:
            user.click_button(f"/html/body/div[1]/div[2]/div[1]/div/form/div[3]/span[2]/a[{i+1}]")
            time.sleep(1)
            try:
                for j in range(40):  # 제목이나 사이트 등 더 추가하고 싶다면 여기서 추가 입력
                    if j % 2 == 0:
                        time.sleep(1)
                        q_xpath = f"/html/body/div[1]/div[2]/div[1]/div/form/span/div/ul/li[{j+1}]"
                        q = user.find_ele_text(q_xpath)
                        q_lst.append(q)
                        print(q)
                    else:
                        user.click_button(f"/html/body/div[1]/div[2]/div[1]/div/form/span/div/ul/li[{j}]/a")
                        time.sleep(1)
                        a_xpath = f'/html/body/div[1]/div[2]/div[1]/div/form/span/div/ul/li[{j+1}]/div[@class="text"]'
                        a = user.find_ele_text(a_xpath)
                        a_lst.append(a)
                        print(a)
            except Exception as e:
                print(f"질문/답변 처리 중 오류 발생: {e}")
                continue

            print(f'------------ {i+1}페이지 완료!! -------------')

        except Exception as e:
            print(f"{i+1}페이지 처리 중 오류 발생: {e}")
            continue
    
    # 두 리스트의 길이를 맞추기 위해 짧은 리스트에 빈 문자열을 추가
    max_len = max(len(q_lst), len(a_lst))
    q_lst += [""] * (max_len - len(q_lst))
    a_lst += [""] * (max_len - len(a_lst))
    
    user.close_connect()
    print(f"질문 {len(q_lst)}개가 저장되었습니다.")
    print(f"답변 {len(a_lst)}개가 저장되었습니다.")

    df = pd.DataFrame({"질문": q_lst, "답변": a_lst})

    # result 파일 경로 만들기
    result_path = os.path.join(os.getcwd(), "result")
    os.makedirs(result_path, exist_ok=True)
    # csv로 저장
    df.to_csv(os.path.join(result_path, "review_faq.csv"), index=False, encoding="utf-8")
    print(f'#### "review_faq.csv"가 {result_path}에 저장되었습니다. ####')

if __name__ == "__main__":
    main()
