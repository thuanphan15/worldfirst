import time
import requests
import random
import os
import undetected_chromedriver as uc
import win32gui
import win32con
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import datetime


# Thư mục chứa ảnh
base_dir = r"C:\Users\eRic Mobile\Desktop\worldfirst\info\1"

# Danh sách file ảnh cố định
file_mapping = {
    "upanh1": "1.jpg",
    "upanh2": "2.jpg",
    "upanh3": "3.jpg"
}

def get_random_line(file_path):
    """Đọc ngẫu nhiên một dòng từ file."""
    with open(file_path, 'r', encoding="utf-8") as file:
        lines = file.readlines()
    return random.choice(lines).strip()

def add_random_symbol_to_password_v2():
    """Tạo password bằng công thức: Firstname + Lastname + 2 symbol."""
    special_characters = "!#@?;=~"
    num = "1234567890"
    random_num = random.choice(num)
    firstname = get_random_line("Firstname.txt")
    lastname = get_random_line("Lastname.txt")
    random_symbol = random.choice(special_characters)
    return firstname + lastname + random_num + random_symbol
    
def get_data_from_txt(file_path):
    with open(file_path, 'r') as file:
        data = file.readlines()
    email, password, oauth, client_id = data[0].strip().split('|')
    return email, password, oauth, client_id
    
def get_all_accounts(file_path):
    """Đọc danh sách tất cả tài khoản từ file."""
    with open(file_path, "r") as file:
        lines = file.readlines()
    accounts = [line.strip().split('|') for line in lines if line.strip()]
    return accounts


def get_random_user_agent(file_path):
    """Lấy user-agent ngẫu nhiên từ file user.txt."""
    with open(file_path, 'r') as file:
        user_agents = file.readlines()
    return random.choice(user_agents).strip()
class ProxyManager:
    def __init__(self, api_key):
        self.api_key = api_key
        self.proxy = None
        self.timeout = 0
        self.last_update = 0
        self.next_change = 0

    def get_new_proxy(self):
        url = f"http://proxy.shoplike.vn/Api/getNewProxy?access_token={self.api_key}"
        response = requests.get(url)
        print("API New Proxy Response:", response.text)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                self.proxy = data["data"]["proxy"]
                self.timeout = 1800
                self.last_update = time.time()
                self.next_change = data["data"]["nextChange"]
                print(f"Lấy proxy mới: {self.proxy}, timeout: {self.timeout}s, nextChange: {self.next_change}s")
                return self.proxy
            elif data.get("status") == "error":
                print(f"Proxy còn {self.next_change} giây trước khi lấy proxy mới")
                return self.proxy
        else:
            raise Exception(f"Không thể kết nối tới API! Mã lỗi: {response.status_code}")

    def get_current_proxy(self):
        if self.proxy and (time.time() - self.last_update) < self.timeout:
            print(f"Sử dụng proxy hiện tại: {self.proxy}")
            return self.proxy
        else:
            print("Proxy hết hạn hoặc gần hết hạn, lấy proxy mới...")
            return self.get_new_proxy()
    

#class ProxyManager:
#    def __init__(self, api_key):
#        self.api_key = api_key
#        self.proxy = None
#        self.timeout = 0
#        self.last_update = 0
#        self.next_change = 0
#
#    def get_new_proxy(self):
#        url = f"http://proxy.shoplike.vn/Api/getNewProxy?access_token={self.api_key}"
#        response = requests.get(url)
#        print("API New Proxy Response:", response.text)
#        if response.status_code == 200:
#            data = response.json()
#            if data.get("status") == "success":
#                self.proxy = data["data"]["proxy"]
#                self.timeout = 1800
#                self.last_update = time.time()
#                self.next_change = data["data"]["nextChange"]
#                print(f"Lấy proxy mới: {self.proxy}, timeout: {self.timeout}s, nextChange: {self.next_change}s")
#                return self.proxy
#            elif data.get("status") == "error":
#                print(f"Proxy còn {self.next_change} giây trước khi lấy proxy mới")
#                return self.proxy
#        else:
#            raise Exception(f"Không thể kết nối tới API! Mã lỗi: {response.status_code}")
#    def get_current_proxy(self):
#        if self.proxy:
#            if (time.time() - self.last_update) < self.timeout and self.next_change > 300:
#                print(f"Sử dụng proxy hiện tại: {self.proxy}")
#                return self.proxy
#            else:
#                print("Proxy hết hạn hoặc gần hết hạn, lấy proxy mới...")
#                return self.get_new_proxy()
#        else:
#            print("Chưa có proxy, lấy proxy mới...")
#            return self.get_new_proxy()
            
# Hàm để lưu dữ liệu vào tệp txt
def save_to_txt(email, password, modified_password, oauth, client_id): #phone_number
    # Lấy thời gian hiện tại theo định dạng "14h35p-23/11/24"
    current_time = datetime.datetime.now().strftime("%Hh%Mp-%d/%m/%y")
    
    # Ghi dữ liệu vào file cùng với ngày giờ
    with open("output.txt", "a") as file:
        file.write(f"{email}|{password}|{modified_password}|{current_time}\n")
        
def add_random_symbol_to_password(password):
    special_characters = "!#@?;=~"
    num = "1234567890"
    random_num = random.choice(num)
    random_symbol = random.choice(special_characters)
    return password + random_symbol + random_num

def get_phone_number_from_api():
    url = "https://api.viotp.com/request/getv2"
    network_options = ["VIETNAMOBILE","VIETTEL","MOBIPHONE","VINAPHONE"] #"VIETNAMOBILE", 
    selected_network = random.choice(network_options)

    params = {
        "token": "886a20403629471b8411f65594cd03c9",
        "serviceId": "1264",
        "network": selected_network
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data.get("status_code") == 200 and data.get("success"):
            return data["data"].get("phone_number"), data["data"].get("request_id")
        else:
            print("Lỗi khi lấy số điện thoại:", data.get("message"))
            return None, None
    else:
        print("Lỗi khi gửi yêu cầu API:", response.status_code)
        return None, None

# Hàm gửi yêu cầu API để lấy mã OTP
def get_otp_from_api(request_id):
    url = "https://api.viotp.com/session/getv2"
    params = {
        "token": "886a20403629471b8411f65594cd03c9", ##  9fe387d367ae4eddaf6e5dd69a01f911
        "requestId": request_id
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data.get("status_code") == 200 and data.get("success"):
            return data["data"].get("Code")
        else:
            print("Lỗi khi lấy mã OTP:", data.get("message"))
            return None
    else:
        print("Lỗi khi gửi yêu cầu API lấy OTP:", response.status_code)
        return None

def log_account_status(email, status, reason=None):
    """Ghi trạng thái xử lý tài khoản vào file log."""
    with open("log.txt", "a") as log_file:
        log_file.write(f"{email}|{status}|{reason if reason else 'OK'}\n")
        
def wait_until_next_proxy(min_duration=30):
    """Chờ đợi ít nhất min_duration giây (1 phút 40 giây) giữa các tài khoản."""
    start_time = time.time()

    # Xử lý tài khoản (đoạn code xử lý từng tài khoản nằm ở đây)

    elapsed_time = time.time() - start_time
    remaining_time = min_duration - elapsed_time

    if remaining_time > 0:
        print(f"Chờ {int(remaining_time)} giây trước khi tiếp tục tài khoản tiếp theo...")
        time.sleep(remaining_time)

def type_like_human(element, text, min_delay=0.05, max_delay=1):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(min_delay, max_delay))

def get_verification_code_from_api(email, oauth, client_id):
    url = "https://tools.dongvanfb.net/api/get_messages_oauth2"
    data = {
        "email": email,  # Dùng email truyền vào thay vì hardcode
        "refresh_token": oauth,  # Sử dụng oauth từ tham số
        "client_id": client_id  # Sử dụng client_id từ tham số
    }
    response = requests.post(url, json=data)
    response.encoding = 'utf-8'  # Đảm bảo phản hồi được xử lý dưới định dạng UTF-8    
    if response.status_code == 200:
        response_data = response.json()
        if "messages" in response_data:
            messages = response_data["messages"]
            if isinstance(messages, list):
                messages = " ".join(str(msg) for msg in messages)  # Nếu messages là list, nối thành chuỗi
            # Sử dụng split để trích xuất mã xác minh
            if "Mã xác minh: " in messages and "bạn đang thực hiện đăng ký" in messages:
                start_index = messages.split("Mã xác minh: ")[1]
                code = start_index.split(", bạn đang thực hiện đăng ký")[0]
                return code
            else:
                print("Không tìm thấy mã xác minh trong email.")
        else:
            print("No 'messages' field found in response.")
    else:
        print(f"Failed to get messages. Status code: {response.status_code}")
    return None
    
# Tạo cấu hình Chrome với proxy và user-agent
def create_chrome_driver(proxy=None, user_agent=None):
    options = uc.ChromeOptions()
    if proxy:
        options.add_argument(f"--proxy-server={proxy}")
    if user_agent:
        options.add_argument(f"user-agent={user_agent}")
        
    options.add_argument("--disable-features=WebRTC-HW-Decoding,WebRTC-HW-Encoding,WebRTC-Screen-Capturing,WebRTC-Audio-Processing")
    options.add_argument("--disable-webrtc-apm-in-audio-service")
    options.add_argument("--disable-webrtc-dtls-cipher-suites-blacklist")
    options.add_argument("--disable-gpu")  # Tùy chọn để tránh một số lỗi liên quan đến GPU
    # Tắt các chế độ chống tự động hóa
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = uc.Chrome(options=options, force_replace=True)
    return driver


# Cấu hình và khởi chạy
api_key = "cb6c39b5f35a811fa3cc5a5842fa3bdc"    #d36c2ac38fe64341dc1ff066cd9b55d6
proxy_manager = ProxyManager(api_key)
accounts = get_all_accounts("data.txt")
index = 0

while index < len(accounts):
    account = accounts[index]
    email, password, oauth, client_id = account
    print(f"Đang xử lý tài khoản: {email}")

    try:
            # Tách logic xử lý từng tài khoản vào đây (dùng mã gốc của bạn)
        proxy = proxy_manager.get_new_proxy()
        user_agent = get_random_user_agent("user.txt")

        # Khởi tạo trình duyệt
        browser = create_chrome_driver(proxy=proxy, user_agent=user_agent)
        browser.get("https://portal.worldfirst.com/register?region=VN&lang=vi-VN")
        print("Trình duyệt được mở với proxy:", proxy, "và user-agent:", user_agent)
        # Thiết lập kích thước và vị trí cửa sổ
        width = 1024
        height = 1024
        browser.set_window_size(width, height)
        
        # Đặt cửa sổ ở góc trên bên phải
        screen_width = browser.execute_script("return window.screen.availWidth;")
        x_position = 0  # Góc trái
        y_position = 0  # Góc trên
        browser.set_window_position(x_position, y_position)


            # Click vào button Tiếp tục
        wait = WebDriverWait(browser, 50)

        continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/div/div/div/div[3]/div[4]/div/button")))
        continue_button.click()
        print("Đã click vào button Tiếp tục")
    
            # Lấy dữ liệu từ file txt
        email, password, oauth, client_id = get_data_from_txt("data.txt")
        
        # Nhập email vào trường input
        email_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='email']")))
        type_like_human(email_element, email)
        time.sleep(5)
            # Click vào button gửi mã OTP
        otp_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/div/div/div/div[3]/form/div[2]/div[2]/div/div/div/div/button")))
        otp_button.click()
    
            # Đợi giải captcha bằng tay
        input("Giải captcha bằng tay...")
        
        last_otp_time = None  # Biến lưu thời gian nhận OTP gần nhất
        
        while True:
                # Nhận mã OTP từ API
            verification_code = get_verification_code_from_api(email, oauth, client_id)
                
            if verification_code:
                    # Kiểm tra nếu mã OTP là mới
                current_time = time.time()
                    
                if last_otp_time is None or current_time - last_otp_time > 60:  # 60 giây giữa các lần nhận OTP
                    print(f"Nhận được OTP mới: {verification_code}")
                    otp_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='emailOtpCode']")))
                    type_like_human(otp_element, verification_code)
                    last_otp_time = current_time  # Cập nhật thời gian nhận OTP mới
                    time.sleep(5)
                    break
                else:
                    print("Mã OTP chưa thay đổi, thử lại sau...")
                    time.sleep(10)  # Chờ 10 giây trước khi thử lại
            else:
                print("Chưa nhận được OTP, thử lại sau...")
                time.sleep(10)  # Chờ 10 giây trước khi thử lại

                # Nhập password_modifiled vào trường password
        password_modified = add_random_symbol_to_password_v2()
        password_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='password']")))
        type_like_human(password_element, password_modified)
        time.sleep(10)
        # Chọn checkbox và click các nút tiếp theo
        checkbox1 = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/div/div/div/div[3]/form/div[9]/div/div/div")))
        checkbox1.click()
        time.sleep(10)
        checkbox2 = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/div/div/div/div[3]/form/div[10]/div/div/div/div/label/span[2]/div/div")))
        checkbox2.click()
        time.sleep(10)
        create_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[3]/form/div[11]/button")))
        browser.execute_script("arguments[0].scrollIntoView(true);", create_button)
#        browser.execute_script("arguments[0].scrollIntoView(true);", create_button)
        time.sleep(10)
        create_button.click()
        save_to_txt(email, password, password_modified, oauth, client_id) #phone_number
        log_account_status(email, "success")
        print(f"Đã xử lý thành công tài khoản: {email}")
        accounts.pop(index)
        time.sleep(10)
           
                # Lấy số điện thoại và request_id
        phone_number, request_id = get_phone_number_from_api()
            
        while True:
            # Gọi hàm để lấy số điện thoại mới từ API
            phone_number, request_id = get_phone_number_from_api()
        
            if phone_number:
                print(f"Số điện thoại được cấp: {phone_number}")
            
                # Nhập số điện thoại vào form
                phone_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@aria-labelledby="PhoneNumber"]')))
                    
                # Xóa nội dung cũ trong ô nhập liệu trước khi nhập số mới
                type_like_human(phone_input, phone_number)
            
                # Nhấn nút gửi mã
                send_code_button = browser.find_element(By.XPATH, '//button[span[text()="Gửi mã"]]')
                send_code_button.click()
                time.sleep(3)
            
                otp_attempts = 0  # Đếm số lần thử lấy OTP
                max_attempts = 15  # Số lần tối đa thử lấy OTP
    
                while otp_attempts < max_attempts:
                    otp_code = get_otp_from_api(request_id)  # Lấy mã OTP từ API
                
                    if otp_code:  # Nếu lấy được mã OTP
                        print(f"Đã lấy được mã OTP: {otp_code}")
                    
                            # Điền mã OTP vào các ô
                        otp_input1 = browser.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div[2]/div[1]/div[3]/div/fieldset/input[1]')
                        type_like_human(otp_input1, otp_code[0])
                        otp_input2 = browser.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div[2]/div[1]/div[3]/div/fieldset/input[2]')
                        type_like_human(otp_input2, otp_code[1])
                        otp_input3 = browser.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div[2]/div[1]/div[3]/div/fieldset/input[3]')
                        type_like_human(otp_input3, otp_code[2])
                        otp_input4 = browser.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div[2]/div[1]/div[3]/div/fieldset/input[4]')
                        type_like_human(otp_input4, otp_code[3])
                        otp_input5 = browser.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div[2]/div[1]/div[3]/div/fieldset/input[5]')
                        type_like_human(otp_input5, otp_code[4])
                        otp_input6 = browser.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div[2]/div[1]/div[3]/div/fieldset/input[6]')
                        type_like_human(otp_input6, otp_code[5])
                    
                            # Nhấn nút "Tiếp tục" sau khi nhập OTP
                        create_button = WebDriverWait(browser, 20).until(
                            EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div[2]/div/div[2]/div[2]/div/button[2]'))
                        )
                        create_button.click()
                        time.sleep(5)
                            
                        # Nếu thành công, thoát khỏi vòng lặp
                        break
                    else:
                        print("Không thể lấy mã OTP, thử lại...")
                        otp_attempts += 1
                        time.sleep(5)  # Đợi trước khi thử lại
                        
                    # Nếu vượt quá số lần thử, hủy số điện thoại và lấy lại số mới
                if otp_attempts >= max_attempts:
                    print("Không thể nhận OTP, hủy số điện thoại và thử lại.")
                        
                    # Click nút hủy
                    cancel_button = browser.find_element(By.XPATH, '//button[span[text()="Trước"]]')
                    cancel_button.click()
                    time.sleep(2)
                    phone_input.click()  # Đảm bảo ô nhập liệu được focus
                    for _ in range(9):  # Gửi phím Backspace 9 lần
                        phone_input.send_keys(Keys.BACKSPACE)
                    time.sleep(2)
                    continue  # Quay lại bước lấy số điện thoại mới
                else:
                    # Thoát khỏi vòng lặp chính nếu nhận OTP thành công
                    break
            else:
                print("Không lấy được số điện thoại, thử lại.")
                time.sleep(60)  # Đợi trước khi thử lại
                  
                # Lưu dữ liệu vào output.txt sau khi tạo tài khoản thành công
                            
                # Sửa phần lưu thông tin:
        
        kehoach = WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div/div/div[2]/div/div/div/div/form/div[1]/div/div/div/div/div/div/div[2]/div/div'))
        )
        kehoach.click()
        khong_input = WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.ID, "rc_select_1")))
        type_like_human(khong_input, "Không")
        khong_input.send_keys(Keys.ENTER)
        time.sleep(3)
        next_button = browser.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/div[2]/div/div/div/div/div/button[1]')
        next_button.click()
        time.sleep(3)
        job = get_random_line('job.txt')
        search_job = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.ID, "rc_select_2"))
        )
        search_job.click()
        type_like_human(search_job, job)
        search_job.send_keys(Keys.DOWN)
        search_job.send_keys(Keys.ENTER)
        time.sleep(3)
        next_button2 = browser.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div/div/div/div/div/button[1]')
        next_button2.click()
        time.sleep(3)
        no_button = WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div[2]/form/div[2]/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div/div/div/div/div[2]/label/span[2]/div'))
        )
        no_button.click()
        next_button3 = WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Tiếp theo']]"))
        )
        # Nhấn vào nút
        next_button3.click()
        time.sleep(5)
        next_button4 = WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div/div/div/div/div/button[1]'))
        )
        next_button4.click()
        time.sleep(30)
        #upload info
        upload_button = WebDriverWait(browser, 600).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Tải lên ảnh selfie']]"))
        )
        upload_button.click()
        time.sleep(10)

        # Tìm kiếm quốc gia
        quocgia = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="rc_select_11"]'))
        )
        type_like_human(quocgia, "Việt Nam")
        quocgia.send_keys(Keys.ENTER)
        time.sleep(5)
        
        # Nhập CCCD
        cccd = browser.find_element(By.XPATH, ''//*[@id="rc_select_12"]')
        type_like_human(cccd, "CCCD") 
        cccd.send_keys(Keys.ENTER)
        time.sleep(1)
        
        # Tìm element "upanh1" để upload ảnh
        upanh1 = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div[2]/form/div[2]/div[2]/div/div/div/div/div[4]/div/div/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div[1]/div/span/div[1]/span/input'))
        ) 
        # Lấy đường dẫn đến file ảnh từ base_dir
        file_path = os.path.join(base_dir, file_mapping["upanh1"])
        
        # Sử dụng send_keys để upload ảnh
        upanh1.send_keys(file_path)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Cuộn đến cuối trang
        upanh2 = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div[2]/form/div[2]/div[2]/div/div/div/div/div[4]/div/div/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div/span/div[1]/span/input'))
        )
        file_path2 = os.path.join(base_dir, file_mapping["upanh2"])
        upanh2.send_keys(file_path2)
        
        # Cuộn trang đến phần tử upanh2
        
        # Chờ tải ảnh 3
        upanh3 = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div[2]/form/div[2]/div[2]/div/div/div/div/div[5]/div/div/div/div/div/div/div/div[2]/div/div/div/div/div/span/div[1]/span/input'))
        )
        file_path3 = os.path.join(base_dir, file_mapping["upanh3"])
        upanh3.send_keys(file_path3)
        time.sleep(3)
        
        gui_button = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div[2]/div/div/div/div/div/button[1]')))
        browser.execute_script("arguments[0].scrollIntoView(true);", gui_button)
        time.sleep(10)
        gui_button.click()
        # Cuộn trang đến phần tử upanh3

        with open("data.txt", "w") as f:
            for acc in accounts:
                f.write("|".join(acc) + "\n")
        time.sleep(10)        
    except Exception as e:
        log_account_status(email, "failed", str(e))
        print(f"Lỗi khi xử lý tài khoản {email}: {e}")
        index += 1  # Tăng chỉ số để tiếp tục tài khoản tiếp theo
    finally:
        time.sleep(10)
        if browser:
            #browser.quit()
            wait_until_next_proxy(min_duration=30)
print("Đã xử lý tất cả tài khoản.")