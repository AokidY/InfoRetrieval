import os, json
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from tokenkk import tokenize
from tfidf import tfidf_value
import pickle


tag_importance = {
    'title': 1.5,
    'h1': 1.4,
    'h2': 1.3,
    'h3': 1.2,
    'strong': 1.2,
    'b': 1.2,
    'other': 1
}

wordCount = dict()
inverted_index = dict()
word_tag = dict()
pageNum = []
allURL = []
word = set()
test = set()

with open('stop_words.txt', 'r', encoding='utf-8') as file:
    content = file.read()
    content_without_newlines = content.replace('\n', ' ')
    stop_words = content_without_newlines.split()





def add_inverted_index(word, file):
    if word not in inverted_index:
        inverted_index[word] = dict()
        inverted_index[word][file] = 1
    else:
        if file not in inverted_index[word]:
            inverted_index[word][file] = 1
        else:
            inverted_index[word][file] += 1
    # print(inverted_index)


def add_word_tag(word, file, tag):
    if tag not in tag_importance:
        tag = 'other'
    if word not in word_tag:
        word_tag[word] = dict()
        word_tag[word][file] = tag_importance[tag]
    else:
        if file not in word_tag[word]:
            word_tag[word][file] = tag_importance[tag]
        else:
            if tag_importance[tag] > word_tag[word][file]:
                word_tag[word][file] = tag_importance[tag]
    
    # print(word_tag)

        


def run():
    currentPath = os.getcwd()
    webPage = os.path.join(currentPath, 'DEV')
    folderList = os.listdir(webPage)
    for i in folderList:
        folder = os.path.join(webPage, i)
        pageNum.append(len(os.listdir(folder)))
        for j in os.listdir(folder):
            with open(os.path.join(folder, j), 'r', encoding='utf-8') as file:
                data = json.load(file)
                allURL.append(data['url'])
                soup = BeautifulSoup(data['content'], 'html.parser')
                texts = soup.find_all(text=True)
                content = ''
                token_lst = []
                for t in texts:
                    content += t.text
                    # test.add(t.parent.name)
                    for each in tokenize(t.text):
                        token_lst.append((each, t.parent.name))
                # print(content)
                key = str(i) + '/' + str(j)
                print(key)
                # print(token_lst)
                for word, tag in token_lst:
                    stemmed_words = PorterStemmer().stem(word)
                    if stemmed_words not in stop_words and len(stemmed_words)>1:
                        add_inverted_index(stemmed_words, key)
                        add_word_tag(stemmed_words, key, tag)
                # break
        # break

    tfidf_value(sum(pageNum), inverted_index)
    with open("inverted_index_tfidf.pkl", "wb") as file:
        pickle.dump(inverted_index, file, protocol=pickle.HIGHEST_PROTOCOL)
    
    with open("word_tag.pkl", "wb") as file:
        pickle.dump(word_tag, file, protocol=pickle.HIGHEST_PROTOCOL)



if __name__ == "__main__":
    run()
