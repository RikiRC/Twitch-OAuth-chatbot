# Twitch OAuth Chatbot Python example
Here you will find a simple Python chatbot using IRC that can help demonstrate how to interact with chat on Twitch.

## Installation
After you have cloned this repository, use pip or easy_install to install the IRC library.

```sh
$ pip install irc
```

## Usage
To run the chatbot, you will need to provide an OAuth access token with the chat_login scope. You can reference an authentication sample to accomplish this, or simply use the [Twitch Chat OAuth Password Generator](http://twitchapps.com/tmi/)

```sh
$ python3 chatbot_oauth.py <username> <token> <channel>
```

* Username - The username of the chatbot,
* Token - Chatbot OAuth Token,
* Channel - The channel your bot will connect to

I also created python script for easy and fast revoke of OAuth tokens, to use it type following command:

```sh
$ python3 revoke_oauth.py <token>
```

* Token - Chatbot OAuth Token,

Script based on [Twitch Chatbot Python Sample](https://github.com/twitchdev/chatbot-python-sample)
