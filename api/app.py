from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
import pickle


#  popular books
popular_df = pickle.load(open("model/popular_df.pkl", 'rb'))

#pt dataframe
pt = pickle.load(open('model/pt.pkl', 'rb'))
#all books dataframe
books = pickle.load(open('model/books.pkl', 'rb'))


# model for recommendation
similarity_score = pickle.load(open("model/similarity_score.pkl", 'rb'))

# actual function
# def recommend(book_name):
#     recommended_books = []
#     index = np.where(pt.index==book_name)[0][0]
#     similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x:x[1], reverse=True)[1:6]

#     for i in similar_items:
#         recommended_books.append(pt.index[i[0]])

#     return recommended_books



def recommend(book_name):
    if book_name == "":
        return  ""
    else:
        index = np.where(pt.index==book_name)[0][0]
        similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x:x[1], reverse=True)[1:6]
        data = []
        try:
            for i in similar_items:
                items = []
                temp_df = books[books['Book-Title'] == pt.index[i[0]]]
                items.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
                items.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
                items.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
                data.append(items)
        except:
            return data

        return data


app = Flask(__name__)


@app.route('/')
def index():
    return "Hello world"


@app.route('/books', methods= ['POST'])
def getBooks():
    name = request.form.get('name')
    result = recommend(name)
    return jsonify(result)
    
    
@app.route('/popular', methods=['GET'])
def popular_books():
    popular_books_list = popular_df.values.tolist()
    return jsonify(popular_books_list)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')