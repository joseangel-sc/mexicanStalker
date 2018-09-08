try:
    import logging
    import colorlog
    import logging.config
    import sys
    if __debug__:
        logging.config.fileConfig('logging.conf')
        logger = colorlog.getLogger('loggingUser')
    else:
        logging.config.fileConfig('service.conf')
        logger = colorlog.getLogger('loggingUser')
    import datetime
    import json
    import http.client, urllib
    import numpy as np
    import os 
    import requests 
    import time
    
    from os import listdir
    from os.path import isfile, join
    from pymongo import MongoClient

    from urllib.request  import urlopen
    from bs4 import BeautifulSoup as bs
    from selenium.webdriver.common.keys import Keys
    from pexpect import pxssh 
    from selenium import webdriver
    from bs4 import BeautifulSoup as bs

except Exception as e:
    logging.warning("Error importing libraries {}".format(e))
    sys.exit()

options = webdriver.ChromeOptions()
options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
options.add_argument('window-size=800x841')
#options.add_argument('--headless')


def openBrowser():
    browser = webdriver.Chrome(chrome_options=options)
    browser.get("https://www.cedulaprofesional.sep.gob.mx/cedula/presidencia/indexAvanzada.action") 
    #time.sleep(1)
    return browser


def sepSearch(full_name):
    browser = openBrowser()
    nombres = browser.find_element_by_xpath("//*[@id=\"nombre\"]")
    paterno = browser.find_element_by_xpath("//*[@id=\"paterno\"]")
    materno = browser.find_element_by_xpath("//*[@id=\"materno\"]")
    nombres.send_keys(full_name[0])
    paterno.send_keys(full_name[1])
    materno.send_keys(full_name[2])
    login_attempt = browser.find_element_by_xpath("//*[@id=\"dijit_form_Button_0_label\"]")
    login_attempt.click()
    #    time.sleep(4)
    return browser				

def results(browser):
    busqueda = browser.find_element_by_xpath('//*[@id=\"mainContainer_tablist_tab1\"]/span[1]')
    busqueda.click()
    time.sleep(1)
    resultados = browser.find_element_by_xpath('//*[@id=\"mainContainer_tablist_tab2\"]/span[1]')
    resultados.click()

def readTable(browser):
    first_result = browser.find_element_by_xpath('//*[@id=\"dojox_grid__View_1\"]/div/div/div/div[1]/table/tbody/tr/td[2]')
    logging.debug('about to click in the table')
    first_result.click()
    first_result = browser.find_element_by_class_name('dojoxGridCell')
    first_result.click
    
'''
def browseToDashboard(mail):
	browser = loginToNgrok(mail)
	browser.get("https://dashboard.ngrok.com/status")
	my_port = browser.page_source
	try:
		start = my_port.index('0.tcp.ngrok.io')
		thePort = my_port[start + 15:start + 20]
	except:
		thePort = '00000'
	finally:
n		browser.close()
	return thePort


def loopToNgrok():
'''



if __name__ == '__main__':
    name = ['Jose Angel', 'Sanchez', 'Castillejos']
#    name = ['Christiano', 'Vallim', ' Oliviera']
    browser = sepSearch(name)
    time.sleep(2)
    results(browser)
    readTable(browser)
 
 
