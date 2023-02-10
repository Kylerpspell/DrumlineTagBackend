import random
import re

def get_response(message: str) -> str:
    p_message = message.lower()

    if p_message == '!tag':
        roll = int(random.randint(1,6))
        if roll == 1:
            return '*Click* Caught in 4k O_O'
        if roll == 2:
            return 'You hate to see it...'
        if roll == 3:
            return 'Looking good!'
        if roll == 4:
            return 'Thats gonna look great on my wall!'
        if roll == 5:
            return 'Gotcha!'
        if roll == 6:
            return 'They never saw it coming...'

    if p_message == '!help':
        return '`type in "!tag" to tag someone!`'
    # if p_message == '!(any amount of letters after that dont work)':
        #return 'I do not understand... Try typing "!help" for some help!'
    

    return