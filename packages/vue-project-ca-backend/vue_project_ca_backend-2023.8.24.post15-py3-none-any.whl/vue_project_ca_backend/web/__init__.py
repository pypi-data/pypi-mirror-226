from flask import Flask, send_file
import os


def init_app(app: Flask):

    from vue_project_ca_backend.web.view import index, login

    app.add_url_rule('/favicon.ico',
                     endpoint="favicon",
                     view_func=lambda: send_file(os.path.join(app.instance_path,
                                                              "favicon.ico")))
    app.add_url_rule("/", view_func=index)
    app.add_url_rule("/index", view_func=index)
    app.add_url_rule("/login", view_func=login)
