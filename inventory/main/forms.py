from random import choices
from django import forms
from django.forms import ModelForm
from main.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password','email')
    def clean_username(self):
        data = self.cleaned_data.get('username')
        print(type(self.cleaned_data))
        if "@" in data:
            print("Contains @")
            raise forms.ValidationError("Contains @")
        return data

class MasterInventoryForm(ModelForm):
    warranty_start_date=forms.DateTimeField(
        input_formats=['%m/%Y'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    ) 
    warranty_end_date=forms.DateTimeField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    ) 
    class Meta:
        model = MasterInventory
        fields = ['asset_code', 'equipment_id', 'equipment_name', 'employee_id', 'employee_name', 'warranty_start_date', 'warranty_end_date', 'purchase_order_number']  

class EquipmentMasterForm(ModelForm):
    class Meta:
        model = EquipmentMaster
        fields = ['equipment_type', 'name', 'ram', 'storage', 'display_size', 'paper_size', 'operating_system']  

class EquipmentMasterUpdateForm(ModelForm):
    class Meta:
        model = EquipmentMaster
        fields = ['equipment_id', 'equipment_type', 'name', 'ram', 'storage', 'display_size', 'paper_size', 'operating_system']  

class EquipmentCategoryForm(ModelForm):
    class Meta:
        model = EquipmentCategory
        fields = ['name', 'description']  

class EmployeeMasterForm(ModelForm):
    class Meta:
        model = EmployeeMaster
        fields = ['name', 'employee_id', 'email_id']

class PurchaseRequestsForm(ModelForm):
    purchase_request_date=forms.DateTimeField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    ) 
    class Meta:
        model = PurchaseRequests
        fields = ['equipment_master', 'purchase_request_date', 'employee_master']

class PurchaseRequestsUpdateForm(ModelForm):
    purchase_request_date=forms.DateTimeField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    ) 
    class Meta:
        model = PurchaseRequests
        fields = ['equipment_master', 'purchase_request_number', 'purchase_request_date', 'employee_master']

class PurchaseOrdersForm(ModelForm):
    purchase_order_date=forms.DateTimeField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    ) 
    class Meta:
        model = PurchaseOrders
        fields = ['equipment_master', 'purchase_order_date', 'amount', 'vendor']

class PurchaseOrdersUpdateForm(ModelForm):
    purchase_order_date=forms.DateTimeField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    ) 
    class Meta:
        model = PurchaseOrders
        fields = ['equipment_master', 'purchase_order_number', 'purchase_order_date', 'amount', 'vendor']

class VendorsForm(ModelForm):
    class Meta:
        model = VendorDetails
        fields = ['vendor_name', 'phone_number', 'email_id', 'address']

class VendorsUpdateForm(ModelForm):
    class Meta:
        model = VendorDetails
        fields = ['vendor_id', 'vendor_name', 'phone_number', 'email_id', 'address']

class InvoiceForm(ModelForm):
    delivery_challan_date=forms.DateTimeField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    ) 
    class Meta:
        model = InvoiceMaster
        fields = ['equipment', 'delivery_challan', 'delivery_challan_date', 'vendor', 'quantity']

class InvoiceUpdateForm(ModelForm):
    delivery_challan_date=forms.DateTimeField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
    class Meta:
        model = InvoiceMaster
        fields = ['invoice_number', 'equipment', 'delivery_challan', 'delivery_challan_date', 'vendor', 'quantity']
