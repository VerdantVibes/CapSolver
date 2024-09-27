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

def get_spec_code(spec_desc):
    spec_code = ''
    print(spec_desc)
    if spec_desc == 'ADMINISTRATION':
        spec_code = ''
    if spec_desc == 'ADOLESCENT MEDICINE':
        spec_code = '06'           
    elif spec_desc == 'ADULT MEDICINE':
        spec_code = ''
    elif spec_desc == 'ADULT INFECTIOUS DISEASES':
        spec_code = '73'
    elif spec_desc == 'ADULT SURGICAL PATHOLOGY':
        spec_code = '35'
    elif spec_desc == 'ALLERGY & IMMUNOLOGY':
        spec_code = '61'
    elif spec_desc == 'ANAESTHESIA':
        spec_code = '03'
    elif spec_desc == 'ANESTHESIA':
        spec_code = '03'
    elif spec_desc == 'ANATOMIC PATHOLOGY':
        spec_code = '35'
    elif spec_desc == 'ANATOMICAL PATHOLOGY':
        spec_code = '35'
    elif spec_desc == 'ANATOMIC PATHOLOGY & CLINICAL PATHOLOGY':
        spec_code = '35'
    elif spec_desc == 'ANATOMIC PATHOLOGY & CLINIC PATHOLOGY':
        spec_code = '35'
    elif spec_desc == 'ANATOMICAL & CLINICAL PATHOLOGY':
        spec_code = '35'
    elif spec_desc == 'ANATOMIC PATHOLOGY & CLINICAL PATHOLOGY':
        spec_code = '35'
    elif spec_desc == 'ANESTHESIOLOGY':
        spec_code = '03'
    elif spec_desc == 'ASSESSMENT FOR GP ANESTHESIA':
        spec_code = '03'
    elif spec_desc == 'ADDICTION MEDICINE':
        spec_code = '17'
    elif spec_desc == 'ADMINISTRATIVE MEDICINE':
        spec_code = ''
    elif spec_desc == 'ADOLESCENT MEDICINE':
        spec_code = '06'
    elif spec_desc == 'ASSESSMENT FOR LICENSURE':
        spec_code = ''
    elif spec_desc == 'ASSESSMENT TO DO LIMITED ANESTHESIA':
        spec_code = '03'
    elif spec_desc == 'ASSESSMENT/ORIENTATION':
        spec_code = ''
    elif spec_desc == 'ASSESSMENT_ORIENTATION':
        spec_code = ''
    elif spec_desc == 'ASSESSMENT ORIENTATION':
        spec_code = ''
    elif spec_desc == 'CARDIAC ANESTHESIA':
        spec_code == '03'
    elif spec_desc == 'CARDIOLOGY':
        spec_code = '62'
    elif spec_desc =='CARDIOLOGY (INTERNAL MEDICINE OR PEDIATRICS)':
        spec_code = '62/60'
    elif spec_desc == 'CARDIOTHORACIC SURGERY':
        spec_code = '51'        
    elif spec_desc == 'CARDIOVASCULAR DISEASE':
        spec_code = '62'
    elif spec_desc =='CARDIAC SURGERY':
        spec_code = '52'
    elif spec_desc =='CARDIOVASCULAR AND THORACIC SURGERY':
        spec_code = '57'
    elif spec_desc == 'CARE OF THE ELDERLY':
        spec_code = '08'
    elif spec_desc =='CHILD AND ADOLESCENT PSYCHIATRY':
         spec_code = '83/82/8A'
    elif spec_desc == 'CHILD & ADOLESCENT PSYCHIATRY':
         spec_code = '83/82/8A'
    elif spec_desc == 'CHEMICAL PATHOLOGY':
        spec_code = '33'
    elif spec_desc == 'CHILD PSYCHIATRY':
        spec_code = '83'
    elif spec_desc == 'CHRONIC PAIN MEDICINE':
        spec_code = 'PN'
    elif spec_desc == 'CLINICIAN INVESTIGATOR PROGRAM':
        spec_code = 'CN'        
    elif spec_desc =='CLINICAL ASSISTANT - ANESTHESIA':
        spec_code = '03'
    elif spec_desc =='CLINICAL ASSISTANT - GYNECOLOGY ONCOLOGY':
        spec_code = '90'
    elif spec_desc =='CLINICAL ASSISTANT - NEONATOLOGY':
        spec_code = '7L'
    elif spec_desc =='CLINICAL ASSISTANT - ONCOLOGY':
        spec_code = '70'
    elif spec_desc =='CLINICAL FELLOW - MALIGNANT HEMATOLOGY AND STEM CELL TRANSPL':
        spec_code = '72'
    elif spec_desc =='CLINICAL FELLOW - SASK EPILEPSY PROGRAM':
        spec_code = '81'
    elif spec_desc =='CLINICAL IMMUNOLOGY AND ALLERGY':
        spec_code = '34/61'
    elif spec_desc == 'CLINICAL IMMUNOLOGY & ALLERGY':
        spec_code = '34/61'               
    elif spec_desc == 'CLINICAL IMMUNOLOGY':
        spec_code = '34'
    elif spec_desc == 'CLINICAL PHARMACOLOGY AND TOXICOLOGY':
        spec_code = '18/TX'
    elif spec_desc =='CLINICAL INVESTIGATOR PROGRAM/GENERAL INTERNAL MEDICINE':
        spec_code = 'CN/09'
    elif spec_desc =='CLINICAL INVESTIGATOR PROGRAM/GENERAL SURGERY':
        spec_code = '50'
    elif spec_desc == 'COLON & RECTAL SURGERY':
        spec_code = '5B'
    elif spec_desc == 'COLORECTAL SURGERY':
        spec_code = '5B'
    elif spec_desc =='CRITICAL CARE MEDICINE':
        spec_code = 'CI'
    elif spec_desc =='COMMUNITY MEDICINE':
        spec_code = '19'
    elif spec_desc == 'COMMUNITY MEDICINE (PUBLIC HEALTH)':
        spec_code = '19'
    elif spec_desc =='DERMATOLOGY':
        spec_code = '04'
    elif spec_code == 'DERMATOPATHOLOGY':
        spec_code = '4B'
    elif spec_desc == 'DEVELOPMENTAL PEDIATRICS':
        spec_code = '7Q'
    elif spec_desc =='DIAGNOSTIC AND THERAPEUTIC RADIOLOGY':
        spec_code = '42'
    elif spec_desc =='DIAGNOSTIC RADIOLOGY':
        spec_code = '42'
    elif spec_desc =='DIAGNOSTIC_RADIOLOGY':
        spec_code = '42'
    elif spec_desc =='ELDERLY CARE FAMILY PRACTICE':
        spec_code = '08/09'
    elif spec_desc =='EMERGENCY MEDICINE':
        spec_code = 'EM'
    elif spec_desc =='EMERGENCY_MED':
        spec_code = 'EM'
    elif spec_desc =='ENDOCRINOLOGY AND METABOLISM (INTERNAL MEDICINE OR PEDIATRICS)':
        spec_code = '71/60'
    elif spec_desc =='ENDOCRINOLOGY AND METABOLISM':
        spec_code = '71'
    elif spec_desc == 'ENDOCRINOLOGY & METABOLISM':
        spec_code = '71'
    elif spec_desc =='ENT':
        spec_code = '26'
    elif spec_desc =='EXPANDED SKILLS PROGRAM':
        spec_code = ''
    elif spec_desc =='EXPANDED SKILLS PROGRAM (NEUROSURGERY)':
        spec_code = '53'
    elif spec_desc == 'EYE PHYSICIAN':
        spec_code = '25'
    elif spec_desc =='FAMILY_MED':
        spec_code = '09'
    elif spec_desc =='FAMILY MEDICINE':
        spec_code = '09'
    elif spec_desc =='FAMILY MEDICINE (CFPC)':
        spec_code = '09'
    elif spec_desc =='FAMILY MEDICINE/ANAESTHESIA':
        spec_code = '09/03'
    elif spec_desc =='FAMILY MEDICINE/EMERGENCY':
        spec_code = '09/EM'
    elif spec_desc =='FAMILY MEDICINE/EMERGENCY MEDICINE':
        spec_code = '09/EM'
    elif spec_desc =='FAMILY MEDICINE EMERGENCY MEDICINE':
         spec_code = '09/EM'
    elif spec_desc =='FAMILY_MED/EMERGENCY_MED':
        spec_code = '09/EM'
    elif spec_desc =='FAMILY_MED/ENHANCED ANESTHESIA SKILLS':
        spec_code = '09/03'
    elif spec_desc =='FAMILY_MED/ENHANCED SKILLS SPORTS MEDICINE':
        spec_code = '09/SM'
    elif spec_desc =='FAMILY_MED/ENHANCED SURGICAL SKILLS':
        spec_code = '09/50'
    elif spec_desc =='FAMILY MEDICINE / OBSTETRICS & GYNECOLOGY':
        spec_code = '09/90'
    elif spec_desc =='FAMILY MEDICINE/Public HEALTH AND PREVENTIVE MEDICINE':
        spec_code = '19/09'
    elif spec_desc == 'FAMILY MEDICINE ANESTHESIA':
        spec_code = '09/03'
    elif spec_desc == 'FAMILY MEDICINE CARE OF THE ELDERLY':
        spec_code = '09/08'
    elif spec_desc == 'FAMILY MEDICINE OBSTETRICS':
       spec_code = '09/90'
    elif spec_desc == 'FAMILY MEDICINE ONCOLOGY':
        spec_code = '09/70'
    elif spec_desc == 'FAMILY MEDICINE PALLIATIVE MEDICINE':
         spec_code = '09/PC'
    elif spec_desc == 'FAMILY MEDICINE SPORTS MEDICINE':
        spec_code = '09/21'
    elif spec_desc == 'FAMILY PRACTICE':
        spec_code = '09'        
    elif spec_desc == 'FAMILY PRACTICE - ANATOMICAL PATHOLOGY':
        spec_code = '09/35'
    elif spec_desc == 'FAMILY PRACTICE - ANESTHESIOLOGY':
        spec_code = '09/03'
    elif spec_desc == 'FAMILY PRACTICE - CLINICAL IMMUNOLOGY':
        spec_code = '09/34'
    elif spec_desc == 'FAMILY PRACTICE - COMMUNITY MEDICINE':
        spec_code = '09/19'
    elif spec_desc == 'FAMILY PRACTICE - CRITICAL CARE MEDICINE':
        spec_code = '09/CI'
    elif spec_desc == 'FAMILY PRACTICE – DERMATOLOGY':
        spec_code = '09/04'
    elif spec_desc == 'FAMILY PRACTICE - DIAGNOSTIC RADIOLOGY':
        spec_code = '09/42'
    elif spec_desc == 'FAMILY PRACTICE - EMERGENCY MEDICINE':
        spec_code = '09/EM'
    elif spec_desc == 'FAMILY PRACTICE – GASTROENTEROLOGY':
        spec_code = '09/63'
    elif spec_desc == 'FAMILY PRACTICE - GENERAL PATHOLOGY':
        spec_code = '09/31'
    elif spec_desc == 'FAMILY PRACTICE - GENERAL SURGERY':
        spec_code = '09/50'
    elif spec_desc == 'FAMILY PRACTICE – HEMATOLOGY':
        spec_code = '09/72'
    elif spec_desc == 'FAMILY PRACTICE - INTERNAL MEDICINE':
        spec_code = '09/60'
    elif spec_desc == 'FAMILY PRACTICE - MEDICAL BIOCHEMISTRY':
        spec_code = '09/33'
    elif spec_desc == 'FAMILY PRACTICE - OBSTETRICS AND GYNECOLOGY':
        spec_code = '09/90'
    elif spec_desc == 'FAMILY PRACTICE – OPHTHALMOLOGY':
        spec_code = '09/25'
    elif spec_desc == 'FAMILY PRACTICE - PALLIATIVE MEDICINE':
        spec_code = '09/PC'
    elif spec_desc == 'FAMILY PRACTICE - PEDIATRICS':
        spec_code = '09/07'
    elif spec_desc == 'FAMILY PRACTICE - PLASTIC SURGERY':
        spec_code = '09/54'
    elif spec_desc == 'FAMILY PRACTICE - PSYCHIATRY':
        spec_code = '09/82'
    elif spec_desc == 'FAMILY PRACTICE - PUBLIC HEALTH AND PREVENTIVE MEDICINE':
        spec_code = '09/14'
    elif spec_desc == 'FAMILY PRACTICE - RADIATION ONCOLOGY':
        spec_code = '09/43'
    elif spec_desc == 'FAMILY PRACTICE - UROLOGY':
        spec_code = '09/22'               
    elif spec_desc == 'FELLOWSHIP':
        spec_code = ''
    elif spec_desc == 'FOOT & ANKLE DIABETIC FOOT CARE':
        spec_code = 'DB'
    elif spec_desc =='FORENSIC PATHOLOGY':
        spec_code = '11/31'
    elif spec_desc =='FORENSIC PSYCHIATRY':
        spec_code = '8F'
    elif spec_desc =='GASTROENTEROLOGY':
        spec_code = '63'
    elif spec_desc =='GASTROENTEROLOGY (INTERNAL MEDICINE OR PEDIATRICS)':
        spec_code = '63/60'
    elif spec_desc =='GENERAL INTERNAL MEDICINE':
        spec_code = '60'
    elif spec_desc =='GENERAL PATHOLOGY':
        spec_code = '31'
    elif spec_desc =='GENERAL_PRACTICE':
        spec_code = '09'
    elif spec_desc =='GENERAL PRACTICE':
        spec_code = '09'
    elif spec_desc =='GENERAL PRACTICE - ANESTHESIA':
        spec_code = '03/09'
    elif spec_desc =='GENERAL_SURGERY':
        spec_code = '50'
    elif spec_desc =='GENERAL SURGERY': 
        spec_code = '50'
    elif spec_desc =='GENERAL_SURGERY/PLASTIC_SURGERY':
        spec_code = '54/50'
    elif spec_desc == 'GENERAL SURGICAL ONCOLOGY':
        spec_code = '77'
    elif spec_desc =='GERIATRIC MEDICINE':
        spec_code = '08'
    elif spec_desc =='GERIATRIC MEDICINE (INTERNAL MEDICINE)':
        spec_code = '08/60'
    elif spec_desc =='GERIATRIC PSYCHIATRY':
        spec_code = 'PG'
    elif spec_desc =='GYNECOLOGY':
        spec_code = 'GY'
    elif spec_desc =='GYNECOLOGIC ONCOLOGY':
        spec_code = '76'
    elif spec_desc =='GYNECOLOGY PATHOLOGY':
        spec_code = 'GY/31'
    elif spec_desc =='GYNECOLOGIC REPRODUCTIVE ENDOCRINOLOGY AND INFERTILITY':
        spec_code = 'FT'
    elif spec_desc =='HAEMATOLOGICAL_PATHOLOGY':
        spec_code = '36'
    elif spec_desc =='HAEMATOLOGICAL PATHOLOGY':
        spec_code = '36'
    elif spec_desc =='HEMATOLOGICAL PATHOLOGY':
        spec_code = '36'
    elif spec_desc =='HAEMATOLOGY': 
        spec_code = '72'
    elif spec_desc =='HEMATOLOGY':
        spec_code = '72'
    elif spec_desc == 'HEMATOPATHOLOGY':
        spec_code = '36'
    elif spec_desc == 'HEAD & NECK SURGICAL ONCOLOGY':
        spec_code = '77'
    elif spec_desc == 'HEPATOLOGY':
        spec_code = 'HE'
    elif spec_desc =='HOSPITALIST':
        spec_code = 'HO'
    elif spec_desc =='HOUSE OFFICER':
        spec_code = 'OH'
    elif spec_desc =='INFECTIOUS DISEASE':
        spec_code = '73'
    elif spec_desc =='INFECTIOUS_DISEASE':
        spec_code = '73'
    elif spec_desc =='INFECTIOUS DISEASES':
        spec_code = '73'
    elif spec_desc =='INTENSIVE CARE':
        spec_code = 'CI'
    elif spec_desc =='INTERNAL MEDICINE':
        spec_code = '60'
    elif spec_desc =='INTERNAL_MEDICINE':
        spec_code = '60'
    elif spec_desc =='INTERNAL_MED':
        spec_code = '60'
    elif spec_desc =='INTERNAL_MED_DERMATOLOGY':
        spec_code = '04/60'
    elif spec_desc =='INTERNAL_MED_GENERAL':
        spec_code = '60'
    elif spec_desc == 'INTERVENTIONAL CARDIOLOGY':
        spec_code = 'CV'
    elif spec_desc == 'INTERVENTIONAL RADIOLOGY':
        spec_code = '42'
    elif spec_desc == 'LEUKEMIA/BONE MARROW TRANSPLANT PROGRAM':
        spec_code = 'HE/TP'
    elif spec_desc == 'LIVER TRANSPLANT/HEPATOLOGY':
        spec_code = 'HE/TP'
    elif spec_desc =='MATERNAL-FETAL MEDICINE':
        spec_code = '91'
    elif spec_desc =='MEDICAL GENETICS':
        spec_code = '13'
    elif spec_desc =='MEDICAL ONCOLOGY':
        spec_code = '70'
    elif spec_desc =='MATERNAL FETAL MEDICINE':
        spec_code = '91'
    elif spec_desc =='MEDICAL BIOCHEMISTRY':
        spec_code = '33'
    elif spec_code == 'MEDICAL GENETICS AND GENOMICS':
        spec_code='13'
    elif spec_desc =='MEDICAL IMAGING':
        spec_code = '42'
    elif spec_desc =='MEDICAL_IMAGING':
        spec_code = '42'
    elif spec_desc =='MEDICAL MICROBIOLOGY':
         spec_code = '32'
    elif spec_desc =='MEDICAL_ONCOLOGY':
        spec_code = '70'
    elif spec_desc =='MEDICAL ONCOLOGY':
        spec_code = '70'
    elif spec_desc =='MEDICAL ONCOLOGY (INTERNAL MEDICINE)':
        spec_code = '70'
    elif spec_desc == 'MEDICAL TOXICOLOGY':
        spec_code = 'TX'
    elif spec_desc =='MINIMALLY_INVASIVE_SURGERY':
        spec_code = '50'
    elif spec_desc == 'MINIMALLY INVASIVE AND BARIATRIC SURGERY':
        spec_code = 'BS'
    elif spec_desc == 'MUSCULOSKELETAL MEDICINE':
        spec_code = '/SM'
    elif spec_desc == 'NATIONAL COMMISSION ON CERTIFICATION OF PHYSICIAN ASSISTANTS':
        spec_code = ''
    elif spec_desc =='NEONATAL-PERINATAL MEDICINE':
        spec_code = '91'
    elif spec_desc =='NEONATOLOGY':
        spec_code = '91'
    elif spec_desc =='NEPHROLOGY':
        spec_code = '23'
    elif spec_desc =='NEPHROLOGY (INTERNAL MEDICINE OR PEDIATRICS)':
        spec_code = '23/60'
    elif spec_desc =='NEUROLOGY':
        spec_code = '81'
    elif spec_desc =='NEUROPATHOLOGY':
        spec_code = '2F'
    elif spec_desc =='NEURORADIOLOGY':
        spec_code = '46'
    elif spec_desc =='NEUROSURGERY': 
        spec_code = '53'
    elif spec_desc == 'NEURO-OPHTHALMOLOGY':
        spec_code = '2F'
    elif spec_desc =='NUCLEAR MEDICINE':
        spec_code = '44'
    elif spec_desc == 'NUCLEAR RADIOLOGY':
        spec_code = '44'
    elif spec_desc =='OBSTETRICS':
        spec_code = '90'
    elif spec_desc =='OBSTETRICS AND GYNECOLOGY':
        spec_code = '90'
    elif spec_desc == 'OBSTETRICS & GYNECOLOGY':
        spec_code = '90'
    elif spec_desc =='OBSTETRICS_GYNAECOLOGY':
        spec_code = '90'
    elif spec_desc =='OBSTETRICS GYNAECOLOGY':
        spec_code = '90'
    elif spec_desc == 'OCCUPATIONAL HEALTH & DISABILITY MANAGEM':
        spec_code = '15'
    elif spec_desc =='OCCUPATIONAL MEDICINE':
        spec_code = '15'
    elif spec_desc =='OPHTHALMOLOGY': 
        spec_code = '25'
    elif spec_desc =='OROMAXILLOFACIAL SURGERY':
        spec_code = '26'
    elif spec_desc =='ORTHOPAEDIC_SURGERY':
        spec_code = '21'
    elif spec_desc =='ORTHOPEDIC SURGERY':
        spec_code = '21'
    elif spec_desc == 'ORTHOPAEDIC SURGERY HIP & KNEE RECONSTRUCTION':
        spec_code = '21'
    elif spec_desc == 'ORTHOPEDIC AND TRAUMATOLOGY':
        spec_code = '21'
    elif spec_desc == 'ORTHOPEDIC SPINE SURGERY':
        spec_code = '21'
    elif spec_desc == 'ORTHOPEDIC SPORTS MEDICINE':
        spec_code = '21'
    elif spec_desc == 'ORTHOPEDIC SPORTS MEDICINE & UPPER EXTREMITY RECONSTRUCTION':
        spec_code = '21'
    elif spec_desc == 'ORTHOPEDIC TRAUMA':
        spec_code = '21'
    elif spec_desc =='OTOLARYNGOLOGY':
        spec_code = '26'
    elif spec_desc =='OTOLARYNGOLOGY -  HEAD AND NECK SURGERY':
        spec_code = '26'
    elif spec_desc =='OTOLARYNGOLOGY - HEAD AND NECK SURGERY':
        spec_code = '26'
    elif spec_desc =='Otolaryngology — Head and Neck Surgery':
        spec_code = '26'
    elif spec_desc =='PAEDIATRICS':
        spec_code = '07'
    elif spec_desc =='PEDIATRICS':
        spec_code = '07'
    elif spec_desc == 'PAEDIATRICS & CHILD HEALTH':
        spec_code = '07'
    elif spec_desc == 'PAIN MEDICINE':
        spec_code = 'PN'
    elif spec_desc =='PALLIATIVE MEDICINE':
        spec_code = 'PC'
    elif spec_desc == 'PATHOLOGY':
        spec_code = 'PATHOLOGY'
    elif spec_desc =='PEDIATRICS':
        spec_code = '07'
    elif spec_desc == 'PEDIATRIC ANESTHESIA':
        spec_code = '03'
    elif spec_desc == 'PAEDIATRIC CARDIOLOGY':
        spec_code = '78'
    elif spec_desc =='PEDIATRIC CARDIOLOGY': 
        spec_code = '7B'
    elif spec_desc == 'PEDIATRIC CLINICAL IMMUNOLOGY & ALLERGY':
        spec_code = '7H'
    elif spec_desc == 'PEDIATRIC CRITICAL CARE MEDICINE':
        spec_code = 'CP'
    elif spec_desc =='PEDIATRIC EMERGENCY MEDICINE':
        spec_code = '8E'
    elif spec_desc == 'PEDIATRIC GASTROENTEROLOGY':
        spec_code = '7F'
    elif spec_desc == 'PAEDIATRIC GENERAL SURGERY':
        spec_code = '59'
    elif spec_desc == 'PEDIATRIC GENERAL SURGERY':
        spec_code = '59'
    elif spec_desc =='PEDIATRIC HEMATOLOGY/ONCOLOGY':
        spec_code = '7G/07/7K'
    elif spec_desc == 'PEDIATRIC INFECTIOUS DISEASES':
        spec_code = '7I'
    elif spec_desc == 'PEDIATRIC NEPHROLOGY':
        spec_code = '7P'
    elif spec_desc == 'PEDIATRIC NEUROLOGY':
        spec_code = '7J'
    elif spec_desc =='PEDIATRIC ONCOLOGY': 
        spec_code = '7K/07'
    elif spec_desc == 'PEDIATRIC OPHTHALMOLOGY':
        spec_code = '24'
    elif spec_desc == 'PEDIATRIC ORTHOPEDIC SURGERY':
        spec_code = '7X'
    elif spec_desc == 'PEDIATRIC RADIOLOGY':
        spec_code = '45'
    elif spec_desc == 'PEDIATRIC RESPIRATORY MEDICINE':
        spec_code = '7M'
    elif spec_desc =='PEDIATRIC RESPIROLOGY':
        spec_code = '7M'
    elif spec_desc == 'PEDIATRIC RHEUMATOLOGY':
        spec_code = '7N'
    elif spec_desc =='PEDIATRIC SURGERY':
        spec_code = '59'
    elif spec_desc == 'PEDIATRIC & ADULT NEPHROPATHOLOGY':
        spec_code = '31'
    elif spec_desc == 'PERIOPERATIVE MEDICINE':
        spec_code = '03'
    elif spec_desc == 'PERIOPERATIVE ECHO CARDIOGRAPHY':
        spec_code = 'EC'
    elif spec_desc =='PHYSICAL MEDICINE AND REHABILITATION':
        spec_code = '64'
    elif spec_desc == 'PHYSICAL MEDICINE & REHABILITATION':
        spec_code = '64'
    elif spec_desc =='PHYSICAL_REHAB_MED':
        spec_code = '64'
    elif spec_desc =='PHYSICAL REHAB MED':
        spec_code = '64'
    elif spec_desc =='PHYSIATRY': 
        spec_code = '82'
    elif spec_desc =='PHYSICIAN ENHANCEMENT PROGRAM':
        spec_code = ''
    elif spec_desc =='PLASTIC SURGERY':
        spec_code = '54'
    elif spec_desc =='PRE-LICENSURE ASSESSMENT - PEDIATRIC CARDIOLOGY':
        spec_code = '7B'
    elif spec_desc =='PRE-LICENSURE ASSESSMENT - PEDIATRIC RHEUMATOLOGY':
        spec_code = '7N'
    elif spec_desc =='PRE-LICENSURE ASSESSMENT-MEDICAL HEALTH OFFICER':
        spec_code = 'OH'
    elif spec_desc == 'PERIOPERATIVE MEDICINE':
        spec_code = '60'
    elif spec_code == 'PODIATRIC SURGEON':
        spec_code='05'
    elif spec_desc =='PSYCHIATRY':
        spec_code = '82'
    elif spec_desc =='PUBLIC HEALTH':
        spec_code = '19'
    elif spec_desc =='PUBLIC HEALTH AND PREVENTIVE MEDICINE':
        spec_code = '19'
    elif spec_desc =='PUBLIC_HEALTH_AND_PREVENTIVE_MEDICINE':
        spec_code = '19'
    elif spec_desc =='PUBLIC HEALTH &AMP; GENERAL PREVENTIVE MEDICINE':
        spec_code = '19'
    elif spec_desc == 'PUBLIC HEALTH & GENERAL PREVENTIVE MEDICINE':
        spec_code = '19'
    elif spec_desc =='PULMONARY DISEASES':
        spec_code = '69'
    elif spec_desc =='RADIATION_ONCOLOGY':
        spec_code = '43'
    elif spec_desc =='RADIATION ONCOLOGY': 
        spec_code = '43'
    elif spec_desc == 'RADIOLOGY':
        spec_code = '42'
    elif spec_desc =='REHABILITATION MEDICINE':
        spec_code = '64'
    elif spec_desc == 'REPRODUCTIVE ENDOCRINOLOGY AND INFERTILIT':
        spec_code = 'FT'
    elif spec_desc =='REPIRATORY_MED':
        spec_code = '69'
    elif spec_desc =='RESPIRATORY MEDICINE':
        spec_code = '69'
    elif spec_desc =='RESPIROLOGY':
        spec_code = '69'
    elif spec_desc =='RESPIROLOGY (INTERNAL MEDICINE OR PEDIATRICS)':
        spec_code = '69/60'
    elif spec_desc =='RHEUMATOLOGY':
        spec_code = '74'
    elif spec_desc =='RHEUMATOLOGY (INTERNAL MEDICINE OR PEDIATRICS)':
        spec_code = '74/60'
    elif spec_desc == 'RHINOLOGY & SINUS SURGERY':
        spec_code = '26'
    elif spec_desc =='SASKATCHEWAN INTERNATIONAL PHYSICIAN PRACTICE ASSESSMENT (SIPPA)':
        spec_code = ''
    elif spec_desc =='SASKATCHEWAN INTERNATIONAL PHYSICIAN PRACTICE ASSESSMENT(SIPPA)':
        spec_code = ''
    elif spec_desc =='SASKATCHEWAN INTERNATIONAL PHYSICIAN PRACTICE ASSESSMENT(SIPPA)':
        spec_code = ''
    elif spec_desc =='SIPPA':
        spec_code = '09'
    elif spec_desc == 'SLEEP MEDICINE':
        spec_code = 'SL'
    elif spec_desc == 'SPINE FELLOWSHIP':
        spec_code = '21'
    elif spec_desc == 'SPORT MEDICINE':
        spec_code = 'SM'
    elif spec_desc == 'SPORTS MEDICINE':
        spec_code = 'SM'
    elif spec_desc == 'SPORTS MEDICINE - PEDIATRICS':
        spec_code = '07/SM'
    elif spec_desc =='SPORT AND EXERCISE MEDICINE':
        spec_code = '21'
    elif spec_desc =='SURGICAL ASSISTS':
        spec_code = '5A'
    elif spec_desc =='SURGERY':
        spec_code = '50'
    elif spec_desc =='SURGICAL FOUNDATIONS':
        spec_code = '50'
    elif spec_desc == 'THERAPEUTIC RADIOLOGY':
        spec_code = '42'
    elif spec_desc =='THORACIC SURGERY':
        spec_code = '51'
    elif spec_desc == 'TRAUMA/CRITICAL CARE':
        spec_code = 'CI'
    elif spec_desc =='UROLOGY':
        spec_code = '22'
    elif spec_desc =='VASCULAR SURGERY':
        spec_code = '56'
    else:
        spec_code = spec_desc
    return spec_code