from django.contrib import admin
from .models import Like,Follow,Post,Tag,Stream
admin.site.register([Like,Follow,Tag,Stream])


class PostAdmin(admin.ModelAdmin):
    list_display=["id","user","caption","posted"]


admin.site.register(Post,PostAdmin)