from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

shoes = pickle.load(open('shoes.pkl','rb'))

@app.route('/')
def index():
    return render_template('index.html', 
        shoeId = list(shoes['shoeId'].values),
        shoeBrand = list(shoes['shoeBrand'].values),
        shoeImage = list(shoes['shoeImage'].values),
        shoeCatagory = list(shoes['shoeCategory'].values),
        shoeColor = list(shoes['shoeColour'].values),
        shoePrice = list(shoes['shoePrice'].values)
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
    app.run(debug = True)
