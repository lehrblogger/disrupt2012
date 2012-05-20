import logging
import os
from flask import Flask, request
import simplejson as json
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
        try:
            checkin = json.loads(request.form['checkin'])
            logging.info('got checkin')
            conn = psycopg2.connect(host=os.environ['DB_HOST'], database=os.environ['DB_NAME'], user=os.environ['DB_USER'], password=os.environ['DB_PASSWORD'], sslmode='require')
            logging.info('connected to DB')
            cur = conn.cursor()
            cur.execute("SELECT numbers FROM users WHERE foursquare_id=%s;", (checkin['user']['id']))
            numbers = cur.fetchone()
            logging.info('got numbers %s' % numbers)
            conn.close()
            if numbers:
                client = TwilioRestClient(os.environ['TWILIO_ACCOUNT'], os.environ['TWILIO_TOKEN'])
                logging.info('got twilio')
                for number in numbers[0].split(','):
                    client.sms.messages.create(to='+1%s' % number, from_=os.environ['TWILIO_OUTGOING'],
                        body='%s %s just checked in to %s. Why don\'t you head there now?' % (checkin['user']['firstName'], checkin['user']['lastName'], checkin['user']['venue']['name']))
            return 'Checkin push received successfully', 200
        except Exception, e:
            logging.error("Error processing checkin: %s" % e)
            if conn: conn.close()
            raise e
            return 'Internal server error', 500
    return 'Invalid push secret', 401
        
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)-8s %(message)s')
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
