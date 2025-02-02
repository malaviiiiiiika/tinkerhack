from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)  # This will allow cross-origin requests from any domain

# Sample dataset (in real scenarios, this can be fetched from a database)
df = pd.DataFrame([
    {'user_id': 1, 'major': 'Computer Science', 'interests': 'AI, Deep Learning, Data Science'},
    {'user_id': 2, 'major': 'Mathematics', 'interests': 'Statistics, Algebra, Calculus'},
    {'user_id': 3, 'major': 'Electrical Engineering', 'interests': 'Circuit Design, Signal Processing'},
    {'user_id': 4, 'major': 'Computer Science', 'interests': 'Machine Learning, Data Science, Cloud Computing'}
])

# Preprocessing the data
vectorizer = TfidfVectorizer(stop_words='english')
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')  # FIXED sparse -> sparse_output, added handle_unknown

def preprocess_data():
    # Convert study interests to lowercase
    df['interests'] = df['interests'].apply(lambda x: x.lower())

    # Fit vectorizer and encoder
    X_text = vectorizer.fit_transform(df['interests'])
    X_major = encoder.fit(df[['major']]).transform(df[['major']])  # Fit before transform

    return np.hstack([X_text.toarray(), X_major])

# Preprocessed feature matrix
X = preprocess_data()

@app.route('/match-students', methods=['POST'])
def match_students():
    try:
        # Get user input
        data = request.get_json()
        major = data.get('major', '').strip()
        interests = data.get('interests', '').strip()

        if not major or not interests:
            return jsonify({'error': 'Both major and interests are required'}), 400

        # Vectorize user input
        input_data = vectorizer.transform([interests]).toarray()  # Vectorize interests
        input_major = encoder.transform(pd.DataFrame([[major]], columns=['major'])).toarray()
        input_features = np.hstack([input_data, input_major])  # Combine both

        # Compute cosine similarity
        cosine_sim = cosine_similarity(input_features, X)

        # Get top 3 similar users
        similar_users_idx = cosine_sim.argsort()[0][-4:-1][::-1]  # Exclude self
        matched_users = df.iloc[similar_users_idx].to_dict(orient='records')
        print("Matched Users:", matched_users)
        return jsonify({'matchedUsers': matched_users})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/")
def index():
    return "<h1>Study Group Matching API</h1>"

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)  # FIX: Prevents double reload issues
