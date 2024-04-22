from flask import Flask, request, render_template, redirect, url_for
import json
import string, random

app = Flask(__name__)

shortened_urls = {}
shortened_urls = json.load(open("urls.json", "+r"))

def create_url(lenght=6):
    letters = string.ascii_letters + string.digits
    url = ''.join(random.choice(letters) for i in range(lenght))
    return url

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_url = create_url()

        if long_url in shortened_urls.values():
            return "error: url already shortened"

        while short_url in shortened_urls:
            short_url = create_url()
        
        shortened_urls[short_url] = long_url
        with open('urls.json', '+w') as file:
            json.dump(shortened_urls, file)
        return render_template("index.html", short_url=short_url)
    else:
        return render_template('index.html')

@app.route('/<short_url>')
def redirect_url(short_url):
    long_url = shortened_urls.get(short_url)
    if long_url: 
        return redirect("http://" + long_url)
    else:
        return render_template("index.html", not_found=True)

if __name__ == '__main__':
    app.run(debug=False)