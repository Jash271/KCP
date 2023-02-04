from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import PyPDF2
import re


articles = pd.read_csv('data.csv')
# print(articles.head())
print(articles)

'''
data = list(articles['data'])
tagged_data = [TaggedDocument(words = word_tokenize(_d.lower()), tags = [str(i)]) for i, _d in enumerate(data)]


model = Doc2Vec(vector_size = 50,
min_count = 10,
epochs = 50
)

model.build_vocab(tagged_data)
k = model.wv.vocab.keys()
print(len(k))

model.train(tagged_data,
total_examples = model.corpus_count,
epochs = model.epochs)
model.save('doc2vec.model')
print("Model saved")


resume_path = 'resume.pdf'
resume = ''
pdfReader = PyPDF2.PdfFileReader(resume_path)
for i in range(pdfReader.numPages):
    pageObj = pdfReader.getPage(i)
    resume += pageObj.extractText()

resume = resume.lower()
resume = re.sub('[^a-z]', ' ', resume)

'''