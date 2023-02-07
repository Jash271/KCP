# nltk.download('punkt')
import re

import nltk
import numpy as np
import pandas as pd
import PyPDF2
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity

documents = [
    'Machine learning is the study of computer algorithms that improve automatically through experience.\
Machine learning algorithms build a mathematical model based on sample data, known as training data.\
The discipline of machine learning employs various approaches to teach computers to accomplish tasks \
where no fully satisfactory algorithm is available.',
    'Machine learning is closely related to computational statistics, which focuses on making predictions using computers.\
The study of mathematical optimization delivers methods, theory and application domains to the field of machine learning.',
    'Machine learning involves computers discovering how they can perform tasks without being explicitly programmed to do so. \
It involves computers learning from data provided so that they carry out certain tasks.',
    'Machine learning approaches are traditionally divided into three broad categories, depending on the nature of the "signal"\
or "feedback" available to the learning system: Supervised, Unsupervised and Reinforcement',
    'Software engineering is the systematic application of engineering approaches to the development of software.\
Software engineering is a computing discipline.',
    'A software engineer creates programs based on logic for the computer to execute. A software engineer has to be more concerned\
about the correctness of the program in all the cases. Meanwhile, a data scientist is comfortable with uncertainty and variability.\
Developing a machine learning application is more iterative and explorative process than software engineering.'
]


# Finally we will remove this function.
# Not that much needed.
def most_similar(doc_id, similarity_matrix, matrix, documents_df):
    print(f'Document: {documents_df.iloc[doc_id]["documents"]}')
    print('\n')
    print(f'Similar Documents using {matrix}:')
    if matrix == 'Cosine Similarity':
        similar_ix = np.argsort(similarity_matrix[doc_id])[::-1]
    elif matrix == 'Euclidean Distance':
        similar_ix = np.argsort(similarity_matrix[doc_id])
    for ix in similar_ix:
        if ix == doc_id:
            continue
        print('\n')
        print(f'Document: {documents_df.iloc[ix]["documents"]}')
        print(f'{matrix} : {similarity_matrix[doc_id][ix]}')


# Checks the similarity between the inputs, using the already saved model.
def resume_jd_similarity():
    pd.set_option('display.max_colwidth', 0)
    pd.set_option('display.max_columns', 0)

    documents_df = pd.DataFrame(documents, columns=['documents'])
    stop_words_l = stopwords.words('english')
    documents_df['documents_cleaned'] = documents_df.documents.apply(
        lambda x: " ".join(
            re.sub(r'[^a-zA-Z]', ' ', w).lower() for w in x.split()
            if re.sub(r'[^a-zA-Z]', ' ', w).lower() not in stop_words_l))

    tagged_data = [
        TaggedDocument(words=word_tokenize(doc), tags=[i])
        for i, doc in enumerate(documents_df['documents_cleaned'])
    ]
    model_d2v = Doc2Vec.load('doc2vec.model')

    document_embeddings = np.zeros((documents_df.shape[0], 100))
    for i in range(len(document_embeddings)):
        document_embeddings[i] = model_d2v.infer_vector(tagged_data[i][0])

    pairwise_similarities = cosine_similarity(document_embeddings)

    # print(type(pairwise_similarities))

    most_similar(0, pairwise_similarities, 'Cosine Similarity', documents_df)


# Extract information from the pdf resume in the form of a string.
def extract_resume() -> str:
    resume_path = '/Users/keshavbhalla/Desktop/KeshavBhalla_Resume.pdf'
    resume = ''
    pdfReader = PyPDF2.PdfReader(resume_path)
    for i in range(len(pdfReader.pages)):
        pageObj = pdfReader.pages[i]
        resume += pageObj.extract_text()
    resume = resume.lower()
    resume = re.sub('\W+', ' ', resume)
    return resume
    # print(resume)


def main():
    resume_jd_similarity()


if __name__ == "__main__":
    main()

'''
# USING BERTA

from sentence_transformers import SentenceTransformer
nltk.download('stopwords')


stop_words_l=stopwords.words('english')
documents_df['documents_cleaned']=documents_df.documents.apply(lambda x: " ".join(re.sub(r'[^a-zA-Z]',' ',w).lower() for w in x.split() if re.sub(r'[^a-zA-Z]',' ',w).lower() not in stop_words_l) )
# print(documents_df['documents_cleaned'])
sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')

document_embeddings = sbert_model.encode(documents_df['documents_cleaned'])
# document_embeddings = sbert_model.encode(documents_df)
pairwise_similarities=cosine_similarity(document_embeddings)
pairwise_differences=euclidean_distances(document_embeddings)
most_similar(0,pairwise_similarities,'Cosine Similarity')

'''