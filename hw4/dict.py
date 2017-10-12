from flask import Flask, render_template, request, url_for
import re
from math import log
from collections import Counter,  defaultdict
import glob
from pymystem3 import Mystem
import operator
from IPython.display import HTML, display


app = Flask (__name__)

def score_BM25(n, qf, N, dl, avdl):
    K = compute_K(dl, avdl)
    IDF = log((N - n + 0.5) / (n + 0.5))
    frac = ((k1 + 1) * qf) / (K + qf)
    
    return IDF * frac
    

def compute_K(dl, avdl):
    return k1 * ((1-b) + b * (float(dl)/float(avdl))) 

def BM25_foralldocs(query, list_of_word_massives, frequency, index_dict, BM25_for_all, stop_words):
    
    avdl = 0
    total_dl = 0
    
    for doc in list_of_word_massives:
        total_dl += len(doc)
        
    for n_text, doc in enumerate(list_of_word_massives):
        for word in query:
            if word not in doc or word in word in stop_words:
                pass
            else:
                score = score_BM25(len(index_dict[word]), frequency[str(n_text)][word], len(list_of_word_massives),
                                   len(list_of_word_massives[n_text]), (total_dl/len(list_of_word_massives)))
                if str(n_text) in BM25_for_all:
                    BM25_for_all[str(n_text)] = BM25_for_all[str(n_text)] + score
                else:
                    BM25_for_all[str(n_text)] = score
        
    if  BM25_for_all == {}:
        print('Ничего не найдено')
        
    return BM25_for_all

def text_to_words_massive(list_of_docs, stop_words):                                                               
    list_of_word_massives = []
    
    for doc in list_of_docs:
        
        m = Mystem()
        all_words = m.lemmatize(open(doc, 'r', encoding='UTF-8').read())
        
        all_words_clean = []
        for w in all_words:
            if w in stop_words or re.search('[А-Яа-я]', w) == None:
                pass
            else:
                all_words_clean.append(w)
                
        list_of_word_massives.append(all_words_clean)
        
    return list_of_word_massives



def reverse_index(list_of_word_massives, index_dict):
    #функция выдающая массив индексов для каждого слова в коллекции документов
    for n_text, doc in enumerate(list_of_word_massives):
        for word in set(doc):
            index_dict.setdefault(word, [])
            if str(n_text) not in index_dict[word]:
                index_dict[word].append(str(n_text))

    return index_dict





@app.route('/', methods=['get'])
def index():
    #text = request.form['text']
    with open('data.csv', encoding='utf-8') as csvfile:
        data = csv.DictReader(csvfile)

    #conn = sqlite3.connect('data.csv')
        results = []
        results_num = 0
        for row in data:
            if request.values['request'] in row['translation'] or request.values['request'] in row['hamnosys']:
                results.append(row)
                results_num += 1
    return render_template('index.html', results = results, results_num = results_num)


if __name__ == '__main__':
    app.run(debug = True)

