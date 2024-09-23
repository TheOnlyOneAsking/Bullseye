# Bullseye - Stock Market Companion
#### Video Demo:  <URL HERE>

Bullseye is a sophisticated stock analysis application developed using Python and Flask. It empowers users with essential financial data and metrics for informed investment decisions.

#### Key Features:

Financial Indicators: Analyze key metrics like 52-week highs/lows, SMAs, EPS, P/E ratios, market capitalization, dividend yield, and beta.
User Authentication: Securely create accounts, log in, and manage profiles.
Watchlist : track all your favorite stocks and monitor potential investments.
# User Authentication

Explanation: User passwords are hashed (scrambled) for security before storage.

# Watchlist Feature
The watchlist feature allows users to keep track of stocks they are interested in without necessarily investing in them immediately. Users can add and remove stocks from their watchlist, enabling them to monitor potential investment opportunities over time. This feature is crucial for users who want to make informed decisions based on market trends and stock performance.

Here is an example code snippet for managing the watchlist in app.py:
```
@app.route('/watchlist', methods=['GET', 'POST'])
def watchlist():
    if request.method == 'POST':
        stock_symbol = request.form['stock_symbol']
        # Code to add stock to the user's watchlist goes here
        flash(f'{stock_symbol} has been added to your watchlist.')
        return redirect(url_for('watchlist'))
    # Code to retrieve user's watchlist goes here
    return render_template('watchlist.html', watchlist=watchlist_data)
```    


# Community Engagement

The community page provides a platform for users to engage in discussions, share insights, and ask questions about stock trading. This interactive feature fosters a sense of community among users and encourages knowledge sharing.

# Installation Instructions

#### Clone the Repository:
```
git clone https://github.com/yourusername/bullseye.git
cd bullseye
```
#### Set Up a Virtual Environment:
```
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```
#### Install Packages:
```
pip install Flask Flask-SQLAlchemy Werkzeug
```
(Installs Flask web framework, SQLAlchemy for database management, and Werkzeug for secure password hashing)

#### Run the Application:
```
python app.py
```
Access it at http://127.0.0.1:5000 in your web browser.

# Code Explanation

Additional functionalities enhance Bullseye:

Data Retrieval: Utilizes APIs to fetch real-time financial data.
```
import requests

def get_stock_data(symbol):
    url = f'https://api.example.com/stocks/{symbol}'
    response = requests.get(url)
    return response.json()
```

#### Application Structure: Well-defined directories for separation of concerns:

- **app.py**: 
  - This is the main entry point of the application. It initializes the Flask application, sets up the database connections, and defines the various routes (URLs) that users can access. It also contains the logic for handling user authentication, and watchlist functionalities.

- **templates/**: 
  - This directory contains all the HTML files used for rendering the user interface. Flask uses the Jinja2 templating engine, allowing for dynamic content rendering. Key files include:
    - `index.html`: The landing page that provides an overview of the application and features.
    - `register.html`: The user registration page where new users can sign up for an account.
    - `login.html`: The login page for existing users to access their accounts.
    - `watchlist.html`: Allows users to view and manage their watchlist of stocks.
    - `community.html`: A page for user engagement and discussion about stock trading.

- **static/**: 
  - This directory contains all static assets, including CSS files for styling, and images used throughout the application. Key files include:
    - `styles.css`: Contains the custom styles for the application, including layout, typography, and color schemes that enhance the user interface.
    - `logo.png`: The logo image displayed in the header of the application.

# Conclusion

Bullseye represents a significant advancement in stock analysis applications, merging essential financial metrics with a user-friendly interface and community engagement features. By prioritizing usability, security, and interactive capabilities, Bullseye aims to be a valuable resource for anyone navigating the complexities of the stock market. The continuous evolution of the application will be driven by user feedback and technological advancements, ensuring that it remains relevant and beneficial to its users.

Feel free to explore Bullseye and leverage its capabilities to enhance your stock trading experience!
