import sys, irc.bot, requests

class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, token, channel):
        self.token = token.removeprefix("oauth:")
        self.ircChannel = '#' + channel.lower()
        self.channel = channel.lower()

        # Get client id based on user OAuth token 
        oauthValidateUrl = 'https://id.twitch.tv/oauth2/validate'
        oauthValidateHeaders = {'Authorization': 'OAuth ' + self.token}
        oauthValidateRequest = requests.get(oauthValidateUrl, headers=oauthValidateHeaders).json()
        self.client_id = oauthValidateRequest['client_id']

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print('Connecting to ' + server + ' on port ' + str(port) + '...')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:'+self.token)], username, username)
        
    def on_welcome(self, c, e):
        print('Joining ' + self.ircChannel)
        c.join(self.ircChannel)
        print('Joined ' + self.ircChannel)
        c.privmsg(self.ircChannel, "Connected!")

    def on_pubmsg(self, c, e):
        # If a chat message starts with an exclamation point, try to run it as a command
        if e.arguments[0][:1] == '!':
            cmd = e.arguments[0].split(' ')[0][1:]
            print('Received command: ' + cmd)
            self.do_command(e, cmd)
        return

    def do_command(self, e, cmd):
        c = self.connection

        # Poll the API to get current game.
        if cmd == "game":
            url = 'https://api.twitch.tv/helix/search/channels?query=' + self.channel
            headers = {'Client-ID': self.client_id, 'Authorization': 'Bearer ' + self.token}
            r = requests.get(url, headers=headers).json()
            gameUrl = 'https://api.twitch.tv/helix/games?id=' + r['data'][0]['game_id']
            gameRequest = requests.get(gameUrl, headers=headers).json()
            c.privmsg(self.ircChannel, r['data'][0]['display_name'] + ' is currently playing ' + gameRequest['data'][0]['name'])

        # Poll the API the get the current title of the stream
        elif cmd == "title":
            url = 'https://api.twitch.tv/helix/search/channels?query=' + self.channel
            headers = {'Client-ID': self.client_id, 'Authorization': 'Bearer ' + self.token}
            r = requests.get(url, headers=headers).json()
            c.privmsg(self.ircChannel, r['data'][0]['display_name'] + ' channel title is currently ' + r['data'][0]['title'])

        # Provide basic information to viewers for specific commands
        elif cmd == "raffle":
            message = "This is an example bot, replace this text with your raffle text."
            c.privmsg(self.ircChannel, message)
        elif cmd == "schedule":
            message = "This is an example bot, replace this text with your schedule text."            
            c.privmsg(self.ircChannel, message)

        # The command was not recognized
        else:
            c.privmsg(self.ircChannel, "Did not understand command: " + cmd)

def main():
    if len(sys.argv) != 4:
        print('Usage: twitchbot <username> <token> <channel>')
        sys.exit(1)

    username  = sys.argv[1]
    token     = sys.argv[2]
    channel   = sys.argv[3]

    bot = TwitchBot(username, token, channel)
    bot.start()

if __name__ == "__main__":
    main()