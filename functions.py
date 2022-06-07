import requests
import re
import random
from config import bot_token
from config import alternative_services_links
from config import alternative_services_regex_noncompiled
from config import reply_mode

# functions for messages are in this file

# get a text message and do whatever is needed
def process_text_message(text:str,chat_id, message_id):

    text_to_send = find_and_replace_links(text)

    # make a message to send to telegram
    message = {
        # chat id should be id of the one who had requested
        "chat_id":chat_id,
        # text is command output in monospace format
        "text":text_to_send,
        # set parse mode to markdown so that text can be in monospace
        "parse_mode":"HTML",
        "reply_to_message_id":message_id,
    }

    # send message to telegram
    if len(text_to_send) > 0:
        requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage', data=message)

alternative_services_compiled = []

# this function should be executed once before other functions
def compile_services_regex():

    global alternative_services_compiled

    for service_name in alternative_services_links:
        service_links = alternative_services_links[service_name]
        if len(service_links) > 0:

            alt_regex = alternative_services_regex_noncompiled[service_name]
            compiled_links = [
                alt_regex[1].replace('LINK', service_link)
                for service_link in service_links
            ]
            alternative_services_compiled.append( (alt_regex[0],compiled_links) )


# this function will find links to services in a message and return alternative links.
def find_and_replace_links(text:str):

    global alternative_services_compiled

    # check method of replying
    if reply_mode == "substitute":

        outText = text
        should_substtiute = False

        # substitute all links with alternative ones.
        for alt_regex in alternative_services_compiled:

            # check if any links were found
            found_links = re.findall('(' + alt_regex[0] + ')', text)
            if len(found_links) > 0:
                should_substtiute = True

            outText = re.sub(alt_regex[0], random.choice(alt_regex[1]), outText)

        # if no links were found, reply nothing
        if should_substtiute == False:
            outText = ''

    elif reply_mode == "links":
        # reply links only

        outText = ""

        # find all links
        for alt_regex in alternative_services_compiled:
            found_links = re.findall('(' + alt_regex[0] + ')', text)

            # add alternative of found links to outText
            for found_link in found_links:
                outText += re.sub(alt_regex[0], random.choice(alt_regex[1]), found_link[0]) + '\n'

    # if nothing were found, will return empty string
    # otherwise, depending on the method, it will return result
    return outText