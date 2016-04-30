import json, requests, urllib
import tornado
import tornado.ioloop
import tornado.web
import nltk
import re
from torndsession.sessionhandler import SessionBaseHandler
from tornado.options import define, options, parse_command_line
import datetime
from utils import dateFunc, dateMonth

monthList = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

define("port", default=8888, help="run on the given port", type=int)
year = '2016'

class IndexHandler(SessionBaseHandler):
    def post(self):
        msg = {}
        msg['msg'] = ''
        post = tornado.escape.json_decode(self.request.body)
        if 'data' in self.session:
            user_msg = post['msg']
            if len(user_msg.split(" ")) < 3 and (user_msg[0].lower() == 'h' or nltk.pos_tag(nltk.sent_tokenize(user_msg))[0][1] == 'VBG'):
                msg['msg'] = 'Hi, how can I help you?'
            else:
                # Finding the location
                cp = nltk.RegexpParser('CHUNK: {<N.*>+ <IN> <N|J.*>* <N.*>+}')
                chunking = cp.parse(nltk.pos_tag(nltk.word_tokenize(user_msg)))
                chunk_found = False
                for tree in chunking:
                    if type(tree) is not tuple:
                        if tree.label() == 'CHUNK':
                            chunk_found = True
                            type_of_stay = ""
                            location = ""
                            x = 0
                            for tags in tree:
                                if tags[1] == 'IN':
                                    x = 1
                                elif x == 0:
                                    type_of_stay += tags[0]
                                elif x == 1:
                                    location += tags[0] + " "
                if chunk_found:
                    self.session['place'] = location[:-1]
                    msg['msg'] = "So you want a stay around " + location[:-1] + ". "
                # Finding the dates if available
                cp = nltk.RegexpParser('DATES: {<CD>+ <MD|CC|N|J|,|.|-|:|TO.*>* <N.*>*}')
                temp = user_msg.replace('th', 'st')
                chunking = cp.parse(nltk.pos_tag(nltk.word_tokenize(temp)))
                chunk_found = False
                dates = []
                months = []
                for tree in chunking.subtrees(filter=lambda t: t.label() == 'DATES'):
                    chunk_found = True
                    datesT, monthsT = dateFunc(tree)
                    dates = dates + datesT
                    months = months + monthsT
                if chunk_found:
                    self.session['date'] = dateRange = dateMonth(dates, months)
                    msg['msg'] += 'You want to book between ' + str(dateRange[0]) + '/' + str(dateRange[1]) + ' to ' + str(dateRange[2]) + '/' + str(dateRange[3]) + '. '
                # To check if place is asked for some action
                if 'place_asked' in self.session:
                    del self.session['place_asked']
                    pass
                if 'place' not in self.session:
                    msg['msg'] += "Okay, what place do you want to book at ? "
                    self.session['place_asked'] = True
                if 'date' not in self.session:
                    msg['msg'] += "What dates are looking for ? "
                    self.session['date_asked'] = True
                if 'place' in self.session and 'date' in self.session:
                    autocomplete = requests.get('https://search.stayzilla.com/v1/json/suggestlocbusspell/'+str(self.session['place'])+'/0/0/null/5')
                    autocomplete_params = autocomplete.json()['data'][0]
                    params = {}
                    params['area'] = autocomplete_params['area']
                    params['suggest'] = autocomplete_params['suggest']
                    params['type'] = autocomplete_params['type']
                    params['lat'] = autocomplete_params['lat']
                    params['lng'] = autocomplete_params['lng']
                    params['dist'] = '20km'
                    dateRange = self.session['date']
                    params['checkInDate'] = str(dateRange[0]).zfill(2)+'-'+str(dateRange[1]).zfill(2)+'-'+year
                    params['checkOutDate'] = str(dateRange[2]).zfill(2)+'-'+str(dateRange[3]).zfill(2)+'-'+year
                    url_params = urllib.urlencode(params, True)
                    msg['msg'] += 'Check these stays at https://www.stayzilla.com/search?'+url_params
        else:
            if 'name' not in post:
                msg['msg'] = 'Enter your name please'
                self.session['login'] = False
            else:
                name = post['name']
                if name[-1].lower() in ['a', 'i']:
                    salutation = 'mam'
                else:
                    salutation = 'sir'
                msg['msg'] = 'Hello ' + salutation + '. Welcome to Stayzilla. How may I assist you?'
                self.session['data'] = True;
        self.write(json.dumps(msg))
        self.finish()

app = tornado.web.Application([
    (r'/', IndexHandler),
])

if __name__ == '__main__':
    parse_command_line()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

