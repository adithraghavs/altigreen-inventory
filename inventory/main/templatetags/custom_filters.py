from django import template
from main.models import MasterInventory, EquipmentMaster, EquipmentCategory, EmployeeMaster, PurchaseOrders, PurchaseRequests, VendorDetails, InvoiceMaster

register = template.Library()

@register.filter
def updatedeletefilter(table_name, row):
    if table_name == "masterinventory":
        objects = MasterInventory.objects.filter(asset_code=row.cells[0])
    elif table_name == "equipmentmaster":
        objects = EquipmentMaster.objects.filter(equipment_id=row.cells[0])
    elif table_name == "equipmentcategory":
        objects = EquipmentCategory.objects.filter(name=row.cells[0])
    elif table_name == "employeemaster":
        objects = EmployeeMaster.objects.filter(employee_id=row.cells[1])
    elif table_name == "purchaseorders":
        objects = PurchaseOrders.objects.filter(purchase_order_number=row.cells[1])
    elif table_name == "purchaserequests":
        objects = PurchaseRequests.objects.filter(purchase_request_number=row.record.purchase_request_number)
    elif table_name == "vendordetails":
        objects = VendorDetails.objects.filter(vendor_id=row.record.vendor_id)
    elif table_name == "invoicemaster":
        objects = InvoiceMaster.objects.filter(invoice_number=row.record.invoice_number)
    else:
        return None

    if objects.exists():
        return objects.first().pk
    else:
        return None
