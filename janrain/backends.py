from django.contrib.auth.models import User
from janrain.models import JanrainUser 
import django.contrib.auth

class JanrainBackend:
	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None

	def authenticate(self, profile):
        # identifier is the unique identifier used to sign user into site
		identifier = profile['identifier']	# a URL to the user profile of the service

		# these fields MAY be in the profile, but are not guaranteed. it
		# depends on the provider and their implementation.
		providerName = profile.get('providerName')	# e.g. Google or Facebook
		displayName = profile.get('displayName')	# for google, this is the username
		name = profile.get('name')					# a dictionary containing givenName, familyName, and formatted
		givenName = name.get('givenName')	# e.g. Hain-Lee
		familyName = name.get('familyName')	# e.g. Hsueh
		formatted = name.get('formatted')	# e.g. Hain-Lee Hsueh
		email = profile.get('email') or profile.get('verifiedEmail')	# not provided by Facebook

		try:
			janrain_user = JanrainUser.objects.get(identifier=identifier, provider=providerName)
			return janrain_user.django_user
		except JanrainUser.DoesNotExist:
			# create new JanrainUser record and associate with a django User object,
			# creating one if one does not exist
			janrain_user = JanrainUser(
								identifier=identifier,
								provider=providerName,
							display_name=displayName)

			# try to associate with an existing user by first and last name and email
			try:
				u = User.objects.get(first_name__iexact=givenName, last_name__iexact=familyName, email__iexact=email)
			except User.DoesNotExist, User.MultipleObjectsReturned:
				u = User()
				# if provider is google make the username the google username
				if providerName == 'Google':
					u.username = displayName
				else:
					# hash the identifier to ensure a unique username for the User object
					# base64 to ensure that username is 30 characters max
					u.username = b64encode(sha1(identifier).digest())
				u.first_name = givenName
				u.last_name = familyName
				u.is_superuser = False
				u.is_active = True
				u.set_unusable_password()
				u.is_staff = False
				if email:
					u.email = email
				u.save()
	
			# associate django user, and save
			janrain_user.django_user = u
			janrain_user.save()

			return janrain_user.django_user

