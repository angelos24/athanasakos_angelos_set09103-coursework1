from flask  import Flask, url_for, abort, request, render_template, json, flash, redirect, session
app = Flask(__name__)
app.secret_key = "super secret key"

# Custom 401
@app.errorhandler(401)
def http_error_handler(error):
        return render_template('401.html', error=error), error.code

# Custom 404
@app.errorhandler(404)
def http_error_handler(error):
    return render_template('404.html', error=error), error.code

# Web root
@app.route("/")
def root():
        return render_template('index.html'), 200

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            flash('<div class="alert alert-danger" role="alert"> Invalid Credentials. Please try again.</div>')
        else:
            session['logged_in'] = True
            session['username'] = request.form['username']
            return redirect(url_for('root')), 303
    return render_template('login.html'), 200

# Logout page
@app.route("/logout")
def logout():
    session['logged_in'] = False
    flash('<div class="alert alert-success" role="alert"> <strong>Well done!</strong> You have successfully logged out</div>')
    return redirect(url_for('root')), 303

# Add a castle page
@app.route("/upload", methods=['POST', 'GET'])
def upload():

    if not session.get('logged_in'):
        return abort(401)

    if request.method == 'POST':
        name = request.form['castle']
        clan = request.form['clan']
        region = request.form['region']
        date = request.form['date']
        description = request.form['description']

        castles = []
        castles.append({'Castle': name,'Clan': clan, 'Region': region, 'Date': date, 'Description': description})

        # Code for replace "[" with "," when appending new data
        f2 = open("castles.json","r+")
        f2.seek(-2,2)
        f2.write(json.dumps(castles, indent=4).replace('[',',',1))
        f2.close()

        flash(' <div class="alert alert-success" role="alert"> <strong>Well done!</strong> You have successfully added a new entry</div>')

        return  redirect(url_for('upload')), 303
    else :
        return render_template('upload.html'), 200

# Regions page
@app.route("/regions/")
def regions():
    if not session.get('logged_in'):
        return abort(401)
    else:
        return render_template("regions.html"), 200

# Castle Regions page
@app.route("/regions/<path:castle_region>")
def choose_regions(castle_region):
    regions = {'highlands':1,'lowlands':2}
    if not session.get('logged_in'):
        return abort(401)
    
    if castle_region in regions:
        with open("regions.json","r") as f:
            parent_dict = json.load(f)
        return render_template("castle_regions.html", castle_region=castle_region, parent_dict=parent_dict), 200
    else:
        return abort(404)

# Castles page
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
