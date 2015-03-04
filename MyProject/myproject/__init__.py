from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from myproject.security import groupfinder

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    authn_policy = AuthTktAuthenticationPolicy(
        settings['myproject.secret'], callback=groupfinder, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings, 
                        root_factory='myproject.models.RootFactory')
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)

#### ROUTES #########
    config.add_route('home', '/')
    config.add_route('signup', '/signup')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    # config.add_route('view_profile', '/profile', factory='myproject.models.Profile')
    # config.add_route('create_profile','/profile/create', factory='myproject.models.Profile')
    config.add_route('private', '/private')


    config.add_route('idea', 'ideas/{idea}', factory='myproject.models.Profile')
    # config.add_route('idea', 'ideas/{idea}')
    

    # users
    config.add_route('users', '/users')
    # user
    config.add_route('user', '/users/{id}')
    config.add_route('approve_user', 'users/{id}/approve')
    config.add_route('delete_user', 'users/{id}/delete')
    config.add_route('ban_user', 'users/{id}/ban')
    config.add_route('flag_user', 'users/{id}/flag')
    config.add_route('message_user', 'users/{id}/message')
    config.add_route('alter_user_standing', 'users/{id}/{operator}')



    config.scan()
    return config.make_wsgi_app()
