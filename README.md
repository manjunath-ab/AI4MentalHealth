# AI4MentalHealth 💚

## Live Application Links 🌐

- Please use this application responsibly, as we have limited free credits remaining.

[![Codelabs](https://img.shields.io/badge/codelabs-4285F4?style=for-the-badge&logo=codelabs&logoColor=white)](https://codelabs-preview.appspot.com/?file_id=1blarGD_LQ5o5aGcJWiKKbhDBissQSL9qfs28dx5HyFk#11)

[![Demo Link](https://img.shields.io/badge/Demo_Link-808080?style=for-the-badge&logo=YouTube&logoColor=white)](https://youtu.be/DnmAYNL0kcI)

## Abstract 📝

## Project Goals 🎯

1. Scrape mental health related data from various blog sites like Blurt, Chipur, and Natashatracy.com using Selenium with Dagster Orchestration tool. 🕷️
2. Clean and categorize the scraped data using OpenAIExtractionChain, then store it into a Snowflake database along with associated metadata. 🧹
3. Use dbt to run transformations on the scraped data. 🔧
4. Embed the transformed data using OpenAI embeddings and store it into ChromaDB for efficient similarity search. 🔍
5.

## Use Case 📖

The use case for this project is to develop a mental health platform that leverages conversation AI based on Retrieval-augmented generation (RAG) to offer users a supportive and non-judgmental space, fostering emotional well-being and personal introspection. 🧠

## Technologies Used 🛠️

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/)
[![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![dbt](https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white)](https://www.getdbt.com/)
[![LangChain](https://img.shields.io/badge/LangChain-FF9900?style=for-the-badge&logo=langchain&logoColor=white)](https://python.langchain.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)
[![Dagster](https://img.shields.io/badge/Dagster-F23FC5?style=for-the-badge&logo=dagster&logoColor=white)](https://dagster.io/)
[![Cohere](https://img.shields.io/badge/Cohere-000000?style=for-the-badge&logo=cohere&logoColor=white)](https://cohere.ai/)
[![Snowflake](https://img.shields.io/badge/Snowflake-0093F1?style=for-the-badge&logo=snowflake&logoColor=white)](https://www.snowflake.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-7289DA?style=for-the-badge&logo=chromadb&logoColor=white)](https://www.chromadb.com/)
[![DeepEval](https://img.shields.io/badge/DeepEval-000000?style=for-the-badge&logo=deepeval&logoColor=white)](https://deepeval.com/)
[![Google Calendar](https://img.shields.io/badge/Google_Calendar-4285F4?style=for-the-badge&logo=google-calendar&logoColor=white)](https://calendar.google.com/)

## Data Source 📚

1. [Chipur](https://chipur.com)


2. [Blurt](https://blurt.blog)


3. [NatashaTracy](https://natashatracy.com)

## Steps

1. **Knowledge Base Preparation**: The chatbot's knowledge base is populated with mental health-related information from various sources, such as blogs and websites. This data is scraped, cleaned, and processed using techniques like OpenAI's extraction chain.

2. **Embedding and Storage**: The processed knowledge chunks are embedded using OpenAI's text embedding model, and the resulting vectors are stored in a ChromaDB vector database for efficient similarity search.

3. **User Input and Knowledge Retrieval**: When a user enters a message in the chatbot interface, the message is embedded using the same OpenAI embedding model. The chatbot then queries the ChromaDB database to retrieve the most relevant knowledge chunks based on vector similarity.

4. **Reranking**: The retrieved knowledge chunks are reranked using the Cohere reranker to improve their semantic relevance to the user's query.

5. **Language Generation**: The reranked knowledge chunks and the user's input are passed to the OpenAI GPT-3.5 language model, which generates a contextual and empathetic response.

6. **Conversation Management**: The generated response, along with the user's input, is added to the conversation history managed by LangChain's memory module. This conversation history is used to provide context for future responses.

7. **Appointment Scheduling**: If the user requests to schedule an appointment, the chatbot prompts the user for available dates and times. Once confirmed, the chatbot creates a calendar event using the Google Calendar API and sends appointment details via email.

8. **Data Storage**: User chat history and relevant information, including scheduled appointments, are stored in a Snowflake database for future reference and analysis.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-repo/mental-health-chat.git
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up the necessary environment variables (e.g., API keys, database credentials, etc.)

4. Run the Streamlit app:
``` bash
streamlit run app.py
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with descriptive commit messages.
4. Push your changes to your forked repository.
5. Submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

