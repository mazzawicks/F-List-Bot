import json
import os
import requests

from dotenv import load_dotenv
load_dotenv()

ticket_url = 'https://www.f-list.net/json/getApiTicket.php'
account = {
    "account": os.getenv('account'),
    "password": os.getenv('password'),
}

logged_in = None

# Acquiring a ticket.
def get_ticket():
    r = requests.post(ticket_url, data=account)
    print(r.status_code)
    response = r.json()
    print(json.dumps(response, indent=2))
    logged_in = {
        "account": os.getenv('account'),
        "ticket": response['ticket'],
    }
    return logged_in

def flist_req(url, logged_in, extra_data={}):
    data = { **logged_in, **extra_data }
    r = requests.post(url, data=data)
    print(r.status_code)
    response = r.json()
    print(json.dumps(response, indent=2))


if __name__ == '__main__':
    logged_in = get_ticket()

    import ipdb; ipdb.set_trace()