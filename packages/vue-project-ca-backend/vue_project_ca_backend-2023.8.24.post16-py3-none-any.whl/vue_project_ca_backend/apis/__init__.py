from flask import Flask


def init_app(app: Flask):
    from .users.urls import init_app as init_users
    init_users(app)

    from .projects.urls import init_app as init_projects
    init_projects(app)
