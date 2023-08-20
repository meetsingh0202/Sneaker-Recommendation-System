from flask import Flask, render_template, request, redirect, session, url_for, jsonify
import pickle
import numpy as np
from collections import *
import csv

app = Flask(__name__, static_url_path='/static')

shoes = pickle.load(open('shoes.pkl','rb'))
userCart = pickle.load(open('userCart.pkl','rb'))
currSession = pickle.load(open('session.pkl','rb'))

sneakers = {}

with open("ShoeDatabaseFinal.csv", "r") as db:
    csv_reader = csv.reader(db)
    count = 0
    for row in csv_reader:
        if count == 0:
            count += 1
            continue
        id, brand, categories, colors, imageUrl, price, rating = row
        sneakers[int(id)] = {"shoeId" : id, "brand": brand, "categories": categories, "colors": colors, "imageUrl": imageUrl, "price": price, 'rating': rating}

users = { '1' : 'a', '2' : 'b'}

bestSellerShoes = []
for i in sneakers:
    currItem = []
    for fields in sneakers[int(i)]:
        currItem.append(sneakers[int(i)][fields])
    bestSellerShoes.append(currItem)

bestSellerShoes.sort(key=lambda x : x[-1], reverse=True)
bestSellerShoes = bestSellerShoes[:52]

@app.route('/bestSellers')
def bestSellers():
    currSession = pickle.load(open('session.pkl','rb'))
    return render_template('bestSellers.html', 
        bestSeller = bestSellerShoes, 
        user = currSession,
        userCart = list(userCart[currSession]),
    )

@app.route("/getCartValues/<userId>")
def getCartValues(userId):
    print(userCart)
    return jsonify(list(userCart.get(userId, [])))

@app.route('/addToCart/<shoeId>')
def addToCart(shoeId):
    currSession = pickle.load(open('session.pkl','rb'))
    tempCart = userCart
    tempCart[currSession].add(shoeId)
    pickle.dump(tempCart, open('userCart.pkl','wb'))
    return render_template('bestSellers.html', 
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
    currSession = pickle.load(open('session.pkl','rb'))
    tempCart = userCart
    tempCart[currSession].remove(shoeId)
    pickle.dump(tempCart, open('userCart.pkl','wb'))
    return render_template('bestSellers.html', 
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
    print(username, password)
    if users.get(username) == password and username != None:
        session['user'] = username
        pickle.dump(username, open('session.pkl','wb'))
        return render_template('homepage.html', 
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
        return render_template('homepage.html', 
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
    return render_template('homepage.html', user = None)

@app.route('/openCart')
def openCart():
    currSession = pickle.load(open('session.pkl','rb'))
    res = []
    for i in userCart[currSession]:
        currItem = []
        for fields in sneakers[int(i)]:
            currItem.append(sneakers[int(i)][fields])
        res.append(currItem)
    return render_template('openCart.html', currCart = res, user = currSession)

@app.route('/')
def home():
    currSession = pickle.load(open('session.pkl','rb'))
    return render_template('homepage.html', user = currSession,shoeId = list(shoes['shoeId'].values),
        shoeBrand = list(shoes['shoeBrand'].values),
        shoeImage = list(shoes['shoeImage'].values),
        shoeCatagory = list(shoes['shoeCategory'].values),
        shoeColor = list(shoes['shoeColour'].values),
        shoePrice = list(shoes['shoePrice'].values),)

@app.route('/recommend')
def recommend():

    def getRecommendations(currUserId):
        # Mock dataset: User interactions (collaborative filtering)
        user_interactions = userCart

        # Calculate collaborative similarity (mock values)
        def collaborative_similarity(user1, user2):
            if user1 in user_interactions and user2 in user_interactions:
                intersection = len(set(user_interactions[user1]) & set(user_interactions[user2]))
                union = len(set(user_interactions[user1]) | set(user_interactions[user2]))

                if intersection == 0 or union == 0:
                    return 0
                    
                return intersection / union
            else:
                return 0.0

        # Calculate content-based similarity (mock values)
        def content_based_similarity(sneaker1, sneaker2):
            shared_attributes = sum(sneaker1[attr] == sneaker2[attr] for attr in ['brand', 'categories', 'colors', 'price', 'rating'])
            total_attributes = len(['brand', 'categories', 'colors', 'price', 'rating'])
            return shared_attributes / total_attributes

        # Hybrid recommendation algorithm
        def hybrid_recommendation(user_id, num_recommendations=20, collaborative_weight=1, content_based_weight=0.5):
            user_interacted_sneakers = user_interactions.get(user_id, [])
            
            collaborative_scores = {}
            content_based_scores = {}
            
            for other_user in user_interactions:
                if other_user != user_id:
                    collaborative_scores[other_user] = collaborative_similarity(user_id, other_user)
            
            for sneaker_id, sneaker in sneakers.items():
                content_based_scores[sneaker_id] = 0
                for user_sneaker_id in user_interacted_sneakers:
                    content_based_scores[sneaker_id] += content_based_similarity(sneaker, sneakers[int(user_sneaker_id)])
            
            recommendations = []
            for sneaker_id in sneakers:
                hybrid_score = (collaborative_weight * np.mean(list(collaborative_scores.values()))) + (content_based_weight * content_based_scores[sneaker_id])
                recommendations.append((sneaker_id, hybrid_score))
            
            recommendations.sort(key=lambda x: x[1], reverse=True)
            recommended_sneakers = []

            for sneaker_id, _ in recommendations[:num_recommendations]:
                if str(sneaker_id) not in user_interacted_sneakers:
                    recommended_sneakers.append(sneaker_id) 
            
            res = []
            for i in recommended_sneakers:
                currItem = []
                for fields in sneakers[i]:
                    currItem.append(sneakers[i][fields])
                res.append(currItem)
            return res

        return hybrid_recommendation(currUserId)

    currSession = pickle.load(open('session.pkl','rb'))
    recommendedData = getRecommendations(currSession)

    if currSession == None:
        return render_template('recommend.html',
            user = None,
            userCart = list(userCart[currSession]),
            emptyRecommendation = True,
            personalisedRecommendation = None,
        )

    if len(userCart[currSession]) == 0:
        return render_template('recommend.html',
            shoeId = list(shoes['shoeId'].values),
            shoeBrand = list(shoes['shoeBrand'].values),
            shoeImage = list(shoes['shoeImage'].values),
            shoeCatagory = list(shoes['shoeCategory'].values),
            shoeColor = list(shoes['shoeColour'].values),
            shoePrice = list(shoes['shoePrice'].values),
            user = currSession,
            userCart = list(userCart[currSession]),
            emptyRecommendation = True,
            personalisedRecommendation = None,
        )
    else:
        return render_template('recommend.html',
            shoeId = list(shoes['shoeId'].values),
            shoeBrand = list(shoes['shoeBrand'].values),
            shoeImage = list(shoes['shoeImage'].values),
            shoeCatagory = list(shoes['shoeCategory'].values),
            shoeColor = list(shoes['shoeColour'].values),
            shoePrice = list(shoes['shoePrice'].values),
            user = currSession,
            userCart = list(userCart[currSession]),
            emptyRecommendation = None,
            personalisedRecommendation = recommendedData,
        )

@app.route('/contactUs')
def contactUs():
    currSession = pickle.load(open('session.pkl','rb'))
    return render_template('contact.html', user = currSession)

@app.route('/allProducts')
def allProducts():
    currSession = pickle.load(open('session.pkl','rb'))
    return render_template('allProducts.html', 
        shoeId = list(shoes['shoeId'].values),
        shoeBrand = list(shoes['shoeBrand'].values),
        shoeImage = list(shoes['shoeImage'].values),
        shoeCatagory = list(shoes['shoeCategory'].values),
        shoeColor = list(shoes['shoeColour'].values),
        shoePrice = list(shoes['shoePrice'].values),
        user = currSession,
        userCart = list(userCart[currSession]),
    )

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug = True)
