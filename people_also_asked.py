from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
from joblib import Parallel, delayed

def google(input_keyword):
    PATH = "chromedriver_win32/chromedriver.exe" #  path to chrome driver
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    #options.add_argument('headless')
    driver = webdriver.Chrome(executable_path=PATH, chrome_options=options)
    #driver.set_window_size(1080, 1080) # set window size to 700*1080 pixel
    # CRAWL GOOGLE -------------------------------------------------------------------------------------------------------------------------
    # navigate to Google website and accept cookies
    driver.get("https://google.com/")
    WebDriverWait(driver,10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[src^='https://consent.google.com']")))
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//div[@id='introAgreeButton']"))).click()
    
    # set input and start google search
    eingabe_google = input_keyword
    searchbar = driver.find_element_by_css_selector("[title='Suche']")
    searchbar.send_keys(eingabe_google)
    try:
        searchbar.send_keys(Keys.RETURN)
    except Exception as e:
        pass
    google_results = []
    openup = driver.find_element_by_class_name("ifM9O")
    all_children_by_css = openup.find_elements_by_css_selector("[class='hide-focus-ring cbphWd']")
    for i in all_children_by_css:
        i.click()
        time.sleep(3)
        i.click()        
    all_children_by_css = openup.find_elements_by_css_selector("[class='ygGdYd related-question-pair']")
    for question in all_children_by_css:
        google_results.append(question.text)
    driver.close()
    return google_results

def bing(input_keyword):
    try:
        PATH = "chromedriver_win32/chromedriver.exe" #  path to chrome driver
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        #options.add_argument('headless')
        driver = webdriver.Chrome(executable_path=PATH, chrome_options=options)
        #driver.set_window_size(1080, 1080) # set window size to 700*1080 pixel
        # CRAWL GOOGLE -------------------------------------------------------------------------------------------------------------------------
        # navigate to Google website and accept cookies
        driver.get("https://bing.com/")    
        # set input and start google search
        eingabe_google = input_keyword
        searchbar = driver.find_element_by_xpath('//*[@id="sb_form_q"]')
        searchbar.send_keys(eingabe_google)
        try:
            searchbar.send_keys(Keys.RETURN)
        except Exception as e:
            pass
        bing_results = []
        openup = driver.find_element_by_class_name("b_vPanel")
        all_children_by_css = openup.find_elements_by_css_selector("#relatedQnAListDisplay")
        for question in all_children_by_css:
            bing_results.append(question.text)
        bing_results = bing_results[0].split("\n")
        driver.close()
        return bing_results
    except:
        driver.close()
        return []
        
def crawl(keyword):
    bing_results = bing(keyword)
    google_results = google(keyword)
    print("\n")
    print("\n")
    print("Google results")
    print("------------------")
    print("\n")
    for question in google_results:
        print(question)
    print("\n")
    print("Bing results")
    print("------------------")
    print("\n")
    for question in bing_results:
        print(question)
    print("\n")

keyword = input("keyword? \n")
crawl(keyword)