import logging
import time
import requests

from api_urls import *

log = logging.getLogger('main')

class API:
    _requests = 0
    _cache = {}

    @classmethod
    def __init__(cls, config):
        cls.config = config
        cls.ticket = None
        cls.ticket_expires = 0
        cls.login_fields = {
            "account": cls.config['account'],
            "ticket": cls.ticket
        }

    @classmethod
    def refresh_ticket(cls):
        url = refresh_ticket_url
        data = {
            "account": cls.config['account'],
            "password": cls.config['password'],
        }

        r = requests.post(url, data=data)
        API._requests += 1
        assert(r.status_code == 200)
        assert(r.json()['error'] == '')

        response = r.json() # contains characters, friends, bookmarks, and ticket
        cls.ticket = response['ticket']
        cls.ticket_expires = time.time() + (25 * 60) # refresh ticket after 25 minutes
        cls.login_fields['ticket'] = cls.ticket
        log.info('ticket is good')

    @classmethod
    def post(cls, url, data={}):
        if not cls.ticket or time.time() > cls.ticket_expires:
            cls.refresh_ticket()

        authed_data = cls.login_fields
        authed_data.update(data)
        
        r = requests.post(url, data=authed_data) # All endpoints use POST 
        API._requests += 1
        response = r.json()
        
        log.info(r.status_code)
        # log.info(json.dumps(response, indent=2))
        log.info(len(r))
        return response

    @staticmethod
    def friend_list():
        return API.post(friend_list_url)
    
    @staticmethod
    def incoming_friend_requests():
        return API.post(friend_request_incoming_list_url)
        
    @staticmethod
    def accept_friend_request(request_id):
        data = { "request_id": request_id }
        return API.post(friend_request_accept_url, data=data)
        
    @staticmethod
    def deny_friend_request(request_id):
        data = { "request_id": request_id }
        return API.post(friend_request_deny_url, data = data)
        
    @staticmethod
    def remove_friend(name):
        data = { 
            "source_name": API.config['character'],
            "dest_name": name,
        }
        return API.post(friend_remove_url, data=data)
        
    @staticmethod
    def send_friend_request(name):
        data = { 
            "source_name": API.config['character'],
            "dest_name": name,
        }
        return API.post(friend_request_send_url, data=data)
        
    @staticmethod
    def outgoing_friend_requests():
        return API.post(friend_request_outgoing_list_url)
        
    @staticmethod
    def cancel_friend_request(request_id):
        data = { "request_id": request_id }
        return API.post(friend_request_cancel_url, data=data)
    
    @staticmethod
    def bookmark_list():
        return API.post(bookmark_list_url)
    
    @staticmethod
    def add_bookmark(name):
        data = { "name": name }
        return API.post(bookmark_add_url, data=data)
    
    @staticmethod
    def remove_bookmark(name):
        data = { "name": name }
        return API.post(bookmark_remove_url, data=data)
            
    @staticmethod
    def character_list():
        return API.post(character_list_url)
        
    # Note: If you try to use these on an account which is banned, timed out, 
    #       blocked, or deleted, you will receive an error
    @staticmethod
    def character_data(name):
        data = { "name": name }
        # cls.mapping = cls._cached(cls.data_map)
        # character_data = API.post(character_data_url, data=data)
        # fill_map_data(character_data) # TODO write fill_map_data
        
        return API.post(character_data_url, data=data)

    @staticmethod
    def ignore_list():
        return API.post(ignore_list_url)

    @staticmethod
    def group_list():
        return API._cached(group_list_url)
    
    @staticmethod
    def info_list():
        return API._cached(info_list_url)

    @staticmethod
    def kink_list():
        return API._cached(kink_list_url)

    @staticmethod
    def data_mapping():
        return API._cached(data_mapping_list_url)

    # Doesn't invalidate cache atm
    @classmethod
    def _cached(cls, url):
        cache = cls._cache.get(url)
        if not cache:
            cache = API.post(url)
            cls._cache[url] = cache
        return cache

