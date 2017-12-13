import stripe
import json
import datetime

from rauth import OAuth2Service

def setupOAuth(secret_key, client_key):

#secret key from stripe
API_KEY = "sk_test_UYMnzUZuCVwBhvrw5AaXhrLr"
CLIENT_ID = "ca_BwZlB8boPtETxPr19vMjVRuzfsnO2Nnr"
NOW = datetime.datetime.now()

stripe.api_key = API_KEY

# Create Customer uses email
customer = stripe.Customer.create(email="customer1@yahoo.com")
print customer

#Create Card (Stripes Dummy card data)
DUMMY_CARD = { "number":'4242424242424242',
               "exp_month":NOW.month,
               "exp_year":NOW.year +4,
               "cvc":123
               }

# You need a token for the customer in order to make a connect version of the customer
# The next line simulates the response from using stripe.js to tokenize a customer's card details
# You should NOT be replicating this on the server

fakeToken = stripe.Token.create(card=DUMMY_CARD, api_key=API_KEY)

#put customers tokenized card on file
charge = stripe.Charge.create(card=fakeToken.id,currency="usd",amount=1000)

# Now we can charge customer

