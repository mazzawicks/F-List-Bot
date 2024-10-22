
### Sequence Diagram

      Client                         Server
                                       |
                                       |
      connect                          |
      startup                          |
         | ----------> IDN ----------> |    Identify
         | <---------- IDN <---------- |    Conirm Identity
         | <---------- VAR* <--------- |    Server Variables (several messages)
         | <-------- HLO,CON <-------- |    Hello, Connected Users
         | <-------- FRL,IGN <-------- |    Friend list, Ignore list
         | <---------- ADL <---------- |    List of chatops
         | <--------- LIS** <--------- |    Name, gender, status of every user 
         |                             |      online. Many large messages.
         |                             |
         | --------> CHA,ORS --------> |    Get list of public/private rooms
         | <-------- CHA,ORS <-------- |    Send list of public/private rooms
         |                             |
         |                             |
         | ----------> JCH ----------> |    Join channel
         | <---- JCH,COL,ICH,CDS <---- |    Joined channel, channel oplist,
         |                             |    initial channel data, description
         |                             |
         | <---------- PIN <---------- |    Ping, every 30 minutes
         | ----------> PIN ----------> |    Pong, disconnected if not received 
         |                             |      in 90 seconds
         |                             |


### Client Design

  ------> incoming -> receive_message
                           v
                      read_message -> ServerCommands 
                                            v                   
      GeneratedEvents ---------------> EventCreator <-----> DataStore
                                            v                  ^
                                        EventQueue             |
                                            v                  |
                                         Handlers -------------+
                                            v
                      ClientCommands <-- Actions
                           v
                      send_message -> outgoing ------------------>

## EventQueue

   ServerCommands ---------> add_event <--------- GeneratedEvents
                                v
                            EventQueue 
                                v
     DataStore <-------> DefaultHandlers ------> Actions ------> + 
        ^                       v                                |
        |             enter_custom_handlers                      |
        |                       v                                v
        + ------ data -----> Handler - - potential Actions - - > +
        |                       v                                |
        + -- fetch/store --> Handler                             |
                                |                                |
                             Handler - - -> ...                  |
                                |                                |
                                v                                |
                               ...                               |
                                                                 v
                                                              Actions
                                                                 |
                                                                 v
                                                           ClientCommands


Need to implement:

EventHandler
GeneratedEvents
DataStore
Action

Custom Handler

- reward_character
- define/run game
- dice, bottle
- relay - owner messages, bot relay to channel
