from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route('/')
def hello_world():
    author = "Jesse Harris"
    return render_template('start.html', author=author)

@app.route('/start', methods = ['POST'])
def start():
    server = request.form['server']
    print("Starting {0}".format(server))
    return redirect('/')

if __name__ == '__main__':
    app.run()
