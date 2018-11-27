import datetime
import json
import logging
from collections import namedtuple

import confidence
import pymongo
from requests import Session

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PolarFlowClient(Session):

    def __init__(self):
        super().__init__()

    def login(self, username, password):
        return self.post('https://flow.polar.com/login',
                         data={"email": username,
                               "password": password,
                               "returnUrl": '/'})


class RunkeeperClient(Session):

    def __init__(self):
        super().__init__()

    def login(self, username, password):
        return self.post('https://runkeeper.com/login',
                         data={'_eventName': 'submit',
                               'redirectUrl': '',
                               'flow': '',
                               'failUrl': '',
                               'secureParams': '',
                               'email': username,
                               'password': password}
                         )


def run(event, context):
    config = confidence.load_name('polarflowtorunkeeper')
    current_time = datetime.datetime.now().time()
    name = context.function_name
    database = pymongo.MongoClient(config.mongodb)
    synced_runs = database['polar-flow-to-runkeeper'][
        'synced-runs'].find_one() or {'synced': []}
    synced_runs = synced_runs['synced']
    logging.info(json.dumps(synced_runs))
    database['polar-flow-to-runkeeper']['synced-runs'].delete_one({})
    logger.info("Function " + name + " runs at " + str(current_time))
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
    logging.info(f'{len(activities)} retrieved from Polar Flow')
    activities = list(filter(lambda x: x['listItemId'] not in synced_runs,
                             activities))
    logging.info(f'{len(activities)} not yet in Runkeeper')
    for activity in activities:
        tcx_export = flow.get(
            'https://flow.polar.com/api/export/training/tcx/' +
            str(activity['listItemId']
        ))
        response = runkeeper.post(
            'https://runkeeper.com/trackMultipleFileUpload',
            data={'handleUpload': 'handleUpload'},
            files={'trackFiles': ('import.tcx', tcx_export.text,
                                  'application/octet-stream')}
        )
        logger.info(f'{str(activity["listItemId"])} returned {response.text}')
        synced_runs.append(activity['listItemId'])
    database['polar-flow-to-runkeeper']['synced-runs'].insert_one(
        {'synced': synced_runs}
    )


if __name__ == "__main__":
    # mimic serverless context with a namedtuple in testing
    Serverless = namedtuple("Serverless", ['function_name'])
    context = Serverless(function_name='run')
    event = ''
    run(event, context)
