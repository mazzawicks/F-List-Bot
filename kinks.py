# response from json endpoint - /chat-search-fields

# FKS
# Sent by as a response to the client's FKS command, containing the results of the search.
# Syntax

# >> FKS { "characters": [object], "kinks": [object] }
# Raw sample
# FKS {"characters":["Some Guy", "Another Guy", "Some Gal"] "kinks": ["523","66"]}
# Notes/Warnings
# The numbers under kinks are the kinkids sent by the client. All search parameters can be retrieved http://www.f-list.net/json/chat-search-getfields.json?ids=true.

