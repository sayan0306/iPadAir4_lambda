import json
import requests
from bs4 import BeautifulSoup
import boto3
from botocore.exceptions import ClientError
import datetime


def lambda_handler(event, context):
    changed = scrape_webpage()
    if changed is None:
        send_email("error")
    elif not changed:
        send_email("same")
    else:
        send_email(changed)
    return {
        'statusCode': 200,
        'body': json.dumps({'timestamp': str(datetime.datetime.utcnow()),
                            'status': changed})
    }


def scrape_webpage():
    #visit URL and check the text in the HTML tag
    webpage_url = "https://www.apple.com/ie/ipad-air/"
    page = requests.get(webpage_url).text
    soup = BeautifulSoup(page, "html.parser")
    try:
        span = soup.find('span', {'class': 'ac-ln-title-comingsoon'})
    except:
        print("Something went wrong")
        return None
    if span.text != "Available in October":
        print("Something changed")
        return span.text
    else:
        print("nothing changed")
        return False


def send_email(msg):

    #fill in your info here:
    SENDER = "" 
    RECIPIENT = ""
    ACCESS_KEY = ""
    SECRET_KEY = ""

    AWS_REGION = "eu-west-1"
    CHARSET = "UTF-8"

    if msg == 'error':
        SUBJECT = "AppleiPadAir4 - ERROR"

        BODY_TEXT = "Something has gone wrong with the script. Please check immediately"

        BODY_HTML = """<html>
        <head></head>
        <body>
        <div style="text-align:center;">
          <h1>AppleiPadAir4 - Script Error:</h1>
          <p>Something has gone wrong with the script. Please check immediately</p>
        </div>
        </body>
        </html>"""

    elif msg == 'same':
        SUBJECT = "AppleiPadAir4 - STAYALIVE"

        BODY_TEXT = "No status change regarding iPad Air 4 availability yet."

        BODY_HTML = """<html>
        <head></head>
        <body>
          <div style="text-align:center;">
              <h1>Status update - No Change:</h1>
              <p>The iPad Air 4 status is still "Available in October"</p>
        </div>
        </body>
        </html>"""

        if not datetime.datetime.now().strftime("%H") == '14':
            return

    else:
        SUBJECT = "AppleiPadAir4 - Status Change!"

        BODY_TEXT = "AppleiPadAir4 status has changed! Check the website for a definite date."

        BODY_HTML = """<html>
        <head></head>
        <body>
          <div style="text-align:center;">
              <h1>Status update - IT HAS CHANGED!</h1>
              <p>The iPad Air 4 status has changed to %s "</p>
        </div>
        </body>
        </html>""" % msg

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',
                          region_name=AWS_REGION,
                          aws_access_key_id=ACCESS_KEY,
                          aws_secret_access_key=SECRET_KEY
                          )

    # Try to send the email.
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])


if __name__ == "__main__":
    lambda_handler(None, None)
