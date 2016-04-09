from .base import *

try:
    from .local import *
    live = False
    print 'NOT LIVE'

except:
    live = True
    print "LIVE"

if live:
    from .production import *
