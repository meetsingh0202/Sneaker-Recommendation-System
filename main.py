import numpy as np
import csv

# Mock dataset: Sneaker attributes (content-based features)
sneakers = {}

with open("ShoesDatabaseFinalCsv.csv", "r") as db:
    csv_reader = csv.reader(db)
    for row in csv_reader:
        id, brand, categories, colors, imageUrl, price = row
        sneakers[int(id)] = {"brand": brand, "categories": categories, "colors": colors, "imageUrl": imageUrl, "price": price}
        if id == '50':
            break
print(sneakers)

# Mock dataset: User interactions (collaborative filtering)
user_interactions = {
    101: [1, 2],  # User 101 liked sneakers 1 and 2
    102: [1],     # User 102 liked sneaker 1
    # ... more users
}

# Calculate collaborative similarity (mock values)
def collaborative_similarity(user1, user2):
    if user1 in user_interactions and user2 in user_interactions:
        intersection = len(set(user_interactions[user1]) & set(user_interactions[user2]))
        union = len(set(user_interactions[user1]) | set(user_interactions[user2]))
        return intersection / union
    else:
        return 0.0

# Calculate content-based similarity (mock values)
def content_based_similarity(sneaker1, sneaker2):
    shared_attributes = sum(sneaker1[attr] == sneaker2[attr] for attr in ['brand', 'style', 'color'])
    total_attributes = len(['brand', 'style', 'color'])
    return shared_attributes / total_attributes

# Hybrid recommendation algorithm
def hybrid_recommendation(user_id, num_recommendations=5, collaborative_weight=0.5, content_based_weight=0.5):
    user_interacted_sneakers = user_interactions.get(user_id, [])
    
    collaborative_scores = {}
    content_based_scores = {}
    
    for other_user in user_interactions:
        if other_user != user_id:
            collaborative_scores[other_user] = collaborative_similarity(user_id, other_user)
    
    for sneaker_id, sneaker in sneakers.items():
        content_based_scores[sneaker_id] = 0
        for user_sneaker_id in user_interacted_sneakers:
            content_based_scores[sneaker_id] += content_based_similarity(sneaker, sneakers[user_sneaker_id])
    
    recommendations = []
    for sneaker_id in sneakers:
        hybrid_score = (collaborative_weight * np.mean(list(collaborative_scores.values()))) + (content_based_weight * content_based_scores[sneaker_id])
        recommendations.append((sneaker_id, hybrid_score))
    
    recommendations.sort(key=lambda x: x[1], reverse=True)
    recommended_sneakers = [sneaker_id for sneaker_id, _ in recommendations[:num_recommendations]]
    
    return recommended_sneakers

# Example usage
user_id = 101
recommended_sneakers = hybrid_recommendation(user_id)
print("Recommended Sneakers:", recommended_sneakers)
