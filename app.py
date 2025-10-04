from flask import Flask, render_template, request, jsonify
from newspaper import Article
from transformers import pipeline
from textblob import TextBlob
import re

app = Flask(__name__)

# Initialize the summarization pipeline (using BART model)
try:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
except Exception as e:
    print(f"Error loading summarization model: {e}")
    summarizer = None

def is_valid_url(url):
    """Validate URL format"""
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None

def extract_article(url):
    """Extract article text from URL using newspaper3k"""
    try:
        article = Article(url)
        article.download()
        article.parse()
        return {
            'title': article.title,
            'text': article.text,
            'authors': article.authors,
            'publish_date': str(article.publish_date) if article.publish_date else None
        }
    except Exception as e:
        raise Exception(f"Failed to extract article: {str(e)}")

def summarize_text(text):
    """Summarize text using Hugging Face transformer"""
    if not summarizer:
        raise Exception("Summarization model not available")
    
    try:
        # BART works best with text between 56-1024 tokens
        # Split long texts into chunks
        max_chunk_length = 1024
        words = text.split()
        
        if len(words) < 56:
            return text  # Text too short to summarize
        
        # For longer texts, take first chunk
        if len(words) > max_chunk_length:
            text = ' '.join(words[:max_chunk_length])
        
        # Generate summary
        summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        raise Exception(f"Failed to summarize: {str(e)}")

def analyze_sentiment(text):
    """Analyze sentiment using TextBlob"""
    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        # Classify sentiment
        if polarity > 0.1:
            sentiment = "Positive"
        elif polarity < -0.1:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        
        return {
            'sentiment': sentiment,
            'polarity': round(polarity, 3),
            'subjectivity': round(blob.sentiment.subjectivity, 3)
        }
    except Exception as e:
        raise Exception(f"Failed to analyze sentiment: {str(e)}")

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Process the news URL and return analysis"""
    try:
        # Get URL from request
        url = request.form.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'Please provide a URL'}), 400
        
        # Validate URL
        if not is_valid_url(url):
            return jsonify({'error': 'Invalid URL format. Please provide a valid http:// or https:// URL'}), 400
        
        # Extract article
        article_data = extract_article(url)
        
        if not article_data['text'] or len(article_data['text'].strip()) < 100:
            return jsonify({'error': 'Could not extract sufficient article text from the URL'}), 400
        
        # Summarize article
        summary = summarize_text(article_data['text'])
        
        # Analyze sentiment
        sentiment_data = analyze_sentiment(article_data['text'])
        
        # Return results
        return jsonify({
            'success': True,
            'title': article_data['title'],
            'summary': summary,
            'sentiment': sentiment_data['sentiment'],
            'polarity': sentiment_data['polarity'],
            'subjectivity': sentiment_data['subjectivity'],
            'original_length': len(article_data['text'].split()),
            'summary_length': len(summary.split())
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
