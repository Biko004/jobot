"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import urllib.request
import random
import json
import uuid


my_id = uuid.uuid1()
print(my_id)

flag = {"count": 0}
heywords = ["hey", "hello", "hi", "hii", "yo"]
animationwords = ["afraid", "bored", "confused", "crying", "dancing", "dog", "excited", "giggling", "heartbroke", "inlove", "laughing", "money", "takeoff", "waiting"]
badwords = ["fuck", "kill", "anal", "anus", "arse", "ass", "ballsack", "balls", "bastard", "bitch", "bloody", "blowjob",
            "blow job", "bollock", "bollok", "boner", "boob", "bugger", "bum", "butt", "buttplug", "clitoris", "cock",
            "coon", "crap", "cunt", "damn", "dick", "dildo", "dyke", "feck", "fellate", "fellatio", "felching", "fuck",
            "f u c k", "fudgepacker", "fudge packer", "flange", "Goddamn", "God damn", "hell", "homo", "jerk", "jizz",
            "knobend", "knob end", "labia", "lmao", "lmfao", "muff", "nigger", "nigga", "omg", "penis", "piss", "poop",
            "prick", "pube", "pussy", "queer", "scrotum", "sex", "shit", "s hit", "sh1t", "slut", "smegma", "spunk",
            "tit", "tosser", "turd", "twat", "vagina", "wank", "whore", "wtf"]


@route('/', method='GET')
def index():
    return template("chatbot.html")


# greeting user with name
def greetUser(usermsg):
    newmsg = usermsg.lower()
    namewords = ["name is", "i'm", "im"]

    for word in namewords:
        if word in newmsg:
            newword = word.lower()
            name = newmsg.split(newword + " ", 1)[1].capitalize()
            return {"animation": "dancing", "msg": "Hello " + name + "! How can I help you?"}

# set robot animation
def animationbyword(usermsg):
    newmsg = usermsg.lower()
    for word in animationwords:
        if word in newmsg:
            print(word)
            return {"animation": word, "msg": word.capitalize() + "?..."}

def tellJoke(usermsg):

    joke = json.loads(urllib.request.urlopen("http://api.icndb.com/jokes/random/").read().decode('utf-8'))
    return {"animation": "laughing", "msg": joke["value"]["joke"]}


# find infromation for user about specific keyword in Wikipedia - FAKE - need to change to API
def findInfo(usermsg):
    if "want" and "know" and "about" in usermsg:
        topic = usermsg.split("about ", 1)[1]
        return {"animation": "excited",
                "msg": "Here's some info about " + topic + ": <a href='https://en.wikipedia.org/wiki/" + topic + "'>follow the link</a>"}


# find photo by keyword - TODO - API
def findImg(usermsg):
    if "what is" in usermsg:
        topic = usermsg.split("what is ", 1)[1]
        return {"animation": "excited",
                "msg": "Here's some info about " + topic + ": https://en.wikipedia.org/wiki/" + topic}


def swearWords(usermsg):
    if any(x in usermsg for x in badwords):
        return {"animation": "no", "msg": "I don't like to hear this kind of words.. please stop!"}

def checkhey(usermsg):
    if any(x in usermsg for x in heywords):
        return False
    return True

@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')

    if (flag["count"]==0) and (checkhey(user_message)):
        name = user_message.capitalize()
        flag['count'] += 1
        return json.dumps({"animation": "dancing", "msg": "Hello " + name + "! How can I help you?"})

    if (any(x in user_message for x in heywords)):
        return json.dumps({"animation": "dancing", "msg": "Hey there!"})

    if (greetUser(user_message)):
        answer = greetUser(user_message)
        return json.dumps({"animation": answer['animation'], "msg": answer['msg']})

    if (any(x in user_message for x in animationwords)):
        answer = animationbyword(user_message)
        return json.dumps({"animation": answer['animation'], "msg": answer['msg']})
    if ("joke" in user_message):
        answer = tellJoke(user_message)
        return json.dumps({"animation": answer['animation'], "msg": answer['msg']})

    if "want" and "know" and "about" in user_message:
        answer = findInfo(user_message)
        return json.dumps({"animation": answer['animation'], "msg": answer['msg']})

    if findImg(user_message):
        answer = findImg(user_message)
        return json.dumps({"animation": answer['animation'], "msg": answer['msg']})

    if any(x in user_message for x in badwords):
        answer = swearWords(user_message)
        return json.dumps({"animation": answer['animation'], "msg": answer['msg']})
    return json.dumps({"animation": 'inlove', "msg": "Didn't got you.. please try again.."})


@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)


if __name__ == '__main__':
    main()
