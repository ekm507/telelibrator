#!/usr/bin/python3

# import bot configurations
from config import bot_token
from functions import process_text_message
from functions import compile_services_regex
import requests
from time import sleep
import threading

# time to sleep between requests
sleep_time = 0.1

message_limit = 1
message_offset = 0

compile_services_regex()

# main bot loop
while(True):

    # this delay is for preventing high CPU load
    sleep(sleep_time)
    json_message = dict()

    # try getting messages and processing them
    try:

        # get message updates
        updates = requests.post(
            f'https://api.telegram.org/bot{bot_token}/getupdates?offset={message_offset}&limit={message_limit}')

        # pprint(updates.json())
        #  if there is no message, do nothing.
        if len(updates.json()['result']) < 1:
            # reloop it
            continue

        # print all new messages
        # for message in updates.json()['result']:
        #     pprint(message)

        # jsonified message to process
        json_message = updates.json()['result'][0]
        # pprint(json_message)

        # type of message will be stored here. we will later use it for processing
        message_type = ''

        # if there is a new "message"
        if 'message' in json_message:

            # get chat id of the message
            chat_id = json_message['message']['chat']['id']
            message_id = json_message['message']['message_id']

            if 'text' in json_message['message']:

                # set message type
                message_type = 'text'
                # get message text
                # note: if message is not text type, error handling will catch it and continue the loop
                text = json_message['message']['text']

        # if there is not any key of the specified ones
        else:
            # mark message as read
            message_offset = json_message['update_id'] + 1
            # do nothing and just reloop it
            continue

        if message_type == 'text':
            # create a new thread for processing command
            x = threading.Thread(target=process_text_message,
                                 args=(text, chat_id, message_id))
            # start the thread
            x.start()

        # increase message offset. sending next request with this offset is like marking message as read.
        message_offset = json_message['update_id'] + 1

    # usually means message is in a type that is not supported in babaee (yet).
    except KeyError:
        # just mark message as read

        if 'update_id' in json_message:
            message_offset = json_message['update_id'] + 1

    # if there was a connection error
    except requests.exceptions.ConnectionError:
        # print error text but do not kill the bot.
        print('connection error')

    except KeyboardInterrupt:
        print('exiting')
        exit(0)
