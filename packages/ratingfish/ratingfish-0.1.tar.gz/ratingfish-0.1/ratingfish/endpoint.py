import requests


class Endpoint:
    api_uri = "https://backend.rating.fish/api/v1.0/external"
    endpoint = None

    def __init__(self, api_key):
        '''init

        :param str api_key: RatingFish API KEY
        '''
        self.api_key = api_key

    def _craft_url(self, endpoint, params):
        '''make api url

        :param str endpoint: Endpoint to format
        :param list params: Parameters to insert in endpoint
        '''
        return "{}{}".format(
            self.api_uri,
            endpoint.format(*params) if params else endpoint,
        )

    def _make_call(self, endpoint_params=None, params={}, endpoint=None,
                   data=None, method="GET"):
        '''make call api

        :param list endpoint_params: Endpoint params list
        :param dict params: Query params for request
        :param str endpoint: Endpoint for request
        :param dict data: Data for request
        :param str method: Method for request
        '''
        params["key"] = self.api_key
        return requests.request(
            method,
            url=self._craft_url(
                self.endpoint if not endpoint else endpoint,
                endpoint_params
            ),
            data=data,
            params=params,
        )
