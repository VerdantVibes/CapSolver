# -*- coding: utf-8 -*-
"""
Created on Tue May 24 15:38:51 2022

@author: VerdantVibes
"""
import unidecode
import re


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