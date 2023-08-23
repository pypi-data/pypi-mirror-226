from enum import Enum

class BaseEnum(Enum):
    @classmethod
    def values(cls):
        return list(i.value for i in cls)

    @classmethod
    def count(cls):
        return len(cls)

class Category(BaseEnum):
    MUSIC = "Music"
    AUTO = "Autos & Vehicles"
    COMEDY = "Comedy"
    EDUCATION = "Education"
    FILM = "Film & Animation"
    ENTERTAINMENT = "Entertainment"
    GAMING = "Gaming"
    HOWTO = "Howto & Style"
    NEWS = "News & Politics"
    NONPROFIT = "Nonprofits & Activism"
    PEOPLE = "People & Blogs"
    PETS = "Pets & Animals"
    SCIENCE = "Science & Technology"
    SPORTS = "Sports"
    TRAVEL = "Travel & Events"
    

class Privacy(BaseEnum):
    PUBLIC = "Public"
    PRIVATE = "Private"
    UNLISTED = "Unlisted"     
    
# Overrideable paths for breaking elements
class ElementsPath(BaseEnum):
    YES_KIDS_CLASS = "style-scope ytkc-made-for-kids-select"
    YES_KIDS_INDEX = "18"
    DESCRIPTION_QUERY_SELECTOR = "div.style-scope.ytcp-social-suggestions-textbox"
    DESCRIPTION_INDEX = "5"
    