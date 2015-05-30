from django.shortcuts import render

# Create your views here.
def new catagory(catagory):
	pass

#Catagory Database Builder:
	# Reduce catagories to a non-space, non-cap form, this will be an indentifier column
	# There is a unicode column for what it is actually called
	# example - unicode column = 'Costume Making', reduced column = 'costumemaking'
	# all inputed catagories are broken down into the reduced column and compared
	# May want to do a scrub of names, in this case 'Costume Making' could also be named 'Costume Tailoring'.
	# The scrub could happen daily on the serverside only.  The scrub could be automated.
	# For catagories that have a certain amount of projects in them, they can be then compared to catagories with a large amount of projects and the wording compared.
	# autocomplete light can be used to prevent mutliple types

