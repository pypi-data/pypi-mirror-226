# whatsappconnect: On-Premises WhatsApp Integration Module

whatsappconnect is a versatile Python module designed to facilitate seamless integration of WhatsApp messaging capabilities within your on-premises environment. With an emphasis on security, control, and customization, this module empowers you to manage your communication needs directly from your infrastructure. Whether it's sending and receiving messages, handling user interactions, or managing settings, WhatsAppPrem simplifies on-premises WhatsApp integration.

## Features

- **Secure Integration**: WhatsAppPrem allows you to integrate WhatsApp messaging while maintaining data privacy and security within your on-premises environment.

- **User Management**: Efficiently manage users by creating, updating, deleting, and retrieving user details through the provided API functions.

- **Message Handling**: Send, receive, and mark messages as read through the intuitive API, enabling smooth communication flows.

- **Settings Control**: Customize your integration with flexible settings management. Retrieve, update, and configure application settings as per your requirements.

- **Webhooks Support**: Integrate with external services seamlessly using webhook functionality for real-time updates.

- **Compliance Management**: Fulfill regulatory requirements by managing business profiles and compliance information.

## Installation

You can install WhatsAppPrem using pip:

```bash
pip install whatsappconnect



Usage

Here's a simple example of using WhatsAppPrem to send a text message:

python

from whatsappprem import WhatsApp

api_ip = "YOUR_API_IP"
base64_auth = "YOUR_BASE64_AUTH"
password = "YOUR_PASSWORD"

whatsapp = WhatsApp(api_ip, base64_auth, password)

payload = {
    "to": "RECIPIENT_NUMBER",
    "text": "Hello, this is a test message."
}

response = whatsapp.message.send(payload)
print(response)



Please replace placeholders like `YOUR_API_IP`, `YOUR_BASE64_AUTH`, and others with actual values. Also, ensure to provide an actual link to your documentation if available.


Class: WhatsApp

This is the main class that serves as an entry point for interacting with the WhatsApp on-premises API.

Constructor:

python

whatsapp = WhatsApp(api_ip, base64_auth, password)

    api_ip (str): The URL of the WhatsApp on-premises API.
    base64_auth (str): Base64-encoded authentication token for authorization.
    password (str): Password for authentication.

Attributes:

    whatsapp.user: An instance of the User class for user-related operations.
    whatsapp.message: An instance of the Message class for sending and receiving messages.
    whatsapp.settings: An instance of the Settings class for managing application settings.
    whatsapp.registration: An instance of the Registration class (if available) for user registration and verification.

Class: Message

This class handles sending and receiving messages.

Method: send(payload)
Send a text message.

    payload (dict): A dictionary containing message details, such as recipient's number and message text.
    Returns: JSON response indicating the status of the sent message.

Method: read(message_id)
Mark a message as read.

    message_id (str): ID of the message to be marked as read.
    Returns: JSON response indicating the status of marking the message as read.

Class: User

This class manages user-related operations.

Method: adminLogin(password)
Authenticate as an admin user.

    password (str): Password for admin authentication.
    Returns: JWT token after successful admin login.

Method: userLogin(username, password)
Authenticate as a regular user.

    username (str): Username of the user.
    password (str): Password of the user.
    Returns: JWT token after successful user login.

Method: createUser(username, password)
Create a new user.

    username (str): Username for the new user.
    password (str): Password for the new user.
    Returns: JSON response indicating the status of user creation.

... and more methods for user management, such as retrieving user details, updating passwords, deleting users, and logging out.
Class: Settings

This class handles application settings and configurations.

Method: getSettings()
Retrieve application settings.

    Returns: JSON response containing application settings.

Method: getShards()
Retrieve information about shards.

    Returns: JSON response containing shard information.

... and more methods for managing settings, webhooks, media providers, compliance info, profile details, and more.
Class: Registration (if available)

This class manages user registration and verification.

Method: request_code(cc, phone_number, method, cert)
Request a verification code for registration.

    cc (str): Country code.
    phone_number (str): Phone number.
    method (str): Verification method.
    cert (str): Certificate.
    Returns: JSON response indicating the status of the code request.

Method: verify_registration(code)
Verify registration using the provided code.

    code (str): Verification code.
    Returns: JSON response indicating the status of the verification.

Note: This class is only present if registration-related functionality is available.