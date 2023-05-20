import math

from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains

# navigate to Dice login page
chrome_driver = webdriver.Chrome()
chrome_driver.get("https://www.dice.com/apply-with-dice/login?buttonType=easyApply")
chrome_driver.maximize_window()

# Login to Dice
username = chrome_driver.find_element(By.NAME, "email")
username.send_keys("mnt19@pitt.edu")
time.sleep(1)
password = chrome_driver.find_element(By.ID, "password-input")
password.send_keys("pass")
time.sleep(1)
password.send_keys(Keys.ENTER)

# navigate to job search
time.sleep(5)
chrome_driver.get(
    "https://www.dice.com/jobs?countryCode=US&radius=30&radiusUnit=mi&page=1&pageSize=20&language=en&eid=S2Q_,gKQ_")
time.sleep(10)

# search for java and remote filter by easy apply
searchTerm = chrome_driver.find_element(By.XPATH, "//*[@id='typeaheadInput']")
searchTerm.send_keys("java")
searchLocation = chrome_driver.find_element(By.ID, "google-location-search")
searchLocation.send_keys("remote")
searchLocation.send_keys(Keys.ENTER)
time.sleep(10)
easyApplyFilter = chrome_driver.find_element(By.XPATH, "//*[@id='singleCheckbox']/span/button")
easyApplyFilter.click()

# set posted by date to last 3 days (optional)
# postedDate = chrome_driver.find_element(By.XPATH, "//*[@id='facets']/dhi-accordion[2]/div["
#                                                   "2]/div/js-single-select-filter/div/div/button[3]")
# postedDate.click()

jobPostingLinksParent = chrome_driver.find_element(By.XPATH, "//*[@id='searchDisplay-div']/div["
                                                             "3]/dhi-search-cards-widget/div")
jobPostingLinks = jobPostingLinksParent.find_elements(By.TAG_NAME, "a")
time.sleep(5)

numOfJobs = chrome_driver.find_element(By.XPATH, "//*[@id='totalJobCount']").text
numOfPages = math.ceil(int(numOfJobs.replace(",", ""))/20)
pageCount = 0

# iterate through links from job search and apply
while pageCount <= numOfPages:
    count = 0
    for jobPosting in jobPostingLinks:
        jobPostingLinksParent = chrome_driver.find_element(By.XPATH, "//*[@id='searchDisplay-div']/div["
                                                                     "3]/dhi-search-cards-widget/div")
        jobPostingLinks = jobPostingLinksParent.find_elements(By.TAG_NAME, "a")

        actions = ActionChains(chrome_driver)
        actions.move_to_element(jobPostingLinks[count]).perform()
        time.sleep(2)
        if "DO NOT APPLY" in jobPostingLinks[count].text:
            # move to next link for dice test account
            count = count + 1
            continue
        jobPostingLinks[count].click()
        count = count + 1
        time.sleep(5)
        try:
            easyApplyGreatGrandParent = chrome_driver.find_element(By.XPATH, "//*[@id='__next']/div/main/header")
            easyApplyGrandParent = easyApplyGreatGrandParent.find_element(By.XPATH, "//*[@id='__next']/div/main/header"
                                                                                    "/div/div")
            easyApplyParent = easyApplyGrandParent.find_element(By.XPATH, "//*[@id='__next']/div/main/header/div/div/div["
                                                                          "4]/div[2]/div[2]")
            easyApplyButton = easyApplyParent.find_element(By.XPATH, "//*[@id='__next']/div/main/header/div/div/div[4]/div["
                                                                     "2]/div[2]/apply-button-wc")
            easyApplyButton.click()
            time.sleep(5)

            nextButtonGreatGrandParent = chrome_driver.find_element(By.XPATH, "/html/body/div[3]")
            nextButtonGrandParent = nextButtonGreatGrandParent.find_element(By.XPATH, "//*[@id='app']/div/span")
            nextButtonParent = nextButtonGrandParent.find_element(By.XPATH, "//*[@id='app']/div/span/div/main")
            nextButton = nextButtonParent.find_element(By.XPATH, "//*[@id='app']/div/span/div/main/div[4]/button[2]")
            nextButton.click()
            time.sleep(5)

            applyButton = chrome_driver.find_element(By.XPATH, "//*[@id='app']/div/span/div/main/div[3]/button[2]")
            applyButton.click()
            time.sleep(5)

            goToSearch = chrome_driver.find_element(By.XPATH, "/html/body/div[3]/div[4]/div/div["
                                                              "1]/dhi-job-applications-post-apply-ui/section/a")
            goToSearch.click()

            time.sleep(12)
        except:
            chrome_driver.back()
            time.sleep(12)

    # click to next page
    nextPage = chrome_driver.find_element(By.XPATH, "//*[@id='pagination_2']/pagination/ul/li[7]/a")
    nextPage.click()
    time.sleep(10)
    pageCount = pageCount + 1
