import web
import flip_switch


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
        print('switch flipped')
        return render.switch_panel()


if __name__ == "__main__":
    app.run()
