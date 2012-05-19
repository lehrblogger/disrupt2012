import logging
import os
from flask import Flask, request
import simplejson as json
from twilio.rest import TwilioRestClient
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'
    
@app.route('/foursquare/push', methods=['POST'])
def checkin_push():
    if request.form['secret'] == os.environ['PUSH_SECRET']:
        checkin = json.loads(request.form['checkin'])
        client = TwilioRestClient(os.environ['TWILIO_ACCOUNT'], os.environ['TWILIO_TOKEN'])
        client.sms.messages.create(to=os.environ['MY_CELL'], from_=os.environ['TWILIO_OUTGOING'],
            body='Hello there, %s %s!' % (checkin['user']['firstName'], checkin['user']['lastName']))
        return "Checkin push received successfully", 200
    else:
        return "Invalid push secret", 401
        
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)-8s %(message)s')
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)