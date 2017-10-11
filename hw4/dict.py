from flask import Flask, render_template, request, url_for
import re
import sqlite3
import csv

app = Flask (__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search',  methods=['get'])
def search():
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
    return render_template('search.html', results = results, results_num = results_num)

@app.route('/word/<word>')
def word(word):
    with open('data.csv', encoding='utf-8') as csvfile:
        data = csv.DictReader(csvfile)
        word_info = {}
        for row in data:
            if word in row['translation'] or word in row['hamnosys']:
                word_info = row
    return render_template('word.html', results = word_info)


if __name__ == '__main__':
    app.run(debug = True)

