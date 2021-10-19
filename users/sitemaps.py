from django.contrib.sitemaps import Sitemap
from merchants.models import Partner_Merchant

class PartnerSiteMap(Sitemap):
    changefreq = "daily"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Partner_Merchant.objects.all()

    def lastmod(self, obj):
        return obj.date_joined
    
    def location(self, obj):
        return '/brands/'
