##############
django-janrain
##############

Janrain integration into Django using built-in django.contrib.auth package. It
creates a django user using django.contrib.auth.models.User on first login and
retrieves that User object on future logins.

Tries to associate with an existing django User object by first and last name. If one does not exist, a new User object is created and associated with the profile identifier provided by Janrain. Mappings from Janrain profile identifiers to django User objects are stored in the JanrainUser object.

============
Installation
============
Add the janrain app to your project ``myproject``

Add a url entry in ``urls.py``::

	urlpatterns += patterns('',
		(r'^janrain/', include('myproject.janrain.urls')),
	)

Add ``janrain`` to your ``INSTALLED_APPS``::

	INSTALLED_APPS = (
		'django.contrib.admin',
		'django.contrib.auth',
		'django.contrib.contenttypes',
		'django.contrib.sessions',
		'myproject.janrain',
	)

Add ``myproject.janrain.backends.JanrainBackend`` to ``AUTHENTICATION_BACKENDS``::

	# put janrain.backends.JanrainBackend first
	AUTHENTICATION_BACKENDS = (
		'myproject.janrain.backends.JanrainBackend',
		'django.contrib.auth.backends.ModelBackend',
	)

Add your janrain api key to ``settings``::

	JANRAIN_API_KEY = "0123456789abcdef0123456789abcdef0123456789abcdef"

=====
Usage
=====

Configure your ``token_url`` in janrain to be http://yoursite.com/janrain/login/

Modify your login template to include the janrain widget. Optionally append the ``next`` query parameter in the token URL to redirect after login.

Create a button to hit ``/janrain/logout/`` to log out.