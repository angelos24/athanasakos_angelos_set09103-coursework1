from flask  import Flask, url_for, abort, request, render_template, json
app = Flask(__name__)

@app.route("/")
def root():
    return render_template('index.html'), 200

@app.route("/upload", methods=['POST', 'GET'])
def upload():
    mdict = {'default' : u'', 'required': u'on', 'name': u'short_text', 'name': u'name', 'submit': u'submit'}
    json_value = json.dumps(mdict, separators=(',',':'))
    return render_template('upload.html'), 200

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
