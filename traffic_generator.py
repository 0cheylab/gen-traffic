import requests
import random
import time
import re

class ConfigClass:
    MAX_DEPTH = 10
    MIN_DEPTH = 3
    MAX_WAIT = 10
    MIN_WAIT = 5
    DEBUG = True
    ROOT_URLS = [
        "https://dolatiaschan.com/afu.php?zoneid=5999405&var=5999405&rid=XXz4jyvWNyEJSqRKY8d18w%3D%3D&rhd=false&os=windows&os_version=10.0.0",
        "https://dolatiaschan.com/4/5999405"
    ]
    blacklist = [
        'facebook.com',
        'pinterest.com'
    ]
    USER_AGENT = 'Mozilla/5.0 (Android 12; Mobile; LG-M255; rv:100.0) Gecko/100.0 Firefox/100.0Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.61 Mobile Safari/537.36'

config = ConfigClass

class Colors:
    RED = '\033[91m'
    YELLOW = '\033[93m'
    PURPLE = '\033[95m'
    NONE = '\033[0m'

def debug_print(message, color=Colors.NONE):
    if config.DEBUG:
        print(color + message + Colors.NONE)

def hr_bytes(bytes_, suffix='B', si=False):
    bits = 1024.0 if si else 1000.0

    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(bytes_) < bits:
            return "{:.1f}{}{}".format(bytes_, unit, suffix)
        bytes_ /= bits
    return "{:.1f}{}{}".format(bytes_, 'Y', suffix)

def do_request(url):
    global data_meter
    global good_requests
    global bad_requests

    debug_print("กำลังร้องขอหน้าเว็บ: {}".format(url))

    headers = {'user-agent': config.USER_AGENT}

    try:
        r = requests.get(url, headers=headers, timeout=(5, 10))
    except:
        # ป้องกันการวนซ้ำ CPU 100% ในกรณีเครือข่ายล่ม
        time.sleep(30)
        return False

    page_size = len(r.content)
    data_meter += page_size

    debug_print("ขนาดหน้าเว็บ: {}".format(hr_bytes(page_size)))
    debug_print("เมตรข้อมูล: {}".format(hr_bytes(data_meter)))

    status = r.status_code

    if status != 200:
        bad_requests += 1
        debug_print("สถานะการตอบกลับ: {}".format(r.status_code), Colors.RED)
        if status == 429:
            debug_print("เรากำลังทำการร้องขอบ่อยเกินไป... หยุดสักครู่...")
            config.MIN_WAIT += 10
            config.MAX_WAIT += 10
    else:
        good_requests += 1

    debug_print("การร้องขอที่สำเร็จ: {}".format(good_requests))
    debug_print("การร้องขอที่ล้มเหลว: {}".format(bad_requests))

    return r

def get_links(page):
    pattern = r"(?:href\=\")(https?:\/\/[^\"]+)(?:\")"
    links = re.findall(pattern, str(page.content))
    valid_links = [link for link in links if not any(b in link for b in config.blacklist)]
    return valid_links

def recursive_browse(url, depth):
    debug_print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    debug_print("การเรียกเว็บเรื่องราว [{}] ~~~ [ความลึก = {}]".format(url, depth))

    if not depth:
        do_request(url)
        return
    else:
        page = do_request(url)
        if not page:
            debug_print("หยุดและเพิกเฉย: ข้อผิดพลาดของหน้าเว็บ".format(url), Colors.YELLOW)
            config.blacklist.append(url)
            return

        debug_print("สกัดข้อมูลลิงก์จากหน้าเว็บ".format(url))
        valid_links = get_links(page)
        debug_print("พบลิงก์ที่ถูกต้อง {} รายการ".format(len(valid_links)))

        if not valid_links:
            debug_print("หยุดและเพิกเฉย: ไม่มีลิงก์".format(url), Colors.YELLOW)
            config.blacklist.append(url)
            return

        sleep_time = random.randrange(config.MIN_WAIT, config.MAX_WAIT)
        debug_print("หยุดประมวลผลเป็นเวลา {} วินาที...".format(sleep_time))
        time.sleep(sleep_time)

        next_url = random.choice(valid_links)
        debug_print("คลิกที่ลิงก์: {}".format(next_url))
        recursive_browse(next_url, depth - 1)

if __name__ == "__main__":
    data_meter = 0
    good_requests = 0
    bad_requests = 0

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("เริ่มต้นเครื่องเมื่อร้องขอทราฟฟิค")
    print("https://github.com/ecapuano/web-traffic-generator")
    print("เรียกเว็บรากตามความลึกระหว่าง 3 ถึง {} รายการ,".format(config.MAX_DEPTH))
    print("รอเวลาระหว่าง {} ถึง {} วินาที ระหว่างการร้องขอ".format(config.MIN_WAIT, config.MAX_WAIT))
    print("สคริปต์นี้จะเรียกใช้งานไปเรื่อยๆ ใช้ Ctrl+C เพื่อหยุด")

    while True:
        debug_print("เลือกเว็บรากอย่างสุ่มจาก {} รายการ".format(len(config.ROOT_URLS)), Colors.PURPLE)

        random_url = random.choice(config.ROOT_URLS)
        depth = random.choice(range(config.MIN_DEPTH, config.MAX_DEPTH))

        recursive_browse(random_url, depth)

        sleep_time = random.randint(2, 5)
        debug_print("หยุดประมวลผลเป็นเวลา {} วินาทีก่อนการทำซ้ำถัดไป".format(sleep_time))
        time.sleep(sleep_time)
