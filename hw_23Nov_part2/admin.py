from django.contrib import admin

from hw_23Nov_part2.models import Icecream, Stall

class StallInline(admin.TabularInline):  # или StackedInline, в зависимости от вашего предпочтения
    model = Stall.icecream.through
    extra = 1
class IcecreamAdmin(admin.ModelAdmin):
    inlines = [StallInline]
    list_display = ('title', 'mark')
class StallAdmin(admin.ModelAdmin):
    filter_horizontal = ['icecream']
    list_display = ('name','address')

admin.site.register(Icecream, IcecreamAdmin)
admin.site.register(Stall, StallAdmin)
