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


def sepSearch(full_name,browser):
    nombres = browser.find_element_by_xpath("//*[@id=\"nombre\"]")
    paterno = browser.find_element_by_xpath("//*[@id=\"paterno\"]")
    materno = browser.find_element_by_xpath("//*[@id=\"materno\"]")
    nombres.send_keys(full_name[0])
    paterno.send_keys(full_name[1])
    materno.send_keys(full_name[2])
    login_attempt = browser.find_element_by_xpath("//*[@id=\"dijit_form_Button_0_label\"]")
    login_attempt.click()
    #    time.sleep(4)			


def results(browser):
    time.sleep(1)
    busqueda = browser.find_element_by_xpath('//*[@id=\"mainContainer_tablist_tab1\"]/span[1]')
    logging.debug('busqueda')
    busqueda.click()
    time.sleep(1)
    resultados = browser.find_element_by_xpath('//*[@id=\"mainContainer_tablist_tab2\"]/span[1]')
    resultados.click()
    logging.debug('results done')

def readTable(full_name,browser):
    time.sleep(1)
    for x in range(1,10):
        this_xpath = '//*[@id=\"dojox_grid__View_1\"]/div/div/div/div[' + str(x) + ']/table/tbody/tr/td[2]'
        result = browser.find_element_by_xpath(this_xpath)
        logging.warning('I am looking for {}, I founded {}'.format(full_name[0].upper(), result.text.upper()))
        time.sleep(0.5)

        if result.text.upper() == full_name[0].upper():
            time.sleep(1)
            result.click()
            data = getCareer()
            break
        else:
            data = {}
            pass
    if len(data) > 1 :
        return data
    else:
        return 0
    
def getCareer():
    cedula = browser.find_element_by_xpath('//*[@id=\"detalleCedula\"]')
    nombre = browser.find_element_by_xpath('//*[@id=\"detalleNombre\"]')
    genero  = browser.find_element_by_xpath('//*[@id=\"detalleGenero\"]')
    profesion  = browser.find_element_by_xpath('//*[@id=\"detalleProfesion\"]')
    year  = browser.find_element_by_xpath('//*[@id=\"detalleFecha\"]')
    escuela = browser.find_element_by_xpath('//*[@id=\"detalleInstitucion\"]')
    human_data = {'given_name':name, 'cedula':cedula.text, 'nombre':nombre.text, 'genero':genero.text, 
           'profesion':profesion.text, 'year':year.text, 'escuela': escuela.text}
    return (human_data)



def getAll(name, responses): 
    sepSearch(name, browser)
    results(browser)
    data = readTable(name,browser)
    browser.close()
    return data

    
if __name__ == '__main__':
    names =  [['Viridiana', 'Zurita' , 'Zubieta'],['Luis Francisco', 'Contreras', 'Castillejos']]
    with_college = {}
    for name in names:
        try:
            browser = openBrowser()
            data = getAll(name, with_college)
            with_college[name[0] + name[1] + name[2] ] = data 
            print(with_college)
        except Exception as e:
            logging.warning(e)
            browser.close()
       
