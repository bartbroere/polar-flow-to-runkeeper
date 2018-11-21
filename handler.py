import datetime
import logging

import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PolarFlowClient:

    def __init__(self):
        self.session = requests.Session()

    def login(self, username, password):
        self.session.post('https://flow.polar.com/login',
                          data={"email": username,
                                "password": password,
                                "returnUrl": '/'})


class RunkeeperClient:

    def __init__(self):
        self.session = requests.Session()
        self.post = self.session.post
        self.get = self.session.get

    def login(self, username, password):
        self.session.post('https://runkeeper.com/login',
                          data={'_eventName': 'submit',
                                'redirectUrl': '',
                                'flow': '',
                                'failUrl': '',
                                'secureParams': '',
                                'email': username,
                                'password': password,
                                '_sourcePage': 'wiAO6roZofdSMkQ2IKb_mRoc-'
                                               'IQ0sMyrmpVzZ9KGq7kaHPiENL'
                                               'DMq5qVc2fShqu5knVNNT0OC_8'
                                               '%3D',
                                '_fp': 'WAvsyf4_Zig%3D'}
                          )


def run(event, context):
    current_time = datetime.datetime.now().time()
    name = context.function_name
    logger.info("Your cron function " + name + " ran at " + str(current_time))
    # TODO ETL here
