import time
import random
import requests
from bs4 import BeautifulSoup

# กำหนด URL เป้าหมาย
target_url = "https://dino-th.pages.dev"


# ฟังก์ชันสำหรับการคลิกลิงก์ที่เป็น popup
def click_popup_links(links):
    # ค้นหาลิงก์ที่เป็น popup
    popup_links = [link for link in links if "popup" in link.get("class", [])]

    if popup_links:
        # สุ่มเลือกลิงก์ popup
        random_link = random.choice(popup_links)

        # ดึง URL ของลิงก์
        link_url = random_link.get("href")

        # เรียกเข้าถึงเนื้อหาของลิงก์
        response = requests.get(link_url)

        # แสดงข้อความแจ้งเตือน
        print("Clicked on popup link:", link_url)


# ลูปการคลิกลิงก์ในหน้าเว็บ
while True:
    # เรียกเข้าถึงเนื้อหาของหน้าเว็บเป้าหมาย
    response = requests.get(target_url)

    # แสดงข้อความแจ้งเตือน
    print("Accessed target URL:", target_url)

    # สร้างตัวแปรเพื่อใช้ในการค้นหาลิงก์
    soup = BeautifulSoup(response.content, "html.parser")

    # ค้นหาลิงก์ทั้งหมดในหน้าเว็บ
    links = soup.find_all("a")

    # คลิกลิงก์ที่เป็น popup
    click_popup_links(links)

    # หน่วงเวลาก่อนการคลิกลิงก์ถัดไป
    time.sleep(random.randint(2, 5))
