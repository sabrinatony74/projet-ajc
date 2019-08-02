# coding: utf-8

from mailjet_rest import Client
import os
api_key = '4c392ed6313cbe35ff946c4a67bd5698'
api_secret = 'ff1d1fd6e23e34400d6b95abe8822706'
mailjet = Client(auth=(api_key, api_secret), version='v3.1')
data = {
  'Messages': [
    {
      "From": {
        "Email": "ribeiromaxance@gmail.com",
        "Name": "Maxance"
      },
      "To": [
        {
          "Email": "sabrinatony74@gmail.com",
          "Name": "Sab"
        }
      ],
      "Subject": "Test envoi email",
      "TextPart": "Mon premier email",
      "HTMLPart": "<h3>Salut ça va ?<a href='https://www.mailjet.com/'>Mailjet</a>!</h3><br />May the delivery force be with you!",
      "CustomID": "AppGettingStartedTest"
    }
  ]
}
result = mailjet.send.create(data=data)
print (result.status_code)
print (result.json())