import requests
from .errors import *
from .classes import *

class Session:
    def __init__(self, login, password):
        self.session = None
        self.login(login, password)

    def login(self, login, password):
        '''
        Used to login into the system.
        '''
        if self.session != None:
            raise AlreadyLoggedIn(f'You are already logged in!')

        self.login_name = login
        self.password = password

        # logging in
        self.session = requests.Session()
        res = self.post('https://learn.algoritmika.org/s/auth/api/e/student/auth', data={
            'login': self.login_name,
            'password': self.password
        })
        
        # successfully logged in
        if res.status_code == 200:
            item = res.json()['item']
            self.id = item['studentId']

        # error handling
        elif res.status_code == 400:
            raise InvalidCredentials('Login or password are incorrect')
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

        You'll need to `login()` in order to continue
        using the system.
        '''
        self.session.close()
        self.session = None


    # actions
    def my_profile(self):
        '''
        Fetches and returns the profile of currently 
        logged in user.
        '''
        data = self.get(
            'https://learn.algoritmika.org/api/v1/profile?\
            expand=branch,settings,locations,permissions,avatar,referral,course',
        )
        if data.status_code != 200:
            return UnknownException(data.json())
        return SelfProfile(data.json()['data'])
    
    
    def get_profile(self, id):
        '''
        Fetches and returns the profile of the user
        with the passed ID.
        '''
        if type(id) != int:
            raise TypeError(f'\'id\' should be int')
        
        data = self.get(
            f'https://learn.algoritmika.org/api/v2/community/profile/index?\
            expand=stats,avatars&studentId={id}'
        )
        if data.status_code == 200:
            if data.json()['status'] == 'error':
                raise ProfileNotFound(f'Incorrect id value: {id}')
            else:
                return Profile(data.json()['data'])
        else:
            raise UnknownException(data.json())