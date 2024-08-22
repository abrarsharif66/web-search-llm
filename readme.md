# Web Search using LLMs

## Project Overview

This project allows users to query the web using a Streamlit-based interface that utilizes a Flask backend. The backend performs web searches, scrapes relevant content, and generates contextually accurate responses using a Large Language Model (LLM). While the application is designed to handle sequential queries, it is not a fully conversational model due to token limitations, despite maintaining a basic conversation history.

### Project Structure

```
LLM_SEARCH_TEMPLATE/
│
├── flask_app/
│   ├── __pycache__/
│   ├── app.py
│   ├── utils.py
│
├── streamlit_app/
│   ├── app.py
│
├── .env
├── readme.md
├── requirements.txt
```
### Demo video 

https://github.com/user-attachments/assets/a0ab50e7-0a91-4930-99b8-8e8bcca67a9e

### Key Components

1. **Streamlit Interface (`streamlit_app/app.py`):**
   - Provides a user-friendly interface for asking queries.
   - Communicates with the Flask backend to retrieve and display responses.
   - Maintains conversation history by appending user and assistant messages to a session-based history. This history is passed back to the LLM with each query, but the model's token limit restricts it from functioning as a true conversational model.

2. **Flask Backend (`flask_app/app.py`):**
   - Manages the query handling process.
   - Performs web searches, scrapes relevant articles, and generates responses using LLMs.

3. **Utility Functions (`flask_app/utils.py`):**
   - `search_articles(query)`: Uses the Serper API to search and retrieve articles relevant to the user's query.
   - `fetch_article_content(url)`: Extracts and cleans the content from the retrieved articles.
   - `concatenate_content(articles)`: Combines the content from multiple articles into a single text body.
   - `generate_answer(content, query, prev_msgs)`: Uses GPT-4 or other LLMs to generate an answer from the concatenated content.

### Environment Setup

1. **Python Version:**
   - Ensure that Python 3.8 or above is installed.

2. **Virtual Environment:**
   - Create a virtual environment:
     ```bash
     python3 -m venv venv
     ```
   - Activate the virtual environment:
     - On Windows:
       ```bash
       venv\Scripts\activate
       ```
     - On macOS/Linux:
       ```bash
       source venv/bin/activate
       ```

3. **Install Dependencies:**
   - Install the required Python packages:
     ```bash
     pip install -r requirements.txt
     ```

4. **Environment Variables:**
   - Create a `.env` file in the root directory with the following variables:
     ```
     SERPER_API_KEY=<Your Serper API Key>
     OPENAI_API_KEY=<Your OpenAI API Key>
     GROQ_API_KEY=<Your Groq API Key (if applicable)>
     ```

### Running the Project

1. **Start the Flask Backend:**
   - Navigate to the `flask_app` directory:
     ```bash
     cd flask_app
     ```
   - Run the Flask application:
     ```bash
     python app.py
     ```
   - The Flask server will start and listen on `http://localhost:5001`.

2. **Start the Streamlit Interface:**
   - In another terminal, navigate to the `streamlit_app` directory:
     ```bash
     cd streamlit_app
     ```
   - Run the Streamlit application:
     ```bash
     streamlit run app.py
     ```
   - Access the Streamlit interface at `http://localhost:8501`.

### Usage

1. Open the Streamlit interface in your browser.
2. Enter your query in the provided input box.
3. The query will be sent to the Flask backend, which will return a contextually relevant answer after searching the web and processing the results using LLMs.

### Conversation History

- The application maintains a basic conversation history by appending each user query and the corresponding response to the chat history. 
- This history is included in subsequent queries to provide context.
- However, due to the LLM's token limit, this approach does not enable full conversational capabilities, as the history may be truncated when the token limit is reached.

