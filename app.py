import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import streamlit as st

# Load dataset
def load_dataset(dataset_path):
    with open(dataset_path, 'r') as file:
        data = json.load(file)
    return data

# Function to perform semantic search
def semantic_search(query, dataset):
    # Combine all course titles into a list
    courses = []
    for category, course_list in dataset.items():
        for course in course_list:
            courses.append(course['Title'])

    # Initialize TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(stop_words='english')

    # Fit and transform the courses and query into vectors
    all_documents = courses + [query]
    tfidf_matrix = vectorizer.fit_transform(all_documents)

    # Compute cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

    # Sort the results based on cosine similarity scores
    sorted_indices = np.argsort(cosine_sim[0])[::-1]
    
    # Prepare the top courses as the results
    results = []
    for rank, idx in enumerate(sorted_indices[:5], 1):
        course = courses[idx]
        score = cosine_sim[0][idx]
        results.append({
            'Rank': rank,
            'Content': course,
            'Score': score
        })

    return results

# Streamlit interface
st.title('Smart Search System')

# No dataset input field, using a fixed file path
dataset_path = 'courses.json'  # Fixed file path

# Input form for query only
query = st.text_input('Enter a query to find the most relevant courses.')

if st.button('Submit'):
    if query:
        try:
            dataset = load_dataset(dataset_path)
            results = semantic_search(query, dataset)
            
            # Display the results in a user-friendly format
            if results:
                for result in results:
                    st.write(f"**Rank {result['Rank']}:**")
                    st.write(f"**Title:** {result['Content']}")
                    st.write(f"**Relevance Score:** {result['Score']:.4f}")
                    st.write("-" * 50)
            else:
                st.write("No relevant courses found.")
        except Exception as e:
            st.error(f"An error occurred while loading the dataset: {e}")
    else:
        st.warning("Please enter a query to search for relevant courses.")
