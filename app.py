from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests
import logging
import os
from datetime import datetime
import pytz

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Use a secure key in production

# Mock user data, portfolios, and simulated trading balance
users = {'testuser': 'testpass'}
watchlists = {}  # This should hold lists for each user
posts = []

# Finnhub API Key
FINNHUB_API_KEY = 'crso609r01qpjadukir0crso609r01qpjadukirg'

# Helper function to check if the stock market is open
def is_market_open():
    now = datetime.now(pytz.timezone('America/New_York'))  # Eastern Time
    start = now.replace(hour=9, minute=30, second=0, microsecond=0)
    end = now.replace(hour=16, minute=0, second=0, microsecond=0)
    return start <= now <= end and now.weekday() < 5  # Weekdays only

# Function to get the latest stock price using Finnhub API
def get_stock_price(ticker):
    url = f'https://finnhub.io/api/v1/quote'
    params = {
        'symbol': ticker,
        'token': FINNHUB_API_KEY
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        logging.debug(f"Stock price API response: {data}")
        return float(data['o']), float(data['c'])  # Open and close price
    except requests.RequestException as e:
        logging.error(f"Request error: {e}")
    return None, None

# Routes
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/learning')
def learning():
    return render_template('learning.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.get(username) == password:
            session['user'] = username
            return redirect(url_for('index'))
        return 'Invalid credentials'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return render_template('logout.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in users:
            users[username] = password
            return redirect(url_for('login'))
        return 'Username already exists'
    return render_template('signup.html')

@app.route('/watchlist', methods=['GET'])
def watchlist():
    if 'user' not in session:
        return redirect(url_for('login'))

    user = session['user']
    logging.debug(f"Type of watchlists: {type(watchlists)}")  # Check type of watchlists
    user_watchlist = watchlists.get(user, [])

    # Prepare data for rendering
    watchlist_data = [
        {'ticker': item['ticker'], 'current_price': item['current_price'], 'price_change': item['price_change']}
        for item in user_watchlist
    ]

    return render_template('watchlist.html', watchlist=watchlist_data)

@app.route('/add_to_watchlist', methods=['POST'])
def add_to_watchlist():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'User not logged in'}), 401  # Check for authentication

    data = request.get_json()  # Get JSON data from the request
    ticker = data.get('ticker', '').upper()  # Extract the ticker

    user = session['user']
    if user not in watchlists:
        watchlists[user] = []  # Initialize the user's watchlist as a list

    # Check if the ticker is already in the watchlist
    if any(stock['ticker'] == ticker for stock in watchlists[user]):
        return jsonify({'success': False, 'message': 'Ticker already in watchlist.'})

    # Fetch the current price and price change
    current_price, price_change = get_stock_price(ticker)
    if current_price is None:
        return jsonify({'success': False, 'message': 'Invalid ticker symbol.'})

    # Add the stock to the user's watchlist
    watchlists[user].append({
        'ticker': ticker,
        'current_price': current_price,
        'price_change': price_change  # You can modify how price change is calculated
    })

    return jsonify({'success': True, 'ticker': ticker, 'current_price': current_price})  # Return success response

@app.route('/community', methods=['GET'])
def community():
    return render_template('community.html', posts=posts)

@app.route('/post', methods=['POST'])
def create_post():
    if 'user' not in session:
        return redirect('/login')

    ticker = request.form['ticker']
    prediction = request.form['prediction']
    file = request.files.get('file')
    filename = None

    if file:
        filename = f"uploads/{file.filename}"
        file.save(os.path.join('static/uploads', file.filename))

    new_post = {
        'ticker': ticker,
        'prediction': prediction,
        'file': filename,
        'username': session['user'],
        'likes': 0,
        'comments': []
    }
    posts.append(new_post)
    return redirect('/community')

@app.route('/comment/<int:post_index>', methods=['POST'])
def add_comment(post_index):
    if 'user' not in session or post_index < 1 or post_index > len(posts):
        return redirect('/community')

    comment_text = request.form['comment']
    comment = {
        'username': session['user'],
        'text': comment_text
    }
    posts[post_index - 1]['comments'].append(comment)
    return redirect('/community')

@app.route('/like_post/<int:post_index>', methods=['POST'])
def like_post(post_index):
    if post_index < 1 or post_index > len(posts):
        return 'Post not found', 404

    posts[post_index - 1]['likes'] += 1
    return 'Liked', 200

@app.route('/delete_post/<int:post_index>', methods=['GET'])
def delete_post(post_index):
    if post_index < 1 or post_index > len(posts):
        return redirect('/community')
    
    posts.pop(post_index - 1)
    return redirect('/community')

@app.route('/analyze', methods=['POST'])
def analyze_stock():
    # Get ticker from the request
    ticker = request.json.get('ticker')
    
    # Finnhub API URL for company profile and metrics
    overview_url = f'https://finnhub.io/api/v1/stock/metric?symbol={ticker}&metric=all&token={FINNHUB_API_KEY}'
    
    try:
        response = requests.get(overview_url)
        stock_info = response.json()

        if 'metric' not in stock_info:
            return jsonify({'success': False, 'message': 'Invalid ticker symbol'}), 400

        # Extract relevant information
        analysis_data = {
            '52_week_high': stock_info['metric'].get('52WeekHigh', 'N/A'),
            '52_week_low': stock_info['metric'].get('52WeekLow', 'N/A'),
            'SMA': stock_info['metric'].get('50DayMA', 'N/A'),
            'EPS': stock_info['metric'].get('epsBasicExclExtraItemsTTM', 'N/A'),
            'PE_ratio': stock_info['metric'].get('peInclExtraTTM', 'N/A'),
            'market_cap': stock_info['metric'].get('marketCapitalization', 'N/A'),
            'dividend_yield': stock_info['metric'].get('dividendYieldIndicatedAnnual', 'N/A'),
            'beta': stock_info['metric'].get('beta', 'N/A'),
            'summary': stock_info.get('companyProfile', {}).get('description', 'N/A')
        }

        return jsonify({'success': True, 'data': analysis_data}), 200
    except requests.RequestException as e:
        logging.error(f"Error fetching stock data: {e}")
        return jsonify({'success': False, 'message': 'Error fetching stock data'}), 500

if __name__ == '__main__':
    app.run(debug=True)