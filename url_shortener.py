from flask import Flask,render_template,request,redirect,url_for,flash,abort,session,jsonify
import json
import os

app = Flask(__name__)
app.secret_key = 'abrakadabra'

@app.route('/')
def index():
    return render_template('index.html',codes=session.keys())

@app.route('/your-url',methods=['GET','POST'])
def your_url():
    if request.method == 'POST':
        urls = {}
        if os.path.exists('urls.json'):
            with open('urls.json') as url_file:
                urls = json.load(url_file)
        if request.form['code'] in urls.keys():
            flash('That short name has already been taken. Please use another name.')
            return redirect(url_for('index'))


        urls[request.form['code']] = { 'url' : request.form['url'] }

        with open('urls.json','w') as url_file:
            json.dump(urls, url_file)
            session[request.form['code']] =True

        return render_template('your_url.html',code=request.form['code'])
    else:
        return redirect(url_for('index'))

@app.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as url_file:
            urls = json.load(url_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])

    return abort(404)

@app.errorhandler(404)
def page_not_found_error(error):
    return render_template('page_not_found.html'),404

@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))

if __name__ == '__main__':
    app.run(debug=True)