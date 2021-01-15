import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
GITHUB_USERNAME = ""
GITHUB_TOKEN = ""
GITHUB_PASSWORD = ""
cache = {}
driver = webdriver.Firefox()
wait = WebDriverWait(driver, 50)
driver.get("https://stripcode.dev/ranked")
driver.find_element_by_id("login_field").send_keys(GITHUB_USERNAME)
driver.find_element_by_id("password").send_keys(GITHUB_PASSWORD)
driver.find_element_by_name("commit").click()
while True:
	filename = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'h1.my-8'))).text
	repos = [i.split("<")[0] for i in driver.page_source.split('<span class="text-bblack font-medium">')][1:]
	for repo in repos:
		if not repo in cache.keys():
			cache[repo] = requests.get(f'https://api.github.com/repos/{repo}/git/trees/master?recursive=1',auth=(
			GITHUB_USERNAME,
			GITHUB_TOKEN
			)).text
		if filename in cache[repo]:
			for button in driver.find_elements_by_css_selector('.bg-sandy'):
				if repo in button.text:
					button.click()
					break
			break
	driver.find_elements_by_css_selector('.bg-sandy')[0].click()
	driver.get("https://stripcode.dev/ranked")

