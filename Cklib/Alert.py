from pubnub import Pubnub

class Alert(object):
    def __init__(self, config):
        self.config = config
        self.pnconfig = config['alert']['PubNub']
        self.pn = Pubnub(publish_key=self.pnconfig['pubkey'], subscribe_key=self.pnconfig['subkey'], ssl_on=True)

    def info(self, message):
        self.pn.publish(channel='pyrunhpcg', message="INF:"+message)

    def warn(self, message):
        self.pn.publish(channel='pyrunhpcg', message="WRN:"+message)

    def error(self, message):
        self.pn.publish(channel='pyrunhpcg', message="ERR:"+message)

    def ok(self, message):
        self.pn.publish(channel='pyrunhpcg', message="OK:"+message)

    def text(self, message):
        self.pn.publish(channel='pyrunhpcg', message=message)
