import logging
import os

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    logging.warning('ok')
    return 'Hello World!'
    
@app.route('/foursquare/push', methods=['POST'])
def checkin_push():
    logging.warning('   received a post')
    logging.warning(request.form['secret'])
    logging.warning(request.form['checkin'])

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)