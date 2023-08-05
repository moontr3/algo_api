import requests
import datetime
from .errors import *

class NotImplemented:
    def __init__(self, message):
        self.message = message
    def __call__(self):
        raise NotImplementedException(self.message)
    

# profiles

class Branch:
    def __init__(self, data):
        '''
        Branch that the user is learning in.
        '''
        self.id: int =         data['id']
        self.brand_name: str = data['brandName']
        self.title: str =      data['title']
        self.code: str =       data['code']
        self.phone: str =      data['phone']
        self.site_url: str =   data['siteUrl']
        # self.chat_token =      NotImplemented('Unknown freshChatToken format')

class Ban:
    def __init__(self, data):
        '''
        User's ban status.
        '''
        self.is_banned: bool = data['active']
        self.reason: str =     data['reason']
        # self.expires_at =      NotImplemented('Unknown expiresAt format')

class Settings:
    def __init__(self, data):
        '''
        User's editor settings.
        '''
        self.allowed_file_extensions: list = data['platformUploadFileExtensions'].split(' ')
        self.vscode_file_name_pattern: str = data['vscodeFileNamePattern']
        self.prosveshenie_token: str =       data['prosveshenieToken']

class Avatar:
    def __init__(self, data):
        '''
        User's avatar data.
        '''
        self.name: str =      data['name']
        self.small_url: str = data['smallUrl']
        self.svg_url: str =   data['svgUrl']

class Course:
    def __init__(self, data):
        '''
        User's course.
        '''
        self.id: int =                        data['id']
        self.name: str =                      data['name']
        self.display_name: str =              data['displayName']
        self.description: str =               data['description']
        self.use_first_task: int =            data['useFirstTask']
        # self.icon =                           NotImplemented('Unknown format')
        self.gamification_enabled: int =      data['gamification']['isEnabled']
        self.gamification_level_points: int = data['gamification']['regularLevelPoints']
        self.gamification_bonus_points: int = data['gamification']['bonusLevelPoints']
        # self.gamification_characters: list =  NotImplemented('Unknown format')

class SelfProfile:
    def __init__(self, data):
        '''
        The user that is currently logged in.
        '''
        # data
        self.dict = data

        self.id: int =            data['studentId']
        self.first_name: str =    data['firstName']
        self.last_name: str =     data['lastName']
        self.parent_name: str =   data['parentName']
        self.full_name: str =     data['fullName']
        self.username: str =      data['username']
        self.phone: str =         data['phone']
        self.email: str =         data['email']
        self.is_teacher: bool =   data['isTeacher']
        self.is_celebrity: bool = data['isCelebrity']
        self.lang: str =          data['lang']
        self.branch: Branch =     Branch(data['branch'])
        self.ban: Ban =           Ban(data['ban'])
        self.settings: Settings = Settings(data['settings'])
        self.avatar: Avatar =     Avatar(data['avatar'])
        self.course: Course =     Course(data['course'])

        # date
        date = [int(i) for i in data['birthDate'][0:10].split('-')]
        self.birth_date: datetime.date = datetime.date(
            year=date[0], month=date[1], day=date[2]
        )

        # not implemented
        # self.referral =        NotImplemented('Unknown format')
        # self.locations: list = NotImplemented('Unknown format')

    def __str__(self) -> str:
        return self.username
    
    def __int__(self) -> int:
        return self.id