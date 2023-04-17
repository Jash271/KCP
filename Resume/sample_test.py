# Recommend jobs to user (kind of like a job alert)
# Create a discuss section....(Kind of like leetcode experience with company tags and position tags)
# 
# 



'''

str  = "Exposed data in a machine-friendly format and designed an efficient pre-processing module for handling bulk\
         and real-time data requests, reducing overall latency from minutes to a few seconds. Modified service responsible\
             for generating stats of components, to get access to and modify data on a granular level. Setting up an automation\
                 pipeline for data extraction from Stargate service and insertion into TimescaleDB. Designed a data analytics \
                    module for finding errors/abnormalities on high workload data and plotting results on Grafana, which \
                        allowed us to query, visualise and understand metrics through dynamic & reusable dashboards.\
                            Led a 6 member team during an internal hackathon and created a service for performing Metadata Analysis for buckets in Amazon S3."




str = "Implemented a Microsoft PowerPlatform Application to automate access requests \
    for S/4 systems by reducing manual effort by around 60% Integrated GSAP (SAP ECC system) with a 3rd party tool\
         Hexagon for replacing legacy system to cloud. Analyzed and managed defect management process to ensure no delays \
            in deployment Piloted and built a S4 Role Repository application in Microsoft PowerPlatform integrated \
                with MS SQL server to streamline CRUD operations for role management Enhanced ABAP (Advanced Business\
                     Application Programming) reports and scripts to generate netting documents, archive it in OpenText \
                        and email user to optimize month end process"

'''



'''
Entities
[{'Score': 0.920968770980835, 'Type': 'ORGANIZATION', 'Text': 'Microsoft', 'BeginOffset': 14, 'EndOffset': 23}, 
{'Score': 0.7453033328056335, 'Type': 'TITLE', 'Text': 'PowerPlatform', 'BeginOffset': 24, 'EndOffset': 37}, 
{'Score': 0.6596642732620239, 'Type': 'TITLE', 'Text': 'S/4', 'BeginOffset': 86, 'EndOffset': 89}, 
{'Score': 0.9821351170539856, 'Type': 'QUANTITY', 'Text': 'around 60%', 'BeginOffset': 127, 'EndOffset': 137}, 
{'Score': 0.8562743663787842, 'Type': 'TITLE', 'Text': 'GSAP', 'BeginOffset': 149, 'EndOffset': 153}, 
{'Score': 0.8194435834884644, 'Type': 'TITLE', 'Text': 'SAP ECC', 'BeginOffset': 155, 'EndOffset': 162}, 
{'Score': 0.6881545186042786, 'Type': 'TITLE', 'Text': 'S4', 'BeginOffset': 360, 'EndOffset': 362}, 
{'Score': 0.901006817817688, 'Type': 'ORGANIZATION', 'Text': 'Microsoft', 'BeginOffset': 394, 'EndOffset': 403},
{'Score': 0.676632821559906, 'Type': 'TITLE', 'Text': 'PowerPlatform', 'BeginOffset': 404, 'EndOffset': 417}, 
{'Score': 0.7878288626670837, 'Type': 'TITLE', 'Text': 'MS', 'BeginOffset': 450, 'EndOffset': 452}, 
{'Score': 0.5886542797088623, 'Type': 'TITLE', 'Text': 'SQL', 'BeginOffset': 453, 'EndOffset': 456}, 
{'Score': 0.990151047706604, 'Type': 'TITLE', 'Text': 'OpenText', 'BeginOffset': 657, 'EndOffset': 665}]

'''

'''
[{'Score': 0.7132087349891663, 'Type': 'QUANTITY', 'Text': 'minutes', 'BeginOffset': 175, 'EndOffset': 182},
 {'Score': 0.7615995407104492, 'Type': 'QUANTITY', 'Text': 'a few seconds', 'BeginOffset': 186, 'EndOffset': 199}, 
 {'Score': 0.933834969997406, 'Type': 'ORGANIZATION', 'Text': 'Stargate', 'BeginOffset': 407, 'EndOffset': 415}, 
 {'Score': 0.8402552604675293, 'Type': 'TITLE', 'Text': 'TimescaleDB', 'BeginOffset': 443, 'EndOffset': 454},
  {'Score': 0.5375434756278992, 'Type': 'ORGANIZATION', 'Text': 'Grafana', 'BeginOffset': 588, 'EndOffset': 595},
  {'Score': 0.8808475732803345, 'Type': 'QUANTITY', 'Text': '6 member team', 'BeginOffset': 753, 'EndOffset': 766}, 
  {'Score': 0.8264933228492737, 'Type': 'ORGANIZATION', 'Text': 'Amazon', 'BeginOffset': 866, 'EndOffset': 872}, 
  {'Score': 0.6682716012001038, 'Type': 'TITLE', 'Text': 'S3', 'BeginOffset': 873, 'EndOffset': 875}]
'''



'''
suggestions
we cant rely just on the JD. Need more data to do matching (maybe create a dataset and store data corresponding to every position (generic for every company))
the above thing will improve similarity score and also help in giving suggestions, like we can suggest keywords from our dataset.


Resume generator 
Parallel computaion dekhle (do paraphrasing on gpu than cpu's)  Ray, Hugg Do Face ||ism

'''


# tranformers has different models
# see which one to use
# see t5 (not giving very good output though)
# or pegasus (taking lot of time to process, not sure if it is the correct one since used to give summary.)

# import torch
# from transformers import PegasusForConditionalGeneration, PegasusTokenizer
# from sentence_splitter import SentenceSplitter, split_text_into_sentences

# model_name = 'tuner007/pegasus_paraphrase'
# torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
# tokenizer = PegasusTokenizer.from_pretrained(model_name)
# model = PegasusForConditionalGeneration.from_pretrained(model_name).to(torch_device)
# model.save('temp.model')

# print("hello")
# def get_response(input_text,num_return_sequences):
#   batch = tokenizer.prepare_seq2seq_batch([input_text],truncation=True,padding='longest',max_length=60, return_tensors="pt").to(torch_device)
#   translated = model.generate(**batch,max_length=60,num_beams=10, num_return_sequences=num_return_sequences, temperature=1.5)
#   tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
#   return tgt_text
     
# text = "Exposed data in a machine-friendly format and designed an efficient pre-processing module for handling bulk and real-time data requests, reducing overall latency from minutes to a few seconds.\
#     Modified service responsible for generating stats of components, to get access to and modify data on a granular level. Setting up an automation pipeline for data extraction from Stargate service and insertion into TimescaleDB.\
#     Designed a data analytics module for finding errors/abnormalities on high workload data and plotting results on Grafana, which allowed us to query, visualise and understand metrics through dynamic & reusable dashboards.\
#     Led a 6 member team during an internal hackathon and created a service for performing Metadata Analysis for buckets in Amazon S3."


# splitter = SentenceSplitter(language='en')

# sentence_list = splitter.split(text)
# # sentence_list
# paraphrase = []

# for i in sentence_list:
#   a = get_response(i,1)
#   paraphrase.append(a)

# paraphrase2 = [' '.join(x) for x in paraphrase]
# paraphrase3 = [' '.join(x for x in paraphrase2) ]
# paraphrased_text = str(paraphrase3).strip('[]').strip("'")
# print(paraphrased_text)

# print(get_response(text, 5))

# text = "Exposed data in a machine-friendly format and designed an efficient pre-processing module."
     
# print(get_response(text, 5))


'''
import torch
import warnings
warnings.filterwarnings("ignore")

from parrot import Parrot

# def random_state(seed):
#   torch.manual_seed(seed)
#   if torch.cuda.is_available():
#     torch.cuda.manual_seed_all(seed)

# random_state(1234)

def method2():
  sentence = "Learning is the process of acquiring new understanding, knowledge, behaviors, skills, values, attitudes, and preferences."
  parrot = Parrot()
  print(type(parrot))
  phrases = [
    sentence,
    "One of the best ways to learn is to teach what you've already learned",
    "Paraphrasing is the process of coming up with someone else's ideas in your own words"
  ]

  for phrase in phrases:
    print("-"*100)
    print("Input_phrase: ", phrase)
    print("-"*100)
    paraphrases = parrot.augment(input_phrase=phrase, max_return_phrases = 3, do_diverse=False)
    if paraphrases:
      for paraphrase in paraphrases:
        print(paraphrase)


# method1()
method2()

'''

from multiprocessing import Process
import warnings
warnings.filterwarnings("ignore")

from parrot import Parrot



def method2(phrase, parrot)->str:
  temp = ""
  paraphrases = parrot.augment(input_phrase=phrase, max_return_phrases = 4, do_diverse=False)
  if paraphrases:
    for paraphrase in paraphrases:
      temp+=str(paraphrase[0])
      temp+='\n'
  return temp

# Test this using Ray and GPU waali bkc

# def main():
#     parrot = Parrot()
#     phrases = [
#       "Learning is the process of acquiring new understanding, knowledge, behaviors, skills, values, attitudes, and preferences",
#       "One of the best ways to learn is to teach what you've already learned",
#       "Paraphrasing is the process of coming up with someone else's ideas in your own words",
#       "Paraphrasing is the process of coming up with someone else's ideas in your own words",
#       "Paraphrasing is the process of coming up with someone else's ideas in your own words",
#       "One of the best ways to learn is to teach what you've already learned",
#       "Paraphrasing is the process of coming up with someone else's ideas in your own words",
#       "Learning is the process of acquiring new understanding, knowledge, behaviors, skills, values, attitudes, and preferences",
#       "One of the best ways to learn is to teach what you've already learned",
#       "Paraphrasing is the process of coming up with someone else's ideas in your own words",
#       "Paraphrasing is the process of coming up with someone else's ideas in your own words",
#       "Paraphrasing is the process of coming up with someone else's ideas in your own words",
#       "One of the best ways to learn is to teach what you've already learned",
#       "Paraphrasing is the process of coming up with someone else's ideas in your own words",
#       "Learning is the process of acquiring new understanding, knowledge, behaviors, skills, values, attitudes, and preferences",
#       "One of the best ways to learn is to teach what you've already learned",
#       "Paraphrasing is the process of coming up with someone else's ideas in your own words",
#       "Paraphrasing is the process of coming up with someone else's ideas in your own words",
#       "Paraphrasing is the process of coming up with someone else's ideas in your own words",
#       "One of the best ways to learn is to teach what you've already learned",
#       "Paraphrasing is the process of coming up with someone else's ideas in your own words",
#       "Learning is the process of acquiring new understanding, knowledge, behaviors, skills, values, attitudes, and preferences",
#       "One of the best ways to learn is to teach what you've already learned",
#       "Paraphrasing is the process of coming up with someone else's ideas in your own words",
#       "Paraphrasing is the process of coming up with someone else's ideas in your own words",
#       "Paraphrasing is the process of coming up with someone else's ideas in your own words",
#       "One of the best ways to learn is to teach what you've already learned",
#       "Paraphrasing is the process of coming up with someone else's ideas in your own words"
#     ]
#     procs = []
#     start = time.time()
#     for phrase in phrases:
#         print("-"*100)
#         print("Input_phrase: ", phrase)
#         print("-"*100)

#         proc = Process(target=method2, args=(phrase,parrot))  # instantiating without any argument
#         procs.append(proc)
#         proc.start()

#     for proc in procs:
#         proc.join()
#     end = time.time()
#     print(end - start)

import pickle
import os.path

# Code to generate test.pickle (needed only once)
# parrot = Parrot()
# with open("test.pickle", "wb") as outfile:
#   pickle.dump(parrot, outfile)

def fn2(p_text)->str:

  if not os.path.isfile('test.pickle'):
    parrot = Parrot()
    with open("test.pickle", "wb") as outfile:
      pickle.dump(parrot, outfile)

  with open("test.pickle", "rb") as infile:
    parrot = pickle.load(infile)

  phrases = p_text.split('.')
  ans = ''
  for phrase in phrases:
    temp = method2(phrase=phrase, parrot=parrot)

    if temp == "":
      temp = phrase
    ans+=temp
    ans+='\n\n'
  return ans
  

if __name__ == '__main__':
    # main()
    fn2()
