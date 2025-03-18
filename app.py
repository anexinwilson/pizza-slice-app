from flask import Flask

app = Flask(__name__)

@app.route('/')
def server_check():
    return "Server up and running"


if __name__ == '__main__':
    app.run(port=8888,debug=True)