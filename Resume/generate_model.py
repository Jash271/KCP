# nltk.download('punkt')
import re

import nltk
import pandas as pd
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize

# Cleaning the input data in the dataset.
def cleanResume(resumeText):
    resumeText = re.sub('http\S+\s*', ' ', resumeText)  # remove URLs
    resumeText = re.sub('RT|cc', ' ', resumeText)  # remove RT and cc
    resumeText = re.sub('#\S+', '', resumeText)  # remove hashtags
    resumeText = re.sub('@\S+', '  ', resumeText)  # remove mentions
    # resumeText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', resumeText)  # remove punctuations
    resumeText = re.sub('[%s]' %
                        re.escape("""!"#$%&'()*+,-/;<=>?@[\]^_`{|}~"""), ' ',
                        resumeText)  # remove punctuations
    resumeText = re.sub(r'[^\x00-\x7f]', r' ', resumeText)
    resumeText = re.sub('\s+', ' ', resumeText)  # remove extra whitespace
    return resumeText

# Intializes, trains and saves the model.
def make_model():
    resumeDataSet = pd.read_csv('UpdatedResumeDataSet.csv', encoding='utf-8')
    # resumeDataSet = pd.read_csv('Resume.csv' ,encoding='utf-8')
    resumeDataSet['cleaned_resume'] = ''
    print(resumeDataSet.info())
    resumeDataSet['cleaned_resume'] = resumeDataSet.Resume.apply(
        lambda x: cleanResume(x))
    # resumeDataSet['cleaned_resume'] = resumeDataSet.Resume_str.apply(lambda x: cleanResume(x))

    model_d2v = Doc2Vec(vector_size=100, alpha=0.025, min_count=1)
    tagged_data = [
        TaggedDocument(words=word_tokenize(doc), tags=[i])
        for i, doc in enumerate(resumeDataSet['cleaned_resume'])
    ]
    '''
        At the end of build_vocab(), all memory/objects needed for the model have been created. 
        Per the needs of the underlying algorithm, all vectors will have been initialized to low-magnitude random vectors 
        to ready the model for training.
    '''
    model_d2v.build_vocab(tagged_data)
   
    for epoch in range(25):
        model_d2v.train(tagged_data,
                        total_examples=model_d2v.corpus_count,
                        epochs=model_d2v.epochs)

    model_d2v.save('doc2vec.model')


def main():
    make_model()


if __name__ == "__main__":
    main()
