#!/bin/python

from flask import Flask

app = Flask(__name__)

@app.route("/")
def KioskTerminal():
    return "NuevoTest"

app.run(host="0.0.0.0", port=8000)
