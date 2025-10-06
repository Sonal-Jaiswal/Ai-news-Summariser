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

3. Install dependencies:
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

4. View the results:
   - Article title
   - AI-generated summary
   - Sentiment classification (Positive/Negative/Neutral)
   - Polarity score (-1 to 1)
   - Subjectivity score (0 to 1)
   - Compression ratio

## How It Works

1. **URL Validation**: Validates the provided URL format
2. **Article Extraction**: Uses newspaper3k to download and parse the article
3. **Text Summarization**: Processes the article text through BART transformer model
4. **Sentiment Analysis**: Analyzes the text using TextBlob to determine sentiment polarity
5. **Results Display**: Shows summary and sentiment analysis on a beautiful web interface

## Technologies Used

- **Flask**: Web framework
- **newspaper3k**: Article extraction and parsing
- **Transformers (Hugging Face)**: BART model for summarization
- **PyTorch**: Deep learning framework for transformers
- **TextBlob**: Sentiment analysis
- **HTML/CSS/JavaScript**: Frontend interface

## Error Handling

The application handles various error scenarios:
- Invalid URL formats
- Unreachable URLs
- Articles with insufficient text
- Network errors
- Model loading failures

## Example URLs to Test

- BBC News: https://www.bbc.com/news
- CNN: https://www.cnn.com
- Reuters: https://www.reuters.com
- The Guardian: https://www.theguardian.com

## API Endpoint

### POST /analyze

Analyzes a news article from a given URL.

**Request Body:**
```
url: <news article URL>
```

**Response:**
```json
{
  "success": true,
  "title": "Article Title",
  "summary": "AI-generated summary...",
  "sentiment": "Positive",
  "polarity": 0.25,
  "subjectivity": 0.45,
  "original_length": 500,
  "summary_length": 75
}
```

## 🚀 Deployment

This application can be deployed to various platforms. Here are instructions for common deployment options:

### Deploy to Heroku

1. Install the Heroku CLI and login:
```bash
heroku login
```

2. Create a new Heroku app:
```bash
heroku create your-app-name
```

3. Create a `Procfile` in the project root:
```
web: python app.py
```

4. Update `app.py` to use the PORT environment variable (change the last line):
```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
```

5. Deploy to Heroku:
```bash
git add .
git commit -m "Prepare for Heroku deployment"
git push heroku main
```

6. Open your deployed app:
```bash
heroku open
```

### Deploy to Railway

1. Sign up at [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will automatically detect the Python app and deploy it
5. Add environment variables if needed in the Railway dashboard

### Deploy to Render

1. Sign up at [Render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
5. Click "Create Web Service"

### Deploy to PythonAnywhere

1. Sign up at [PythonAnywhere.com](https://www.pythonanywhere.com)
2. Upload your project files or clone from GitHub
3. Create a new web app with Python 3.8+
4. Install dependencies in a virtual environment:
```bash
pip install -r requirements.txt
```
5. Configure the WSGI file to point to your Flask app
6. Reload the web app

### Deploy to Google Cloud Platform (Cloud Run)

1. Install Google Cloud SDK and login
2. Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

3. Build and deploy:
```bash
gcloud builds submit --tag gcr.io/PROJECT-ID/ai-news-summarizer
gcloud run deploy --image gcr.io/PROJECT-ID/ai-news-summarizer --platform managed
```

### Deploy to AWS (Elastic Beanstalk)

1. Install AWS CLI and EB CLI
2. Initialize Elastic Beanstalk:
```bash
eb init -p python-3.8 ai-news-summarizer
```

3. Create an environment and deploy:
```bash
eb create ai-news-env
eb deploy
```

4. Open the application:
```bash
eb open
```

### Important Notes for Production Deployment

- Set `debug=False` in production
- Use environment variables for sensitive configuration
- Consider using gunicorn or uWSGI as WSGI server instead of Flask's development server
- For better performance with large models, use a deployment with sufficient RAM (at least 2GB)
- First model download may take time; consider pre-downloading models in your deployment setup

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Sonal Jaiswal
