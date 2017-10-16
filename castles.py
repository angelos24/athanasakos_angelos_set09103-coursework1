from flask  import Flask, url_for, abort, request, render_template, json, flash, redirect
app = Flask(__name__)
app.secret_key = "super secret key"

@app.route("/")
def root():
    return render_template('index.html'), 200

@app.route("/upload", methods=['POST', 'GET'])
def upload():
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

@app.route("/results")
def results():
    with open("text.json","r") as f:
        parent_dict = json.load(f)
    return render_template("results.html", parent_dict=parent_dict), 200

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
