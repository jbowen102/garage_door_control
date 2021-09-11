import os
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
        filename = "%s_%s.log" % (timestamp, operation.lower())

        # Wait one second to prevent overwriting previous file if it occurred
        # less than one second ago.
        time.sleep(1)
        full_path = os.path.join(LOG_DIR, filename)
        with open(full_path, "w") as log_file:
            log_file.write("Switch operation: %s [%s]" % (operation, timestamp))


if __name__ == "__main__":
    app.run()
