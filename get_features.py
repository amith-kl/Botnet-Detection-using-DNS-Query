import logging
import re
import numpy as np
import pydnsbl
from collections import Counter
from tld import get_tld

#Return vowel ratio, consonant ratio
def vowelConsonantRatio(domain):
    vcount, ccount = 0, 0
    vowels = ['a', 'e', 'i', 'o', 'u']
    for x in domain:
        if x in vowels:
            vcount += 1
        else:
            ccount += 1
    vratio = float('{:.2f}'.format(vcount/len(domain)))
    cratio = float('{:.2f}'.format(ccount/len(domain)))
    return [vratio, cratio]

#Return special characters ratio, numbers ratio
def specNumRatio(domain):
    specCount = 0
    numCount = 0
    for x in domain:
        if x.isalpha():
            continue
        elif x.isdigit():
            numCount += 1
        else:
            specCount += 1
    specRatio = float('{:.2f}'.format(specCount/len(domain)))
    numRatio = float('{:.2f}'.format(numCount/len(domain)))
    return [numRatio, specRatio]

#Return longest substring of vowels
def longestVowel(s):
    vowels = ['a', 'e', 'i', 'o', 'u']
    count, res = 0, 0
    for i in range(len(s)):
        if (s[i] in vowels):
            count += 1 
        else:
            res = max(res, count)
            count = 0
    return max(res, count)

#Return longest substring of consonants
def longestConsonant(s):
    vowels = ['a', 'e', 'i', 'o', 'u']
    count, res = 0, 0
    for i in range(len(s)):
        if (s[i] not in vowels):
            count += 1 
        else:
            res = max(res, count)
            count = 0
    return max(res, count)

#Return longest substring of numbers
def longestNum(domain):
    count, res = 0, 0
    for x in domain:
        if x.isdigit():
            count += 1
        else:
            res = max(res, count)
            count = 0
    return max(res, count)

#Return longest substring on special characters
def longestSpec(domain):
    count, res = 0, 0
    for x in domain:
        if x.isdigit():
            continue
        elif x.isalpha():
            continue
        else:
            res = max(res, count)
            count = 0
    return max(res, count)

#Return domain without TLD
def getTldFromUrl(url):
    try:
        site_url = 'http://{}'.format(url)
        return get_tld(site_url)
    except Exception as e:
        logging.error("Error in getTldFromUrl(): " + str(e))
        print(str(e))
        return 'null'

#Return Shannon entropy value
def entropyCalc(domain):
    try:
        domain = domain.replace(getTldFromUrl(domain), '')
        p, lens = Counter(domain), np.float(len(domain))
        return int(-np.sum(count / lens * np.log2(count / lens) for count in p.values()))
    except Exception as e:
        logging.error("Error in entropyCalc(): " + str(e))
        return 0

#Check if domain exists in Alexa DB
def existsInAlexaDb(domain):
    tld = getTldFromUrl(domain)
    tldSplitted = tld.split(".")[0]
    domain = domain.split(".")[domain.split(".").index(tldSplitted) - 1] + "." + tld
    with open('Input\\top-1m.csv') as f:
        if domain in f.read():
            return 1
    return 0

#Return strange character sequence
def getStrangeCharacters(domain):
    try:
        domain = re.sub(r'[a-zA-Z\.]+', '', domain)
        if len(domain) > 0:
            digits = sum(char.isdigit() for char in domain)
            digits = 0 if digits <= 2 else digits - 2
            domain = re.sub(r'[0-9]+', '', domain)
            return len(domain) + digits
        return 0
    except Exception as e:
        logging.error("Error on getStrangeCharacters(): " + str(e))
        return 0

#Check if IP is blacklisted
def getIpReputation(ip):
    ip_checker = pydnsbl.DNSBLIpChecker()
    try:
        result = ip_checker.check(ip)
        return int(result.blacklisted)
    except Exception as e:
        print("Exception in getIpReputation: {}" + str(e))
        logging.error("Exception in getIpReputation: {}" + str(e))
        return False

#Check if domain is blacklisted
def getDomainReputation(domain):
    domain_checker = pydnsbl.DNSBLDomainChecker()
    try:
        result = domain_checker.check(domain)
        return int(result.blacklisted)
    except Exception as e:
        print("Exception in getDomainReputation: {}" + str(e))
        logging.error("Exception in getDomainReputation: {}" + str(e))
        return False
