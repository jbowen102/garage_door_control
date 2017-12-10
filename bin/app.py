import web
from .garage_door_control import flip_switch

# Mappings of URL to class
urls = (
    '/', 'Main',
)

app = web.application(urls, globals())

render = web.template.render('templates/')
# base="layout")

class Main(object):
    def GET(self):
        return render.switch_panel()

    def POST(self):
        form = web.input(switch1)
        # flip_switch.flip()
        print('switch flipped')


if __name__ == "__main__":
    app.run()
