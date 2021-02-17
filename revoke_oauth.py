import sys, requests

class RevokeToken():
    def __init__(self, token):
        self.token = token.removeprefix("oauth:")
        # Get client id based on user OAuth token 
        oauthValidateUrl = 'https://id.twitch.tv/oauth2/validate'
        oauthValidateHeaders = {'Authorization': 'OAuth ' + self.token}
        try:
            oauthValidateRequest = requests.get(oauthValidateUrl, headers=oauthValidateHeaders).json()
            self.client_id = oauthValidateRequest['client_id']
        except KeyError:
            print(oauthValidateRequest['message'])
            print('Token may be already revoked')
            exit()
        except:
            print(sys.exc_info()[0])
            exit()

        try:
            oauthRevokeUrl = 'https://id.twitch.tv/oauth2/revoke'
            oauthRevokeData = {'client_id':self.client_id, 'token':self.token}
            oauthRevokeRequest = requests.post(oauthRevokeUrl, data=oauthRevokeData)
            if(oauthRevokeRequest.status_code == 200):
                print("Token has been revoked")
            elif(oauthRevokeRequest.status_code == 400):
                print("TOKEN WAS NOT REVOKED, PLEASE TRY AGAIN")
            else:
                print(oauthRevokeRequest)
        except:
            print(sys.exc_info()[0])
            exit()

def main():
    if len(sys.argv) != 2:
        print('Usage: RevokeToken <token>')
        sys.exit(1)

    token  = sys.argv[1]

    RevokeToken(token)

if __name__ == "__main__":
    main()