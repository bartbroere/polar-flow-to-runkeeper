import datetime
import logging
from collections import namedtuple

import confidence
import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PolarFlowClient:

    def __init__(self):
        self.session = requests.Session()
        self.post = self.session.post
        self.get = self.session.get

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
    config = confidence.load_name('polarflowtorunkeeper.yaml')
    current_time = datetime.datetime.now().time()
    name = context.function_name
    logger.info("Your cron function " + name + " ran at " + str(current_time))
    flow = PolarFlowClient()
    flow.login(config.polarflow.username,
               config.polarflow.password)
    runkeeper = RunkeeperClient()
    runkeeper.login(config.runkeeper.username,
                    config.runkeeper.password)
    year = datetime.datetime.now().year
    activities = flow.get('https://flow.polar.com/training/getCalendarEvents',
                          params={'start': f'01.01.{year}',
                                  'end': f'31.12.{year}'}).json()
    for activity in activities:
        tcx_export = flow.get(
            'https://flow.polar.com/api/export/training/tcx/' +
            str(activity['listItemId']
        )).raw
        runkeeper.post('https://runkeeper.com/trackMultipleFileUpload',
                       files={'handleUpload': tcx_export})


if __name__ == "__main__":
    # mimic serverless context with a namedtuple in testing
    Serverless = namedtuple("Serverless", ['function_name'])
    context = Serverless(function_name='run')
    event = ''
    run(event, context)
