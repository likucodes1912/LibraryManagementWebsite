from flask import Flask

app = Flask(__name__,template_folder="template")

@app.route("/test")
def test():
    return "__init__ route test"

from app import ISBN  # Import routes after initializing app