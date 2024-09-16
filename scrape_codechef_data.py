import re
import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_column_data(file_path, col_name):
    df = pd.read_excel(file_path)
    return df[col_name]

def save_to_excel(data, file_name="codechef_data.xlsx"):
    df = pd.DataFrame(data)

    # Write the DataFrame to an Excel file
    df.to_excel(file_name, index=False)
    print(f"Data saved to {file_name}")

def scrape_codechef_data(username):

    url = f"https://www.codechef.com/users/{username}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve data for user: {username}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    try:
        current_rating_element = soup.select_one("div.rating-number").text.strip()
        current_rating = re.search(r"\d+", current_rating_element).group()
        current_rating = int(current_rating)

        # Returns the string (Highest Rating 2034)
        max_rating_element = soup.select_one("div.rating-header small").text.strip()
        max_rating = re.search(r"\d+", max_rating_element).group()
        max_rating = int(max_rating)
        
        # Returns str: No. of Contests Participated: 75 for eg. 
        contests_element = soup.select_one(
            "div.rating-title-container > div"
        ).text.strip()
        no_of_contests = re.search(r'\d+',contests_element).group()
        no_of_contests = int(no_of_contests)

        user_data = {
            "Codechef Username": str(username),
            "Codechef Current Rating": current_rating,
            "Codechef Maximum Rating": max_rating,
            "Codechef Contest Count": no_of_contests,
        }

        return user_data

    except Exception as e:
        print(f"Error occurred while scraping {username}: {e}")
        user_data = {
            "Codechef Username": str(username),
            "Codechef Current Rating": 0,
            "Codechef Maximum Rating": 0,
            "Codechef Contest Count": 0,
        }
        return user_data



usernames = get_column_data("codechef_usernames.xlsx", "Codechef Username")
print(usernames)
scraped_data = []

for username in usernames:
    result = scrape_codechef_data(username)
    if result:
        scraped_data.append(result)

if scraped_data:
    save_to_excel(scraped_data)
else:
    print("No data to save.")
