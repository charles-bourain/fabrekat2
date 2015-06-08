from .base import *

try:
	from .local import *
	live = False

except:
	live = True

if live:
	print live
	from .production import *