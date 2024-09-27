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

def extract_data(a,s1,s2):
    x = a.partition(s1)[2].partition(s2)[0]
    return x

def cfDecodeEmail(encodedString):
    r = int(encodedString[:2],16)
    email = ''.join([chr(int(encodedString[i:i+2], 16) ^ r) for i in range(2, len(encodedString), 2)])
    return email

def convert_html(x):
    if x != None:
        x = x.replace("&NBSP;", " ")
        x = x.replace("&nbsp;", " ")
        x = x.replace("&#39;", "'")
        x = x.replace("&AMP;", "&")
        x = x.replace("&amp;", "&")
        x = x.replace("&#200;", "E")
        x = x.replace("&#201;", "E")
        x = x.replace("&#232;", "E")
        x = x.replace("&#233;", "E")
        x = x.replace("&#234;", "E")
        x = x.replace("&#235;", "E")
        x = x.replace("&#192;", "A")
        x = x.replace("&#194;", "A")
        x = x.replace("&#196;", "A")
        x = x.replace("&#224;", "A")
        x = x.replace("&#226;", "A")
        x = x.replace("&#228;", "A")
        x = x.replace("&#229;", "A")
        x = x.replace("&#212;", "O")
        x = x.replace("&#214;", "O")
        x = x.replace("&#242;", "O")
        x = x.replace("&#244;", "O")
        x = x.replace("&#246;", "O")
        x = x.replace("&#248;", "O")
        x = x.replace("&#206;", "I")
        x = x.replace("&#238;", "I")
        x = x.replace("&#239;", "I")
        x = x.replace("&#220;", "U")
        x = x.replace("&#231;", "C")
        x = x.replace("&#223;", "B")
        x = x.replace("&#230;", "AE")
        x = x.replace("&#160;", " ") # space
        x = x.replace("&QUOT;", '"') # double quote
        x = x.replace("&quot;", '"') # double quote
        x = x.replace("&#174;", "") # ® so use nothing
        x = x.replace("&#176;", "") # degree so use nothing
    else:
        x = ''
    return x

def splitfullname(fullname):
    firstname = ""
    lastname = ""
    suffix = ""
    fullname = fullname.strip().upper()
    vCountSpaces = fullname.count(" ")
    if (vCountSpaces == 0):
        lastname = fullname
    elif (vCountSpaces == 1):
        firstname = fullname.partition(" ")[0]
        lastname = fullname.partition(" ")[2]
    else:
        # Repmove any prefixes
        if fullname.startswith("DR. "):
            fullname = fullname.replace('DR. ', '')
        elif fullname.startswith("DR "):
            fullname = fullname.replace('DR ', '')
        elif fullname.startswith("DRE "):
            fullname = fullname.replace('DRE ', '')
        elif fullname.startswith("MR. "):
            fullname = fullname.replace('MR. ', '')
        elif fullname.startswith("MR "):
            fullname = fullname.replace('MR ', '')
        elif fullname.startswith("MRS. "):
            fullname = fullname.replace('MRS. ', '')
        elif fullname.startswith("MRS "):
            fullname = fullname.replace('MRS ', '')
        elif fullname.startswith("MISS "):
            fullname = fullname.replace('MISS ', '')
        elif fullname.startswith("MS. "):
            fullname = fullname.replace('MS. ', '')
        elif fullname.startswith("MS "):
            fullname = fullname.replace('MS ', '')
        elif fullname.startswith("MME. "):
            fullname = fullname.replace('MME. ', '')
        elif fullname.startswith("MME "):
            fullname = fullname.replace('MME ', '')