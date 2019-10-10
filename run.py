from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit
import os
import random
from shutil import copyfile

# Init the server
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

def get_next_image(data):
    if data == {}: return "static/landscape_target/"+random.choice([x for x in os.listdir("static/landscape_target/") if "seen" not in x and "semantic" not in x])    
    src = data["src"].split('/')[-1]    
    os.rename("static/landscape_target/"+src, "static/landscape_target/seen_"+src)
    return "static/landscape_target/"+random.choice([x for x in os.listdir("static/landscape_target/") if "seen" not in x and "semantic" not in x])

@app.route('/')
def root():
    """ Send HTML from the server."""
    return render_template('chat.html')

@socketio.on('joined')
def user_joined(message):
    emit('image', {"image":get_next_image(message)})    

@socketio.on('next_image')
def next_image(message):    
    emit('image', {"image":get_next_image(message)})    


@socketio.on('save_image')
def save_image(data):
    if data != {}:
        src = data["src"].split('/')[-1]    
        copyfile("static/landscape_target/"+src, "output/"+src)        
    emit('image', {"image":get_next_image(data)})

if __name__ == '__main__':
    socketio.run(app)