import requests
import pandas as pd

url = "https://www.hackerrank.com/rest/contests/turing-hut-workshop-practice/leaderboard"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

limit = 100  # Number of records per API call
offset = 0  # Initial offset
leaderboard_data = []  # List to hold all leaderboard data
count = 0 # Count the number of entries
max_count = float("inf") # Set it to some value to get max_count number of entries instead of the whole leaderboard 

while True:
    paginated_url = f"{url}?offset={offset}&limit={limit}"
    response = requests.get(paginated_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        models = data.get("models", [])
        if not models:
            break
        for entry in models:
            if count >= max_count:
                break
            rank = entry.get("rank", "N/A")
            username = entry.get("hacker", "N/A")
            score = entry.get("score", "N/A")
            count = count + 1
            leaderboard_data.append({"S.No": count, "Rank": rank, "Username": username, "Score": score})
        offset += limit
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        break

df = pd.DataFrame(leaderboard_data)
df.to_excel("hackerrank_leaderboard.xlsx", index=False)
print("All data has been scraped and saved to 'hackerrank_leaderboard.xlsx'")
