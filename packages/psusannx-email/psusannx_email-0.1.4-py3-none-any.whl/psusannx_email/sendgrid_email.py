import sendgrid
from sendgrid.helpers.mail import Mail, Content

def send_email(sendgrid_api_key: str, subject: str, body: str, from_email: str, recipients: list):
    """
    A function to send emails using the sendgrid service.
    A valid sendgrid API keey needs to be passed for the function to work.
    
    Parameters
    ----------
    subject: The subject of the email.
        
    body: The body of text for the email.

    from_email: The email to be used to send the email 
                (this should be set up on the sendgrid website when setting up the sendgrid api key).

    recipients: A list of email addresses to send the email to.
                Or just a string for a single recipient.
        
    sendgrid_api_key: The verified sendgrid api key associated with the sender email.
    
    Returns
    -------
    None
    """
    
    # Create the content to be sent in the email
    content = Content("text/plain", str(body))
    
    # Compile the email info as a Mail object
    mail = Mail(from_email, recipients, str(subject), content)
    
    # Try to send the email
    try:
        sg = sendgrid.SendGridAPIClient(sendgrid_api_key)
        response = sg.client.mail.send.post(request_body=mail.get())

    except Exception as e:
        print("ERROR")
        print(e.message)