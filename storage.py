import json

def load_highscore():
    try:
        with open("highscore.json", "r") as file:
            data = json.load(file)
            return data.get("highscore", 0)
    except FileNotFoundError:
        return 0 
    
def save_highscore(newScore):
    currHigh = load_highscore()
    if newScore > currHigh:
        data = {"highscore": newScore}
        with open("highscore.json", "w") as file:
            json.dump(data, file, indent=4)