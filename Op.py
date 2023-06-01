import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# กำหนด URL เป้าหมาย
target_url = "https://dino-th.pages.dev"

# กำหนดเบราว์เซอร์ที่ต้องการใช้ (ต้องมี WebDriver ของเบราว์เซอร์นั้น ๆ ลงในระบบก่อน)
browser = webdriver.Chrome()

# เข้าสู่หน้าเว็บเป้าหมาย
browser.get(target_url)

# ฟังก์ชันสำหรับการสุ่มคลิกลิงก์ในหน้าเว็บ
def click_random_link():
    # ค้นหาลิงก์ทั้งหมดในหน้าเว็บ
    links = browser.find_elements(By.TAG_NAME, "a")
    
    # สุ่มเลือกลิงก์
    random_link = random.choice(links)
    
    # คลิกลิงก์
    random_link.click()

# ลูปการคลิกลิงก์ในหน้าเว็บ
while True:
    # สุ่มคลิกลิงก์ในหน้าเว็บ
    click_random_link()
    
    # หน่วงเวลาก่อนการคลิกลิงก์ถัดไป
    time.sleep(random.randint(2, 5))
