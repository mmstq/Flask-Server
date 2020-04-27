from flask import Flask
from datetime import datetime
app = Flask(__name__)

@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return """
    <h1>Hello heroku</h1>
    <p>It is currently {time}.</p>
    """.format(time=the_time)

@app.route('/notice', methods=['GET'])
def getNotice():
    return 'Getting Notices'


if __name__ == '__main__':
    from waitress import serve
    serve(app, host='localhost', port=5000)
