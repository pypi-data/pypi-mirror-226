from ratingfish.endpoint import Endpoint


class Agents(Endpoint):

    def __init__(self, api_key):
        '''init

        :param str api_key: RatingFish API KEY
        '''
        super().__init__(api_key)
        self.endpoint = "/agents"

    def get(self, page=None, count=None, user_id=None):
        '''get agents data

        :param int page: Page #
        :param int count: Number of itmes in returned data set
        :param str user_id: User ID
        '''
        if user_id:
            # if searched by user ID
            page = None
            count = None

        return self._make_call(
            params={
                "page": page,
                "count": count,
                "user_id": user_id,
            }
        ).json()

    def stats(self, page=None, count=None, user_id=None, sort=None,
              sort_field=None, interval=None, rating=None, hide_non_rated=None,
              hide_non_commented=None, hide_non_recommended=None):
        '''get agents stats data

        :param int page: Page #
        :param int count: Number of itmes in returned data set
        :param str user_id: User ID
        :param str sort: Sort direction
        :param str sort_field: Sort field
        :param str interval: Interval to search for in format YYYYMMDD-YYYYMMDD
        :param int rating: Specific rating to search for
        :param bool hide_non_rated: Hide non rated survey
        :param bool hide_non_commented:  Hide non commented survey
        :param bool hide_non_recommended: Hide survey without recommendation
        '''
        if user_id:
            # if searched by user ID
            page = None
            count = None
        if not hide_non_rated:
            hide_non_rated = None
        if not hide_non_commented:
            hide_non_commented = None
        if not hide_non_recommended:
            hide_non_recommended = None

        return self._make_call(
            endpoint="/agents/stats",
            params={
                "page": page,
                "count": count,
                "user_id": user_id,
                "sort": sort,
                "sort_field": sort_field,
                "interval": interval,
                "rating": rating,
                "hide_non_rated": hide_non_rated,
                "hide_non_commented": hide_non_commented,
                "hide_non_recommended": hide_non_recommended,
            }
        ).json()
