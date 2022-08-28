from django.contrib import admin
from authentication.models import User, Query

class User_Admin(admin.ModelAdmin):
    model = User
    search_fields = ['Phone']
    list_display = ("first_name", "College_name", "Year")

admin.site.register(User, User_Admin)
admin.site.register(Query)