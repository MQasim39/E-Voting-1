from flask import Flask, render_template, request
import uuid
import csv

app = Flask(__name__)
import os
print(os.getcwd())


# Database to store registered users and their voter IDs
registered_users = {}

# Path to the CSV file to save the registered users
CSV_FILE_PATH = 'registered-users.csv'

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        # Get form data
        name = request.form['name']
        hu_id = request.form['huid']
        batch_year = request.form['batch']
        print(name)
        print(hu_id)
        print(batch_year)

        # Generate unique voter ID using uuid library
        voter_id = hash(hu_id + batch_year + name.capitalize())
        # voter_id = uuid.uuid4().hex
        print(voter_id)

        # Check if the voter ID already exists in the CSV file
        with open(CSV_FILE_PATH, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == str(voter_id):
                    # If the voter ID already exists, show an error message
                    error_message = "Voter ID already exists."
                    return render_template("registration_dup.html", error_message=error_message)
        csvfile.close()

        # Add registered user to database
        registered_users[voter_id] = {"name": name, "hu_id": hu_id, "batch_year": batch_year}

        # Save the registered user to the CSV file
        with open(CSV_FILE_PATH, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([voter_id, name, hu_id, batch_year])
            csvfile.flush()
        csvfile.close()

        # Display the generated voter ID to the user
        return render_template("registration.html", voter_id=voter_id)

    return render_template("registration.html")

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        # Get form data
        name = request.form.get("name")
        voter_id = request.form.get("voter_id")

        # Check if the user is registered
        if voter_id in registered_users and registered_users[voter_id]["name"] == name:
            return "You are logged in!" # In practice, you'd want to redirect to a new page instead of returning a string

        # If the user is not registered or their name doesn't match, show an error message
        error_message = "Invalid name or voter ID."
        return render_template("signin.html", error_message=error_message)

    return render_template("signin.html")

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        # Get form data
        name = request.form.get("name")
        voter_id = request.form.get("voter_id")

        # Check if the user is registered and their voter ID is in the database
        if voter_id in registered_users and registered_users[voter_id]["name"] == name:
            return render_template("admin_dashboard.html", registered_users=registered_users)

        # If the user is not registered or their name doesn't match, show an error message
        error_message = "Invalid name or voter ID."
        return render_template("admin.html", error_message=error_message)

    return render_template("admin.html")

@app.route("/viewresults")
def viewresults():
    return render_template("viewresults.html")

if __name__ == "__main__":
    app.run(port=3000, debug=True)