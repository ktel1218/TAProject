from pyramid.response import Response
from pyramid.view import (
    view_config,
    forbidden_view_config,
    )

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    User,
    )

from pyramid.httpexceptions import (
    HTTPFound,
    # HTTPNotFound,
    )

from pyramid.security import (
    remember,
    forget,
    )

# from pyramid.events import NewRequest
# from pyramid.events import subscriber

# @subscriber(NewRequest)
# def mysubscriber(event):
#     print event


@view_config(route_name='home', renderer='templates/home.jinja2', permission='view')
def home(request):
    try:
        user = DBSession.query(User).filter(User.name == 'Provider One').first()
    except DBAPIError:
        return Response(conn_err_msg, 
                        content_type='text/plain', 
                        status_int=500,
                        )
    return dict(
        logged_in = request.authenticated_userid,
        )

@view_config(route_name='private', renderer='templates/private.jinja2', permission='view')
def private(request):
    return dict(
        logged_in = request.authenticated_userid
        )

@view_config(route_name='signup', renderer='templates/signup.jinja2')
def signup(request):
    message = ''
    email = ''
    name = ''
    password = ''
    if 'form.submitted' in request.params:
        email = request.params['email']
        name = request.params['name']
        password = request.params['password']
        confirm_password = request.params['confirm']
        preexisting_user = DBSession.query(User).filter(User.name == name).first()
        preexisting_email = DBSession.query(User).filter(User.email == email).first()
        matching_passwords = (password == confirm_password)
        if preexisting_user:
            message = message + "A user by that name already exists\n"
        if preexisting_email:
            message = message + "That email address is already registered\n"
        if not matching_passwords:
            message = message + "Passwords do not match\n"
        if not message:
            new_user = User(name=name, email=email, password=password)
            DBSession.add(new_user)
            DBSession.flush()
            headers = remember(request, new_user.id)
            return HTTPFound(location = request.route_url('home'),
                            headers = headers,
                            )

    return dict(
        message = message,
        name = name,
        email = email,
        password = password,
        )


@view_config(route_name='login', renderer='templates/login.jinja2')
@forbidden_view_config(renderer='templates/login.jinja2')
def login(request):
    login_url = request.route_url('login')
    referrer = request.url
    print "CAME_FROM according to LOGIN", referrer

    if referrer == login_url:
        referrer = '/' # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)
    message = ''
    email = ''
    password = ''
    if 'form.submitted' in request.params:
        email = request.params['email']
        password = request.params['password']
        user = DBSession.query(User).filter(User.email == email).first()
        if user and user.password == password:
            headers = remember(request, user.id)
            return HTTPFound(location = came_from,
                            headers = headers,
                            )
        message = 'Failed login'

    return dict(
        message = message,
        email = email,
        password = password,
        came_from = came_from,
        )


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location = request.route_url('home'),
                     headers = headers,
                     )


# pagename = request.matchdict['pagename']

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_MyProject_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

