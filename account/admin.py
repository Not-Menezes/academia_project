from django.contrib import admin

from account.models import Class , Registration , LoggedInUser

admin.site.register(Class)
admin.site.register(Registration)
admin.site.register(LoggedInUser)