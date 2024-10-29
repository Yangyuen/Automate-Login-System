from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # ใช้เพื่อจัดการ chromedriver อัตโนมัติ
import time

# ฟังก์ชันการทดสอบการ Login
def login_test(username_input, password_input, expected_result):
    #driver = webdriver.Chrome(executable_path='path/to/chromedriver')  # ใส่ path ที่ถูกต้อง
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.get("https://timesheet.onetoonecontacts.com:8082/oto_timesheet")  # เปลี่ยน URL ตามจริง
    
    try:
        # ป้อน Username
        username = driver.find_element(By.ID, "sign_in_username")
        username.clear()
        username.send_keys(username_input)
        
        # ป้อน Password
        password = driver.find_element(By.ID, "sign_in_password")
        password.clear()
        password.send_keys(password_input)
        
        # คลิกปุ่ม Login
        login_button = driver.find_element(By.XPATH, '//*[@id="login-page"]/form/fieldset/div/p/input')
        login_button.click()
        
        # รอการโหลดของหน้า
        time.sleep(3)
        
        # ตรวจสอบผลลัพธ์
        if expected_result == "valid":
            # ตรวจสอบว่าล็อกอินสำเร็จ (เช่น Dashboard URL)
            assert "time_sheet" in driver.current_url, "Login Failed"
            print("Login successful with valid credentials.")
        elif expected_result == "invalid":
            # ตรวจสอบข้อความแสดงข้อผิดพลาด
            error_message = driver.find_element(By.ID, "error-message").text
            assert "Invalid username or password" in error_message, "Error message not displayed"
            print("Login failed with invalid credentials as expected.")
        elif expected_result == "empty":
            # ตรวจสอบข้อความเตือนเมื่อช่องข้อมูลว่างเปล่า
            error_message = driver.find_element(By.ID, "error-message").text
            assert "Please enter username and password" in error_message, "Error message not displayed"
            print("Login failed with empty fields as expected.")
    
    except Exception as e:
        print(f"Test failed: {e}")
    
    finally:
        # ปิดเบราว์เซอร์
        driver.quit()

# Test Case 1: Valid Login with Correct Credentials
def test_valid_login():
    print("Test Case 1: Valid Login")
    login_test('1000616541', 'Skyy_20242', 'valid')  # ใส่ข้อมูลที่ถูกต้อง

# Test Case 2: Invalid Login with Incorrect Password
def test_invalid_login():
    print("Test Case 2: Invalid Login")
    login_test('1000616541', 'Skyy12345', 'invalid')  # ใส่ข้อมูลที่ไม่ถูกต้อง

# Test Case 3: Empty Username and Password
def test_empty_login():
    print("Test Case 3: Empty Username and Password")
    login_test('', '', 'empty')  # ทดสอบกรณีช่องข้อมูลว่างเปล่า

# เรียกใช้ฟังก์ชันทดสอบทั้งหมด
if __name__ == "__main__":
    test_valid_login()  # ทดสอบการ Login ด้วยข้อมูลที่ถูกต้อง
    test_invalid_login()  # ทดสอบการ Login ด้วยข้อมูลที่ไม่ถูกต้อง
    test_empty_login()  # ทดสอบการ Login โดยไม่กรอกข้อมูล
