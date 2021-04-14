from django.contrib import admin
from .models import *

from django.apps import apps


# models = apps.get_models()

# for model in models:
#     try:
#         admin.site.register(model)
#     except:
#         pass

admin.site.index_title = "DenCoin"
admin.site.site_header = "DenCoin"
admin.site.site_title = "DenCoin"


class UserProfileListAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in UserProfile._meta.fields if True]


admin.site.register(UserProfile, UserProfileListAdmin)


class TransactionListAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in Transaction._meta.fields if True]


admin.site.register(Transaction, TransactionListAdmin)


class BlockListAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in Block._meta.fields if True]


admin.site.register(Block, BlockListAdmin)
