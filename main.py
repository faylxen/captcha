# Import the required modules
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import json
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import requests
import os
import whisper
import warnings
warnings.filterwarnings("ignore")

model = whisper.load_model("base")

def transcribe(url):
    with open('.temp', 'wb') as f:
        f.write(requests.get(url).content)
    result = model.transcribe('.temp')
    return result["text"].strip()

def click_checkbox(driver):
    driver.switch_to.default_content()
    time.sleep(3)	
    driver.switch_to.frame(driver.find_element(By.XPATH, ".//iframe[@title='reCAPTCHA']"))
    time.sleep(3)
    driver.find_element(By.ID, "recaptcha-anchor-label").click()
    time.sleep(3)
    driver.switch_to.default_content()

def request_audio_version(driver):
    driver.switch_to.default_content()
    time.sleep(3)
    driver.switch_to.frame(driver.find_element(By.XPATH, ".//iframe[@title='Le test reCAPTCHA expire dans deux minutes']"))
    time.sleep(3)
    driver.find_element(By.ID, "recaptcha-audio-button").click()

def solve_audio_captcha(driver):
    time.sleep(3)
    text = transcribe(driver.find_element(By.ID, "audio-source").get_attribute('src'))
    time.sleep(3)
    driver.find_element(By.ID, "audio-response").send_keys(text)
    time.sleep(3)
    driver.find_element(By.ID, "recaptcha-verify-button").click()

if __name__ == "__main__":
    #driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    options = Options()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service,options = options)	
    driver.get("https://www.google.com/recaptcha/api2/demo")
    time.sleep(3)
    click_checkbox(driver)
    time.sleep(3)
    request_audio_version(driver)
    time.sleep(3)
    solve_audio_captcha(driver)
    time.sleep(10)
