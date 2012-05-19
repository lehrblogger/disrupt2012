import logging
import os
from flask import request

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    logging.warning('ok')
    return 'Hello World!'
    
@app.route('/foursquare/push', methods=['POST'])
def checkin_push():
    if request.form['secret'] == os.environ['PUSH_SECRET']:
        logging.info(request.form['checkin'])
        return "Checkin push received successfully", 200
    else:
        return "Invalid push secret", 401
        
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)