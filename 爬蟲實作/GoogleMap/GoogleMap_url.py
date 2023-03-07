# 操作 browser 的 API
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 處理逾時例外的工具
from selenium.common.exceptions import TimeoutException

# 處理找不到元素的工具
from selenium.common.exceptions import NoSuchElementException

# 面對動態網頁，等待某個元素出現的工具，通常與 exptected_conditions 搭配
from selenium.webdriver.support.ui import WebDriverWait

# 搭配 WebDriverWait 使用，對元素狀態的一種期待條件，若條件發生，則等待結束，往下一行執行
from selenium.webdriver.support import expected_conditions as EC

# 期待元素出現要透過什麼方式指定，通常與 EC、WebDriverWait 一起使用
from selenium.webdriver.common.by import By

# 加入行為鍊 ActionChain (在 WebDriver 中模擬滑鼠移動、點繫、拖曳、按右鍵出現選單，以及鍵盤輸入文字、按下鍵盤上的按鈕等)
from selenium.webdriver.common.action_chains import ActionChains

# 加入鍵盤功能 (例如 Ctrl、Alt 等)
from selenium.webdriver.common.keys import Keys

# 強制等待 (執行期間休息一下)
import time
from time import sleep

# 整理 json 使用的工具
import json

# 讓顯示好讀
import pprint

# 平行任務處理
from concurrent.futures import ProcessPoolExecutor as ppe
from concurrent.futures import as_completed

# 啟動瀏覽器
def browser():

    # 啟動瀏覽器的工具選項
    my_options = webdriver.ChromeOptions()
    my_options.add_argument("--headless")  # 不開啟實體瀏覽器背景執行
    my_options.add_argument('--disable-gpu')  # 關閉 GPU，避免某些系統或是網頁出錯
    # my_options.add_argument("--start-maximized")  # 最大化視窗
    # my_options.add_argument('window-size=1920,1080')
    my_options.add_argument("--incognito")  # 開啟無痕模式
    my_options.add_argument("--disable-popup-blocking")  # 禁用彈出攔截
    my_options.add_argument("--disable-notifications")  # 取消 chrome 推播通知
    my_options.add_argument("--lang=zh-TW")  # 設定為正體中文
    my_options.add_experimental_option("detach", True)
    my_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    my_service = Service(ChromeDriverManager().install())

    # 使用 Chrome 的 WebDriver
    return webdriver.Chrome(options = my_options, service = my_service)

# 開啟目標網頁
def TargetMap(links: str):

    googleMap = 'https://www.google.com.tw/maps?hl=zh-TW'

    # 開啟 Google Map 首頁
    driver = browser()
    driver.get(googleMap)

    # 等待元素出現
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'button[aria-label="搜尋"]')
        )
    )
    
    sleep(2) # 依網路狀況調整

    ac = ActionChains(driver)
    # 輸入 Keyword
    ac.send_keys(links)
    ac.pause(1)
    # 按下 ENTER
    ac.send_keys(Keys.ENTER)
    ac.perform()

    sleep(3) # 依網路狀況調整

    urlList = []  # 存放首頁查詢滾 動完的所有店家資訊網址

    # 滾動頁面
    offset = 0
    innerHeight = 0
    count = 0  # 累計無效滾動次數
    limit = 2  # 最大無效滾動次數
    refresh_counter = 0 

    try:

        # # 等待篩選元素出現
        # WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located(
        #         (By.CSS_SELECTOR, 'div[role="feed"]')
        #     )
        # )

        # focus: 主角頁面
        focus = driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')
        pass

        # 持續捲動
        while True:

            try:

                # focus: 主角頁面
                focus = driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')

                # 檢查是否滾動到底，並且有顯示「你已看完所有搜尋結果」的標籤
                driver.find_element(By.CSS_SELECTOR, 'div[data-js-log-root] div[data-js-log-root] div[data-js-log-root] p[style^="font-family"] span[style^="color"]')

                break
                
            except NoSuchElementException:

                # offset: 拉槓到頁面頂端的距離
                offset = driver.execute_script('return arguments[0].scrollTop', focus)
                # print(offset)

                # 執行js指令捲動頁面
                driver.execute_script('arguments[0].scrollTo(0, arguments[0].scrollHeight)', focus)

                # innerHeight: 頁面高度 = 拉槓到頁面頂端的距離
                innerHeight = driver.execute_script('return arguments[0].scrollHeight = arguments[0].scrollTop', focus)
                # print(innerHeight)

                sleep(2)  # 依網路狀況調整

                # 經過計算，如果「拉槓到頁面頂端的距離」(offset)等於「頁面高度 = 拉槓到頁面頂端的距離」(innerHeight)，代表已經到底了
                if offset == innerHeight:
                    count += 1

                # 計數器等於限制數則跳脫
                if count == limit:

                    # print(f'[{links}] 捲動失敗! 重新整理!')

                    count = 0  # 計數器歸零

                    refresh_counter += 1

                    if refresh_counter == 1:

                        # print(f'[{links}] 重新整理三次，直接抓取網址')

                        break

                    driver.refresh()  # 重整頁面
            
        # 紀錄首頁滾動完的所有店家資訊網址
        for a in driver.find_elements(By.CSS_SELECTOR, 'div[data-js-log-root] div[role="article"] > a[aria-label]'):
            urlList.append(a.get_attribute("href"))

        print(f'[{links}] 搜尋已到底，滾動結束，有 {len(urlList)} 筆店家')

        sleep(1)

        driver.quit()
        
        # pprint.pprint(urlList)
        # print(len(urlList))

        return urlList

    except NoSuchElementException:

        print(f'[{links}] 掛掉了!!!!!')

        driver.quit()

        return []

# 平行處理
def FirstPage():

    comList = []  # 整合所有 Keywords 查詢完的網頁 List
    allurlList = []  # 最終寫出檔案的 List
    keywords = []  # 儲存所有條件字的組合
    counter = 1

    street = ['中正區', '大同區', '中山區', '松山區', '大安區', '萬華區', '信義區', '士林區', '北投區', '內湖區', '南港區', '文山區'] 

    category = ['紀念公園', '歷史地標', '旅遊景點', '歷史建築', '夜景']

    for item_1 in street:
        for item_2 in category:
            links = f'{item_1}{item_2}'

            keywords.append(links) 

    with ppe(max_workers=4) as executor:
        
        results = [executor.submit(TargetMap, key) for key in keywords]
        try:
            for result in as_completed(results):

                for i in (result.result()):

                    comList.append(i)

                print(counter) 

                counter += 1

            allurlList.append({
                "href": comList  # 篩選掉重複的網址
            })

            print(len(comList))

            # 寫出 json 檔
            with open(f'台北市景點.json', 'w', encoding='utf-8') as file:
                (json.dump(allurlList, file, ensure_ascii=False, indent=4))
            
            sleep(2)

        except TimeoutException:
            pass

if __name__ == '__main__':
    time1 = time.time()
    FirstPage()
    print(f'執行總花費時間: {time.time() - time1}')

# 餐廳 ['火鍋', '拉麵', '日本料理', '美式', '義式', '法式', '中式', '台灣菜', '韓式', '德式', '地中海料理', '印度料理', '越式', '港式', '泰式', '南洋', '素食', '鐵板燒', '餐酒館', '咖啡廳', '熱炒店', '早午餐', '甜點店', '燒肉', '海鮮餐廳', '牛排'] # 26 * category

# 景點 ['紀念公園', '歷史地標', '旅遊景點', '歷史建築', '夜景'] # 5 * category

# 大同區 ['大龍街_', '五原路_', '天水路_', '太原路_', '市民大道一段_', '平陽街_', '民生西路_', '民族西路_', '民樂街_', '民權西路_', '永昌街_', '甘州街_', '甘谷街_', '伊寧街_', '安西街_', '西寧北路_', '赤峰街_', '延平北路一段_', '延平北路二段_', '延平北路三段_', '延平北路四段_', '忠孝西路二段_', '承德路一段_', '承德路二段_', '承德路三段_', '昌吉街_', '長安西路_', '保安街_', '大南京西路_', '哈密街_', '迪化街一段_', '迪化街二段_', '重慶北路一段_', '重慶北路二段_', '重慶北路三段_', '庫倫街_', '酒泉街_', '涼州街_', '通河西街一段_', '敦煌路_', '景化街_', '華亭街_', '華陰街_', '貴德街_', '塔城街_', '萬全街_', '寧夏路_', '撫順街_', '鄭州路_', '興城街_', '錦西街_', '環河北路一段_', '環河北路二段_', '歸綏街_', '雙連街_', '蘭州街_']

# 士林區 ["下樹林街_", "中山北路四段_", "中山北路五段_", "中山北路六段_", "中山北路七段_", "中庸一路_", "中庸二路_", "中庸五路_", "中正路_", "中社路一段_", "中社路二段_", "中興街_", "中華路_", "仁民路_", "仰德大道一段_", "仰德大道二段_", "仰德大道三段_", "仰德大道四段_", "倫等街_", "光華路_", "克強路_", "凱旋路_", "前港街_", "前街_", "劍南路_", "劍潭路_", "力行街_", "和平路_", "和豐街_", "國泰街_", "基河路_", "士商路_", "士東路_", "大亨路_", "大光街_", "大北路_", "大南路_", "大東路_", "大西路_", "天母北路_", "天母東路_", "天母西路_", "天玉街_", "安平街_", "小北街_", "小南街_", "小東街_", "小西街_", "平菁街_", "幸福街_", "延平北路五段_", "延平北路六段_", "延平北路七段_", "延平北路八段_", "延平北路九段_", "建業路_", "後港街_", "後街_", "德行東路_", "德行西路_", "志成街_", "忠勇街_", "忠義街_", "忠誠路一段_", "忠誠路二段_", "愛富一街_", "愛富三街_", "愛富三街長生巷_", "愛富二街_", "愛富二街厚生巷_", "愛富二街樂生巷_", "承德路四段_", "承德路五段_", "故宮路_", "文昌路_", "文林路_", "新園街_", "新安路_", "明溪街_", "東山路_", "格致路_", "永公路_", "永平街_", "環河北路三段_", "磺溪街_", "社中街_", "社子街_", "社正路_", "福國路_", "福壽街_", "福德路_", "福志路_", "福林路_", "福榮街_", "福港街_", "福華路_", "竹子湖路_", "美崙街_", "美德街_", "翠山街_", "臨溪路_", "自祥街_", "至善路一段_", "至善路二段_", "至善路三段_", "至誠路一段_", "至誠路二段_", "芝玉路一段_", "芝玉路二段_", "莊頂路_", "菁山路_", "華光街_", "華岡路_", "華榮街_", "華聲街_", "華興街_", "華齡街_", "葫東街_", "葫蘆街_", "貴富街_", "通河東街一段_", "通河東街二段_", "通河街_", "通河西街一段_", "通河西街二段_", "重慶北路四段_", "長春街_", "陽明路一段_", "陽明路二段_", "雙溪街_", "雨聲街_", "雨農路_"]

# 行政區 ['中正區_', '大同區_', '中山區_', '松山區_', '大安區_', '萬華區_', '信義區_', '士林區_', '北投區_', '內湖區_', '南港區_', '文山區_']