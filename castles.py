from flask  import Flask, url_for, abort, request, render_template, json, flash, redirect, session
app = Flask(__name__)
app.secret_key = "super secret key"

@app.errorhandler(401)
def http_error_handler(error):
        return render_template('401.html', error=error), error.code

@app.errorhandler(404)
def http_error_handler(error):
    return render_template('404.html', error=error), error.code

@app.route("/")
def root():
        return render_template('index.html'), 200

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            flash('Invalid Credentials. Please try again.')
        else:
            session['logged_in'] = True
            session['username'] = request.form['username']
            return redirect(url_for('root'))
    return render_template('login.html')

@app.route("/logout")
def logout():
    session['logged_in'] = False
    flash('<h1>You have successfully logged out!</h1>')
    return redirect(url_for('root')), 200


@app.route("/upload", methods=['POST', 'GET'])
def upload():

    if not session.get('logged_in'):
        return abort(401)

    if request.method == 'POST':
        name = request.form['castle']
        clan = request.form['clan']
        region = request.form['region']
        date = request.form['date']

        data = [{'Castle': name,'Clan': clan, 'Region': region, 'Date': date}]

        with open('text.json','a') as file:
            file.write(json.dumps(data, sort_keys=True, indent=4))
            file.close()

            flash(' <div class="alert alert-success" role="alert"> <strong>Well done!</strong> You have successfully added a new entry</div')

        return  redirect(url_for('upload'))
    else :
        return render_template('upload.html'), 200


@app.route("/regions")
def regions():
    if not session.get('logged_in'):
        return abort(401)
    else:
        with open("regions.json","r") as f:
            parent_dict = json.load(f)
            return render_template("regions.html", parent_dict=parent_dict), 200

@app.route("/castles")
def results():
    if not session.get('logged_in'):
        return abort(401)
    else:
        with open("castles.json","r") as f:
            parent_dict = json.load(f)
            return render_template("castles.html", parent_dict=parent_dict), 200

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
