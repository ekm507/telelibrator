import requests
from config import bot_token
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

    requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage', data=message)


# this function will find links to services in a message and return alternative links.
def find_and_replace_links(text:str):
    return "test"