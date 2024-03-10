#!/usr/bin/python3
"""
    Class to Handle API requests and Message generation
                                                        """
import time
import json
import requests
import re

class MessageAPI:
    """
        Handles API requests to external APIs such as text generation and sending of messages
                                                                                            """
    def open_ai(topic):
        """
            Uses OpenAI API to generate message based on user input
                                                                    """
        from openai import OpenAI

        client = OpenAI()

        ai_responses = []

        for i in range(3):
            response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Suggest one mid-length message for bulk sms based on topic provided."},
                {"role": "user", "content": "{}".format(topic)},
            ]
            )

            ai_responses.append(response.choices[0].message.content)
            time.sleep(1)
        
        return ai_responses
    
    def verify_number_api(phonenumber):
        """
            Checks validity of phone numbers
                                            """
        # key = 'KMH8ovJtxEQGMliPkdItmPcej6V185yJ'
        validity_dict = {
                        'True': [],
                        'False': []
                        }

        for number in phonenumber:
            val_number = str(number)
            regex = re.match('\+', val_number)
            
            if not regex:
                if val_number.startswith('0'):
                    val_number = val_number[1:]
                val_number = '+233' + val_number
            
            if regex and not val_number[1:].isdigit():
                continue
            
            # url = 'https://www.ipqualityscore.com/api/json/phone/{}/{}'.format(key, val_number)
            # x = requests.get(url)
        
            # result = json.loads(x.text)
            # print(result)
            
            response = requests.get("https://phonevalidation.abstractapi.com/v1/?api_key=374e0576f42843b2a6840292c3c5a933&phone={}".format(val_number))
            response_dict = response.content.decode('utf-8')
            response_dict =  json.loads(response_dict)
            response_code = response.status_code
            print(response_dict)
            
            if response_dict['valid'] and response_code == 200:
                 validity_dict['True'].append(number)
            
            if not response_dict['valid'] and response_code == 200:
                 validity_dict['False'].append(number)
        
        return validity_dict

    def message_engine(message: str, recipient_list: list, user_object):
        """
            Sends Messages to specified numbers
                                                """
        sender_message = "FROM:\n{0}, {1}\n\n{2}".format(user_object.name, user_object.number, message).encode('utf-8')

	
        endPoint = 'https://api.mnotify.com/api/sms/quick'
        apiKey = 'FMjNgP4IheIsRPnNWo80MEM2L'

        print(recipient_list)
        data = {
                'recipient[]': recipient_list,
                'sender': 'ALX PROJECT',
                'message': sender_message,
                'is_schedule': False,
                'schedule_date': ''
            }

        url = endPoint + '?key=' + apiKey
        response = requests.post(url, data)
        data = response.json()

        with open('TextTitan.txt', mode="a", newline="") as file:
            file.write(str(data) + "\n\n")

        if data['status'] == 'success' and data['code'] == '2000':
            return True

        return False
