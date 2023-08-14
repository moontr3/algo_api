import datetime
from .errors import *
from .datatypes import *

class NotImplemented:
    def __init__(self, message):
        self.message = message
    def __call__(self):
        raise NotImplementedException(self.message)
    

# PROFILES

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

    def __str__(self) -> str:
        return self.title

    def __int__(self) -> int:
        return self.id

class Ban:
    def __init__(self, data):
        '''
        User's ban status.
        '''
        self.is_banned: bool = data['active']
        self.reason: str =     data['reason']

        # date
        if data['expiresAt'] != None:
            date = [int(i) for i in data['expiresAt'][0:19].split('T')[0].split('-')]
            time = [int(i) for i in data['expiresAt'][0:19].split('T')[1].split(':')]
            self.expires_at: datetime.datetime = datetime.datetime(
                year=date[0], month=date[1], day=date[2],
                hour=time[0], minute=time[1], second=time[2]
            )
        else:
            self.expiresAt = None

class Settings:
    def __init__(self, data):
        '''
        User's editor settings.
        '''
        self.allowed_file_extensions: list = data['platformUploadFileExtensions'].split(' ')
        self.vscode_file_name_pattern: str = data['vscodeFileNamePattern']
        self.prosveshenie_token: str =       data['prosveshenieToken']

class Course:
    def __init__(self, data):
        '''
        User's course.
        '''
        self.id: int =                        data['id']
        self.name: str =                      data['name']
        self.display_name: str =              data['displayName']
        self.description: str =               data['description']
        # self.use_first_task: int =            NotImplemented('Unknown format')
        # self.icon =                           NotImplemented('Unknown format')
        self.gamification_enabled: bool =     data['gamification']['isEnabled'] != 0
        self.gamification_level_points: int = data['gamification']['regularLevelPoints']
        self.gamification_bonus_points: int = data['gamification']['bonusLevelPoints']
        # self.gamification_characters: list =  NotImplemented('Unknown format')

    def __str__(self) -> str:
        return self.display_name

class UserStats:
    def __init__(self, data):
        '''
        User's stats.
        '''
        self.classmates: int =    data['totalClassmates']
        self.projects: int =      data['totalProjectCount']
        self.views: int =         data['totalProjectViews']
        self.likes: int =         data['totalProjectLikes']
        self.reactions: int =     data['totalReactions']
        self.friends: int =       data['totalFriends']
        self.followers: int =     data['totalFollowers']
        self.following: int =     data['totalFollowing']
        self.avatars: int =       data['totalAvatars']
        self.avatar_items: int =  data['totalAvatarItems']
        self.lootboxes: int =     data['totalLootboxes']

class Avatar:
    def __init__(self, data):
        '''
        User's avatar data.
        '''
        self.name: str =      data['name']
        self.small_url: str = data['smallUrl']
        self.svg_url: str =   data['svgUrl']

    def __str__(self) -> str:
        return self.svg_url

class AvatarTemplate:
    def __init__(self, data):
        '''
        Avatar preset.
        '''
        self.name: str =      data['name']
        self.url: str =       data['originalUrl']
        self.small_url: str = data['smallUrl']

    def __str__(self) -> str:
        return self.url

class Avatars:
    def __init__(self, data):
        # self.selected =        NotImplemented('Unknown format')
        self.available: list = [AvatarTemplate(i) for i in data['available']]
        self.svg_url: str =    data['svgUrl']

    def __str__(self) -> str:
        return self.svg_url

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
        self.url: str =           f'https://learn.algoritmika.org/student-profile?profileId={self.id}'

        # date
        date = [int(i) for i in data['birthDate'][0:10].split('-')]
        self.birth_date: datetime.date = datetime.date(
            year=date[0], month=date[1], day=date[2]
        )

        # not implemented
        # self.referral =        NotImplemented('Unknown format')
        # self.locations: list = NotImplemented('Unknown format')

    def __str__(self) -> str:
        return self.full_name
    
    def __int__(self) -> int:
        return self.id
    
class ProfilePreview:
    def __init__(self, data):
        '''
        A preview of a user.
        '''
        # data
        self.dict = data

        self.id: int =            data['id']
        self.first_name: str =    data['firstName']
        self.last_name: str =     data['lastName']
        self.full_name: str =     data['name']
        self.is_celebrity: bool = data['isCelebrity']
        self.avatar: Avatar =     Avatar(data['avatar'])
        self.url: str =           f'https://learn.algoritmika.org/student-profile?profileId={self.id}'

    def __str__(self) -> str:
        return self.full_name
    
    def __int__(self) -> int:
        return self.id
    
class Profile:
    def __init__(self, data):
        '''
        The fetched user.
        '''
        # data
        self.dict = data

        self.id: int =            data['id']
        self.first_name: str =    data['firstName']
        self.last_name: str =     data['lastName']
        self.full_name: str =     data['fullName']
        self.is_celebrity: bool = data['isCelebrity']
        self.about: str =         data['about']
        self.course_name: str =   data['activeCourse']
        self.city: str =          data['city']
        self.friend_status: str = data['friendStatus'] # follow, friend or None
        self.stats: UserStats =   UserStats(data['stats'])
        self.avatar: Avatars =    Avatars(data['avatars'])
        self.friends: list =      [ProfilePreview(i) for i in data['friends']]
        self.classmates: list =   [ProfilePreview(i) for i in data['classmates']]
        self.url: str =           f'https://learn.algoritmika.org/student-profile?profileId={self.id}'

        # date
        if data['updatedAt'] != None:
            date = [int(i) for i in data['updatedAt'][0:19].split('T')[0].split('-')]
            time = [int(i) for i in data['updatedAt'][0:19].split('T')[1].split(':')]
            self.updated_at: datetime.datetime = datetime.datetime(
                year=date[0], month=date[1], day=date[2],
                hour=time[0], minute=time[1], second=time[2]
            )
        else:
            self.updated_at = None

    def __str__(self) -> str:
        return self.full_name
    
    def __int__(self) -> int:
        return self.id
    

# PROJECTS

class PreviewImage:
    def __init__(self, data):
        '''
        A preview image for a project.
        '''
        self.name: str =      data['name']
        self.small_url: str = data['small']
        self.url: str       = data['large']

    def __str__(self) -> str:
        return self.url
    
class Reactions:
    def __init__(self, data):
        self.you_placed_like: bool = REACTION_LIKE in data['my']
        self.you_placed_love: bool = REACTION_LOVE in data['my']
        self.you_placed_fire: bool = REACTION_FIRE in data['my']
        self.likes: int =            data['counters'][REACTION_LIKE]\
                                     if REACTION_LIKE in data['counters'] else 0
        self.loves: int =            data['counters'][REACTION_LOVE]\
                                     if REACTION_LOVE in data['counters'] else 0
        self.fires: int =            data['counters'][REACTION_FIRE]\
                                     if REACTION_FIRE in data['counters'] else 0

class Upload:
    def __init__(self, data):
        self.id: int       = data['id']
        self.filename: str = data['filename']
        self.url: str      = 'https://learn.algoritmika.org'+data['filepath']

        # date
        date = [int(i) for i in data['createdAt'][0:19].split('T')[0].split('-')]
        time = [int(i) for i in data['createdAt'][0:19].split('T')[1].split(':')]
        self.created_at: datetime.datetime = datetime.datetime(
            year=date[0], month=date[1], day=date[2],
            hour=time[0], minute=time[1], second=time[2]
        )
        date = [int(i) for i in data['updatedAt'][0:19].split('T')[0].split('-')]
        time = [int(i) for i in data['updatedAt'][0:19].split('T')[1].split(':')]
        self.updated_at: datetime.datetime = datetime.datetime(
            year=date[0], month=date[1], day=date[2],
            hour=time[0], minute=time[1], second=time[2]
        )

    def __str__(self) -> str:
        return self.url
    
    def __int__(self) -> int:
        return self.id
    
class RemixedProject:
    def __init__(self, data):
        self.id: int =          data['id']
        self.title: str =       data['title']
        self.author_name: str = data['studentName']
        self.url: str =         f'https://learn.algoritmika.org/community?projectId={self.id}'

    def __str__(self) -> str:
        return self.title
    
    def __int__(self) -> int:
        return self.id

class Project:
    def __init__(self, data):
        '''
        A project.
        '''
        # data
        self.dict = data

        self.id: int =                          data['id']
        self.title: str =                       data['title']
        self.description: str =                 None if data['description'] == None\
                                                or len(data['description']) == 0 else data['description']
        self.type: str =                        data['type']
        self.availability: str =                data['sharingMode']
        if SHARING_MODE_PRIVATE in self.availability:
            self.availability.remove(SHARING_MODE_PRIVATE)
        self.likes: int =                       data['likesCount']
        self.views: int =                       data['viewsCount']
        self.remixes: int =                     data['remixesCount']
        self.comments: int =                    data['commentsCount']
        self.is_deleted: bool =                 data['isDeleted'] != 0
        self.author: ProfilePreview =           ProfilePreview(data['author'])
        self.image: PreviewImage =              None if data['previewImages']['large'] == None\
                                                else PreviewImage(data['previewImages'])
        self.reactions: Reactions =             Reactions(data['reactions'])
        self.remix_enabled: bool =              data['remix']['isRemixEnabled'] != 0
        self.original_project: RemixedProject = None if data['remix']['originalProject'] == None\
                                                else RemixedProject(data['remix']['originalProject'])
        self.uploads: list =                    [Upload(i) for i in data['uploads']]
        self.url: str =                         f'https://learn.algoritmika.org/community?projectId={self.id}'

        # date
        date = [int(i) for i in data['createdAt'][0:19].split('T')[0].split('-')]
        time = [int(i) for i in data['createdAt'][0:19].split('T')[1].split(':')]
        self.created_at: datetime.datetime = datetime.datetime(
            year=date[0], month=date[1], day=date[2],
            hour=time[0], minute=time[1], second=time[2]
        )
        date = [int(i) for i in data['updatedAt'][0:19].split('T')[0].split('-')]
        time = [int(i) for i in data['updatedAt'][0:19].split('T')[1].split(':')]
        self.updated_at: datetime.datetime = datetime.datetime(
            year=date[0], month=date[1], day=date[2],
            hour=time[0], minute=time[1], second=time[2]
        )

    def __str__(self) -> str:
        return self.title
    
    def __int__(self) -> int:
        return self.id
    

# comments

class Comment:
    def __init__(self, data):
        '''
        A comment.
        '''
        # data
        self.dict = data

        self.id: int =                data['id']
        self.message: str =           data['message']
        self.author: ProfilePreview = ProfilePreview(data['author'])
        self.children: list =         [Comment(i) for i in data['children']]

        # date
        date = [int(i) for i in data['createdAt'][0:19].split('T')[0].split('-')]
        time = [int(i) for i in data['createdAt'][0:19].split('T')[1].split(':')]
        self.created_at: datetime.datetime = datetime.datetime(
            year=date[0], month=date[1], day=date[2],
            hour=time[0], minute=time[1], second=time[2]
        )

    def __str__(self) -> str:
        return self.message
    
    def __int__(self) -> int:
        return self.id