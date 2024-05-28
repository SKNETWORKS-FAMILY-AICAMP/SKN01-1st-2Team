# runner.py
import os
import time
import pandas as pd
from util.util import User

# 사이트 접속 -> 전기친환경 클릭 -> 개인 클릭 -> 페이지 번호 클릭
if __name__ == "__main__":
    user = User()
    user.getBrowser("http://www.encar.com/", new_window=True)
    time.sleep(2)
    # user.search_keword('//*[@id="AKCSearch"]', '맥북')
    user.click_button('//*[@id="evmenu"]')  # 전기친환경
    time.sleep(2)
    user.click_button(
        '//*[@id="rySch_car"]/div[2]/fieldset/div[11]/h5/a'
    )  # 판매자 구분
    time.sleep(2)
    user.scroll_down(500)  # 내려서
    time.sleep(2)
    user.click_button(
        '//*[@id="schBuytype"]/div/ul/li[1]/label'
    )  # 개인 판매자 체크박스
    time.sleep(2)
    # user.click_button('//*[@id="searchCondition2"]/div[6]/div[2]/a') # 검색버튼
    # # user.scroll_down(200)
    # # user.click_button('//*[@id="opinionDESC"]')  # 상품평 많은 순 --> 생략
    # time.sleep(3)
    # user.click_button('/html/body/div[2]/div[4]/div[3]/div[2]/div[8]/div[1]/div[2]/div[3]/ul/li[1]/div/div[2]/p/a')  # 상품이름 클릭

    # time.sleep(3)
    # user.change_window() # 탭 전환
    # user.scroll_down(600, init_pos=True)
    # user.click_button('//*[@id="bookmark_cm_opinion_item"]/a/h3') # 의견/리뷰 누르기
    # user.click_button('//*[@id="danawa-prodBlog-productOpinion-button-tab-companyReview"]') # 쇼핑몰 상품 리뷰 클릭
    # time.sleep(3)
    # user.scroll_down(300)

    name_lst = []
    year_lst = []
    kilo_lst = []
    price_lst = []
    

    for i in range(17):
        try:
            if i <= 9:
                user.click_button(f"/html/body/div[1]/div[2]/div[1]/div[2]/div[3]/div[1]/div[4]/div[5]/span[{i+1}]/a") #다음페이지
            elif 9 < i <= 17:
                user.click_button(f"/html/body/div[1]/div[2]/div[1]/div[2]/div[3]/div[1]/div[4]/div[5]/span[{i-8}]/a") #다음페이지
            time.sleep(3)
            try:
                for j in range(21):  # 제목이나 사이트 등 더 추가하고 싶다면 여기서 추가 입력
                    name = f"/html/body/div[1]/div[2]/div[1]/div[2]/div[3]/div[1]/div[4]/div[3]/table/tbody/tr[{j+1}]/td[2]/a"  # 차이름
                    year = f"/html/body/div[1]/div[2]/div[1]/div[2]/div[3]/div[1]/div[4]/div[3]/table/tbody/tr[{j+1}]/td[2]/span[1]/span[1]"  # 연식
                    kilo = f"/html/body/div[1]/div[2]/div[1]/div[2]/div[3]/div[1]/div[4]/div[3]/table/tbody/tr[{j+1}]/td[2]/span[1]/span[2]"  # 킬로수
                    price = f"/html/body/div[1]/div[2]/div[1]/div[2]/div[3]/div[1]/div[4]/div[3]/table/tbody/tr[{j+1}]/td[3]/strong"  # 가격
                    
                    name = user.find_ele_text(name)
                    print(name)
                    year = user.find_ele_text(year)
                    print(year)
                    kilo = user.find_ele_text(kilo)
                    print(kilo)
                    price = user.find_ele_text(price)
                    print(price)
                    
                    name_lst.append(name)
                    year_lst.append(year)
                    kilo_lst.append(kilo)
                    price_lst.append(price)
                    
            except:
                pass

            if i==9:
                user.click_button("/html/body/div[1]/div[2]/div[1]/div[2]/div[3]/div[1]/div[4]/div[5]/span[11]")
                print(f'------------ {i+1}페이지 finished!! -------------')
                print(f'------------ 11페이지 부터 시작!!-------------')
                
            else:
                print(f'------------ {i+1}페이지 finished!! -------------')
                # time.sleep(2)
                # user.click_button(f'/html/body/div[2]/div[5]/div[2]/div[4]/div[4]/div/div[3]/div[2]/div[3]/div[2]/div[5]/div/div/div/a[{i+1}]')

                ## 오류가 났던 이유
                # 나머지 페이지들의  PATH : /html/body/div[2]/div[5]/div[2]/div[4]/div[4]/div/div[3]/div[2]/div[3]/div[2]/div[5]/div/div/div/a[1] # page 1
                # 마지막 페이지(6쪽) PATH : /html/body/div[2]/div[5]/div[2]/div[4]/div[4]/div/div[3]/div[2]/div[3]/div[2]/div[5]/div/div/div/span
        except:
            pass
    name_lst = [name for name in name_lst if name.strip()]
    year_lst = [year for year in year_lst if year.strip()]
    kilo_lst = [kilo for kilo in kilo_lst if kilo.strip()]
    price_lst = [price for price in price_lst if price.strip()]
    user.close_connect()
    print(f"차량 {len(name_lst)}대가 저장되었습니다.")

    df = pd.DataFrame(
        {
            "차 이름": name_lst,
            "연식": year_lst,
            "키로수": kilo_lst,
            "가격": price_lst,
        }
    )

    # result 파일 경로 만들기
    result_path = os.path.join(os.getcwd(), "result")
    os.makedirs(result_path, exist_ok=True)
    # csv로 저장
    df.to_csv(os.path.join(result_path, "review.csv"), index=False, encoding="utf-8")
    print(f'#### "review.csv"가 {result_path}에 저장되었습니다. ####')
