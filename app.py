import os

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'
    
@app.route('/foursquare/push', methods=['POST'])
def checkin_push():
    if request.method == 'POST':
        app.logger.error('received a post')
        app.logger.error(request.form['secret'])
        app.logger.error(request.form['checkin'])
    else:
        app.logger.error('not a post')
    return 'ok'

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)