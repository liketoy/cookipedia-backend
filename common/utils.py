import boto3
from botocore.exceptions import ClientError
from django.conf import settings

def slug_to_name(value):
    return value.replace("-", " ")




def send_email(subject=None, recipients=None, html=None):
    SENDER = "byby8992@naver.com"
    AWS_REGION = "ap-northeast-2"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = (
        "Amazon SES Test (Python)\r\n"
        "This email was sent with Amazon SES using the "
        "AWS SDK for Python (Boto)."
    )

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client(
        "ses",
        region_name=AWS_REGION,
        aws_access_key_id=settings.SES_ACCESS_KEY_ID,
        aws_secret_access_key=settings.SES_SECRET_ACCESS_KEY,
    )

    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                "ToAddresses": recipients,
            },
            Message={
                "Body": {
                    "Html": {
                        "Charset": CHARSET,
                        "Data": html,
                    },
                    "Text": {
                        "Charset": CHARSET,
                        "Data": BODY_TEXT,
                    },
                },
                "Subject": {
                    "Charset": CHARSET,
                    "Data": subject,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print("메일 전송 에러", e.response["Error"]["Message"])
    else:
        print("메일 발신 성공")
        print("Email sent! Message ID:"),
        print(response["MessageId"])
