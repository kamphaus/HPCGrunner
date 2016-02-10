from pubnub import Pubnub
import time

class Alert(object):
    def __init__(self, config):
        self.config = config
        self.pnconfig = config['alert']['PubNub']
        self.pn = Pubnub(publish_key=self.pnconfig['pubkey'], subscribe_key=self.pnconfig['subkey'], ssl_on=True)

    def info(self, message):
        self.text(message="INF:"+message)

    def warn(self, message):
        self.text(message="WRN:"+message)

    def error(self, message):
        self.text(message="ERR:"+message)

    def ok(self, message):
        self.text(message="OK:"+message)

    def text(self, message):
        self.pn.publish(channel='pyrunhpcg', message=time.strftime('%Y-%m-%d %H:%M:%S')+" "+message)
