from tabnanny import verbose
from tokenize import blank_re
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.apps import apps

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    status = models.IntegerField(default=0)
    creation_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name_plural = "User profiles"
    

class EquipmentCategory(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True)
    description = models.TextField(blank=True)
    is_visible = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    creation_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "03. Equipment Categories"

equipment_categories = []
for index, item in enumerate(EquipmentCategory.objects.all()):
    lst = [str(index), item.name]
    tupl = tuple(lst)
    equipment_categories.append(tupl)


class EquipmentMaster(models.Model):
    equipment_id = models.CharField(max_length=50, blank=True, null=True)
    equipment_type = models.CharField(max_length=50, choices=equipment_categories)
    name = models.CharField(max_length=200, blank=True, null=True)
    ram = models.CharField(max_length=100, blank=True, null=True)
    storage = models.CharField(max_length=100, blank=True, null=True)
    display_size = models.CharField(max_length=100, blank=True, null=True)
    paper_size = models.CharField(max_length=100, blank=True, null=True)
    operating_system = models.CharField(max_length=100, blank=True, null=True)
    is_visible = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    creation_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "02. Equipment Master"
        

class MasterInventory(models.Model):
    asset_code = models.CharField(max_length=30, blank=True, null=True)
    equipment_id = models.CharField(max_length=50, blank=True, null=True)
    equipment_name = models.ForeignKey(EquipmentMaster, on_delete=models.PROTECT, blank=True, null=True)
    employee_id = models.CharField(max_length=20, blank=True, null=True)
    employee_name = models.CharField(max_length=100, blank=True, null=True)
    warranty_start_date = models.DateField()
    warranty_end_date = models.DateField()
    purchase_order_number = models.CharField(max_length=30, blank=True, null=True)
    is_visible = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    creation_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.equipment_name.name
    
    def name_value(self):
        return self.equipment_name.name

    @property
    def equipment_number(self):
        return self.equipment_name.name

    class Meta:
        verbose_name_plural = "01. Master Inventory"

class VendorDetails(models.Model):
    vendor_id = models.CharField(max_length=50, blank=True, null=True)
    vendor_name = models.CharField(max_length=500, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    email_id = models.CharField(max_length=500, blank=True, null=True)
    address = models.CharField(max_length=1000, blank=True, null=True)
    is_visible = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    creation_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.vendor_name

    class Meta:
        verbose_name_plural = "09. Vendor Details"

class InvoiceMaster(models.Model):
    invoice_number = models.CharField(max_length=50, blank=True, null=True)
    delivery_challan = models.CharField(max_length=1000, blank=True, null=True)
    delivery_challan_date = models.DateTimeField(blank=True, null=True)
    vendor = models.ForeignKey(VendorDetails, on_delete=models.PROTECT, blank=True, null=True)
    equipment = models.ForeignKey(EquipmentMaster, on_delete=models.PROTECT, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    is_visible = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    creation_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.invoice_number

    class Meta:
        verbose_name_plural = "10. Invoice Master"


class OrderDetails(models.Model):
    purchase_order_number = models.CharField(max_length=100, blank=True, null=True)
    purchase_order_date = models.CharField(max_length=100, blank=True, null=True)
    purchase_request_number = models.IntegerField(blank=True, null=True)
    delivery_no = models.IntegerField(blank=True, null=True)
    delivery_equipment = models.CharField(max_length=500, blank=True, null=True)
    delivery_quantity = models.IntegerField(blank=True, null=True)  
    warranty_start_date = models.DateField()
    warranty_end_date = models.DateField()
    amount = models.IntegerField(null=True)
    invoice_details = models.ForeignKey(InvoiceMaster, on_delete=models.PROTECT, blank=True, null=True)
    vendor_number = models.ForeignKey(VendorDetails, on_delete=models.PROTECT, blank=True, null=True)
    equipment_number = models.ForeignKey(EquipmentMaster, on_delete=models.PROTECT, blank=True, null=True)
    is_visible = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    creation_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.purchase_order_number

    @property
    def invoice_number(self):
        return self.invoice_details.invoice_number

    @property
    def vendor_id(self):
        return self.vendor_number.vendor_id

    @property
    def equipment_id(self):
        return self.equipment_number.equipment_id

    class Meta:
        verbose_name_plural = "08. Order Details"    

# class EquipmentSubcategory(models.Model):
#     equipment_category = models.ForeignKey(EquipmentCategory, on_delete=models.PROTECT, blank=True, null=True)
#     equipment_name = models.CharField(max_length=100, blank=True, null=True)
#     description = models.TextField()
#     is_visible = models.BooleanField(default=True)
#     created_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
#     creation_date = models.DateTimeField(default=timezone.now)

#     @property
#     def equipment_Category(self):
#         return self.equipment_category.equipment_master.name

#     def __str__(self):
#         return self.equipment_category.name + ": " + self.equipment_name

#     class Meta:
#         verbose_name_plural = "04. Equipment Subcategories"   

class PurchaseOrders(models.Model):
    equipment_master = models.ForeignKey(EquipmentMaster, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Equipment name")
    purchase_order_number = models.CharField(max_length=100, blank=True, null=True)
    purchase_order_date = models.DateTimeField(blank=True, null=True)
    amount = models.IntegerField(null=True, verbose_name="Quantity")
    vendor = models.ForeignKey(VendorDetails, on_delete=models.PROTECT, blank=True, null=True)
    is_visible = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    creation_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.purchase_order_number

    class Meta:
        verbose_name_plural = "07. Purchase Orders"

    @property
    def equipment_name(self):
        return self.equipment_master.name

class EmployeeMaster(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True)
    employee_id = models.CharField(max_length=50, blank=True, null=True)
    email_id = models.EmailField(max_length=500, blank=True, null=True)
    is_visible = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    creation_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "05. Employee Master"

class PurchaseRequests(models.Model):
    equipment_master = models.ForeignKey(EquipmentMaster, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Equipment name")
    purchase_request_number = models.CharField(max_length=100, blank=True, null=True)
    purchase_request_date = models.DateField(blank=True, null=True)
    employee_master = models.ForeignKey(EmployeeMaster, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Requested by")
    is_visible = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    creation_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.purchase_request_number

    class Meta:
        verbose_name_plural = "06. Purchase Requests"

    @property
    def equipment_name(self):
        return self.equipment_master.name

    @property
    def requested_by(self):
        return self.employee_master.name
    
class AuditLog(models.Model):
    name = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    action = models.CharField(max_length=1000, blank=True, null=True)
    subject = models.CharField(max_length=1000, blank=True, null=True)
    datetime = models.DateTimeField(default=timezone.now)
    additional_info = models.TextField(blank=True, null=True)