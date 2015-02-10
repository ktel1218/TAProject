from .models import (
    DBSession,
    User
    )

def groupfinder(userid, request):
    if DBSession.query(User).get(userid):
#       return GROUPS.get(userid, [])
        return []

