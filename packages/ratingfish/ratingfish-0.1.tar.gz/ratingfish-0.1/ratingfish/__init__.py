from ratingfish.website import Website
from ratingfish.agents import Agents

class RatingFish:

    def __init__(self, api_key):
        '''init'''
        self.website = Website(api_key)
        self.agents = Agents(api_key)

