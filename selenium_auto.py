# from selenium import webdriver
# import random
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium import webdriver
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.chrome.service import Service
from datetime import datetime, timedelta, date
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import env
from selenium.webdriver.chrome.service import Service as ChromeService


def isValid(radio):
    # return (radio.get_attribute('value').__contains__('~47~') or radio.get_attribute('value').__contains__('~34~') or radio.get_attribute('value').__contains__('~42~') or radio.get_attribute('value').__contains__('~45~') or radio.get_attribute('value').__contains__('~46~'))
    return radio.get_attribute("value").__contains__("Basement")


open(env.logPath + str(date.today()) + ".txt", "w").close()
f = open(env.logPath + str(date.today()) + ".txt", "a")

try:
    # service = Service()
    # options = webdriver.ChromeOptions()
    # driver = webdriver.Chrome(service=service, options=options)
    f.write("trying to install driver" + "\n")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    f.write("navigating to login page" + "\n")
    # time.sleep(10)
    driver.get(env.homePage)

    element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="btn-login"]'))
    WebDriverWait(driver, 100).until(element_present)
    # time.sleep(1)
    userId = driver.find_element(By.XPATH, '//*[@id="login-username"]')
    userId.send_keys(env.userId)
    # time.sleep(3)
    userId = driver.find_element(By.XPATH, '//*[@id="login-password"]')
    userId.send_keys(env.password)
    driver.find_element(By.XPATH, '//*[@id="btn-login"]').click()
    f.write("trying to login" + "\n")
    element_present = EC.presence_of_element_located((By.ID, "header"))
    WebDriverWait(driver, 100).until(element_present)
    # driver.find_element(By.TAG_NAME,'body').send_keys(Keys.CONTROL + 't')

    # driver.find_element(By.XPATH,'//*[@id="container"]/div/div/div/div/div/div/div/div[1]/div[2]/div[1]/div[6]/div/div[2]/div/ul/li[2]/a').click()

    while True:
        f.write("parking page loading" + "\n")
        driver.get(env.parkLink)
        element_present = EC.presence_of_element_located((By.ID, "frmDt"))
        WebDriverWait(driver, 100).until(element_present)
        f.write("Date selection" + "\n")
        dateInp = driver.find_element(By.ID, "frmDt")
        dateInp.click()
        time.sleep(1)
        allDates = driver.find_elements(
            By.XPATH, "/html/body/div[1]/div[1]/div[2]/table/tbody/tr/td"
        )

        while len(allDates) == 0:
            allDates = driver.find_elements(
                By.XPATH, "/html/body/div[1]/div[1]/div[2]/table/tbody/tr/td"
            )
        print(type(date))
        # f.write(type(date))
        today = str(date.today())
        print(today)
        f.write(today + "\n")
        Begindate = datetime.strptime(today, "%Y-%m-%d")
        beginDay = Begindate + timedelta(days=2)
        validDate: bool = (
            False
            if (beginDay.weekday() == "Saturday" or beginDay.weekday() == "Sunday")
            else True
        )
        if not validDate:
            print("Holiday")
            quit()
        # print(beginDay.weekday(),end="\n")
        mapping = [
            "JAN",
            "FEB",
            "MAR",
            "APR",
            "MAY",
            "JUN",
            "JUL",
            "AUG",
            "SEP",
            "OCT",
            "NOV",
            "DEC",
        ]

        # the book name uses 01 or 1 no clue and so the website
        bookName = (
            "book_"
            + str(beginDay.day)
            + "-"
            + str(mapping[int(beginDay.month) - 1])
            + "-"
            + str(beginDay.year)
        )
        # print(bookName)

        beginDay = str(beginDay.day)
        if beginDay[0] == "0":
            beginDay = beginDay[1]
        # print(beginDay)
        notValid = ["weekend off disabled", "off disabled", "weekend available"]

        # tempDriver = driver
        # print(allDates)

        for d in allDates:
            if d.text == beginDay and d.get_attribute("class").find("available") != -1:
                # print(d.text)
                d.click()
                # print(d)
                validDate = True
                break
        if not validDate:
            print("Holiday probably")
            quit()
        f.write("Date found" + "\n")
        driver.find_element(By.ID, "getBookingDtl").click()
        f.write("parking page" + "\n")
        allInputs = []
        f.write("Getting all inputs...." + "\n")
        while len(allInputs) <= 36:
            allInputs = driver.find_elements(By.TAG_NAME, "input")
        # print(allInputs)
        f.write("fetching all open slots" + "\n")
        openSlots = []
        for input in allInputs:
            # radio = input
            if input.is_enabled():
                if isValid(input):
                    openSlots.insert(0, input)
                else:
                    openSlots.append(input)
        print(len(openSlots))
        if len(openSlots) <= 4:
            print("full")
            print("Check if the parking is really full? If not, message Adhyyan.")
            f.write("Check if the parking is really full? If not, message Adhyyan.\n")
            raise Exception("Full")
            # time.sleep(99999)

        # print(len(allInputs))
        # openSlots.pop(0)
        # for i in openSlots:
        #     print(i.get_attribute('value'),end="\n")
        booked: bool = False
        for i in openSlots:
            i.click()
            f.write(str(i.get_attribute("value")) + "\n")
            print(i.get_attribute("value"))
            booked = True
            break

        success = False
        if booked:
            element_present = EC.presence_of_element_located((By.ID, "saveBooking"))
            WebDriverWait(driver, 100).until(element_present)
            driver.find_element(By.ID, "saveBooking").click()
            f.write("Save button clicked" + "\n")
            time.sleep(6)
            a = driver.switch_to.alert
            alert_text: str = a.text
            if alert_text.__contains__("Car Parking Booking done successfully"):
                print("Booked")
                f.write("Booked\n")
                f.close()
                driver.quit()
                success = True
                # time.sleep(999)
                break
            if success:
                break
            a.accept()
            print("again")
            f.write("again\n")
        if success:
            break
        # driver.quit()

except Exception as e:
    print("------Error------", end="\n")
    print(str(e))
    print("Message Adhyyan")
    f.write("------Error------\n")
    f.write(str(e) + "\n")
    f.write("Message Adhyyan\n")
    # time.sleep(99999)
finally:
    f.close()
    # driver.quit()
