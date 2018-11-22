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
        return self.session.post('https://flow.polar.com/login',
                                 data={"email": username,
                                       "password": password,
                                       "returnUrl": '/'})


class RunkeeperClient:

    def __init__(self):
        self.session = requests.Session()
        self.post = self.session.post
        self.get = self.session.get

    def login(self, username, password):
        return self.session.post('https://runkeeper.com/login',
                                 data={'_eventName': 'submit',
                                       'redirectUrl': '',
                                       'flow': '',
                                       'failUrl': '',
                                       'secureParams': '',
                                       'email': username,
                                       'password': password,
                                       '_sourcePage': 'wiAO6roZofdSM'
                                                      'kQ2IKb_mRoc-'
                                                      'IQ0sMyrmpVzZ9'
                                                      'KGq7kaHPiENL'
                                                      'DMq5qVc2fShqu'
                                                      '5knVNNT0OC_8'
                                                      '%3D',
                                       '_fp': 'WAvsyf4_Zig%3D'}
                                 )


def run(event, context):
    config = confidence.load_name('polarflowtorunkeeper')
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
        ))
        tcx_data = tcx_export.raw
        response = runkeeper.post(
            'https://runkeeper.com/trackMultipleFileUpload',
            data={'handleUpload': 'handleUpload'},
            files={'trackFiles': tcx_export.text})
        if response.status_code == 200:
            print(response.status_code)



if __name__ == "__main__":
    # mimic serverless context with a namedtuple in testing
    Serverless = namedtuple("Serverless", ['function_name'])
    context = Serverless(function_name='run')
    event = ''
    run(event, context)

    # successful = []
    # profile_picture = runkeeper.get(
    #     'https://runkeeper.com/user/2534855156/profile').text
    # profile_picture = runkeeper.get(
    #     'https://profile-pic' +
    #     profile_picture.split(
    #         "<img src=\"https://profile-pic")[1].split("\"")[0]
    # ).raw
    # if response.status_code == 200:
    #     successful.append(activity['listItemId'])
    # if response.status_code == 200:
    #     'Mark as processed'
    #     processed = flow.post(
    #         f'https://flow.polar.com/training/a'
    #         f'nalysis/{activity["listItemId"]}',
    #         data={'id': activity['listItemId'],
    #               'userId': '42417880',
    #               'preciseDuration': str(
    #                   datetime.timedelta(milliseconds=activity[
    #                   'duration']))[:-3],
    #               'distanceStr': str(activity['distance']),
    #               'preciseDistanceStr': activity['title'].split(';')[1][
    #                                    :-3],
    #               'note': 'synced-with-runkeeper',
    #               }
    #     )
    #     print()
    # id = 2990825720
    # userId = 42417880
    # preciseDuration = 00:13: 43.250
    # preciseDistanceStr = 1850.699951171875
    # duration = 00:13: 43.250
    # distanceStr = 1.8506999512
    # heartRateAvg = 138
    # powerAvg = 280
    # sport = 1
    # note = synced -
    # with-runkeeper
    # flow.post('https://flow.polar.com/settings/profile/',
    #           data={
    #               'imageUrl': 'https%3A%2F%2Fflow.cdn.polar.com'
    #                           '%2Fflow%2F4.72.1'
    #                           '%2Fimages%2Fprofile-image.png',
    #               'motto': ' '.join(successful),
    #               'countryCode': '',
    #               'city': '',
    #               'state': '',
    #               'street': '',
    #               'phone': ''
    #           })
    #     motto = profile.split('<input type=text id=motto name=motto value="')[1]
    #     motto = motto.split('"')[0]
    #     successful = motto.split(' ')
    # if str(activity['listItemId']) in successful:
    #     continue