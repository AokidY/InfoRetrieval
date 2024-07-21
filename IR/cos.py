import math
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
import os, json, sys, re
from nltk.stem import PorterStemmer
import pickle


# cos_similarity function: (a * b) / (||a|| * ||b||)

def query_tf_idf(term: str, query: list, num_docs: int, inverted_index: dict) -> float:
        tf_val = 1 + math.log(query.count(term))
        num_docs_with_term = len(inverted_index[term])# increment num of doc as counting query as doc
        idf_val = math.log(num_docs/num_docs_with_term)
        return tf_val * idf_val


def cos_ranking(query, inverted_index, tag_index, num_docs) -> dict:
    query_vec = dict() 
    query_len = 0

    doc_vec = dict() 
    doc_len = 0
    
    for term in query:
        if term in inverted_index:
            query_vec[term] = query_tf_idf(term, query, num_docs, inverted_index)
            query_len += math.pow(query_vec[term], 2)

            for docID, tfidf in inverted_index[term].items():
                if not term in doc_vec:
                    doc_vec[term] = dict()

                if not docID in doc_vec[term]:
                    doc_vec[term][docID] = tfidf

                else:
                    doc_vec[term][docID] += tfidf

                doc_len += math.pow(tfidf, 2)
    scores = dict()
    for term in query_vec:
        for docID in doc_vec[term]:
            if not docID in scores:
                scores[docID] = (query_vec[term] / math.sqrt(query_len)) * (doc_vec[term][docID]/math.sqrt(doc_len))
            else:
                scores[docID] += (query_vec[term] / math.sqrt(query_len)) * (doc_vec[term][docID]/math.sqrt(doc_len))
            
            scores[docID] += (tag_index[term][docID])

    search_res = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return search_res


if __name__ == "__main__":
    with open("inverted_index_tfidf.pkl", 'rb') as file:
        inverted_index = pickle.load(file)
    with open('word_tag.pkl', 'rb') as file:
        word_tag = pickle.load(file)
    test = ['Iftekhar', 'ahmed']
    update = []
    for i in test:
        update.append(PorterStemmer().stem(i))

    cur = cos_ranking(update, inverted_index, word_tag, 55393)[0:10]
    currentPath = os.getcwd()
    webPage = os.path.join(currentPath, 'DEV')
    res = []
    for i, j in cur:
        with open(os.path.join(webPage, i), 'r', encoding='utf-8') as file:
            data = json.load(file)
            res.append(data['url'])
    for i in res:
        print(i)

  

  
    
  