from django.contrib import admin

from profiles.models import Artist
from profiles.models import Customer
from profiles.models import User

admin.site.register(User)
admin.site.register(Artist)
admin.site.register(Customer)
