from django.contrib import admin
from models import *

class UserAdmin(admin.ModelAdmin):
    search_fields = ['username']
    list_filter = ('domain', )

admin.site.register(Domain)
admin.site.register(User, UserAdmin)
admin.site.register(Alias)
admin.site.register(Route)
admin.site.register(Access)
