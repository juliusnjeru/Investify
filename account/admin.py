from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Account, Record

admin.site.unregister(Group)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    pass
