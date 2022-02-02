from django.contrib import admin
from .models import SimpleOffer, PremiumOffer, Trade


admin.site.register(SimpleOffer)
admin.site.register(PremiumOffer)
admin.site.register(Trade)