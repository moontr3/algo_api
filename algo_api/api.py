import requests
from .errors import *
from .classes import *

class Session:
    def __init__(self, login, password):
        self.session = None
        self.id = None
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
            if res.status_code != 200:
                raise UnknownException(res.json())
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
            if res.status_code != 200:
                raise UnknownException(res.json())
            return res 
        else:
            raise SessionClosed('Session is closed, use login() to login')

    def delete(self, *args, **kwargs) -> requests.Response:
        '''
        Submits a DELETE request to your endpoint using
        the system's session.

        It is not recommended to send requests to
        third-party endpoints.
        '''
        if self.session != None:
            res = self.session.delete(*args, **kwargs)
            if res.status_code != 200:
                raise UnknownException(res.json())
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
        self.id = None


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
        return SelfProfile(data.json()['data'])
    
    
    def get_profile(self, id:int):
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
        return Profile(data.json()['data'])
        
        
    def my_projects(self, sort=SORT_LATEST):
        '''
        Fetches and returns all projects of currently
        logged in user.
        '''
        data = self.get(
            f'https://learn.algoritmika.org/api/v1/projects?\
            expand=uploads,remix&sort=-{sort}&scope=student&\
            type=design,gamedesign,images,presentation,python,scratch,unity,video,vscode,website',
        )
        return [Project(i) for i in data.json()['data']['items']]
        
        
    def get_projects(self, id:int=None, page:int=1, per_page:int=50, sort=SORT_LATEST):
        '''
        Fetches and returns all projects of the user
        with the passed ID or if the ID is not provided
        will fetch the projects from the universe.
        '''
        if id is None:
            data = self.get(
                f'https://learn.algoritmika.org/api/v1/projects?\
                expand=uploads,remix&sort=-{sort}&scope=universe&\
                type=design,gamedesign,images,presentation,python,scratch,unity,video,vscode,website&\
                page={page}&perPage={per_page}',
            )
        elif type(id) == int:
            data = self.get(
                f'https://learn.algoritmika.org/api/v1/projects?\
                expand=uploads,remix&sort=-{sort}&scope=universe&\
                type=design,gamedesign,images,presentation,python,scratch,unity,video,vscode,website&\
                page={page}&perPage={per_page}&studentId={id}',
            )
        else:
            raise TypeError(f'\'id\' should be int')

        return [Project(i) for i in data.json()['data']['items']]
        
        
    def get_project(self, id:int):
        '''
        Fetches and returns a project with the ID
        provided.
        '''
        if type(id) != int:
            raise TypeError(f'\'id\' should be int')
        
        data = self.get(
            f'https://learn.algoritmika.org/api/v1/projects/info/{id}?\
            expand=uploads,remix',
        )
        return Project(data.json()['data'])
        
        
    def place_reaction(self, id:int, reaction:str):
        '''
        Places a reaction under a project with the
        ID provided.
        '''
        if type(id) != int:
            raise TypeError(f'\'id\' should be int')
        
        self.post(
            'https://learn.algoritmika.org/api/v2/community/reaction/add',
            data={
                'ownerId': id,
                'ownerType': 'project_relation',
                'type': reaction
            }
        )
        
        
    def remove_reaction(self, id:int, reaction:str):
        '''
        Removes a reaction under a project with the
        ID provided.
        '''
        if type(id) != int:
            raise TypeError(f'\'id\' should be int')
        
        self.post(
            'https://learn.algoritmika.org/api/v2/community/reaction/remove',
            data={
                'ownerId': id,
                'ownerType': 'project_relation',
                'type': reaction
            }
        )
        
        
    def post_comment(self, id:int, text:str, reply_to:int = None):
        '''
        Posts a comment under a project with the
        ID provided.
        '''
        if type(id) != int:
            raise TypeError(f'\'id\' should be int')
        
        if reply_to == None:
            data = {'message': text}
        else:
            if type(reply_to) != int:
                raise TypeError(f'\'reply_to\' should be int')
            data = {'message': text, 'parentCommentId': reply_to}
        
        data = self.post(
            f'https://learn.algoritmika.org/api/v1/projects/comment/{id}',
            data=data
        )
        return Comment(data.json()['data'])
        
        
    def delete_comment(self, id:int):
        '''
        Deletes a comment with the ID provided.
        '''
        if type(id) != int:
            raise TypeError(f'\'id\' should be int')
        
        self.delete(
            f'https://learn.algoritmika.org/api/v1/projects/comment/{id}'
        )
        
        
    def get_comments(self, id:int, page:int = 1, per_page:int = 50):
        '''
        Fetches and returns all comments under the project
        with the passed ID.
        '''
        if type(id) != int:
            raise TypeError(f'\'id\' should be int')
        if type(page) != int:
            raise TypeError(f'\'page\' should be int')
        if type(per_page) != int:
            raise TypeError(f'\'per_page\' should be int')
        
        data = self.get(
            f'https://learn.algoritmika.org/api/v1/projects/comment/{id}?\
            page={page}&perPage={per_page}&sort=-createdAt',
        )
        return [Comment(i) for i in data.json()['data']['items']]


class AnonSession:
    def __init__(self):
        self.session = None
        self.login()

    def login(self):
        '''
        Used to login into the system.
        '''
        if self.session != None:
            raise AlreadyLoggedIn(f'You are already logged in!')

        # logging in
        self.session = requests.Session()
        res = self.post("https://learn.algoritmika.org/s/auth/api/e/student/logika-promo",
            {
                'branchCode': "logikapromoru",
                'guid': "bf651565-cfc5-11ed-8ea4-6cb31108b164"
            }
        )

        # error handling
        if res.status_code != 200:
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
            if res.status_code != 200:
                raise UnknownException(res.json())
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
            if res.status_code != 200:
                raise UnknownException(res.json())
            return res 
        else:
            raise SessionClosed('Session is closed, use login() to login')

    def delete(self, *args, **kwargs) -> requests.Response:
        '''
        Submits a DELETE request to your endpoint using
        the system's session.

        It is not recommended to send requests to
        third-party endpoints.
        '''
        if self.session != None:
            res = self.session.delete(*args, **kwargs)
            if res.status_code != 200:
                raise UnknownException(res.json())
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

    def place_reaction(self, id:int, reaction:str):
        '''
        Places a reaction under a project with the
        ID provided.
        '''
        if type(id) != int:
            raise TypeError(f'\'id\' should be int')
        
        self.post(
            'https://learn.algoritmika.org/api/v2/community/reaction/add',
            data={
                'ownerId': id,
                'ownerType': 'project_relation',
                'type': reaction
            }
        )
        
        
    def remove_reaction(self, id:int, reaction:str):
        '''
        Removes a reaction under a project with the
        ID provided.
        '''
        if type(id) != int:
            raise TypeError(f'\'id\' should be int')
        
        self.post(
            'https://learn.algoritmika.org/api/v2/community/reaction/remove',
            data={
                'ownerId': id,
                'ownerType': 'project_relation',
                'type': reaction
            }
        )
    
    def post_comment(self, id:int, text:str, reply_to:int = None):
        '''
        Posts a comment under a project with the
        ID provided.
        '''
        if type(id) != int:
            raise TypeError(f'\'id\' should be int')
        
        if reply_to == None:
            data = {'message': text}
        else:
            if type(reply_to) != int:
                raise TypeError(f'\'reply_to\' should be int')
            data = {'message': text, 'parentCommentId': reply_to}
        
        data = self.post(
            f'https://learn.algoritmika.org/api/v1/projects/comment/{id}',
            data=data
        )
        return Comment(data.json()['data'])
        
        
    def delete_comment(self, id:int):
        '''
        Deletes a comment with the ID provided.
        '''
        if type(id) != int:
            raise TypeError(f'\'id\' should be int')
        
        self.delete(
            f'https://learn.algoritmika.org/api/v1/projects/comment/{id}'
        )