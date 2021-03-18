from flask import Flask, send_from_directory, safe_join

app = Flask(__name__, template_folder='tmp')

app.config['COUNTRY_IMG_PATH'] = 'flags'

@app.route('/')
def index():
    return "Hello World"


@app.route('/flags/<country>')
def get_image(country):
    filename = country + ".gif"
    filepath = safe_join(country,filename)
    a = send_from_directory(app.config['COUNTRY_IMG_PATH'], filepath)
    return a

if __name__ == "__main__":
    app.run()