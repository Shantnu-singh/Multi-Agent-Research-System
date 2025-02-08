# Cognito 🔍🤖


**Cognito** is an AI-powered tool that helps users efficiently gather research materials from the web. It allows users to retrieve information through either Google organic search results or LLM-generated results, summarize content, and even fetch relevant YouTube videos.
<div align="center">
  <img src="asset/logo.jpg" alt="Text Alchemy Banner" width="300">
</div>

<div align="center">
  <di>
</div>



## Features

- 🌍 **Search Options**: Choose between Google organic search and LLM-generated results.
- 📑 **Content Summarization**: Automatically summarizes web content.
- 🎥 **YouTube Transcripts**: Fetches and summarizes video transcripts.
- 📜 **Final Report Generation**: Compiles research findings into a structured report.
- 🖥️ **User-Friendly Interface**: Simple and interactive Streamlit web app.

## Demo Video 📽️

For a demonstration of how the Web Agent works, check out the video:

![How Web Agent Works](asset\How agent works.mp4)

## Prerequisites

- Python 3.8+
- Streamlit
- Google API access
- SERP API access

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Shantnu-singh/Browser-agent---Task-1
cd app
```

2. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Environment Configuration

Create a `.env` file in the project root with the following variables:

```env
# Google API Configuration
GOOGLE_API_KEY="YOUR_API_KEY_HERE"

# SERP API Configuration
SERP_API_KEY="YOUR_API_KEY_HERE"  # Optional : only if you want to use google search
```

### API Key Setup

#### **Google API Key**
1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project and enable the relevant APIs
3. Generate an API key and copy it to your `.env` file

#### **SERP API Key**
1. Sign up at [SERP API](https://serpapi.com/)
2. Obtain your API key and add it to your `.env` file

## Running the Application

```bash
streamlit run app.py
```

## Usage

1. Open the Streamlit web interface.
2. Enter your research topic.
3. Choose between **Google Organic Results** or **LLM-Generated Results**.
4. Click on "Search" to retrieve relevant web pages and YouTube videos.
5. View summarized content and generate a research report.


## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.


Enjoy seamless research with **Web Agent for Research**! 🚀

