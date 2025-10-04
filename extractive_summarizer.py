"""
Lightweight summarization using extractive approach
This is a fallback when transformer models are not available
"""
from textblob import TextBlob
import re


def extractive_summarize(text, num_sentences=3):
    """
    Create a summary by extracting the most important sentences
    Uses a simple scoring mechanism based on sentence position and keywords
    """
    # Split text into sentences
    blob = TextBlob(text)
    sentences = blob.sentences
    
    if len(sentences) <= num_sentences:
        return text
    
    # Score sentences
    scored_sentences = []
    for i, sentence in enumerate(sentences):
        score = 0
        
        # Position score (first and last sentences are often important)
        if i == 0:
            score += 3
        elif i == len(sentences) - 1:
            score += 1
        
        # Length score (prefer moderate length sentences)
        words = len(sentence.words)
        if 10 <= words <= 25:
            score += 2
        
        # Keyword score (count important words)
        important_words = ['said', 'announced', 'reported', 'according', 'will', 'new']
        for word in important_words:
            if word in sentence.lower():
                score += 1
        
        scored_sentences.append((score, i, str(sentence)))
    
    # Sort by score and select top sentences
    scored_sentences.sort(reverse=True)
    top_sentences = scored_sentences[:num_sentences]
    
    # Sort selected sentences by original position
    top_sentences.sort(key=lambda x: x[1])
    
    # Join sentences
    summary = ' '.join([sent[2] for sent in top_sentences])
    return summary
