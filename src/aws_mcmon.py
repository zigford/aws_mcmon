import aws_mcstatus
import time
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import jsonify
from threading import Timer

app = Flask(__name__)
debug = True
defaultTimeout = 30 #minutes

# Initialize instance statuses
awsinstances = aws_mcstatus.initInstances(defaultTimeout)
bgCheck = aws_mcstatus.RepeatedTimer(300, aws_mcstatus.updateStatuses, awsinstances) # it auto-starts, no need of rt.start()

@app.route('/')
def home_page():
    title = "aws_mcstatus"
    return render_template('start.html', title=title)

@app.route('/start', methods = ['POST'])
def start():
    server = request.form['server']
    print("Starting {0}".format(server))
    aws_mcstatus.startInstance(server)
    return redirect('/')

@app.route('/status')
def status():
    stats = []
    for i in awsinstances:
        stats.append({'instance' : i.id, 'state' : i.state, 'users' : i.users, 'host' : i.host})
    return jsonify(stats)


if __name__ == '__main__':
    app.run()
