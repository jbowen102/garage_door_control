import os
import time
from datetime import datetime
import web

import flip_switch


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(SCRIPT_DIR, "logs")


# Mappings of URL to class
urls = (
    '/', 'Main'
)

app = web.application(urls, globals())

render = web.template.render('templates/')
# base="layout")

class Main(object):
    def GET(self):
        return render.switch_panel()

    def POST(self):
        form = web.input()
        flip_switch.flip()
        # print('switch flipped')
        self.log_action()
        return render.switch_panel()

    def log_action(self, operation="flip"):
        """Record activity in log file."""
        timestamp = datetime.now().strftime("%Y-%m-%dT%H%M%S")

        # Wait one second to prevent overwriting previous file if it occurred
        # less than one second ago.
        time.sleep(1)
        log_filename = "activity.log"
        full_path = os.path.join(LOG_DIR, log_filename)
        with open(full_path, "a") as log_file:
            log_file.write("[%s] Switch operation: %s\n" % (timestamp, operation))


if __name__ == "__main__":
    app.run()
