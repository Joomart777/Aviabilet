from django.contrib import admin

from api.aviabilet.models import *

admin.site.register(Passenger)
admin.site.register(Aviabilet)
admin.site.register(Image)
admin.site.register(Rating)
admin.site.register(Planes)
admin.site.register(Like)

# admin.site.register(Order)
# admin.site.register(Favorite)
class ImageInAdmin(admin.TabularInline):
    model = Image
    fields = ('image',)
    max_num = 2

@admin.register(Airlines)
class AirlinesAdmin(admin.ModelAdmin):
    inlines = [
        ImageInAdmin
    ]
