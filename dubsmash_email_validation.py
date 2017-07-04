from flask import Flask, abort, request
import re
import dns.resolver
import smtplib

app = Flask(__name__)

# Create an SMTP client globally to re-use the connection if possible
server = smtplib.SMTP()

@app.route('/validate', methods=['GET'])
def validate():
    email = request.args.get('email', '')

    # Do some basic regex validation first
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
    if not match:
        abort(400)

    # Extract the host
    host = email.split('@')[1]

    # Get the MX record so we can get the SMTP connection afterwards
    try:
        records = dns.resolver.query(host, 'MX')
        mx_record = str(records[0].exchange)
    except dns.exception.DNSException:
        # DNS record couldn't be found!
        abort(400)

    # SMTP Conversation
    server.connect(mx_record)
    server.helo(host)
    server.mail(email)
    code, message = server.rcpt(str(email))
    server.quit()

    # Assume 250 as Success
    if code != 250:
        abort(400)

    return "", 200

# We only need this for local development.
if __name__ == '__main__':
    app.run()
