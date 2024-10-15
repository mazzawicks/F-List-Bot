import json
import logging
import requests

log = logging.getLogger('main')

config = {
    "account": '',
    "ticket": '',
    "ticket_exp": '',
}

def flist_endpoint(url, params): # params or data?
    r = requests.post(url, params) # All endpoints use POST
    log(r.status_code)
    response = r.json()
    log(json.dumps(response, indent=2))
    return response

# Acquiring a ticket.
# POST to 
get_ticket_url = "https://www.f-list.net/json/getApiTicket.php" 
# Do NOT use GET for acquiring API tickets, this is beingphased out.Send two form fields, account and password.If you do not require information about characters, friends or bookmarks, please pass one or more of the followingfields with "true" as the value(without quotes): no_characters, no_friends, no_bookmarks.Tickets are valid for 30 minutes from issue, and invalidate all previous tickets for the account when issued.


# Sending a ticket.
# Any endpoint that requires a ticket must have the additional POST parameters of "account" which is the usernameof the account issued the ticket, and "ticket" which is the ticket acquired during the previous step.

### Bookmarks

bookmark_add_url = "https://www.f-list.net/json/api/bookmark-add.php" # Bookmark a profile. Takes one argument, "name"
bookmark_list_url = "https://www.f-list.net/json/api/bookmark-list.php" # List all bookmarked profiles
bookmark_remove_url = "https://www.f-list.net/json/api/bookmark-remove.php" # Remove a profile bookmark. Takes one argument, "name".

### Character data
# Note: If you try to use these on an account which is banned, timed out, blocked or deleted, you will receive anerror.

character_data_url = "https://www.f-list.net/json/api/character-data.php" # Get a character's information. Requires one parameter, "name".Must be POST. Includes id, name, description, view count, infotags, kinks, custom kinks, subkinks, images, andinlines. You will need to assemble the data based on information from the mapping endpoint to obtain humanreadable names for infotags, kinks and list items.

character_list_url = "https://www.f-list.net/json/api/character-list.php" # Get a list of all the account's characters.


### Getting misc data

groups_list_url = "https://www.f-list.net/json/api/group-list.php" # Get the global list of all f-list groups.

ignore_list_url = "https://www.f-list.net/json/api/ignore-list.php" # Get a list of all profiles your account has on chat-ignore.

info_list_url = "https://www.f-list.net/json/api/info-list.php" # Get the global list of profile info fields, grouped. Dropdown optionsinclude a list of the options. Does not require the account and ticket form fields.

kink_list_url = "https://www.f-list.net/json/api/kink-list.php" # Get the global list of kinks, grouped. Does not require the account andticket form fields.

data_mapping_list_url = "https://www.f-list.net/json/api/mapping-list.php" # Get the global list of kinks, infotags, infotag groups, and list items.Does not require the account and ticket form fields.

### Handling friend requests, friend list data

friend_list_url = "https://www.f-list.net/json/api/friend-list.php" # List all friends, account-wide, in a "your-character (dest) => thecharacter's friend (source)" format.

friend_remove_url = "https://www.f-list.net/json/api/friend-remove.php" # Remove a profile from your friends. Takes two argument,"source_name" (your char) and "dest_name" (the character's friend you're removing).

friend_request_accept_url = "https://www.f-list.net/json/api/request-accept.php" # Accept an incoming friend request. Takes one argument,"request_id", which you can get with the request-list endpoint.

friend_request_cancel_url = "https://www.f-list.net/json/api/request-cancel.php" # Cancel an outgoing friend request. Takes one argument,"request_id", which you can get with the request-pending endpoint.

friend_request_deny_url = "https://www.f-list.net/json/api/request-deny.php" # Deny a friend request. Takes one argument, "request_id", whichyou can get with the request-list endpoint. 

friend_request_list_url = "https://www.f-list.net/json/api/request-list.php" # Get all incoming friend requests.

friend_request_outgoing_list_url = "https://www.f-list.net/json/api/request-pending.php" # Get all outgoing friend requests.

friend_request_send_url = "https://www.f-list.net/json/api/request-send.php" # Send a friend request. source_name, dest_name.