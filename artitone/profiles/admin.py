from django.contrib import admin

from profiles.models.artist import Artist
from profiles.models.customer import Customer
from profiles.models.user import User

admin.site.register(User)
admin.site.register(Artist)
admin.site.register(Customer)
