import os
import smtplib
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment variables for sensitive data
tomorrow_io_api_key = os.getenv('TOMORROW_IO_API_KEY')
email_user = os.getenv('EMAIL_USER')  # Your email address
email_password = os.getenv('EMAIL_PASSWORD')  # Your email password

# Check if the environment variables are set
if not all([tomorrow_io_api_key, email_user, email_password]):
    print("Please set the environment variables for Tomorrow.io and email credentials.")
    exit(1)

# Tomorrow.io API
location = 'Fort Wayne'
weather_url = f'https://api.tomorrow.io/v4/timelines?location={location}&fields=temperature,weatherCode&apikey={tomorrow_io_api_key}'

try:
    response = requests.get(weather_url)
    response.raise_for_status()  # Raise an error for bad responses
    weather_data = response.json()
    
    # Print the entire weather data for debugging
    print(weather_data)

    # Extract weather information
    temperature = weather_data['data']['timelines'][0]['intervals'][0]['values']['temperature']
    weather_code = weather_data['data']['timelines'][0]['intervals'][0]['values']['weatherCode']

    # Print the weather code for debugging
    print(f"Weather Code: {weather_code}")

    # Implement a simple mapping for weather codes (example)
    weather_description = {
        "0": "Clear",
        "1": "Partly Cloudy",
        "2": "Cloudy",
        "3": "Overcast",
        "4": "Fog",
        "5": "Drizzle",
        "6": "Rain",
        "7": "Snow",
        # Add more mappings as necessary
    }.get(str(weather_code), "Unknown weather condition")

    # Print the weather description for confirmation
    print(f"Weather Description: {weather_description}")

    # Prepare the SMS message
    recipient_number = ''  # Replace with the recipient's number
    carrier_gateway = 'vtext.com'  # Replace with the appropriate gateway
    sms_message = f'The current temperature is {temperature}°C and the weather is {weather_description}.'
    to_number = f"{recipient_number}@{carrier_gateway}"

    # Send the SMS via email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:  # Replace with your SMTP server
        server.starttls()
        server.login(email_user, email_password)
        server.sendmail(email_user, to_number, sms_message.encode('utf-8')) 

    print(f'Message sent to {recipient_number} via SMS.')

except requests.exceptions.RequestException as e:
    print(f'Error fetching weather data: {e}')
except Exception as e:
    print(f'An error occurred: {e}')
