from pyramid.response import Response
from pyramid.view import (
    view_config,
    forbidden_view_config,
    )

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Provider,
    )

from pyramid.httpexceptions import (
    HTTPFound,
    # HTTPNotFound,
    )

from pyramid.security import (
    remember,
    forget,
    )


@view_config(route_name='home', renderer='templates/mytemplate.jinja2')
def my_view(request):
    try:
        provider = DBSession.query(Provider).filter(Provider.name == 'Provider One').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'provider': provider, 'project': 'MyProject'}


@view_config(route_name="signup", renderer='templates/signup.jinja2')
def signup(request):
    messages = []
    if 'form.submitted' in request.params:
        name = request.params['name']
        email = request.params['email']
        password = request.params['password']
        confirm_password = request.params['confirm']
        preexisting_user = DBSession.query(Provider).filter(Provider.name == name).first()
        preexisting_email = DBSession.query(Provider).filter(Provider.email == email).first()
        matching_passwords = (password == confirm_password)
        if preexisting_user:
            messages.append("A user by that name already exists")
        if preexisting_email:
            messages.append("That email address is already registered")
        if not matching_passwords:
            messages.append("Passwords do not match")
        if not messages:
            new_user = Provider(name=name, email=email, password=password)
            DBSession.add(new_user)
            return HTTPFound(location = request.route_url('home'))
        
    return {'messages': messages, 'url': request.route_url('signup') }

@view_config(route_name="login", renderer='templates/login.jinja2')
def login(request):
    messages = []
    if 'form.submitted' in request.params:
        email = request.params['email']
        password = request.params['password']
        user = DBSession.query(Provider).filter(Provider.email == email)\
                                        .filter(Provider.password == password).first()
        if not user:
            messages.append("Username and password do not match")

        if not messages:
            return HTTPFound(location = request.route_url('home'))

    return {'messages': messages, 'url': request.route_url('login')}


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

