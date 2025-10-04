# 🧠 AI News Summarizer and Sentiment Analyzer

A Python Flask web application that extracts, summarizes, and analyzes news articles using AI-powered natural language processing.

## ✨ Features

- **Article Extraction**: Automatically extracts article content from any URL using newspaper3k
- **AI-Powered Summarization**: Uses Hugging Face's BART transformer model for intelligent text summarization
- **Dual Sentiment Analysis**: Analyzes sentiment using both TextBlob and VADER for comprehensive insights
- **Keyword Extraction**: Identifies the most important keywords from articles
- **Word Count Comparison**: Shows original and summarized word counts with compression ratio
- **Responsive UI**: Modern, mobile-friendly interface built with Bootstrap
- **Error Handling**: Robust handling of invalid or unreachable URLs
- **Request Logging**: Logs all user requests for analytics

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Sonal-Jaiswal/Ai-news-Summariser.git
cd Ai-news-Summariser
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

4. Download required NLTK data for TextBlob (run in Python):
```python
python -c "import nltk; nltk.download('brown'); nltk.download('punkt')"
```

### Running the Application

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Enter a news article URL and click "Analyze Article"

## 📁 Project Structure

```
ai_news_app/
├── app.py                 # Main Flask application
├── templates/
│   ├── index.html        # Home page with URL input form
│   └── result.html       # Results page with analysis
├── static/
│   └── style.css         # Custom CSS styling
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore file
└── README.md            # This file
```

## 🔧 Technologies Used

- **Flask**: Web framework
- **newspaper3k**: Article extraction
- **Transformers (Hugging Face)**: Text summarization using BART model
- **PyTorch**: Deep learning framework
- **TextBlob**: Sentiment analysis
- **VADER Sentiment**: Advanced sentiment analysis
- **Bootstrap 5**: Responsive UI framework
- **Font Awesome**: Icons

## 📊 How It Works

1. **Article Extraction**: The application uses newspaper3k to download and parse the article from the provided URL
2. **Text Summarization**: The extracted text is processed by a BART transformer model to generate a concise summary
3. **Sentiment Analysis**: Both TextBlob and VADER analyze the summary to determine sentiment (Positive, Negative, or Neutral)
4. **Keyword Extraction**: A frequency-based algorithm identifies the top 10 keywords from the article
5. **Results Display**: All results are presented in an easy-to-read, responsive interface

## 🎯 Usage Example

1. Visit the home page
2. Enter a news article URL (e.g., `https://www.bbc.com/news/article-example`)
3. Click "Analyze Article"
4. View the results:
   - Article title, authors, and publication date
   - AI-generated summary
   - Word count comparison
   - Sentiment analysis from both TextBlob and VADER
   - Extracted keywords

## 📝 Logging

All user requests are logged to `user_requests.log` with timestamps for analytics purposes.

## ⚠️ Notes

- The first run may take longer as the BART model needs to be downloaded (~1.6GB)
- The model is loaded lazily to improve startup time
- Very long articles are truncated to fit the model's token limit
- Some websites may block automated content extraction

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Hugging Face for the transformer models
- newspaper3k for article extraction
- Bootstrap for the UI framework