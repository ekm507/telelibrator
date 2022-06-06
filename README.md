# TeleLibrator
a telegram bot for converting links to commercial online services like Youtube, Soundcloud, Instagram, Twitter,… into a privacy-respecting alternative.  
it works by replying the alternative link to the message.

## how to set up

1. make a telegram bot and copy it's token.
2. clone this repo
3. copy `config.py.default` into `config.py`
4. configure config.py file:
    1. set bot tokenn
    2. set reply mode
    3. add links to your favorite services. each service can have multiple links and one of them will be used randomly.
5. run `telelibrator.py` with `python3`