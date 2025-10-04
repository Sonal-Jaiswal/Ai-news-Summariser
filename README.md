# AI News Summarizer 🤖📰

A Python Flask web application that extracts news articles from URLs, generates summaries using Hugging Face transformers (BART), and performs sentiment analysis using TextBlob.

## Features

- 📰 **Article Extraction**: Uses newspaper3k to extract article text from any news URL
- 📝 **AI Summarization**: Leverages Facebook's BART model for high-quality text summarization
- 😊 **Sentiment Analysis**: Analyzes article sentiment (Positive, Negative, Neutral) with TextBlob
- 🎨 **Beautiful UI**: Clean, modern web interface with gradient design
- ⚠️ **Error Handling**: Gracefully handles invalid URLs and extraction errors
- 📊 **Analytics**: Shows polarity, subjectivity, and compression ratio

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

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

4. Download required NLTK data for TextBlob (one-time setup):
```bash
python -c "import nltk; nltk.download('brown'); nltk.download('punkt')"
```

## Usage

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

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Sonal Jaiswal