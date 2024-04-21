from flask import Flask, request, render_template, redirect, url_for
import string, random

app = Flask(__name__)

shortened_urls = {}

def create_url(lenght=6):
    letters = string.ascii_letters + string.digits
    url = ''.join(random.choice(letters) for i in range(lenght))
    return url

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['long_url']
        while short_url in shortened_urls:
            short_url = create_url()
        shortened_urls[short_url] = long_url
        print(shortened_urls)
        return f"Shortened URL: {short_url}"
    elif request.method == 'GET':
        return render_template('index.html')

@app.route('/<short_url>')
def redirect_url(short_url):
    long_url = shortened_urls.get(short_url)
    if long_url: return redirect(shortened_urls[long_url])
    else: return f"URL not found"

if __name__ == '__main__':
    app.run(debug=True)