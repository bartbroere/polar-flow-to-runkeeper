import datetime
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def run(event, context):
    # https://flow.polar.com/login
    # POST
    # email: email
    # password: password
    # returnUrl: '/'
    
    # https://runkeeper.com/login
    # POST
    # _eventName=submit&redirectUrl=&flow=&failUrl=&secureParams=&email=email%40email.com&password=undisclosed&_sourcePage=wiAO6roZofdSMkQ2IKb_mRoc-IQ0sMyrmpVzZ9KGq7kaHPiENLDMq5qVc2fShqu5knVNNT0OC_8%3D&__fp=WAvsyf4_Zig%3D
    current_time = datetime.datetime.now().time()
    name = context.function_name
    logger.info("Your cron function " + name + " ran at " + str(current_time))
