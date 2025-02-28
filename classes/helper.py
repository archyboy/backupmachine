
import time
import uuid

class Helper:

    def __main__(self):
        print(__class__)
        print(__file__)
        print(__name__)


    def getDateTimeFromTimestamp(timestamp, timetype):
        unix_timestamp  = int(timestamp)
        utc_time = time.gmtime(unix_timestamp)
        local_time = time.localtime(unix_timestamp)

        if timetype == 'local':
            return time.strftime("%d-%m-%Y-%H:%M:%S", local_time) + '-' + str(uuid.uuid4().fields[-1])[:5]
        if timetype == 'utc':
            return time.strftime("%d-%m-%Y-%H:%M:%S+00:00 (UTC)", utc_time)
