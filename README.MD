## NLP based chatbot

I work at Stayzilla, a website where you can book great stays. Was just looking around to check if I can build an automated chat bot which can redirect to a particular search page. The code looks dicey but works for basic chat. NLP is used without training. I have used basic tagging and chunking mechanism to extract data. This bot may not help anyone but can serve as a basic tutorial. Try chatting with the bot :)

Packages used : tornado, torndsession, nltk, requests, urllib

Good Luck !

## Example Conversation

1.
POST  HTTP/1.1
Host: localhost:8888
Cache-Control: no-cache
Postman-Token: 02700170-4c06-3091-693b-455cc4fb0278

{
}

Response:

{"msg": "Enter your name please"}

2.
POST  HTTP/1.1
Host: localhost:8888
Cache-Control: no-cache
Postman-Token: 2a389181-5d03-2a7f-240f-520092c40d3f

{
    "name" : "Raj"
}

Response:

{"msg": "Hello sir. Welcome to Stayzilla. How may I assist you?"}

3.
POST  HTTP/1.1
Host: localhost:8888
Cache-Control: no-cache
Postman-Token: 0038b36c-b599-4671-60b6-226fb4768018

{
    "msg" : "I am looking for a hotel in Delhi."
}

Response:

{"msg": "So you want a stay around Delhi. What dates are looking for ? "}

4.
POST  HTTP/1.1
Host: localhost:8888
Cache-Control: no-cache
Postman-Token: 6e3c2039-2243-1767-a19c-08e56f65bfa0

{
    "msg" : "22nd April to 3rd May"
}

Response:

{"msg": "You want to book between 22/4 to 3/5. Check these stays at https://www.stayzilla.com/search?dist=20km&area=Delhi&suggest=Delhi&checkInDate=22-04-2016&lat=28.65195&checkOutDate=03-05-2016&lng=77.23149&type=szcity"}
