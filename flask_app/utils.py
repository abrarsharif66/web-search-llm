import os
import requests
from bs4 import BeautifulSoup
import openai
import json
from openai import OpenAI

from groq import Groq

# Load API keys from environment variables
SERPER_API_KEY = os.getenv('SERPER_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')



def search_articles(query):
    """
    Searches for articles related to the query using Serper API.
    Returns a list of dictionaries containing article URLs, headings, and text.
    """
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    results = response.json()
    
    articles = []
    for result in results.get('organic', [])[:3]:  # Limit to top 3 results
        articles.append({
            'url': result['link'],
            'heading': result['title'],
            'text': result['snippet']
        })
    return articles

def fetch_article_content(url):
    """
    Fetches the article content, extracting headings and text.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    content = ""
    for header in soup.find_all(['h1', 'h2', 'h3']):
        content += header.text.strip() + "\n\n"
    
    for paragraph in soup.find_all('p'):
        content += paragraph.text.strip() + "\n\n"
    
    return content.strip()

def concatenate_content(articles):
    """
    Concatenates the content of the provided articles into a single string.
    """
    full_text = ""
    for article in articles:
        full_text += f"Title: {article['heading']}\n\n"
        full_text += f"Content:\n{fetch_article_content(article['url'])}\n\n"
        full_text += "---\n\n"
    return full_text

def generate_answer(content, query, prev_msgs):
    """
    Generates an answer from the concatenated content using GPT-4.
    The content and the user's query are used to generate a contextual answer.
    """
    prompt = f"Based on the following information:\n\n{content}\n\nAnswer the following question: {query}"
    client = OpenAI(api_key=OPENAI_API_KEY) #if you are using openai update the model to gpt-4 and you are good to go
    #client= Groq(api_key=GROQ_API_KEY) #if you are using groq use llama3-70b-8192 or mixtral-8x7b-32768
    
    try:
        prev_msgs.append({"role": "user", "content": prompt})
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=prev_msgs,
            temperature=0.1
        )
        llm_response=response.choices[0].message.content
        prev_msgs.append({"role": "assistant", "content": llm_response})
        return response.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return f"An error occurred while generating the answer.{str(e)}"
