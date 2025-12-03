from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

def get_gamepasses(user_id):
    all_gamepasses = []

    r = requests.get(f"https://games.roproxy.com/v2/users/{user_id}/games?accessFilter=2&sortOrder=Asc&limit=10")
    if r.status_code != 200:
        print("Code 200")
        return []

    data = r.json().get("data", [])
    print("Data: ", data)
    for game in data:
        print("Game: ", game)
        universe_id = game.get("id")
        if not universe_id:
            continue
        gp_request = requests.get(
            f"https://apis.roblox.com/game-passes/v1/universes/{universe_id}/game-passes?passView=Full&pageSize=100"
        )
        print(gp_request)
        if gp_request.status_code != 200:
            continue
        print("Working")
        gamepasses = gp_request.json().get("data", [])
        print(gamepasses)
        for gp in gamepasses:
            print(gp)
            asset_id = gp["id"]

            all_gamepasses.append(asset_id)

    print(all_gamepasses)
    return all_gamepasses

@app.route("/api/gamepasses", methods=["GET"])
def api_gamepasses():
    user_id = request.args.get("userId")
    print(user_id)
    if not user_id or not user_id.isdigit():
        return jsonify({"error": "Parâmetro 'userId' ausente ou inválido"}), 400

    data = get_gamepasses(user_id)
    print(data)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
