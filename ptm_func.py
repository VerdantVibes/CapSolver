# -*- coding: utf-8 -*-
"""
Created on Tue May 24 15:38:51 2022

@author: VerdantVibes
"""
import unidecode
import re

def norm(string):
    decoded = unidecode.unidecode(string) if string else None
    return decoded

def get_addr_info(start_num, the_list, lastname, firstname, lic, gender, b1, extra1, extra2, extra3, extra4, extra5):
    # Function to generate address information
    addr_row = []
    firm, addr1, addr2, city, prov, post = '','','','','',''
    phone, ext, office = '', '', ''
    full_addr, city_prov_post = '', ''
     
    firm = the_list[start_num].text
    if the_list[start_num+1].text:
        firm = firm + '/' + the_list[start_num+1].text
    
    full_addr = the_list[start_num+2].text
    addr1_pattern = r"^(.*?),"
    addr2_pattern = r",\s*(.*?),"
    city_prov_pattern = r",\s*([^,]+)\s+([A-Z]{2})"
    post_pattern = r"([A-Z]\d[A-Z]\s?\d[A-Z]\d)"

    addr1_match = re.search(addr1_pattern, full_addr)
    addr2_match = re.search(addr2_pattern, full_addr)
    city_prov_match = re.search(city_prov_pattern, full_addr)
    post_match = re.search(post_pattern, full_addr)

    addr1 = addr1_match.group(1).strip() if addr1_match else '',
    addr2 = addr2_match.group(1).strip() if addr2_match else '',
    city = city_prov_match.group(1).strip() if city_prov_match else '',
    prov = city_prov_match.group(2).strip() if city_prov_match else '',
    post = post_match.group(1).replace(" ", "") if post_match else '',
    
    addr1 = norm(addr1[0])
    addr2 = norm(addr2[0])
    city = norm(city[0])
    prov = norm(prov[0])
    post = norm(post[0])

    if re.match(r"^\d+[-\d]*$", addr1): 
        addr1 += ' ' + addr2
        addr2 = ''

    phone = the_list[start_num+3].text
    
    if firm:
        firm = firm.strip().upper()
        firm = norm(firm)
    
    if start_num < 5:
        office = '1'
    else:
        office = '2'
        
    addr_row = [lastname,firstname,'',office,firm,addr1,addr2,city,prov,post,phone,'','','','',gender,lic,'','',b1,'','','','','','','','','','','',extra1,extra2,extra3,extra4,extra5,'','']
    
    return addr_row

def format_phone(x):
    if x != None:
        x = x.replace("+1","")
        x = x.replace(" ", "")
        x = x.replace(")", "")
        x = x.replace("(", "")
        x = x.replace("-", "")
        x = x.replace(".", "")
        x = x.replace("*", "")
        x = x.replace("#", "")
    else:
        x = ''
    return x

def format_post(x):
    if x != None:
        x = x.replace(" ", "")
        x = x.replace(")", "")
        x = x.replace("(", "")
        x = x.replace("-", "")
        x = x.replace(".", "")
        x = x.upper()[0:6]
    else:
        x = ''
    return x