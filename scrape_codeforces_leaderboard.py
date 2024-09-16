import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_codeforces_leaderboard(num_entries=None):

    # URL of the Codeforces contest leaderboard
    url = "https://codeforces.com/contest/1538/standings"
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers = headers)
    if response.status_code != 200:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', class_='standings')

    if not table:
        print("Failed to find the leaderboard table.")
        return
    
    rows = table.find_all('tr')[1:]  # Skip the header row
    
    data = []
    for row in rows:
        columns = row.find_all('td')
        if len(columns) < 6:  # Ensure there are enough columns
            continue
        rank = columns[0].text.strip()
        username = columns[1].text.strip()
        time_penalty = columns[3].text.strip()
        num_solved = columns[4].text.strip()
        
        data.append({
            'Rank': rank,
            'Username': username,
            'Time Penalty': time_penalty,
            'Number of Questions Solved': num_solved
        })
    
    # Limit the number of entries if specified
    if num_entries:
        data = data[:num_entries]
    
    # Convert data to DataFrame and save to Excel
    df = pd.DataFrame(data)
    df.to_excel('codeforces_leaderboard.xlsx', index=False)
    print(f"Data saved to codeforces_leaderboard.xlsx")

# Example usage: scrape top 10 entries
scrape_codeforces_leaderboard(num_entries=10)
