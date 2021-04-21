from flask import Flask, render_template, make_response, request
from flask import request
import pymysql

from analyze_speech_funcs import *

con = pymysql.connect(host='some-mysql-taka', user='root', password='my-secret-pw', database='demo', autocommit=True)

# https://stackoverflow.com/questions/55933447/serving-static-files-from-static-folder-with-flask
app = Flask(__name__, static_folder='static')

# Get the current row count. We insert curren session utterances in the next row.
with con.cursor() as cur:
    cur.execute('SELECT * FROM takatable')
    rows = cur.fetchall()  # just a single row containing count
    row_count = len(rows)

# DB methods
# Update curr cum utterances in DB
@app.route("/save", methods=['POST'])
def update_cum_utterances():
    global row_count
    # https://github.com/PyMySQL/PyMySQL/issues/422
    con = pymysql.connect(host='some-mysql-taka', user='root', password='my-secret-pw', database='demo',
                          autocommit=True)
    with con.cursor() as cur:
        # this is our first time connecting (maybe a session existed before)
        curr_cum_utterances = request.form[
            'currCumUtterances']  # .get is for 'GET'. I could prob use .form instead of get_json
        print("curr cum utterances debug: ", curr_cum_utterances)
        print("curr row count debug: ", row_count)
        cur.execute("REPLACE INTO takatable (this_id, this_curr_cum_utterances) VALUES (%s, %s)",
                    [row_count + 1, curr_cum_utterances])

        # TODO: dynamically update this_id to reflect session count
    return {}, 777


# https://www.jitsejan.com/python-and-javascript-in-flask.html
@app.route("/")
def MainPage():
    print("Render default MainPage", flush=True)
    return render_template(
        'MainPage.html')  # Combines a given template with a given context dictionary and returns an HttpResponse object with that rendered text.


# Returns filler word dict
@app.route("/filler", methods=['GET'])
def Filler():
    curr_cum_utterances = request.args.get('currCumUtterances',
                                           default=None)  # Speech text is cumulative. Contains all the text said so far
    filler_count_dict = get_filler_count_dict(curr_cum_utterances)
    # What's returned
    results = {
        "filler_result": filler_count_dict,
    }
    return make_response(results)


# Returns talking speed
@app.route("/speed", methods=['GET'])
def Speed():
    curr_utterance = request.args.get('currUtterance', default=None)  # current sentence/monologue (no break in speech)
    time_elapsed = request.args.get('timeElapsed', default=None)  # in seconds, includes decimal
    talking_speed, corresponding_color, corresponding_text = get_talking_speed(curr_utterance,
                                                                               time_elapsed)  # Talking too fast or slow == red color, just right == green
    # What's returned
    results = {
        "speed_result": talking_speed,
        "speed_color": corresponding_color,
        "speed_text": corresponding_text
    }
    return make_response(
        results)  # https://stackoverflow.com/questions/2428092/creating-a-json-response-using-django-and-python


# Returns most commonly used non-filler words (top 5)
@app.route("/frequent", methods=['GET'])
def Frequent():
    curr_cum_utterances = request.args.get('currCumUtterances',
                                           default=None)  # Speech text is cumulative. Contains all the text said so far
    most_frequent_count_dict = get_frequent_count_dict(curr_cum_utterances)
    # What's returned
    results = {
        "frequent_result": most_frequent_count_dict,
    }
    #		obj = json.dumps(results) # a json object is passed in the json.dumps() function, and its data is extracted and returned in the form of a string:
    return make_response(results)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
