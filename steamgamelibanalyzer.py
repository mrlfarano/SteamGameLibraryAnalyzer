import requests
import json

def get_game_library(api_key, user_id):
    url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={api_key}&steamid={user_id}&format=json"
    response = requests.get(url)
    data = response.json()

    if "response" in data and "games" in data["response"]:
        games = data["response"]["games"]
        return [game["appid"] for game in games]
    else:
        print("Failed to retrieve the game library.")
        return []

def get_game_details(api_key, app_ids):
    for app_id in app_ids:
        url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
        response = requests.get(url)
        data = response.json()

        if data and str(app_id) in data and data[str(app_id)]["success"]:
            name = data[str(app_id)]["data"]["name"]
            review_score = data[str(app_id)]["data"]["metacritic"]["score"] if "metacritic" in data[str(app_id)]["data"] else "N/A"
            print(f"Game: {name} (App ID: {app_id}), Review Score: {review_score}")
        else:
            print(f"Failed to retrieve game details for App ID: {app_id}")
            print(data)  # Print API response for troubleshooting

def main():
    with open('config.json') as config_file:
        config = json.load(config_file)
    
    api_key = config["api_key"]
    user_id = config["user_id"]

    app_ids = get_game_library(api_key, user_id)
    get_game_details(api_key, app_ids)

if __name__ == "__main__":
    main()
