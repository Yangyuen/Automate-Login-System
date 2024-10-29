import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # ใช้เพื่อจัดการ chromedriver อัตโนมัติ
from datetime import datetime

# อ่านข้อมูลจากไฟล์ Excel
excel_path = r'C:\Users\Yungyuen.K\Desktop\Test\job_data_example.xlsx'
data = pd.read_excel(excel_path, sheet_name='Sheet1') #อ่านจาก Sheet Name "Sheet1"

# แปลงคอลัมน์วันที่ให้เป็น datetime object
data['job_date'] = pd.to_datetime(data['job_date'], format='%d/%m/%Y')

# ระบุ path ของ WebDriver และใช้ webdriver_manager ในการจัดการ chromedriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 1. Login เข้าเว็บไซต์
driver.get('https://timesheet.onetoonecontacts.com:8082/oto_timesheet/account/sign_in')

# รอให้หน้าเว็บโหลดและกรอก Username และ Password (ใช้ WebDriverWait)
username = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="sign_in_username"]'))
)
username.send_keys('1006400143') #กรอก Username

# รอให้ฟิลด์ Password ปรากฏ (ลองใช้ XPATH แทน NAME)
password = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="sign_in_password"]'))
)
password.send_keys('P@ssw0rd') #กรอก Password

# ส่งฟอร์ม (กด Enter เพื่อ Login)
password.send_keys(Keys.RETURN)

# รอให้หน้าเว็บโหลด
WebDriverWait(driver, 10).until(
    EC.url_contains('oto_timesheet/time_sheet')
)

# 2. คลิก Link: Timesheet
driver.get('https://timesheet.onetoonecontacts.com:8082/oto_timesheet/time_sheet')

# รอให้หน้าเว็บโหลด
WebDriverWait(driver, 3).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/div/div[2]/a'))
)

# วนลูปสำหรับการกรอกข้อมูลจาก Excel
for index, row in data.iterrows():
    try:
        # 3. คลิกปุ่ม "Create Job"
        create_job_button = driver.find_element(By.XPATH, '//*[@id="container"]/div/div[2]/a')
        create_job_button.click()

        # รอให้ฟอร์มการกรอกข้อมูลปรากฏ
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.NAME, 'job_date'))
        )

        # 4. กรอกข้อมูลตาม Excel
        # 4.1 วันที่ (job_date)
        job_date = driver.find_element(By.NAME, 'job_date')

        # ใช้ JavaScript ในการกำหนดค่าวันที่ให้กับ Datepicker
        date_value = row['job_date'].strftime('%d/%m/%Y')  # แปลงวันที่เป็นรูปแบบที่ต้องการ
        driver.execute_script(f"arguments[0].value = '{date_value}';", job_date)

        # 4.2 ชื่อโครงการ (project)
        project = driver.find_element(By.NAME, 'project')
        project.send_keys(row['project'])

        # 4.3 Activity (activitytype)
        activitytype = driver.find_element(By.NAME, 'activitytype')
        activitytype.send_keys(row['activitytype'])

        # 4.4 Phase (phase)
        phase = driver.find_element(By.NAME, 'phase')
        phase.send_keys(row['phase'])

        # 4.5 Role (role)
        role = driver.find_element(By.NAME, 'role')
        role.send_keys(row['role'])

        # 4.6 Hour (hour)
        hour = driver.find_element(By.NAME, 'hour')
        hour.send_keys(str(row['hour']))

        # 4.7 Minute (minute)
        minute = driver.find_element(By.NAME, 'minute')
        minute.send_keys(str(row['minute']))

        # 4.8 Description (description)
        description = driver.find_element(By.NAME, 'description')
        description.send_keys(row['description'])

        # 5. กดปุ่ม "Save"
        save_button = driver.find_element(By.XPATH, '//*[@id="save"]/span')
        save_button.click()

        # รอให้การบันทึกเสร็จสิ้น
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, '//button[text()="Create Job"]'))
        )

        # แสดงสถานะ Success
        print(f"Row {index + 1}: Success")

    except Exception as e:
        # แสดงสถานะ Error
        print(f"Row {index + 1}: Error - {str(e)}")

# ปิดเบราว์เซอร์เมื่อเสร็จสิ้น
driver.quit()
