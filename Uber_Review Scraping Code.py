import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the User-Agent header
user_agent = 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'

# Extract all links needed to be iterated
links = []
for x in range(1, 769):
    # Send a GET request to the URL with the User-Agent header
    source = requests.get(f'https://www.trustpilot.com/review/www.uber.com?page={x}', headers={'User-Agent': user_agent}).text

    # Create a BeautifulSoup object with the response text
    soup = BeautifulSoup(source, 'lxml')

    # Find all review items
    review_items = soup.find_all('div', class_='styles_consumerDetailsWrapper__p2wdr')

    for view in review_items:
        for link in view.find_all('a', href=True):
            href = link['href']
            full_link = "https://www.trustpilot.com" + href
            links.append(full_link)

# Iterating through each link to extract desired data
reviews = []
for link in links:
    source = requests.get(link, headers={'User-Agent': user_agent}).text
    soup = BeautifulSoup(source, 'lxml')

    ree_view = soup.find_all('div', class_='styles_container__BnfUR')

    for review in ree_view:
        try:
            # Extract the name of the reviewer
            Name = review.find('h1', class_='typography_display-xs__sDdPF typography_appearance-default__AAY17 styles_consumerDisplayName__QDr6f').text.strip()
        except AttributeError:
            Name = 'N/A'

        try:
            # Extract the country of the reviewer
            Date = review.find('p', class_='typography_body-m__xgxZ_ typography_appearance-default__AAY17').text.strip()
        except AttributeError:
            Date = 'N/A'

        try:
            # Extract the review text
            Country = review.find('p', class_='typography_body-l__KUYFJ typography_appearance-subtle__8_H2l').text.strip()
        except AttributeError:
            Country = 'N/A'

        try:
            # Extract the review text
            Revieww = review.find('p', class_='typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn').text.strip()
        except AttributeError:
            Reviewww = 'N/A'

        try:
            # Find the div element with the specified class
            rating_div = review.find('div', class_='star-rating_starRating__4rrcf star-rating_medium__iN6Ty')
            # Use a list comprehension to extract the "alt" attribute from the img elements
            Rating = [img_element.get('alt') for img_element in rating_div.find_all('img')]
            # Join the ratings into a single string and remove single quotes
            Rating = ', '.join(Rating)[6]
        except AttributeError:
            Rating = 'N/A'


        # Print the details
        Uber = {
            'Name': Name,
            'Date': Date,
            'Country': Country,
            'Revieww': Revieww,
            'Ratings' : Rating
        }

        reviews.append(Uber)

df = pd.DataFrame(reviews)
# print(df)

df.to_csv('Uberreview.csv', index=False)