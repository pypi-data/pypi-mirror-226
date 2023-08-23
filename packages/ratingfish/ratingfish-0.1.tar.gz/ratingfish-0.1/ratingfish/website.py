from ratingfish.endpoint import Endpoint


class Website(Endpoint):

    def __init__(self, api_key):
        '''init

        :param str api_key: RatingFish API KEY
        '''
        super().__init__(api_key)
        self.endpoint = "/website"

    def get(self):
        '''get website data'''
        return self._make_call().json()
