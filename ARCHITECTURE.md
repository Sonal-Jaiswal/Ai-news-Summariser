# AI News Summarizer - Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         User Browser                         │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐   │
│  │            Web Interface (index.html)                 │   │
│  │  • URL Input Form                                     │   │
│  │  • Loading Indicator                                  │   │
│  │  • Results Display                                    │   │
│  │  • Error Messages                                     │   │
│  └───────────────────────────────────────────────────────┘   │
│                            ↕ AJAX                             │
└─────────────────────────────────────────────────────────────┘
                               ↕
┌─────────────────────────────────────────────────────────────┐
│                     Flask Application                        │
│                        (app.py)                              │
│                                                               │
│  ┌─────────────┐      ┌──────────────┐                      │
│  │   Routes    │      │  Validators  │                      │
│  │  /          │      │ • URL check  │                      │
│  │  /analyze   │ ───▶ │ • Text length│                      │
│  └─────────────┘      └──────────────┘                      │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Processing Pipeline                     │    │
│  │                                                       │    │
│  │  1. URL Validation                                   │    │
│  │     └─▶ Regex pattern matching                       │    │
│  │                                                       │    │
│  │  2. Article Extraction (newspaper3k)                 │    │
│  │     └─▶ Download, Parse, Extract text                │    │
│  │                                                       │    │
│  │  3. Text Summarization                               │    │
│  │     ┌─▶ BART Transformer (Primary)                   │    │
│  │     └─▶ Extractive Method (Fallback)                 │    │
│  │                                                       │    │
│  │  4. Sentiment Analysis (TextBlob)                    │    │
│  │     └─▶ Polarity & Subjectivity scores               │    │
│  │                                                       │    │
│  │  5. Response Generation                              │    │
│  │     └─▶ JSON with results/errors                     │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                               ↕
┌─────────────────────────────────────────────────────────────┐
│                    External Libraries                        │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  newspaper3k │  │ transformers │  │   TextBlob   │      │
│  │              │  │              │  │              │      │
│  │ • Download   │  │ • BART Model │  │ • Sentiment  │      │
│  │ • Parse HTML │  │ • Tokenizer  │  │ • Polarity   │      │
│  │ • Extract    │  │ • Generate   │  │ • Subjectv.  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         ↕                  ↕                  ↕              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              External Resources                      │   │
│  │  • News Websites                                     │   │
│  │  • Hugging Face Models (first download)             │   │
│  │  • NLTK Data (TextBlob)                              │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### Success Path
1. User submits URL via web form
2. Frontend sends POST request to /analyze
3. Backend validates URL format
4. newspaper3k downloads and parses article
5. Text is processed through summarization
6. Sentiment is analyzed with TextBlob
7. JSON response with results sent to frontend
8. Frontend displays summary and sentiment

### Error Path
1. User submits URL via web form
2. Frontend sends POST request to /analyze
3. Error occurs (invalid URL, extraction fails, etc.)
4. Exception caught by try-except block
5. JSON error response sent to frontend
6. Frontend displays user-friendly error message

## File Structure

```
Ai-news-Summariser/
├── app.py                      # Main Flask application
├── extractive_summarizer.py    # Fallback summarization
├── requirements.txt            # Python dependencies
├── templates/
│   └── index.html             # Web interface
├── .gitignore                 # Git ignore rules
├── README.md                  # Project overview
└── USAGE.md                   # Detailed usage guide
```

## Component Details

### app.py
- **Lines 1-20**: Imports and model initialization
- **Lines 22-30**: URL validation function
- **Lines 32-45**: Article extraction function
- **Lines 47-75**: Text summarization (with fallback)
- **Lines 77-95**: Sentiment analysis function
- **Lines 97-100**: Index route (serves HTML)
- **Lines 102-145**: Analysis route (main processing)

### extractive_summarizer.py
- Lightweight fallback when transformers unavailable
- Scores sentences by position and keywords
- Selects top 3 sentences for summary

### templates/index.html
- **Lines 1-200**: CSS styling
- **Lines 201-250**: HTML structure
- **Lines 251-310**: JavaScript for AJAX requests

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Backend Framework | Flask 3.0 | Web server and routing |
| Article Extraction | newspaper3k | Parse news articles |
| AI Summarization | BART (Hugging Face) | Generate summaries |
| Sentiment Analysis | TextBlob | Analyze sentiment |
| Deep Learning | PyTorch | Support transformers |
| Frontend | HTML/CSS/JS | User interface |

## Security Measures

1. **URL Validation**: Regex pattern to prevent malicious URLs
2. **Error Handling**: Try-except blocks prevent crashes
3. **Input Sanitization**: Flask handles form data safely
4. **No Data Storage**: No user data is persisted
5. **Safe Parsing**: newspaper3k handles HTML safely

## Performance Characteristics

| Operation | Time (avg) | Notes |
|-----------|-----------|-------|
| URL Validation | < 1ms | Regex matching |
| Article Download | 1-3s | Depends on website |
| Article Parsing | 100-500ms | CPU bound |
| BART Summarization | 5-10s | GPU speeds this up |
| Extractive Summarization | 100-200ms | Fallback method |
| Sentiment Analysis | 50-100ms | Fast processing |

## Scalability Considerations

Current implementation is single-threaded and synchronous:
- Good for: Personal use, demos, development
- Limitations: One request at a time

For production:
- Use async/await for concurrent requests
- Add caching layer (Redis) for repeated URLs
- Deploy with Gunicorn + Nginx
- Consider GPU for faster AI inference
- Add rate limiting to prevent abuse

## Future Enhancements

1. **Multi-language support**: Add translation
2. **Multiple models**: Let users choose summarization model
3. **Batch processing**: Handle multiple URLs at once
4. **Article comparison**: Compare sentiment across sources
5. **RSS feed support**: Subscribe to news feeds
6. **History tracking**: Save user's analyzed articles
7. **Export options**: PDF, Word, Markdown export
8. **Chrome extension**: Analyze articles in-browser
