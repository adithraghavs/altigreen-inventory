import django_tables2 as tables
from .models import *

class InventoryTable(tables.Table):
    equipment_id = tables.Column(verbose_name='Equipment ID')
    equipment_name = tables.Column(verbose_name="Equipment Name")
    employee_id = tables.Column(verbose_name="Employee ID")
    employee_name = tables.Column(verbose_name="Employee Name")
    warranty_start_date = tables.Column(verbose_name="Warranty Start Date")
    warranty_end_date = tables.Column(verbose_name="Warranty End Date")
    purchase_order_number = tables.Column(verbose_name="Purchase Order Number")
    asset_code = tables.Column(verbose_name="Asset Code")

    class Meta:
        model = MasterInventory
        exclude = ('id', 'is_visible', 'created_by', 'creation_date')
        template_name = "django_tables2/bootstrap4.html"
        attrs = {'class': 'table table-striped table-hover'}
        paginate_by = 10

class EquipmentTable(tables.Table):
    equipment_id = tables.Column(verbose_name='Equipment ID')
    equipment_type = tables.Column(verbose_name="Equipment Type")
    name = tables.Column(verbose_name="Name")
    ram = tables.Column(verbose_name="RAM")
    storage = tables.Column(verbose_name="Storage")
    display_size = tables.Column(verbose_name="Display Size")
    paper_size = tables.Column(verbose_name="Paper Size")
    operating_system = tables.Column(verbose_name="Operating System")

    class Meta:
        model = EquipmentMaster
        exclude = ('id', 'is_visible', 'created_by', 'creation_date')
        template_name = "django_tables2/bootstrap4.html"
        attrs = {'class': 'table table-striped table-hover'}

class EquipmentCategoriesTable(tables.Table):
    name = tables.Column(verbose_name='Name')
    description = tables.Column(verbose_name="Description")

    class Meta:
        model = EquipmentCategory
        exclude = ('id', 'is_visible', 'created_by', 'creation_date')
        template_name = "django_tables2/bootstrap4.html"
        attrs = {'class': 'table table-striped table-hover'}

class EmployeeTable(tables.Table):
    name = tables.Column(verbose_name='Name')
    employee_id = tables.Column(verbose_name="Employee ID")
    email_id = tables.Column(verbose_name="email_id")

    class Meta:
        model = EmployeeMaster
        exclude = ('id', 'is_visible', 'created_by', 'creation_date')
        template_name = "django_tables2/bootstrap4.html"
        attrs = {'class': 'table table-striped table-hover'}

class PurchaseOrdersTable(tables.Table):
    equipment_master = tables.Column(verbose_name='Equipment Name')
    purchase_order_number = tables.Column(verbose_name="Purchase Order Number")
    purchase_order_date = tables.Column(verbose_name="Purchase Order Date")
    amount = tables.Column(verbose_name="Quantity")
    vendor = tables.Column(verbose_name="Vendor")

    class Meta:
        model = PurchaseOrders
        exclude = ('id', 'is_visible', 'created_by', 'creation_date')
        template_name = "django_tables2/bootstrap4.html"
        attrs = {'class': 'table table-striped table-hover'}

class PurchaseRequestsTable(tables.Table):
    equipment_master = tables.Column(verbose_name='Equipment Name')
    purchase_request_number = tables.Column(verbose_name="Purchase Request Number")
    purchase_request_date = tables.Column(verbose_name="Purchase Request Date")
    employee_master = tables.Column(verbose_name="Employee Name")

    class Meta:
        model = PurchaseRequests
        exclude = ('id', 'is_visible', 'created_by', 'creation_date')
        template_name = "django_tables2/bootstrap4.html"
        attrs = {'class': 'table table-striped table-hover'}

class VendorsTable(tables.Table):
    vendor_id = tables.Column(verbose_name='Vendor ID')
    vendor_name = tables.Column(verbose_name="Vendor Name")
    phone_number = tables.Column(verbose_name="Phone number")
    email_id = tables.Column(verbose_name="Email ID")
    address = tables.Column(verbose_name="Employee Name")

    class Meta:
        model = VendorDetails
        exclude = ('id', 'is_visible', 'created_by', 'creation_date')
        template_name = "django_tables2/bootstrap4.html"
        attrs = {'class': 'table table-striped table-hover'}

class InvoicesTable(tables.Table):
    invoice_number = tables.Column(verbose_name='Invoice Number')
    delivery_challan = tables.Column(verbose_name="Delivery Challan")
    delivery_challan_date = tables.Column(verbose_name="Delivery Challan Date")
    vendor = tables.Column(verbose_name="Vendor Name")
    equipment = tables.Column(verbose_name="Equipment Name")
    quantity = tables.Column(verbose_name="Quantity")

    class Meta:
        model = InvoiceMaster
        exclude = ('id', 'is_visible', 'created_by', 'creation_date')
        template_name = "django_tables2/bootstrap4.html"
        attrs = {'class': 'table table-striped table-hover'}