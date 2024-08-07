from django.contrib import admin
from . models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Addproduct)
admin.site.register(Like)
admin.site.register(Cart)
admin.site.register(Checkout)

