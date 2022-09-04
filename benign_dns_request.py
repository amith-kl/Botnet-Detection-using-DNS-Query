import requests
import json
import csv
import get_features

with open('Input\\top-1m_0.csv') as file_obj:
    count1, count2 = 0, 0
    reader_obj = csv.reader(file_obj)
    for row in reader_obj:
        count1 += 1
        print("A " + str(count1))
        domain = row[1]
        api_url = 'https://api.api-ninjas.com/v1/dnslookup?domain={}'.format(domain)
        response = requests.get(api_url, headers={'X-Api-Key': 'OwyJf4r9DwYbFqhvkPxQUw==MSk7U6NfQas9Jx6F'})
        if response.status_code == requests.codes.ok:
            pass
        else:
            continue
    
        res = json.loads(response.text)

        flag1, flag2 = False, False
        y = {}
        for x in res:
            if 'mname' in x:
                flag1 = True
                y = x
                y['hasMX'] = False
                y['hasTXT'] = False
        for x in res:
            if x['record_type'] == 'MX':
                y['hasMX'] = True
            if x['record_type'] == 'TXT':
                y['hasTXT'] = True
            if x['record_type'] == 'A':
                flag2 = True
                y['ip'] = x['value']
        
        if flag1 and flag2:
            y['vowelRatio'] = get_features.vowelConsonantRatio(domain)[0]
            y['consonantRatio'] = get_features.vowelConsonantRatio(domain)[1]
            y['specialCharsRatio'] = get_features.specNumRatio(domain)[1]
            y['numericCharsRatio'] = get_features.specNumRatio(domain)[0]
            y['vowelSequence'] = get_features.longestVowel(domain)
            y['consonantSequence'] = get_features.longestConsonant(domain)
            y['numericSequence'] = get_features.longestNum(domain)
            y['specialSequence'] = get_features.longestSpec(domain)
            y['strangeCharacters'] = get_features.getStrangeCharacters(domain)
            y['domainInAlexaDB'] = get_features.existsInAlexaDb(domain)
            y['ipReputation'] = get_features.getIpReputation(y['ip'])
            y['domainReputation'] = get_features.getDomainReputation(domain)
            y['entropy'] = get_features.entropyCalc(domain)
            y['domain'] = domain
            y['domainLength'] = len(domain)

            count2 += 1
            print("B " + str(count2))
            json_object = json.dumps(y, indent = 4)
            with open('Output\\benign_response.json', 'a') as outfile:
                outfile.write(json_object + ",\n")
                outfile.seek(0)
