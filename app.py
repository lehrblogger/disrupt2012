import logging
import os
from flask import Flask, request
import simplejson as json
from twilio import TwilioRestException
from twilio.rest import TwilioRestClient
import psycopg2
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'
    
@app.route('/foursquare/push', methods=['POST'])
def checkin_push():
    if request.form['secret'] == os.environ['PUSH_SECRET']:
        conn = None
        checkin = json.loads(request.form['checkin'])
        logging.info(checkin)
        if 'shout' in checkin and (checkin['shout'].find('#posse') >= 0 or checkin['shout'].find('#p0sse') >= 0):
            try:
                conn = psycopg2.connect(host=os.environ['DB_HOST'], database=os.environ['DB_NAME'], user=os.environ['DB_USER'], password=os.environ['DB_PASSWORD'], sslmode='require')
                cur = conn.cursor()
                cur.execute("SELECT nickname, numbers FROM users WHERE foursquare_id=%s;", (checkin['user']['id']))
                result = cur.fetchone()
                conn.close()
            except Exception, e:
                logging.error("Database error: %s" % e)
                if conn: conn.close()
                return 'Internal server error', 500
            logging.info(result)
            if result and result[1]:
                client = TwilioRestClient(os.environ['TWILIO_ACCOUNT'], os.environ['TWILIO_TOKEN'])
                if result[0]:
                    message = '%s just checked in to %s at %s. Why don\'t you head there now?' % \
                        (result[0], checkin['venue']['name'], checkin['venue']['address'])
                else:
                    message = '%s %s just checked in to %s at %s. Why don\'t you head there now?' % \
                        (checkin['user']['firstName'], checkin['user']['lastName'], checkin['venue']['name'], checkin['venue']['address'])
                for number in result[1].split(','):
                    try:
                        client.sms.messages.create(to='+1%s' % number, from_=os.environ['TWILIO_OUTGOING'], body=message)
                    except TwilioRestException, e:
                        logging.error("Error sending message with Twilio to number %s for user %s: %s" % (number, checkin['user']['id'], e))
        return 'Checkin push received successfully', 200
    return 'Invalid push secret', 401
        
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)-8s %(message)s')
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
