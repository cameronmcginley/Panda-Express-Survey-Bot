from asyncio.windows_events import NULL
from cgi import test
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re
from selenium.common.exceptions import NoSuchElementException  
import time
from selenium.webdriver.support.ui import Select

def clickNext(driver):
    wait = WebDriverWait(driver, 10)

    # Click next button
    nextButton = wait.until(EC.element_to_be_clickable((By.ID, 'NextButton')))
    nextButton.click()

# Code input page
def pageOne(driver, surveyCode):
    wait = WebDriverWait(driver, 10)
    codeInputBoxes = ["CN1", "CN2", "CN3", "CN4", "CN5", "CN6"]

    for i in range(len(codeInputBoxes)):
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, codeInputBoxes[i]))
        )
        element.send_keys(surveyCode[i])

    # Click next button
    nextButton = wait.until(EC.element_to_be_clickable((By.ID, 'NextButton')))
    nextButton.click()

    # Check for error
    # Error will occur on code entry asking to fill box, can spam click
    # button to get out of it
    # try:
    #     errorMessage = WebDriverWait(driver, 1).until(
    #         EC.presence_of_element_located((By.NAME, "ErrorMessageOnTopOfThePage"))
    #     )

    #     while errorMessage:
    #         print("Hh")
    #         # Have to refresh nextButton each time
    #         nextButton = wait.until(EC.element_to_be_clickable((By.ID, 'NextButton')))
    #         nextButton.click()
            
    #         if len(driver.find_elements(By.NAME, "ErrorMessageOnTopOfThePage"))>0:
    #             errorMessage = driver.find_element(By.NAME, "ErrorMessageOnTopOfThePage")
    #         else:
    #             errorMessage = NULL

    #         # if (driver.find_element(By.NAME, "ErrorMessageOnTopOfThePage")):
    #         #     errorMessage = driver.find_element(By.NAME, "ErrorMessageOnTopOfThePage")
    #         # else:
    #         #     errorMessage = NULL
    #         #     print("yo")
    # finally:
    #     print("No error")
    
def pageFill(driver):
    wait = WebDriverWait(driver, 0)

    try:
        elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[class="Opt5 inputtyperbloption"]')))

        for element in elements:
            element.click()

        return
    except:
        pass

    # For the 4 option one
    try:
        elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[class="Opt4 inputtyperbloption"]')))

        for element in elements:
            element.click()

        return
    except:
        pass

    # For yes/no
    try:
        elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[class="Opt2 inputtyperbloption"]')))

        for element in elements:
            element.click()

        return
    except:
        pass

    try:
        elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'textarea')))

        # Can just double click past, send an extra next
        clickNext()

        return
    except:
        pass

    # Dropdown
    try:
        elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'select')))

        for element in elements:
            select = Select(element)
            select.select_by_index(1)

        return
    except:
        pass
    


    # try:
    #     # Can't click the actual radio button, but can click it's parent
    #     # elements = driver.find_elements_by_css_selector('[class="Opt5 inputtyperbloption"]')
    #     elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[class="Opt5 inputtyperbloption"]')))
    #     print(elements)

    #     for element in elements:
    #         element.click()

    # # If no elements found, it's a yes/no page
    # except:
    #     print("Yes/no")
    #     # element = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[class="Opt2 inputtyperbloption"]')))
    #     element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[class="Opt2 inputtyperbloption"]')))
    #     element.click()


# 2422238726500192041306
def runSurvey(driver, surveyCode):
    wait = WebDriverWait(driver, 10)

    # Load page
    driver.get("https://www.pandaguestexperience.com/")

    pageOne(driver, surveyCode)

    for i in range(20):
        pageFill(driver)
        clickNext(driver)
    
    # time.sleep(30)

# Returns list of code split into pieces defined by webpage code input
# ["1234", "1234", "1234", "1234", "1234", "12"]
# 1234123412341234123412
# 2422238726500193041306
def getCode():
    # Can input with or without dashes, or with spaces
    surveyCode = input("Enter the 22 digit code: ")
    # surveyCode = "2422 2387 2650 0193 0413 06"

    surveyCode = re.sub("[^0-9]", "", surveyCode)

    if len(surveyCode) != 22:
        print("Code error")
        return NULL

    # Split every 4th
    return [surveyCode[i : i + 4] for i in range(0, len(surveyCode), 4)]


def main():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    surveyCode = getCode()
    if not surveyCode: return

    runSurvey(driver, surveyCode)

if __name__ == "__main__":
    main()
