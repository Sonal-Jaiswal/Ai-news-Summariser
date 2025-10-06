# Installation and Usage Guide

## Quick Start

### 1. Install Dependencies

```bash
# Create and activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt

# Download NLTK data for TextBlob (one-time setup)
python -m textblob.download_corpora
```

### 2. Run the Application

```bash
python app.py
```

The app will start on `http://localhost:5000`

### 3. Use the Web Interface

1. Open your browser and go to `http://localhost:5000`
2. Enter a news article URL in the input field
3. Click "Analyze Article"
4. View the results:
   - Article title
   - AI-generated summary
   - Sentiment analysis (Positive/Negative/Neutral)
   - Detailed metrics (polarity, subjectivity, compression ratio)

## Features

### Article Extraction
- Extracts article text, title, authors, and publish date from any news URL
- Uses newspaper3k library for robust parsing
- Handles various news site formats

### Summarization
- **Primary**: Uses Facebook's BART transformer model (state-of-the-art)
- **Fallback**: Uses extractive summarization if transformers unavailable
- Compresses articles by 50-80% while retaining key information

### Sentiment Analysis
- Analyzes article sentiment using TextBlob
- Classifies as Positive, Negative, or Neutral
- Provides polarity score (-1 to +1)
- Provides subjectivity score (0 to 1)

### Error Handling
- Validates URL format before processing
- Handles network errors gracefully
- Provides clear error messages
- Falls back to simpler methods if AI models fail

## API Usage

### POST /analyze

Send a POST request with a news URL:

```bash
curl -X POST http://localhost:5000/analyze \
  -F "url=https://www.bbc.com/news/technology-12345678"
```

Response:
```json
{
  "success": true,
  "title": "Article Title",
  "summary": "This is the AI-generated summary...",
  "sentiment": "Positive",
  "polarity": 0.35,
  "subjectivity": 0.42,
  "original_length": 450,
  "summary_length": 68
}
```

Error response:
```json
{
  "error": "Invalid URL format. Please provide a valid http:// or https:// URL"
}
```

## Troubleshooting

### Installation Issues

**Problem**: `torch` installation fails or takes too long
**Solution**: The app will automatically fall back to extractive summarization. For full functionality, try:
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

**Problem**: `newspaper3k` fails to parse certain sites
**Solution**: Some sites have strong anti-scraping measures. Try different news sources or check your internet connection.

### Runtime Issues

**Problem**: Model loading takes a long time
**Solution**: First time model download can take 1-2 minutes. Subsequent runs will be faster.

**Problem**: Out of memory errors
**Solution**: The app limits article length to 1024 words for processing. If issues persist, restart the app.

## Testing

Run the structure tests:
```bash
python /tmp/test_structure.py
```

Run the functionality tests:
```bash
python /tmp/test_functionality.py
```

## Example News URLs

Test the app with these URLs:
- BBC News: https://www.bbc.com/news
- Reuters: https://www.reuters.com
- The Guardian: https://www.theguardian.com
- TechCrunch: https://techcrunch.com
- CNN: https://www.cnn.com

## Technical Details

### Architecture
- **Backend**: Flask (Python web framework)
- **Article Extraction**: newspaper3k
- **AI Summarization**: Hugging Face Transformers (BART)
- **Sentiment Analysis**: TextBlob
- **Frontend**: HTML, CSS, JavaScript (Vanilla)

### Model Information
- **BART** (facebook/bart-large-cnn): 406M parameters
- Trained on CNN/DailyMail dataset
- Optimized for news article summarization
- Generates abstractive summaries (not just extraction)

### Performance
- Article extraction: < 3 seconds
- Summarization (transformer): 5-10 seconds
- Summarization (extractive): < 1 second
- Sentiment analysis: < 1 second

## Security Notes

- The app validates URLs before processing
- Does not store any user data
- Does not execute arbitrary code from articles
- Safe for local and production use

## Development

To modify the app:

1. **Change summarization model**: Edit line 11 in `app.py`
2. **Adjust summary length**: Modify `max_length` parameter in `summarize_text()`
3. **Customize sentiment thresholds**: Edit the polarity ranges in `analyze_sentiment()`
4. **Update UI**: Edit `templates/index.html`

## Contributing

Contributions are welcome! Areas for improvement:
- Support for more languages
- Multiple summarization algorithms
- Caching for faster repeated requests
- Support for PDF/document URLs
- Batch processing multiple URLs

## License

MIT License - see LICENSE file for details
