# psusannx_email

A package that allows emails to be sent through a python function using [Sendgrid](https://www.sendgrid.com/), provided a valid [Sendgrid API Key](https://docs.sendgrid.com/ui/account-and-settings/api-keys#creating-an-api-key) is passed as an argument to the function (`sendgrid_api_key`).

The docs for using Sendgrid with python can be found [here](https://docs.sendgrid.com/for-developers/sending-email/quickstart-python).

This package was created to be used as a subpackage in a wider project - PSUSANNX.

## Package Functions

- send_email()

## Installation

```python
pip install psusannx-email
```

## Usage

```python
# Import the function from the package
from psusannx_email import send_email

# Get some info about the function
help(send_email) 
```

Now use the function to send an email.

```python
# Send a test email from your own personal email (once you have a sendgrid api key)
send_email(
    subject="Test email using the psusannx_email package", 
    body="This is a test email.\n\nThanks.",
    from_email="<your-email>",
    recipients=["<recipient-1>", "<recipient-2>"],
    sendgrid_api_key="<verified-sendgrid-api-key>"
)
```

## Notes

- The package is quite restricted in what it can do, but it only needs to do things that are required by the parent project so there won't be much development.
- A new feature that will be added is the ability to send emails where the body is html, rather than just plain text.
