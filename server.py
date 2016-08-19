import requests
from flask import (
    abort,
    Flask,
    request,
)
from flask_cors import cross_origin

from config import (
    API_KEY,
    DOMAIN,
    TARGET_EMAIL,
)

MAILGUN_URL = "https://api.mailgun.net/v3/{}/messages".format(DOMAIN)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 24 * 1024 * 1024  # Limit uploads to 24 MB


@app.route('/mail', methods=['POST'])
@cross_origin(methods='POST')
def mail():
    data = [
        ('from', 'Mailgun Relay <mailgun@{}>'.format(DOMAIN)),
        ('to', TARGET_EMAIL),
        ('subject', 'Application Received'),
        ('text', 'See attached files.'),
    ]
    files = [('attachment', (f.filename, f)) for f in request.files.values()]
    r = requests.post(
        MAILGUN_URL,
        auth=('api', API_KEY),
        data=data,
        files=files,
    )
    return (
        r.content,
        r.status_code,
        {'Content-Type': r.headers['Content-Type']},
    )


# Return a 400 for all other routes
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def nope(path):
    abort(400)
