# 1. import Flask
from flask import Flask, jsonify

# 2. Create an app, being sure to pass __name__
app=Flask(__name__)

# 3. Define what to do when a user hits the index route
@app.route("/")


