from .baseauthorizationrequest import BaseAuthorizedRequest

class OAuthAuthorizationParameters:
    def __init__(self):
        self.token_url = None
        self.client_id = None
        self.client_secret = None
        self.user_name = None
        self.password  = None

class OAuthAuthorizationRequest(BaseAuthorizedRequest):
    def __init__(self, requests, parameters : OAuthAuthorizationParameters):
        BaseAuthorizedRequest.__init__(self, requests)
        self.parameters = parameters
    
    def request(self, url):
        ## Request parameters
        token_request_data = {
            'grant_type': 'password',
            'client_id': self.parameters.client_id,
            'client_secret': self.parameters.client_secret,
            'username': self.parameters.user_name,
            'password': self.parameters.password,
        }
        # Send a POST request to the token endpoint
        response = self.requests.post(self.parameters.token_url, data=token_request_data)
        if response.status_code == 200:
            token_data = response.json()
            if (self.headers is None):
                self.headers = {}
            self.headers['Authorization'] = token_data['access_token']
            self._make_request(url)
        else:
            raise ValueError(f'Failed to get access token. Status code {response.status_code}')