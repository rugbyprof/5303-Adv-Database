## Simulation - Overview of Requirements
#### Day of Final


### Overview

This is a script written in some language (Python preferrably) that will simulate the messaging traffic between approx **1,000,000, One Million** users. Given the folling help from previous classes: 

|    |
|:-------:|
|[Helper Starter Script](./gen_data.py) |
|       |
| Mockaroo Data Template |
| <img src="https://cs.msutexas.edu/~griffin/zcloud/zcloud-files/mockaroo_user_structure.png" width = "400"> |
| Chat Client Mini Schema | 
| <img src="https://cs.msutexas.edu/~griffin/zcloud/zcloud-files/chat_client_mini3.png" width="300"> | 

## Users

Write a customized random data generator that will simulate the messaging between approximately 1,000,000 users. 

Your script should generate the users using the schema we discussed and have the ability to send a **JSON** object to some awaiting process. 

Here is a **`Python Requests` **example:

```python
import requests
url = "127.0.0.1:someport"

payload = "{"user_id": 1,"email": "cdudin0@seattletimes.com","username": "cdudin0","first_name": "Carlota","last_name": "Dudin","password": "7P6SzU","create_time": "1/7/2016","last_update": "7/10/2017"}"
headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'Postman-Token': "8ae3425c-b779-4505-9886-fec6642f7f48"
}

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
```

And here is an example **`cUrl`** request:

```json
curl -X POST \
  127.0.0.1:someport \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: 1963ad46-7b19-44cf-b1f0-7e8cf4b2692b' \
  -H 'cache-control: no-cache' \
  -d '    {
        "user_id": 1,
        "email": "cdudin0@seattletimes.com",
        "username": "cdudin0",
        "first_name": "Carlota",
        "last_name": "Dudin",
        "password": "7P6SzU",
        "create_time": "1/7/2016",
        "last_update": "7/10/2017"
    }'
```

All users will be generated at the beginning as a 1 time cost, and will be assigned an age. See below.

## Age

We don't have age in our schema, however a good simulation will take into account every bit of data that it can. So here is a distribution of ages using "Facebook Messenger" that we can use to generate messages with. This data can be used to "assign" an age to one of our million users, and then the message generation portion of the sim will generate accordingly. 

<img src="https://cs.msutexas.edu/~griffin/zcloud/zcloud-files/ages_messaging.png" width="400">

## Friends

Here is a distribution of "Facebook" friends:

<img src="https://cs.msutexas.edu/~griffin/zcloud/zcloud-files/322028_10150417142243415_33481265_o.jpg" width="400">

Its a little skewed (average = 190) but this distribution would work good:
- 25% of people have less than 10 friends, 
- 25% have between 10 and  25 friends
- 25% have between 25 and 100 
- 25% have over 100 friends.

Your script should generate friendships amongst your Million users pretty close to those boundaries above.

## Messages

18-24 y.o. sent and received about 128 text messages per day
25-34 y.o. sent and received about 75 text messages per day
35-44 y.o. sent and received about 52 text messages per day
45-54 y.o. sent and received about 33 text messages per day
55+ y.o. sent and received about 16 text messages per day

<img src="https://cs.msutexas.edu/~griffin/zcloud/zcloud-files/sms_messages_count.png" width="400">

### Deliverables

Your script should be able to:
- Generate 1 million users
- Assign friendships according to the stats above
- Generate messages according to the stats above (and the DB schema)

Of course it also needs to able to insert its values into some database. That will be discussed in class today. 