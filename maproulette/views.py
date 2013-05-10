from maproulette import app, oauth
from flask import render_template, redirect, request, session

# By default, send out the standard client
@app.route('/')
def index():
    "Display the index.html"
    return render_template('index.html')

@app.route('/api/challenges')
def challenges_api():
    "Returns a list of challenges as json"
    pass

@app.route('/api/task')
def task():
    """Returns an appropriate task based on parameters"""
    # We need to find a task for the user to work on, based (as much
    # as possible)
    difficulty = request.args.get('difficulty', 'easy')
    near = request.args.get('near')
    if near:
        lat, lon = near.split(',')
    else:
        point = None
    pass

@app.route('/api/c/<challenge>/meta')
def challenge_meta(challenge):
    "Returns the metadata for a challenge"
    pass

@app.route('/api/c/<challenge>/stats')
def challenge_stats(challenge):
    "Returns stat data for a challenge"
    pass

@app.route('/api/c/<challenge>/task')
def challenge_task(challenge):
    "Returns a task for specified challenge"
    pass

@app.route('/api/c/<challenge>/task/<id>', methods = ['POST'])
def challenge_post(challenge, task_id):
    "Accepts data for completed task"
    pass

@app.route('/logout')
def logout():
    session.destroy()
    return redirect('/')
