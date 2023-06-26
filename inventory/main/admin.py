from tabnanny import verbose
from django.contrib import admin
from main.models import *

# Register your models here.
admin.site.register(MasterInventory)
admin.site.register(EquipmentMaster)
admin.site.register(OrderDetails)
admin.site.register(VendorDetails)
admin.site.register(InvoiceMaster)
admin.site.register(EquipmentCategory)
admin.site.register(PurchaseOrders)
admin.site.register(EmployeeMaster)
admin.site.register(PurchaseRequests)
admin.site.register(UserProfile)
admin.site.register(AuditLog)

class EventAdminSite(admin.ModelAdmin):
    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        ordering = {
            "Master Inventory": 1,
            "Equipment Master": 2,
            "Order Details": 3,
            "Vendor Details": 4,
            "Invoice Master": 5,
            "Equipment Categories": 6,
            "Equipment Subcategories": 7,
            "Purchase Requests": 8,
            "Purchase Orders": 9,
            "Employee Master": 10,
        }
        app_dict = self._build_app_dict(request)
        # a.sort(key=lambda x: b.index(x[0]))
        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
        # Sort the models alphabetically within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: ordering[x['name']])

        return app_list