#!/usr/bin/env python

import os
import time
import argparse as ap
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def parse_params():

    p = ap.ArgumentParser()
    p.add_argument('-u', '--username', metavar='[STR]', type=str, required=True, help="your gisaid username")
    p.add_argument('-p', '--password', metavar='[STR]', type=str, required=True, help="your gisaid password")
    p.add_argument('-l', '--accession_id_list', metavar='[STR]', type=str, required=True, help="a file contains accession id")
    p.add_argument('-t', '--timeout', metavar='[INT]', type=int, required=False, default=60, help="progress timeout seconds")
    p.add_argument('--headless', action='store_true', help='turn on headless mode')
    args_parsed = p.parse_args()
    return args_parsed


def logining_epicov(username, password, headless, timeout):

    print("logining epicov...")
    mimeType = "application/octet-stream,application/excel,application/vnd.ms-excel,application/pdf,application/x-pdf"
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", os.getcwd())
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", mimeType)
    profile.set_preference("plugin.disable_full_page_plugin_for_types", mimeType)
    profile.set_preference("pdfjs.disabled", True)

    options = Options()
    if headless:
        options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_profile=profile, options=options)

    driver.implicitly_wait(20)
    wait = WebDriverWait(driver, timeout)

    driver.get('https://www.epicov.org/epi3/frontend')
    waiting_sys_timer(wait)
    
    driver.find_element_by_name('login').send_keys(username)
    driver.find_element_by_name('password').send_keys(password)
    driver.execute_script("return doLogin();")
    waiting_sys_timer(wait)

    driver.find_element_by_xpath("//u[text()='Browse']").click()
    waiting_sys_timer(wait)
    waiting_table_to_get_ready(wait)

    return driver, wait    
 
def download_fasta(driver, wait, accession_id):

    print(f'downloading {accession_id}...')
    input = driver.find_element_by_xpath("//div[@class='sys-form-fi-entry']//input")

    input.send_keys(accession_id)
    waiting_sys_timer(wait)

    tr = driver.find_element_by_xpath("//tbody/tr[@class='yui-dt-rec yui-dt-first yui-dt-last yui-dt-even']")
    ActionChains(driver).double_click(tr).perform()
    waiting_sys_timer(wait, 15)
    
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    iframe = driver.find_element_by_xpath("//iframe")
    driver.switch_to.frame(iframe) 
    
    driver.find_element_by_xpath("/html/body/form/div[5]/div/div[2]/div[2]/div/div[2]/div/button").click()
    waiting_sys_timer(wait, 5)
    driver.find_element_by_xpath("/html/body/form/div[5]/div/div[2]/div[2]/div/div[1]/div/button").click()
    
    driver.switch_to.default_content()
    input.clear()
    waiting_sys_timer(wait, 5)

    return driver, wait

def waiting_sys_timer(wait, sec=1):
    wait.until(EC.invisibility_of_element_located((By.XPATH,  "//div[@id='sys_timer']")))
    time.sleep(sec)

def waiting_table_to_get_ready(wait, sec=1):
    wait.until(EC.invisibility_of_element_located((By.XPATH,  "//tbody[@class='yui-dt-message']")))
    time.sleep(sec)

def checking_download(accession_id, timeout):
    sec = 0
    while sec < timeout:
        if os.path.exists(f'{accession_id}.fasta'):
            print(f'completing {accession_id}')
            return True
        else:
            time.sleep(1)
            sec += 1
    print(f'skipping {accession_id}')

def main():
    argvs = parse_params()
    driver, wait = logining_epicov(argvs.username, argvs.password, argvs.headless, argvs.timeout)
    for line in open(argvs.accession_id_list):
        accession_id = line.rstrip()
        driver, wait = download_fasta(driver, wait, accession_id)
        checking_download(accession_id, argvs.timeout)

if __name__ == "__main__":
    main()
