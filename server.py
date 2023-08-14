import json

from flask import Flask, render_template, request, render_template_string, url_for

configs = {}
partecipants = []
events = []
config_file = None

app = Flask(__name__)
app.static_folder = 'static'



@app.route("/")
def index():
    return render_template("index.html") #Redirect to the index page



@app.route("/auction", methods=['POST'])
def auction():

    global config_file_name
    global configs
    global partecipants
    global events

    config_file = request.files["file"]
    config_file_name = config_file.filename

    if config_file: # The user wants to resume an auction

        config_file.save("Uploads/" + config_file.filename)

        with open("Uploads/" + config_file.filename, 'r') as file: # Read configs and partecipants
            data = json.load(file) # Retrieve data
            configs = data["configs"]
            partecipants = data["partecipants"]
            events = data["events"]

        return render_template("auction.html", partecipants=partecipants, events=events)
    else:
        return render_template("auction-config.html")



@app.route("/manage-auction", methods=['POST'])
def manage_auction():

    global configs
    global partecipants
    global events

    if len(configs) == 0:

        configs = {
            "partecipants": int(request.form.get('partecipants')),
            "credits": int(request.form.get('credits')),
            "gk": int(request.form.get('gk')),
            "def": int(request.form.get('def')),
            "mid": int(request.form.get('mid')),
            "att": int(request.form.get('att'))
        } # Save configs

        for i in range(0, configs["partecipants"]): # Initialize the partecipants dict
            partecipants.append({
                "name": f"Partecipant {i}",
                "credits": configs["credits"],
                "gk": [],
                "def": [],
                "mid": [],
                "att": []
                })

        with open("Uploads/auction.txt", 'w') as file: # Save configs and partecipants in the file
            data = {"configs": configs, "partecipants": partecipants, "events": events}
            json.dump(data, file)


    elif request.form.get("new-player"): # New player sold
        new_player_name = request.form.get("new-player").upper() # Get the player name
        new_player_cost = int(request.form.get("cost")) # Get the player cost
        partecipant = request.form.get("partecipant") # Get the partecipant

        print(new_player_name + f" sold for {new_player_cost} to " + partecipant)

        for p in partecipants: # Find the partecipant

            if p["name"] == partecipant:

                p["credits"] -= new_player_cost # Remove the credits

                roles = ["gk", "def", "mid", "att"] # Roles list
                for r in roles: # Choose the role
                    if len(p[r]) < configs[r]:
                        role = r
                        break

                p[role].append({new_player_name: new_player_cost}) # Add the player to the partecipant's list
                events.append({"player": new_player_name, "cost": new_player_cost, "partecipant": p["name"]}) # Add the event

                with open("Uploads/auction.txt", 'w') as file: # Save configs and partecipants in the file
                    data = {"configs": configs, "partecipants": partecipants, "events": events}
                    json.dump(data, file)

                break

    return render_template("auction.html", partecipants=partecipants, events=events)



@app.route("/edit-event", methods=['POST'])
def edit_event():

    new_player_name = request.form.get("new-player").upper() # Get the new player name
    new_player_cost = int(request.form.get("new-cost")) # Get the new player cost
    new_partecipant = request.form.get("new-partecipant") # Get the new partecipant

    old_player_name = request.form.get("old-player").upper() # Get the old player name
    old_player_cost = int(request.form.get("old-cost")) # Get the old player cost
    old_partecipant = request.form.get("old-partecipant") # Get the old partecipant

    # Remove the player to the old player
    for p in partecipants: # Find the partecipant

        if p["name"] == old_partecipant:

            p["credits"] += old_player_cost # Add the credits

            roles = ["gk", "def", "mid", "att"] # Roles list
            for r in roles: # Choose the role
                if old_player_name in p[r]:
                    p[r].remove(old_player_name)
                    break

            for e in events:
                if old_player_name in e.get("player"):
                    e["player"] = new_player_name
                    e["cost"] = new_player_cost
                    e["partecipant"] = new_partecipant
                    break

            break
    

    # Add the player to the new partecipant
    for p in partecipants: # Find the partecipant

        if p["name"] == new_partecipant:

            p["credits"] -= new_player_cost # Remove the credits

            roles = ["gk", "def", "mid", "att"] # Roles list
            for r in roles: # Choose the role
                if len(p[r]) < configs[r]:
                    role = r
                    break

            p[role].append({new_player_name: new_player_cost}) # Add the player to the partecipant's list
            break


    with open("Uploads/auction.txt", 'w') as file: # Save configs and partecipants in the file
        data = {"configs": configs, "partecipants": partecipants, "events": events}
        json.dump(data, file)
    
    return render_template("auction.html", partecipants=partecipants, events=events)



if __name__ == "__main__": # Run the app
  app.run()