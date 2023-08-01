from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException

import time
import pandas as pd
import numpy as np
import pprint

def wait():
    time.sleep(3)

def long_wait():
    time.sleep(5)

# Set up chromedriver
def setup():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')

  # STILL BUGGY, does not stop handshake error. just ignore the error, it still runs
  chrome_options.add_argument('--ignore-certificate-errors')
  chrome_options.add_argument('--ignore-ssl-errors')

  prefs = {"download.default_directory": ""}
  chrome_options.add_experimental_option("prefs", prefs)
  driver = webdriver.Chrome(options=chrome_options)
  driver.get("https://www.timeshighereducation.com/world-university-rankings/2023/subject-ranking/computer-science#!/length/-1/sort_by/rank/sort_order/asc/cols/stats")
  driver.maximize_window()
  long_wait()
  return driver

# Click on "Scores" button
def table_click_scores(driver):
  scores = driver.find_elements(By.XPATH, "//label[contains(@for, 'scores')]")
  scores[0].click()
  wait()

# Launch chromedriver
driver = setup()

# Show scores menu
table_click_scores(driver)

# table_data = driver.find_element(By.CLASS_NAME, "pane-content")

# find_element by XPATH is the recommended way as it is less buggy
# table_data = driver.find_element(By.XPATH, "//div[contains(@class, pane-content)]")

# WTF!! extract function not even needed
def extract(df, driver):
  table_data = driver.find_element(By.XPATH, "//div[contains(@class, 'pane-content')]")
  table_rows = table_data.find_elements(By.XPATH, "//tr[contains(@role, 'row')]")
  for i in range(2, len(table_rows) - 1, 2):
    row = table_rows[i]
    data = row.find_element(By.XPATH, "/")
    for d in data:
      print(d.text)

######################################
# setting up dataframe of results #
######################################
df_columns = ["Rank", "Name", "Country", "Overall", "Citations", "Industry Income", "International Outlook", "Research", "Teaching"]
df = pd.DataFrame(columns=df_columns)
######################################
# running webscrape #
######################################

time.sleep(20)

# Scraping Rank, University Name & Country
df_rank = driver.find_elements(By.XPATH, "//td[contains(@class, 'rank sorting_1 sorting_2')]")
rank_data = list()
for i in range(len(df_rank)):
    rank_data.append(df_rank[i].text)

# returns 27 Russian Unis
# df_name = driver.find_elements(By.XPATH, "//div[contains(@class, 'ranking-institution-title')]")

# returns the remaining 947 Unis
# df_name = driver.find_elements(By.XPATH, "//a[contains(@class, 'ranking-institution-title')]")

df_name = driver.find_elements(By.XPATH, "//*[contains(@class, 'ranking-institution-title')]")
name_data = list()
for i in range(len(df_name)):
    name_data.append(df_name[i].text)

df_country = driver.find_elements(By.XPATH, "//div/span")
country_data = list()
for i in range(len(df_country)):
    country_data.append(df_country[i].text)

# Scraping all the Scores
df_overall = driver.find_elements(By.XPATH, "//td[contains(@class, 'scores overall-score')]")
overall_data = list()
for i in range(len(df_overall)):
    overall_data.append(df_overall[i].text)

df_citations = driver.find_elements(By.XPATH, "//td[contains(@class, 'scores citations-score')]")
citations_data = list()
for i in range(len(df_citations)):
    citations_data.append(df_citations[i].text)

df_industry_income = driver.find_elements(By.XPATH, "//td[contains(@class, 'scores industry_income-score')]")
industry_income_data = list()
for i in range(len(df_industry_income)):
    industry_income_data.append(df_industry_income[i].text)

df_international_outlook = driver.find_elements(By.XPATH, "//td[contains(@class, 'scores international_outlook-score')]")
international_outlook_data = list()
for i in range(len(df_international_outlook)):
    international_outlook_data.append(df_international_outlook[i].text)

df_research = driver.find_elements(By.XPATH, "//td[contains(@class, 'scores research-score')]")
research_data = list()
for i in range(len(df_research)):
    research_data.append(df_research[i].text)

df_teaching = driver.find_elements(By.XPATH, "//td[contains(@class, 'scores teaching-score')]")
teaching_data = list()
for i in range(len(df_teaching)):
    teaching_data.append(df_teaching[i].text)

# Adding data to Dataframe
df["Rank"] = rank_data
df["Name"] = name_data
df["Country"] = country_data
df["Overall"] = overall_data
df["Citations"] = citations_data
df["Industry Income"] = industry_income_data
df["International Outlook"] = international_outlook_data
df["Research"] = research_data
df["Teaching"] = teaching_data

print(df)

# Exporting Dataframe as excel sheet
df.to_excel('THE_scrape.xlsx')