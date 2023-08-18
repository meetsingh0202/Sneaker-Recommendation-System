from flask import Flask, render_template, request, redirect, session, url_for, jsonify
import pickle
import numpy as np
from collections import *

app = Flask(__name__)

shoes = pickle.load(open('shoes.pkl','rb'))
userCart = pickle.load(open('userCart.pkl','rb'))
currSession = pickle.load(open('session.pkl','rb'))

print(userCart)

users = { '1' : 'a', '2' : 'b'}

@app.route('/')
def index():
    return render_template('index.html', 
        shoeId = list(shoes['shoeId'].values),
        shoeBrand = list(shoes['shoeBrand'].values),
        shoeImage = list(shoes['shoeImage'].values),
        shoeCatagory = list(shoes['shoeCategory'].values),
        shoeColor = list(shoes['shoeColour'].values),
        shoePrice = list(shoes['shoePrice'].values),
        user = currSession,
        userCart = list(userCart[currSession]),
    )

@app.route("/getCartValues/<userId>")
def getCartValues(userId):
    return jsonify(list(userCart.get(userId, [])))

@app.route('/addToCart/<shoeId>')
def addToCart(shoeId):
    tempCart = userCart
    tempCart[currSession].add(shoeId)
    pickle.dump(tempCart, open('userCart.pkl','wb'))
    return render_template('index.html', 
            shoeId = list(shoes['shoeId'].values),
            shoeBrand = list(shoes['shoeBrand'].values),
            shoeImage = list(shoes['shoeImage'].values),
            shoeCatagory = list(shoes['shoeCategory'].values),
            shoeColor = list(shoes['shoeColour'].values),
            shoePrice = list(shoes['shoePrice'].values),
            user = currSession,
            userCart = list(tempCart[currSession]),
        )

@app.route('/removeFromCart/<shoeId>')
def removeFromCart(shoeId):
    tempCart = userCart
    tempCart[currSession].remove(shoeId)
    pickle.dump(tempCart, open('userCart.pkl','wb'))
    return render_template('index.html', 
            shoeId = list(shoes['shoeId'].values),
            shoeBrand = list(shoes['shoeBrand'].values),
            shoeImage = list(shoes['shoeImage'].values),
            shoeCatagory = list(shoes['shoeCategory'].values),
            shoeColor = list(shoes['shoeColour'].values),
            shoePrice = list(shoes['shoePrice'].values),
            user = currSession,
            userCart = list(tempCart[currSession]),
        )

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if users.get(username) == password:
        session['user'] = username
        pickle.dump(username, open('session.pkl','wb'))
        return render_template('index.html', 
            shoeId = list(shoes['shoeId'].values),
            shoeBrand = list(shoes['shoeBrand'].values),
            shoeImage = list(shoes['shoeImage'].values),
            shoeCatagory = list(shoes['shoeCategory'].values),
            shoeColor = list(shoes['shoeColour'].values),
            shoePrice = list(shoes['shoePrice'].values),
            user = username,
            userCart = list(userCart[currSession]),
        )
    else:
        return render_template('index.html', 
            shoeId = list(shoes['shoeId'].values),
            shoeBrand = list(shoes['shoeBrand'].values),
            shoeImage = list(shoes['shoeImage'].values),
            shoeCatagory = list(shoes['shoeCategory'].values),
            shoeColor = list(shoes['shoeColour'].values),
            shoePrice = list(shoes['shoePrice']),
            invalid = True,
            userCart = None,
        )

@app.route('/logout')
def logout():
    session.pop('user', None)
    pickle.dump(None, open('session.pkl','wb'))
    return render_template('index.html', 
            shoeId = list(shoes['shoeId'].values),
            shoeBrand = list(shoes['shoeBrand'].values),
            shoeImage = list(shoes['shoeImage'].values),
            shoeCatagory = list(shoes['shoeCategory'].values),
            shoeColor = list(shoes['shoeColour'].values),
            shoePrice = list(shoes['shoePrice'].values),
            user = None,
            userCart = None,
        )

# @app.route('/recommend')
# def recommend_ui():
#     return render_template('recommend.html')

# @app.route('/recommend_books',methods=['post'])
# def recommend():
#     user_input = request.form.get('user_input')
#     index = np.where(pt.index == user_input)[0][0]
#     similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

#     data = []
#     for i in similar_items:
#         item = []
#         temp_df = books[books['Book-Title'] == pt.index[i[0]]]
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

#         data.append(item)

#     print(data)

#     return render_template('recommend.html',data=data)

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug = True)
