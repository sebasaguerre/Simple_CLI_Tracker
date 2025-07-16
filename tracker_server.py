import os
import csv
from dotenv import load_dotenv
from datetime import datetime
from flask import Flask, request, session, redirect, url_for, render_template_string

##NOTES FLASK
# in app.route("\<>") enables you to give input to to feed in as a parameter to a function

#extract secret key from enviorment
load_dotenv()
secret_key = os.getenv("SECRET")

app = Flask(__name__)
app.secret_key = secret_key
 
# extra metrics from data file
with open("data.csv", "r") as fhand:
    reader = csv.reader(fhand)
    metrics = next(reader)


Questions = [metric + ": 1-10 or 'quit'" for metric in metrics]

# template string for rendering the promgt page
PROMPT_TEMPLATE = """
<!doctype html>
<title>Log</title>
<h2>{{question}}</h2>
<form method="post">
    <input type="text" name="reponse">
    <input type="submit" value="Next">
</form>
"""
@app.route("/")
def home():
    home = """
    <!doctype html>
    <title>Tracker Home</title>
    <h1>What would you like to do?</h1>
    <form action="/tracker">
        <button type="submit">Log</button>
    </from>
    """

    return home

# this is the main route where the user interacts with the tracker
@app.route("/tracker", methods=["POST", "GET"])
def tracker():
    # initialize session state if its the first visit
    if "step" not in session:
        session["step"] = 0
        session["responses"] = []

    if request.method == "POST":
        # save the current response
        response = request.form.get("response")
        session["response"].append(response)
        session["step"] += 1
    
    # Check if we are done asking questions
    if session["step"] >=len(Questions):
        log_data(session["responses"])
        session.clear()
        return "Data has been logged. <a href='\tracker'> Log again<\a>"
    
    # ask the next question 
    question = Questions[session["step"]]
    return render_template_string(PROMPT_TEMPLATE, question=question)

def log_data(responses):
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M")
    row = [timestamp] + responses

    # log data to csv
    with open("data.csv", "a", newline="") as fhand:
        writer = csv.writer(fhand)
        writer.writerow(row)

@app.route("/stats")
def stats():
    pass

if __name__ == "__main__":
    app.run(debug=True)