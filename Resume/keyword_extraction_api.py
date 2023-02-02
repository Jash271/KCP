import json
from collections import Counter

import requests
from spellchecker import SpellChecker
from textblob import TextBlob

url = "https://508uo293jg.execute-api.us-east-1.amazonaws.com/get_keyword"

# Function accepts string as an argument and returns an Json dictionary
def text_to_keys(str)->dict:
    payload = json.dumps({
        "text": str
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if(not response.ok):
        print("ERROR")
        # return {}
        # how exactly are we gonna handle this ??

    json_dict = response.json()['result']
    response.close()
    return json_dict


def fn()->dict:
    pass

# how to do matching
# remember we are going to have multiple input strings, corresponding to every box (skills, experience etc)
# looking for grammar and speeling mistakes in the strings and see repetitive words
# how to find out degree
# infer skills from extra curr
# see more about comprehend_client


def get_input_str()->str:
    s = "Python Java Implemented a Microsoft PowerPlatform Application to automate access requests \
        for S/4 systems by reducing manual effort by around 60% Integrated GSAP (SAP ECC system) with a 3rd party tool\
        Hexagon for replacing legacy system to cloud. Analyzed and managed defect management process to ensure no delays \
        in deployment Piloted and built a S4 Role Repository application in Microsoft PowerPlatform integrated \
        with MS SQL server to streamline CRUD operations for role management Enhanced ABAP (Advanced Business\
        Application Programming) reports and scripts to generate netting documents, archive it in OpenText \
        and email user to optimize month end process"
    return s


def get_job_description()->str:
    s  = "Exposed data in a machine-friendly format and designed an efficient pre-processing module for handling bulk\
         and real-time data requests, reducing overall latency from minutes to a few seconds. Modified service responsible\
             for generating stats of components, to get access to and modify data on a granular level. Setting up an automation\
                 pipeline for data extraction from Stargate service and insertion into TimescaleDB. Designed a data analytics \
                    module for finding errors/abnormalities on high workload data and plotting results on Grafana, which \
                        allowed us to query, visualise and understand metrics through dynamic & reusable dashboards.\
                            Led a 6 member team Python Java during an internal hackathon and created a service for performing Metadata Analysis for buckets in Amazon S3."

    return s


def check_repetitive_words(s: str):
    str_list = s.split()
 
    frequency = Counter(str_list)
    # most_freq_words = frequency.most_common()[:5]
    most_freq_words = Counter({k: c for k, c in frequency.items() if c > 3})
    return most_freq_words
    

def entities_dict(json_dict: dict):
    quantifiable_entities = 0
    key_dict = {}
    for i in json_dict:
        if i['Type'] == 'QUANTITY':
            quantifiable_entities+=1
        # org should have more value then normal titles ??
        if i['Type'] == 'ORGANIZATION' or i['Type'] == 'TITLE':
            key_dict[i['Text']]=1
    return quantifiable_entities, key_dict


def main():
    input_str = get_input_str()
    jd_str = get_job_description()

    json_dict = text_to_keys(input_str)
    jb_json_dict = text_to_keys(jd_str)
    
    q, key_dict = entities_dict(json_dict=jb_json_dict['Entities'])
    quantifiable_entities, temp_dict = entities_dict(json_dict=json_dict['Entities'])

    shared_items = {k: key_dict[k] for k in key_dict if k in temp_dict and key_dict[k] == temp_dict[k]}
    print("Percentage Match with Job Description : ", (len(shared_items)/len(key_dict))*100)
    if quantifiable_entities < 5 :
        print("You have only", quantifiable_entities ,"quantifiable entities, add more !!")
        
    most_freq_words =  check_repetitive_words(s=input_str)
    if len(most_freq_words) != 0:
        print("These are the most frequent words. Try to reduce their frequency")
        print(most_freq_words)


    spell = SpellChecker()
 
    # Find those words that may be misspelled
    misspelled = spell.unknown(input_str.split())
    print("Please check the spelling of the following words.")
    print(misspelled)


if __name__ == "__main__":
    main()
