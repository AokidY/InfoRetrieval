from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from nltk.stem import PorterStemmer
import os, json
from cos import cos_ranking
from bs4 import BeautifulSoup
from tokenkk import tokenize
import pickle
from cos import cos_ranking

interface = Blueprint(__name__, 'interface')

with open("inverted_index_tfidf.pkl", 'rb') as file:
    inverted_index = pickle.load(file)
with open('word_tag.pkl', 'rb') as file:
    word_tag = pickle.load(file)


@interface.route('/')
def homepage():
  return render_template('index.html')


@interface.route('/results', methods = ['POST'])
def exhibit_res():
  output = '<p>'
  query = request.form['req']
  update_query = [PorterStemmer().stem(x) for x in tokenize(query)]
  currentPath = os.getcwd()
  webPage = os.path.join(currentPath, 'DEV')
  pageNum = 0
  folderList = os.listdir(webPage)
  for i in folderList:
      folder = os.path.join(webPage, i)
      pageNum += len(os.listdir(folder))
  cur = cos_ranking(update_query, inverted_index, word_tag, pageNum)[0:20]
  count = 1
  for i, j in cur:
      with open(os.path.join(webPage, i), 'r', encoding='utf-8') as file:
          data = json.load(file)
          soup = BeautifulSoup(data['content'], 'html.parser')
          texts = soup.find_all(text=True)
          content = ''
          for t in texts:
              content += t.text
              if len(content)>400:
                content = content[:400] + '...'
                break
          output += "<span style='font-size: 20px'>{id}</span>. <a style='font-size: 25px' href={url}>{url}</a><br>".format(id=count, url=data['url'])
          output += "<span>{content}</span>".format(content=content)
      output += "<br>"
      count += 1
  output += "</p>"
  output += '''<form action='/'>
                    <input type='submit' value='go back' style='margin-left: 500px; width: 250px; height: 50px; font-size: 20px'>
                </form>'''
  output += "<input type='submit' value='top' onclick='scrollToTop()' style='margin-left: 500px; width: 250px; height: 50px; font-size: 20px'>"
  output += '''<script>function scrollToTop() {
                          window.scrollTo({
                            top: 0,
                            behavior: 'smooth'
                          })
                        }
              </script>'''
  return output
