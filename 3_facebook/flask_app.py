from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timezone
import time
import main


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/products/post', methods=['POST'])
def start_bot():
    # print("hello")
    data = request.get_json()
    print(data)

    postLink = data['postLink']
    userName = data['userName']
    password = data['password']
    dateTime = data['dateTime']

    # start_time_string = "2024-03-04T17:51:00.000Z"
    start_time_format = "%Y-%m-%dT%H:%M:%S.%fZ"

    # Convert the start time string to a time struct
    start_time = time.strptime(dateTime, start_time_format)

    # Calculate the time difference in seconds between the current time and the start time
    current_time = time.gmtime()
    time_difference = time.mktime(start_time) - time.mktime(current_time)

    # Wait until the specified start time is reached
    time.sleep(time_difference)

    # Run your program here
    print("Program started at", dateTime)

    response_data = main.run(userName, password)

    return response_data


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)