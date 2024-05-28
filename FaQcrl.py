from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# 웹 드라이버 설정 및 웹 페이지 열기
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("http://www.encar.com/board/boardRead.do?boardId=003&method=faq")

# 필요한 시간 동안 페이지 로드 대기
time.sleep(3)

qstns = []
answer = []


# 페이지 넘김을 위해 다음 페이지 링크를 찾는 함수
def get_next_page():
    partP = driver.find_element(By.CSS_SELECTOR, ".part.page")
    current_page = int(partP.find_element(By.CLASS_NAME, "current").text)
    next_page_elements = partP.find_elements(By.TAG_NAME, "a")

    if current_page < len(next_page_elements):
        return next_page_elements[current_page]
    return None


while True:
    try:
        Qs = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "q"))
        )

        actions = ActionChains(driver)

        for i in Qs:
            try:
                a_tag = i.find_element(By.TAG_NAME, "a")
                actions.move_to_element(a_tag).click().perform()
                time.sleep(0.3)
            except Exception as e:
                print(f"Error processing question: {e}")
                continue

        for i in Qs:
            Qss = i.find_element(By.TAG_NAME, "a").text
            qstns.append(Qss)

        As = driver.find_elements(By.CLASS_NAME, "a")
        for i in As:
            try:
                Ass = i.find_element(By.CLASS_NAME, "text").text
                answer.append(Ass)
            except Exception as e:
                print(f"Error processing answer: {e}")
                continue

        next_page = get_next_page()

        if not next_page:
            break

        next_page.click()
        time.sleep(3)  # 페이지 로드 대기

    except Exception as e:
        print(f"Error in main loop: {e}")
        break

# 데이터프레임 생성
df = pd.DataFrame(
    {
        "Q": qstns,
        "A": answer,
    }
)

# 데이터프레임을 CSV 파일로 저장
df.to_csv("QnAs.csv", index=False)

# 드라이버 종료
driver.quit()
