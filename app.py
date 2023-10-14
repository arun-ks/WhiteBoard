from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

chat_log = {}
user_counts = {}  # A dictionary to keep track of user counts for each session

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    # Generate a unique username for the client based on the session ID
    session_id = request.sid
    session['username'] = session_id
    #session['username'] = 'User_' + session_id[:5]
    
@socketio.on('message')
def handle_message(data):
    username = session.get('username', 'Guest')
    message = {'user': username, 'text': data}
    chat_log.setdefault(session['username'], []).append(message)
    emit('message', message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
