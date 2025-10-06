from flask import Flask, render_template, request, jsonify
from newspaper import Article
from transformers import pipeline
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import logging
from datetime import datetime
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    filename='user_requests.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# Initialize summarization pipeline (using BART model)
summarizer = None

def get_summarizer():
    """Lazy load the summarizer to avoid loading it on startup"""
    global summarizer
    if summarizer is None:
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    return summarizer

def is_valid_url(url):
    """Validate URL format"""
    import re
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None

def analyze_sentiment(text):
    """Analyze sentiment using TextBlob"""
    return analyze_sentiment_textblob(text)

def extract_article(url):
    """Extract article content from URL using newspaper3k"""
    try:
        article = Article(url)
        article.download()
        article.parse()
        return {
            'title': article.title,
            'text': article.text,
            'authors': article.authors,
            'publish_date': article.publish_date,
            'success': True
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def summarize_text(text, max_length=130, min_length=30):
    """Summarize text using Hugging Face transformers"""
    try:
        # Split text into chunks if it's too long (BART has a max token limit)
        max_chunk_length = 1024
        words = text.split()
        
        if len(words) > max_chunk_length:
            # Take the first chunk for summarization
            text = ' '.join(words[:max_chunk_length])
        
        summarizer_model = get_summarizer()
        summary = summarizer_model(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        return f"Error in summarization: {str(e)}"

def analyze_sentiment_textblob(text):
    """Analyze sentiment using TextBlob"""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    
    if polarity > 0.1:
        sentiment = "Positive"
    elif polarity < -0.1:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    
    return {
        'sentiment': sentiment,
        'polarity': polarity,
        'subjectivity': blob.sentiment.subjectivity
    }

def analyze_sentiment_vader(text):
    """Analyze sentiment using VADER"""
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    
    compound = scores['compound']
    if compound >= 0.05:
        sentiment = "Positive"
    elif compound <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    
    return {
        'sentiment': sentiment,
        'compound': compound,
        'pos': scores['pos'],
        'neu': scores['neu'],
        'neg': scores['neg']
    }

def extract_keywords(text):
    """Extract keywords using simple frequency analysis"""
    try:
        # Simple keyword extraction using word frequency
        from collections import Counter
        import re
        
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                     'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
                     'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 
                     'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these',
                     'those', 'it', 'its', 'they', 'them', 'their', 'he', 'she', 'his',
                     'her', 'him', 'we', 'us', 'our', 'you', 'your'}
        
        # Extract words
        words = re.findall(r'\b[a-z]{4,}\b', text.lower())
        
        # Filter stop words and count
        filtered_words = [word for word in words if word not in stop_words]
        word_freq = Counter(filtered_words)
        
        # Get top 10 keywords
        keywords = [word for word, count in word_freq.most_common(10)]
        return keywords
    except Exception as e:
        return []

def log_request(url, success):
    """Log user request to file"""
    log_message = f"URL: {url} | Success: {success}"
    logging.info(log_message)

@app.route('/')
def index():
    """Render the home page"""
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
