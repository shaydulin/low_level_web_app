def index():
    with open("templates/index.html") as tpl:
        return tpl.read()


def blog():
    with open("templates/blog.html") as tpl:
        return tpl.read()
