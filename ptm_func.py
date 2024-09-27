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
            
        # First remove any suffixes
        if fullname.endswith(' JR'):
            suffix = 'JR'
            fullname = fullname[:-3]
        elif fullname.endswith(' JR.'):
            suffix = 'JR'
            fullname = fullname[:-4]
        elif fullname.endswith(' JUNIOR'):
            suffix = 'JUNIOR'
            fullname = fullname[:-7]
        elif  fullname.endswith(' III'):
            suffix = 'III'
            fullname = fullname[:-4]
        elif fullname.endswith(' II'):
            suffix = 'II'
            fullname = fullname[:-3]
        elif fullname.endswith(' IV'):
            suffix = 'IV'
            fullname = fullname[:-3]
        elif fullname.endswith(' SR'):
            suffix = 'SR'
            fullname = fullname[:-3]
        elif fullname.endswith(' SR.'):
            suffix = 'SR'
            fullname = fullname[:-4]
                                                                                                                                                                                                                        # Now handle any multi word last names
        if ')' in fullname:
            lastname = fullname.partition(')')[2]
            firstname = fullname.partition(')')[0] + fullname.partition(')')[1] 
        elif ' VAN ' in fullname:
            lastname = fullname.partition(' VAN ')[1] + fullname.partition(' VAN ')[2]
            firstname = fullname.partition(' VAN ')[0]
        elif ' DER ' in fullname:
            lastname = fullname.partition(' DER ')[1] + fullname.partition(' DER ')[2]
            firstname = fullname.partition(' DER ')[0]
        elif ' VANDER ' in fullname:
            lastname = fullname.partition(' VANDER ')[1] + fullname.partition(' VANDER ')[2]
            firstname = fullname.partition(' VANDER ')[0]
        elif ' DE ' in fullname:
            lastname = fullname.partition(' DE ')[1] + fullname.partition(' DE ')[2]
            firstname = fullname.partition(' DE ')[0]
        elif ' ABD ' in fullname:
            lastname = fullname.partition(' ABD ')[1] + fullname.partition(' ABD ')[2]
            firstname = fullname.partition(' ABD ')[0]
        elif ' EL ' in fullname:
            lastname = fullname.partition(' EL ')[1] + fullname.partition(' EL ')[2]
            firstname = fullname.partition(' EL ')[0]
        elif ' DEL ' in fullname:
            lastname = fullname.partition(' DEL ')[1] + fullname.partition(' DEL ')[2]
            firstname = fullname.partition(' DEL ')[0]                                     
        elif ' DELA ' in fullname:
    	    lastname = fullname.partition(' DELA ')[1] + fullname.partition(' DELA ')[2]
    	    firstname = fullname.partition(' DELA ')[0]
        elif ' DELLA ' in fullname:
    	    lastname = fullname.partition(' DELLA ')[1] + fullname.partition(' DELLA ')[2]
    	    firstname = fullname.partition(' DELLA ')[0]
        elif ' DI ' in fullname:
    	    lastname = fullname.partition(' DI ')[1] + fullname.partition(' DI ')[2]
    	    firstname = fullname.partition(' DI ')[0]
        elif ' DOS ' in fullname:
            lastname = fullname.partition(' DOS ')[1] + fullname.partition(' DOS ')[2]
            firstname = fullname.partition(' DOS ')[0]
        elif ' DU ' in fullname:
    	    lastname = fullname.partition(' DU ')[1] + fullname.partition(' DU ')[2]
    	    firstname = fullname.partition(' DU ')[0]
        elif  ' LE ' in fullname:
    	    lastname = fullname.partition(' LE ')[1] + fullname.partition(' LE ')[2]
    	    firstname = fullname.partition(' LE ')[0]
        elif ' ST ' in fullname:
            lastname = fullname.partition(' ST ')[1] + fullname.partition(' ST ')[2]
            firstname = fullname.partition(' ST ')[0]	
        elif ' ST. ' in fullname:
            lastname = fullname.partition(' ST. ')[1] + fullname.partition(' ST. ')[2]
            firstname = fullname.partition(' ST. ')[0]	
        elif ' VON ' in fullname:
            lastname = fullname.partition(' VON ')[1] + fullname.partition(' VON ')[2]
            firstname = fullname.partition(' VON ')[0]	
        elif ' DER ' in fullname:
            lastname = fullname.partition(' DER ')[1] + fullname.partition(' DER ')[2]
            firstname = fullname.partition(' DER ')[0]	
        else:
            firstname = fullname.rpartition(" ")[0]
            lastname = fullname.rpartition(" ")[2]
                   
    # remove any leading or trailing spaces
    firstname = firstname.strip()
    lastname = lastname.strip()
    
    #to fix problem when the second character of the last name is a space
    # ex: B PENICH
    if len(lastname) > 1:
        if lastname[1] == ' ':
    	    #print('There is a space')
    	    splitlastname = lastname.split(' ',1)
    	    firstname = firstname + ' ' + splitlastname[0]
    	    lastname = splitlastname[1]
        
    return firstname, lastname, suffix

def get_prov_abbrev(prov):
    
    prov_abbrev = ''
    
    if prov == 'ALBERTA':
            prov_abbrev = 'AB'
    elif prov == 'BRITISH COLUMBIA':
            prov_abbrev = 'BC'
    elif prov == 'MANITOBA':
            prov_abbrev = 'MB'
    elif prov == 'NEW BRUNSWICK':
            prov_abbrev = 'NB'
    elif prov == 'NEWFOUNDLAND AND LABRADOR':
            prov_abbrev = 'NL'
    elif prov =='NORTHWEST TERRITORIES':
            prov_abbrev = 'NT'
    elif prov == 'NOVA SCOTIA':
            prov_abbrev = 'NS'
    elif prov == 'NUNAVUT':
            prov_abbrev = 'NU'
    elif prov == 'ONTARIO':
            prov_abbrev = 'ON'
    elif prov == 'PRINCE EDWARD ISLAND':
            prov_abbrev = 'PEI'
    elif prov == 'QUEBEC':
            prov_abbrev = 'QC'
    elif prov == 'SASKATCHEWAN':
            prov_abbrev = 'SK'
    elif prov == 'YUKON':
            prov_abbrev = 'YT'
    else:
        prov_abbrev = prov
        
    return prov_abbrev