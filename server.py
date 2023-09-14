import json
import datetime

from flask import Flask, render_template, request, render_template_string, url_for, session


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.static_folder = 'static'



# Main route
@app.route("/") 
def index():

    return render_template("index.html") #Redirect to the index page



@app.route("/auction", methods=['POST'])
def auction():

    config_file = request.files["file"] # Save the file auction config name 

    if config_file: # The user wants to resume an auction

        session['file_name'] = "Uploads/" + config_file.filename
        config_file.save("Uploads/" + config_file.filename) # Save the file into the Uploads folder

        configs, partecipants, events = get_data_from_file("Uploads/" + config_file.filename)


        return render_template("auction.html", partecipants=partecipants, events=events)
    else:
        return render_template("auction-config.html")



@app.route("/manage-auction", methods=['POST'])
def manage_auction():

    # Retrieve data from session
    file_name = session.get('file_name')

    if not file_name: # New auction

        formatted_datetime = datetime.datetime.now().strftime("%H-%M-%d-%m-%Y") # Get formatted daytime

        configs = {
            "partecipants": int(request.form.get('partecipants')),
            "credits": int(request.form.get('credits')),
            "gk": int(request.form.get('gk')),
            "def": int(request.form.get('def')),
            "mid": int(request.form.get('mid')),
            "att": int(request.form.get('att')),
            "file": f"Uploads/{formatted_datetime}-auction.txt"
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

        save_new_data(f"Uploads/{formatted_datetime}-auction.txt", configs, partecipants, events)


    elif request.form.get("new-player"): # New player sold

        configs, partecipants, events = get_data_from_file(file_name)

        new_player_name = request.form.get("new-player").upper() # Get the player name
        new_player_cost = int(request.form.get("cost")) # Get the player cost
        partecipant = request.form.get("partecipant") # Get the partecipant

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

                print(f"{new_player_name} sold for {new_player_cost} to {p['name']}")

                save_new_data(file_name, configs, partecipants, events)

                break

    return render_template("auction.html", partecipants=partecipants, events=events)



@app.route("/edit-event", methods=['POST'])
def edit_event():

    file_name = session.get('file_name')
    configs, partecipants, events = get_data_from_file(file_name)

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
            for r in roles:
                for player in p[r]:
                    if old_player_name in player:
                        p[r].remove(player)
                        break

            for e in events: # Edit the event
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


    save_new_data(file_name, configs, partecipants, events)
    
    return render_template("auction.html", partecipants=partecipants, events=events)



@app.route("/edit-partecipant", methods=['POST'])
def edit_partecipant():

    file_name = session.get('file_name')
    configs, partecipants, events = get_data_from_file(file_name)

    new_partecipant = request.form.get("new-partecipant") # Get the new partecipant
    old_partecipant = request.form.get("old-partecipant") # Get the old partecipant

    for p in partecipants: # Rename the old partecipant
        if p["name"] == old_partecipant:
            p["name"] = new_partecipant
            break

    for e in events: # Rename the partecipant in each event
        if e["partecipant"] == old_partecipant:
            e["partecipant"] = new_partecipant

    save_new_data(file_name, configs, partecipants, events)
    

    return render_template("auction.html", partecipants=partecipants, events=events)



@app.route("/delete-event", methods=['POST'])
def delete_event():

    file_name = session.get('file_name')
    configs, partecipants, events = get_data_from_file(file_name)

    player = request.form.get("event") # Get the player name

    for e in events: # Edit the event
        if player in e.get("player"):
            events.remove(e)
            partecipant = e["partecipant"]
            cost = e["cost"]
            break

    # Remove the player to the old player
    for part in partecipants: # Find the partecipant

        if part["name"] == partecipant:

            part["credits"] += cost # Add the credits

            roles = ["gk", "def", "mid", "att"] # Roles list
            for r in roles:
                for p in part[r]:
                    if player in p:
                        part[r].remove(p)
                        break

            break
    
    save_new_data(file_name, configs, partecipants, events)

    
    return render_template("auction.html", partecipants=partecipants, events=events)


def get_data_from_file(file_name):

    with open(file_name, 'r') as file: # Read configs and partecipants
            data = json.load(file) # Retrieve data
            configs = data["configs"]
            partecipants = data["partecipants"]
            events = data["events"]

    return configs, partecipants, events

def save_new_data(file_name, configs, partecipants, events):

    with open(file_name, 'w') as file: # Save configs and partecipants in the file
        data = {"configs": configs, "partecipants": partecipants, "events": events}
        json.dump(data, file)

if __name__ == "__main__": # Run the app
  app.run()