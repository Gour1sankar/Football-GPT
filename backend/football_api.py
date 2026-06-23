import os
import requests
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")

HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": RAPIDAPI_HOST,
    "Content-Type": "application/json"
}

BASE_URL = f"https://{RAPIDAPI_HOST}"

def search_player(name: str) -> str:
    url = f"{BASE_URL}/football-players-search"
    params = {"search": name}
    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()

    if data["status"] != "success":
        return "Could not find player information."

    players = data["response"]["suggestions"][:3]
    if not players:
        return f"No players found for '{name}'."

    result = f"Players matching '{name}':\n"
    for p in players:
        result += f"  - {p['name']} -> {p['teamName']}\n"
    return result

def get_livescores() -> str:
    url = f"{BASE_URL}/football-get-all-livescores"
    response = requests.get(url, headers=HEADERS)
    data = response.json()

    matches = data.get("response", {}).get("livescore", [])
    if not matches:
        return "No live matches currently."

    result = "Live matches:\n"
    for match in matches[:5]:
        home = match.get("homeName", "?")
        away = match.get("awayName", "?")
        score = match.get("score", "? - ?")
        result += f"  {home} {score} {away}\n"
    return result

def get_fixtures(league_id: str = "EPL") -> str:
    url = f"{BASE_URL}/football-get-all-upcoming-fixtures-by-league"
    params = {"leagueId": league_id}
    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()

    fixtures = data.get("response", {}).get("fixtures", [])[:5]
    if not fixtures:
        return "No upcoming fixtures found."

    result = "Upcoming fixtures:\n"
    for f in fixtures:
        home = f.get("homeName", "?")
        away = f.get("awayName", "?")
        date = f.get("startTimestamp", "?")
        result += f"  {home} vs {away} on {date}\n"
    return result

if __name__ == "__main__":
    print(search_player("Mbappe"))
    print(get_livescores())