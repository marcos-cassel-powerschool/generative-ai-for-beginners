import os
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get('name', 'World')
    return f'Hello, {name}!'

@app.errorhandler(404)
def page_not_found(error):
    return "Sorry, the requested page was not found.", 404

@app.errorhandler(500)
def internal_server_error(error):
    return "Sorry, something went wrong on the server.", 500

if __name__ == '__main__':
    # Load environment variables
    secret_key = os.environ.get('SECRET_KEY')

    # Start the Flask app
    app.run()