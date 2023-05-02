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

from keyword_extraction_api import get_improvements

'''
Finally we will remove this function.
Not that much needed.
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

'''


def most_similar(resume_id, jd_id, similarity_matrix, matrix, documents_df) -> list:
    # print(f'Document: {documents_df.iloc[doc_id]["documents"]}')
    # print(f'Document: {documents_df.iloc[1]["documents"]}')
    return [matrix, similarity_matrix[resume_id][jd_id]]
    # return f'{matrix} between Resume and Job Description: {similarity_matrix[resume_id][jd_id]}'


# Checks the similarity between the inputs, using the already saved model.
def resume_jd_similarity(documents) -> list:
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

    return most_similar(0, 1, pairwise_similarities, 'Cosine Similarity', documents_df), tagged_data


# Extract information from the pdf resume in the form of a string.
def extract_resume(file_obj) -> str:
    resume = ''
    pdfReader = PyPDF2.PdfReader(file_obj)
    for i in range(len(pdfReader.pages)):
        pageObj = pdfReader.pages[i]
        resume += pageObj.extract_text()
    resume = resume.lower()
    resume = re.sub('\W+', ' ', resume)
    return resume


def get_response(jd_text, resume="", resume_obj=None) -> dict:
    # Fetch resume
    response = {}
    if resume == "":
        resume = extract_resume(resume_obj)

    # cal similarity
    documents = [resume, jd_text]
    sim_list, tagged_data = resume_jd_similarity(documents)
    response['similarity'] = [sim_list[0], sim_list[1]]
    # response += "\n\n\n"
    # response += get_improvements(resume, jd_text)
    response['results'] = get_improvements(resume, jd_text, tagged_data=tagged_data)
    return response


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
