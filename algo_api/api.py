import requests
from .errors import *
from .classes import *

class Session:
    def __init__(self, login, password):
        self.login(login, password)

    def login(self, login, password):
        '''
        Used to login in the system.
        '''
        self.login_name = login
        self.password = password

        # logging in
        self.session = requests.Session()
        res = self.post('https://learn.algoritmika.org/s/auth/api/e/student/auth', data={
            'login': self.login_name,
            'password': self.password
        })
        if res.status_code == 200:
            pass
        elif res.status_code == 400:
            print(res.json())
            raise InvalidCredentials('Login or password you provided are incorrect.')
        else:
            raise UnknownException(res.json())

    def post(self, *args, **kwargs) -> requests.Response:
        '''
        Submits a POST request to your endpoint using
        the system's session.

        It is not recommended to send requests to
        third-party endpoints.
        '''
        if self.session != None:
            res = self.session.post(*args, **kwargs)
            return res 
        else:
            raise SessionClosed('Session is closed, use login() to login')

    def get(self, *args, **kwargs) -> requests.Response:
        '''
        Submits a GET request to your endpoint using
        the system's session.

        It is not recommended to send requests to
        third-party endpoints.
        '''
        if self.session != None:
            res = self.session.get(*args, **kwargs)
            return res 
        else:
            raise SessionClosed('Session is closed, use login() to login')

    def close(self):
        '''
        Closes the session.

        You need to `login()` in order to continue
        using the system.
        '''
        self.session.close()
        self.session = None


    # actions
    def get_profile(self):
        data = self.get(
            'https://learn.algoritmika.org/api/v1/profile?\
            expand=branch,settings,locations,permissions,avatar,referral,course',
        )
        if data.status_code != 200:
            return UnknownException(data.json())
        return SelfProfile(data.json()['data'])