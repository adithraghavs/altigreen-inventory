import django_filters
from .models import *

class MasterInventoryFilter(django_filters.FilterSet):
    equipment_id = django_filters.CharFilter(lookup_expr='exact')
    equipment_name__name = django_filters.CharFilter(lookup_expr='icontains')
    employee_id = django_filters.CharFilter(lookup_expr='exact')
    employee_name = django_filters.CharFilter(lookup_expr='icontains')
    warranty_start_date = django_filters.DateFilter(lookup_expr='exact')
    warranty_end_date = django_filters.DateFilter(lookup_expr='exact')
    purchase_order_number = django_filters.CharFilter(lookup_expr='icontains')
    asset_code = django_filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = MasterInventory
        fields = ['equipment_id', 'equipment_name', 'employee_id', 'employee_name', 'warranty_start_date', 'warranty_end_date', 'purchase_order_number', 'asset_code']
class EquipmentMasterFilter(django_filters.FilterSet):
    equipment_id = django_filters.CharFilter(lookup_expr='exact')
    equipment_type = django_filters.CharFilter(lookup_expr='icontains')
    name = django_filters.CharFilter(lookup_expr='icontains')
    ram = django_filters.CharFilter(lookup_expr='icontains')
    storage = django_filters.DateFilter(lookup_expr='icontains')
    display_size = django_filters.DateFilter(lookup_expr='icontains')
    paper_size = django_filters.CharFilter(lookup_expr='icontains')
    operating_system = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = EquipmentMaster
        fields = ['equipment_id', 'equipment_type', 'name', 'ram', 'storage', 'display_size', 'paper_size', 'operating_system']

class EquipmentCategoriesFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = EquipmentCategory
        fields = ['name', 'description']

class EmployeeMasterFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    employee_id = django_filters.CharFilter(lookup_expr='icontains')
    email_id = django_filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = EmployeeMaster
        fields = ['name', 'employee_id', 'email_id']

class PurchaseRequestsFilter(django_filters.FilterSet):
    equipment_master__name = django_filters.CharFilter(lookup_expr='icontains')
    purchase_request_number = django_filters.CharFilter(lookup_expr='exact')
    purchase_request_date = django_filters.CharFilter(lookup_expr='exact')
    employee_master__name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = PurchaseRequests
        fields = ['equipment_master', 'purchase_request_number', 'purchase_request_date', 'employee_master']

class PurchaseOrdersFilter(django_filters.FilterSet):
    equipment_master__name = django_filters.CharFilter(lookup_expr='icontains')
    purchase_order_number = django_filters.CharFilter(lookup_expr='exact')
    purchase_order_date = django_filters.CharFilter(lookup_expr='exact')
    amount = django_filters.CharFilter(lookup_expr='exact')
    vendor = django_filters.DateFilter(lookup_expr='exact')

    class Meta:
        model = PurchaseOrders
        fields = ['equipment_master', 'purchase_order_number', 'purchase_order_date', 'amount', 'vendor']

class VendorsFilter(django_filters.FilterSet):
    vendor_id = django_filters.CharFilter(lookup_expr='exact')
    vendor_name = django_filters.CharFilter(lookup_expr='icontains')
    phone_number = django_filters.CharFilter(lookup_expr='exact')
    email_id = django_filters.CharFilter(lookup_expr='icontains')
    address = django_filters.DateFilter(lookup_expr='exact')

    class Meta:
        model = VendorDetails
        fields = ['vendor_id', 'vendor_name', 'phone_number', 'email_id', 'address']

class InvoiceMasterFilter(django_filters.FilterSet):
    invoice_number = django_filters.CharFilter(lookup_expr='exact')
    delivery_challan = django_filters.CharFilter(lookup_expr='icontains')
    delivery_challan_date = django_filters.CharFilter(lookup_expr='exact')
    vendor__vendor_name = django_filters.CharFilter(lookup_expr='icontains')
    equipment__name = django_filters.DateFilter(lookup_expr='exact')
    quantity = django_filters.DateFilter(lookup_expr='exact')

    class Meta:
        model = InvoiceMaster
        fields = ['invoice_number', 'delivery_challan', 'delivery_challan_date', 'vendor__vendor_name', 'equipment__name', 'quantity']