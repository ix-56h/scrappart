#!/usr/bin/env python3
import sys
import platform
import os
import time
import requests
import urllib.parse
import warnings
import traceback
import configparser
import base64
import smtplib
from datetime import datetime, date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup

warnings.filterwarnings('ignore')

LBC_URL         = ''
SELOGER_URL     = '' 
PAP_URL         = ''
VILLES          = ''
mail_content    = ''

# Get configuration files (urls, phone number...)
def get_config():
    global LBC_URL
    global PAP_URL
    global SELOGER_URL
    global VILLES
    global sender_address 
    global sender_pass
    global receiver
    global receiver2
    global end_date

    config = configparser.ConfigParser()
    config.read('config.txt')

    PAP_URL = base64.b64decode(config['URLS']['pap'])
    LBC_URL = base64.b64decode(config['URLS']['lbc'])
    SELOGER_URL = base64.b64decode(config['URLS']['seloger'])
    VILLES  = config['REGIONS']['villes']

    #The mail addresses and password
    receiver = config['GMAIL']['receiver']
    receiver2 = config['GMAIL']['receiver2']
    sender_address = config['GMAIL']['email']
    sender_pass = config['GMAIL']['pass']
    
    end_date = config['GLOBAL']['end_date']
    return


# Scrap functions

def scrap_lbc():
    global mail_content
    header = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
            "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language" : "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding" : "gzip, deflate, br",
            "Connection" : "keep-alive",
            "Host" : "www.leboncoin.fr",
            "Sec-GPC" : "1",
            "TE" : "Trailers",
            "Upgrade-Insecure-Requests" : "1"
            }
    r = requests.get(LBC_URL, headers=header)
    print(r.text)
    dom = BeautifulSoup(r.text, "html.parser")
    lists = dom.find_all("div", "styles_classified__aKs-b")
    for elem in lists:
        if not elem.find('a', "AdCard__AdCardLink-sc-1h74x40-0", href=True):
            continue
        try:
            url = elem.find('a', "AdCard__AdCardLink-sc-1h74x40-0", href=True)['href']
            url = "https://www.leboncoin.fr" + url 
            if check_if_data_exist(url) is True:
                continue
            name = elem.find("p", "AdCardTitle-e546g7-0").text
            price = elem.find("span", "AdCardPrice__Wrapper-bz31y2-0").text
            rows = elem.findAll("p", "TextContent__TextContentWrapper-sc-1lw081p-0")
            #tags = rows[0].text
            tags = ''
            localite = rows[0].text
            date = rows[1].text
            write_data(url)
            mail_content += name + " | " + tags + " | " + localite + " | " + price + " | le " + date + "\n" + url + '\n-----------------------------------------------------\n'
            print(name + " | " + tags + " | " + localite + " | " + price + " | le " + date + "\n" + url + '\n-----------------------------------------------------\n')
        except:
            print(traceback.format_exc())
            pass
    return

def scrap_seloger():
    global mail_content
    header = {
            "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0",
            "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language" : "en-US,en;q=0.5",
            "Accept-Encoding" : "gzip, deflate, br",
            "Connection" : "keep-alive",
            "Pragma" : "no-cache",
            "Cache-Control" : "no-cache",
            "Upgrade-Insecure-Requests" : "1"
            }

    r = requests.get(SELOGER_URL, headers=header)
    dom = BeautifulSoup(r.text, "html.parser")
    lists = dom.find_all("div", "Card__ContentZone-sc-7insep-5")
 
    for elem in lists:
        try:
            url = elem.find('a', "CoveringLink-a3s3kt-0", href=True)['href']
            if check_if_data_exist(url) is True:
                continue
            name = elem.find("ul", "ContentZone__Tags-wghbmy-6").text
            price = elem.find("div", "Price__PriceContainer-sc-1g9fitq-0").text
            tags = elem.find("div", "ContentZone__Title-wghbmy-5").text
            localite = elem.find("div", "ContentZone__Address-wghbmy-1").text
            date = "??"
            write_data(url)
            mail_content += name + " | " + tags + " | " + localite + " | " + price + " | le " + date + "\n" + url + '\n-----------------------------------------------------\n'
        except:
            print(traceback.format_exc())
            pass
    return

def scrap_pap():
    global mail_content
    localisations = VILLES.split(', ')
    header = {
            "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0",
            "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language" : "en-US,en;q=0.5",
            "Accept-Encoding" : "gzip, deflate, br",
            "Connection" : "keep-alive",
            "Cache-Control" : "max-age=0",
            "Upgrade-Insecure-Requests" : "1"
            }
    r = requests.get(PAP_URL, headers=header)
    dom = BeautifulSoup(r.text, "html.parser")
    lists = dom.find_all("div", "search-list-item-alt")
 
    for elem in lists:
        try:
            localite = elem.find("a", "item-title").find("span").text
            res = any(ele in localite for ele in localisations)
            if res is False:
                continue
            url = "https://www.pap.fr" + elem.find('a', "item-title", href=True)['href']
            if check_if_data_exist(url) is True:
                continue
            name = elem.find("ul", "item-tags").text.replace("\n", ' ')
            tags = elem.find("p", "item-description").text.strip()
            price = elem.find("span", "item-price").text
            date = "??"
            write_data(url)
            mail_content += name + " | " + tags + " | " + localite + " | " + price + " | le " + date + "\n" + url + '\n-----------------------------------------------------\n'
            print(name + " | " + tags + " | " + localite + " | " + price + " | le " + date + "\n" + url + '\n-----------------------------------------------------\n')
        except:
            print(traceback.format_exc())
            pass;
    return

# Notify me by EMAIL 
def notify_mail(receiver_address):
    global mail_content
    global sender_address 
    global sender_pass
    return
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = '[Python][Appartement] Nouveaux appartements disponibles !'   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    return

# Just check if the current url is present in "appartements.txt"
def check_if_data_exist(url):
    f = open("datas.txt", 'r')
    datas = f.readlines()
    f.close()
    for line in datas:
        if url in line:
            return True
    return False

# Writes datas functions into "appartements.txt"
def write_data(url):
    return
    f = open("datas.txt", 'a')
    f.write(url+'\n')
    f.close()
    return

# Get all datas, using Scrap Functions
def refresh_datas():
    global mail_content
    global receiver
    global receiver2
    
    mail_content = ''
    #scrap datas
    get_config()
    scrap_lbc()
    scrap_seloger()
    scrap_pap()

    if mail_content != '':
        notify_mail(receiver)
        if receiver2 != '':
            notify_mail(receiver2)
        print('Mail sent !')

today = date.today()
get_config()
while today != end_date:
    refresh_datas()
    print('[%s] Updated' % datetime.now().strftime("%H:%M:%S"))
    time.sleep(60 * 30)
    today = date.today()
