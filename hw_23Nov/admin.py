from django.contrib import admin

from .models import Human,Child

class HumanAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'age', 'children_stat', 'children')
class ChildAdmin(admin.ModelAdmin):
    list_display = ('name','gender', 'age', 'parent')

admin.site.register(Human, HumanAdmin)
admin.site.register(Child, ChildAdmin)

