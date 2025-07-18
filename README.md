# Customer Service RAG Chatbot with UI

A customer service chatbot for a restaurant built with React frontend and Python backend using Retrieval-Augmented Generation (RAG) for intelligent responses.

## Features

React-based chat interface \
Python backend with RAG capabilities \
ChromaDB for vector storage \
OpenAI API integration

## Prerequisites

Node.js (v14 or higher)\
Python 3.7+\
OpenAI API key\

## Setup Instructions
### 1. Clone the Repository

git clone https://github.com/samsonDzealot/Customer-Service-RAG-Chatbot-with-UI.git\
cd Customer-Service-RAG-Chatbot-with-UI

### 2. Frontend Setup

npm install

### 3. Backend Setup

pip install -r requirements.txt 

### 4. Environment Configuration

Create a .env file in the first_successful_RAG directory:\
OPENAI_API_KEY=your_openai_api_key_here\
\
Make sure to never commit your .env file to version control!!!

### 5. Run the Application

Start the backend:\
python chatbot_api.py\
\
Start the frontend:\
npm start\
\
Note that you must run the the backend and frontend simultaneously in separate terminal interfaces\
You must also have navigated to the project's directory within each terminal before executing these commands\
\
The app will open at [http://localhost:3000]

## Project Sructure
/src - React frontend components\
/first_successful_RAG - Python backend with RAG implementation\
/source_docs - Original documents used for RAG training\
/chroma_db - ChromaDB vector database\
/public - Static assets

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode at [http://localhost:3000]

### `npm test`

Launches the test runner in the interactive watch mode

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

## Contributing

Fork the repository\
Create your feature branch (`git checkout -b feature/AmazingFeature`)\
Commit your changes (`git commit -m 'Add some AmazingFeature`)\
Push to the branch (`git push origin feature/AmazingFeature`)]\
Open a Pull Request

### Learn More

[Create React App documentation]\
[OpenAI API documentation]\
[ChromaDB documentation]


