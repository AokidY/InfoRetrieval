from nltk.stem import PorterStemmer
import os, json
from cos import cos_ranking
from tokenkk import tokenize
from nltk.stem import PorterStemmer
import pickle


with open("inverted_index_tfidf.pkl", 'rb') as file:
    inverted_index = pickle.load(file)
with open('word_tag.pkl', 'rb') as file:
    word_tag = pickle.load(file)


def search(query):
  currentPath = os.getcwd()
  webPage = os.path.join(currentPath, 'DEV')
  cur = cos_ranking(query, inverted_index, word_tag, pageNum)[0:20]
  res = []
  for i, j in cur:
      with open(os.path.join(webPage, i), 'r', encoding='utf-8') as file:
          data = json.load(file)
          res.append(data['url'])
  for i in res:
      print(i)



if __name__ == "__main__":
    currentPath = os.getcwd()
    webPage = os.path.join(currentPath, 'DEV')
    pageNum = 0
    folderList = os.listdir(webPage)
    for i in folderList:
        folder = os.path.join(webPage, i)
        pageNum += len(os.listdir(folder))
    
    while True:
      info = input('Enter your query: ')
      if info == 'exit':
          break
      update_info = tokenize(info)
      query = []
      for word in update_info:
          query.append(PorterStemmer().stem(word))
      search(query)
