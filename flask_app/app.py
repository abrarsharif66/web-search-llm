from flask import Flask, request, jsonify
from utils import search_articles, concatenate_content, generate_answer
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
history=[
                {"role": "system", "content": """You are a web-based assistant designed to help users by providing accurate answers derived from the top 3 search results on the web. 
                For every question and follow-up, you will receive relevant information from web-scraped data. 
                Your task is to distinguish between new questions and follow-up questions and respond appropriately based on the given context. 
                Adhere strictly to these guidelines."""}
                
            ]
@app.route('/query', methods=['POST'])
def query():
    """
    Handles the POST request to '/query'. Extracts the query from the request,
    processes it through the search, concatenate, and generate functions,
    and returns the generated answer.
    """
    data = request.json
    query = data.get('query')
    print("Received query:", query)
    
    # Step 1: Search and scrape articles based on the query
    print("Step 1: searching articles")
    articles = search_articles(query)
    print(articles)
    
    # Step 2: Concatenate content from the scraped articles
    print("Step 2: concatenating content")
    content = concatenate_content(articles)
    print("ll",content)
    
    # Step 3: Generate an answer using the LLM
    print("Step 3: generating answer")
    answer = generate_answer(content, query, history)
    
    # return the jsonified text back to streamlit
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(host='localhost', port=5001)