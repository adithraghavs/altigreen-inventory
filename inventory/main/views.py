from urllib import response
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from django.apps import apps
from main.models import *
from .forms import *
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from .tables import *
import json
import django_tables2 as django_tables
from django.db.models import BigAutoField
from django.core.paginator import Paginator
from django.views.generic import TemplateView
from .models import MasterInventory
import django_filters
from django_tables2 import SingleTableView
from .models import MasterInventory
from .tables import InventoryTable
from .filters import *
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import pandas
import os
from inventory.settings import MEDIA_ROOT

def model_foreignkey_fields(required_table: models.base.ModelBase) -> dict:
    return_dict = {}
    for field in required_table._meta.get_fields():
        if isinstance(field, models.ForeignKey):
            related_model = field.remote_field.model
            return_dict[field] = related_model

    return return_dict

class ModelEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, EquipmentMaster):
            context = {}
            for i in EquipmentMaster._meta.get_fields():
                # print(i.name)
                context[i.name] = getattr(EquipmentMaster.objects.get(pk=obj.pk), i.name)
                # print(i.name, getattr(EquipmentMaster.objects.get(pk=obj.pk), i.name))
            return context
        return super().default(obj)

tables = connection.introspection.table_names()
while tables[0].startswith("auth") or tables[0].startswith("django"):
    tables.pop(0)

tables_fixed = []
for i in tables:
    tables_fixed.append(i[5:])

seen_models = connection.introspection.installed_models(tables)

def register(request):
    registered = False
    ctx = {}

    if request.method == 'POST':
        username = request.POST.get("username")
        full_name = request.POST.get("full_name")
        password = request.POST.get("password")
        email_id = request.POST.get("email")
        house_number = request.POST.get("house_number")
        phone_number = request.POST.get("phone_number")
        if len(User.objects.filter(username=username)) == 0:
            ctx["username_exists"] = False
            user_form = UserForm(data=request.POST)
            if user_form.is_valid():
                user = user_form.save()
                user.set_password(user.password)
                user.save()
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(username=username, password=password)
                user_profile = UserProfile(user=user)
                user_profile.save()
                if user:
                    if user.is_active:
                        login(request,user)
                        return HttpResponseRedirect(reverse('index'))
                    else:
                        return HttpResponse("Your account was inactive.")
                else:
                    print("Someone tried to login and failed.")
                    print("They used username: {} and password: {}".format(username,password))
                    return HttpResponse("Invalid login details given")
            else:
                return HttpResponse("Contains @")
        else:
            ctx["username_exists"] = True
            return render(request,'main/registration.html', ctx)
    elif request.method == "GET":
        form = MasterInventoryForm()
        ctx["form"] = form
        return render(request,'main/registration.html', ctx)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account is inactive.")
        else:
            return HttpResponse("Invalid login details given")
    else:
        if request.GET.get("next"):
            if request.GET.get("next") == '/main/upload_book/':
                message = "You need to sign in to upload a book."
                return render(request, 'main/login.html', {"msg":message})
            elif request.GET.get("next") == '/main/my_books/':
                message = "You need to sign in to see your books."
                return render(request, 'main/login.html', {"msg":message})
            elif '/main/rent/' in request.GET.get("next"):
                message = "You need to sign in to rent a book."
                return render(request, 'main/login.html', {"msg":message})
        
        return render(request, 'main/login.html', {})

def generate(objects, previous_object_id, prefix):
    # print(objects, len(objects))
    if len(objects) != 0:
        if isinstance(previous_object_id, int):
            # print("int int int int")
            new_object_id = previous_object_id + 1
            # print("previous_object_id = ", previous_object_id)
        else:
            previous_object_id = previous_object_id.split(prefix + "-")[-1]
            new_object_id = int(previous_object_id) + 1
        # print(previous_object_id)
        # new_object_id = "" + str(int(previous_object_id) + 1)
        new_object_id = str(new_object_id)
        if len(new_object_id) < 6:
            if (len(new_object_id) == 1):
                new_object_id = "0" + new_object_id
            if (len(new_object_id) == 2):
                new_object_id = "0" + new_object_id
            if (len(new_object_id) == 3):
                new_object_id = "0" + new_object_id
            if (len(new_object_id) == 4):
                new_object_id = "0" + new_object_id
            if (len(new_object_id) == 5):
                new_object_id = "0" + new_object_id
        new_object_id = prefix + "-" + new_object_id
    else:
        new_object_id = prefix + "-" + "000001"

    return new_object_id

# @login_required  
def index(request):
    return render(request, "main/index.html")

# @login_required
class TableView(SingleTableView, FilterView):
    template_name = "main/table.html"

    def get(self, request, table_name):
        required_table = apps.get_model(app_label='main', model_name=table_name)
        user = request.user
        user_profile = UserProfile.objects.get(user=user)

        if table_name == "masterinventory":
            queryset = MasterInventory.objects.all()
            f = MasterInventoryFilter(request.GET, queryset=queryset)
            table = InventoryTable(data=f.qs)
        elif table_name == "equipmentmaster":
            queryset = EquipmentMaster.objects.all()
            f = EquipmentMasterFilter(request.GET, queryset=queryset)
            table = EquipmentTable(data=f.qs)
        elif table_name == "equipmentcategory":
            queryset = EquipmentCategory.objects.all()
            f = EquipmentCategoriesFilter(request.GET, queryset=queryset)
            table = EquipmentCategoriesTable(data=f.qs)
        elif table_name == "employeemaster":
            queryset = EmployeeMaster.objects.all()
            f = EmployeeMasterFilter(request.GET, queryset=queryset)
            table = EmployeeTable(data=f.qs)
        elif table_name == "purchaserequests":
            queryset = PurchaseRequests.objects.all()
            f = PurchaseRequestsFilter(request.GET, queryset=queryset)
            table = PurchaseRequestsTable(data=f.qs)
        elif table_name == "purchaseorders":
            queryset = PurchaseOrders.objects.all()
            f = PurchaseOrdersFilter(request.GET, queryset=queryset)
            table = PurchaseOrdersTable(data=f.qs)
        elif table_name == "vendordetails":
            queryset = VendorDetails.objects.all()
            f = VendorsFilter(request.GET, queryset=queryset)
            table = VendorsTable(data=f.qs)
        elif table_name == "invoicemaster":
            queryset = InvoiceMaster.objects.all()
            f = InvoiceMasterFilter(request.GET, queryset=queryset)
            table = InvoicesTable(data=f.qs)
        else:
            # Handle unknown table name
            return HttpResponse("Unknown table name")

        paginator = Paginator(table.data, 10)
        page = request.GET.get('page')
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {
            "filter": f,
            "table": table,
            "table_name": table_name,
            "table_verbose_name_plural": required_table._meta.verbose_name_plural,
            "status": user_profile.status,
            'items': items,
        })
    # except:
        #     return HttpResponse("<h1>Error: 2 or more duplicate objects imported</h1>")
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['additional_data'] = 'Some additional data'
        inventory_filter = MasterInventoryFilter(self.request.GET, queryset=self.get_queryset())
        context['filter'] = inventory_filter
        context['table'] = InventoryTable(inventory_filter.qs)
        return context
    

# class FilteredPersonListView(SingleTableMixin, FilterView):
#     table_class = InventoryTable
#     model = MasterInventory
#     template_name = "template.html"   

#     filterset_class = MasterInventoryFilter

# def table(request, table_name):
#     required_table = apps.get_model(app_label='main', model_name=table_name)
#     user = request.user
#     user_profile = UserProfile.objects.get(user=user)
#     print(user_profile.status)
#     # 
#     inventory = InventoryTable()
#     if (table_name == "masterinventory"):
#         return render(request, 'main/table.html', {
#         "tables": inventory,
#         "table_verbose_name_plural": required_table._meta.verbose_name_plural[4:],
#         "table_verbose_name_singular": required_table._meta.verbose_name,
#         "table": required_table,
#         "table_name_with_app_label": 'main_' + table_name,
#         "table_name": table_name,
#         "table_objects": required_table.objects.all(),
#         "status": user_profile.status
#     })
#     return render(request, 'main/table.html', {
#         "tables": tables_fixed,
#         "table_verbose_name_plural": required_table._meta.verbose_name_plural[4:],
#         "table_verbose_name_singular": required_table._meta.verbose_name,
#         "table": required_table,
#         "table_name_with_app_label": 'main_' + table_name,
#         "table_name": table_name,
#         "table_objects": required_table.objects.all(),
#         "status": user_profile.status
#     })

# class InventoryListView(SingleTableView, FilterView):
#     model = MasterInventory
#     table_class = InventoryTable
#     template_name = 'inventory_list.html'
#     filterset_class = InventoryFilter
#     paginate_by = 20

def search(request, table_name):
    query = request.GET.get("q")
    required_table = apps.get_model(app_label='main', model_name=table_name)
    queryset = required_table.objects.all()
    if table_name == "masterinventory":
        table = InventoryTable(queryset)
    if table_name == "equipmentmaster":
        table = EquipmentTable(queryset)
    if table_name == "equipmentcategory":
        table = EquipmentCategoriesTable(queryset)
    if table_name == "employeemaster":
        table = EmployeeTable(queryset)
    if table_name == "purchaserequests":
        table = PurchaseRequestsTable(queryset)
    if table_name == "purchaseorders":
        table = PurchaseOrdersTable(queryset)
    if table_name == "vendordetails":
        table = VendorsTable(queryset)
    if table_name == "invoicemaster":
        table = InvoicesTable(queryset)
    new_query = query.split('[')
    new_query = new_query[1].split(']')
    terms = new_query[0].split('=')
    field = terms[0].split('(')
    field = field[1].split(')')
    field = field[0]
    # print(field)
    value = terms[1].split("'")
    value = value[1]
    paginator = Paginator(queryset, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    if table_name == "masterinventory":
        if field == 'equipment_name':
            queryset = queryset.filter(equipment__equipment_name__icontains=value)
        else:
            queryset = queryset.filter(**{f"{field}__icontains": value})
        table = InventoryTable(queryset)
    return render(request, 'main/search.html', {
            "table": table,
            "query": query,
            "table_name": table_name,
            "table_verbose_name_plural": required_table._meta.verbose_name_plural,
            "status": user_profile.status,
            "page_obj": page_obj,
        })

# def import_csv(request, table_name):
#     required_table = apps.get_model(app_label='main', model_name=table_name)
#     # print(type(required_table))

#     csv_file_path = os.path.join(MEDIA_ROOT, 'file.csv')
#     df = pandas.read_csv(csv_file_path, header=0)
    
#     # Loop through each row in the dataframe
#     for _, row in df.iterrows():
#         # Create a new instance of the required model
#         obj = required_table()
        
#         # Loop through each column in the row
#         for column in df.columns:
#             # Skip the 'id' field
#             if column == 'id':
#                 continue
#             print(model_foreignkey_fields(required_table).keys())
#             # If the current column is the equipment_name field, fetch the EquipmentMaster instance
#             if column in list(model_foreignkey_fields(required_table).keys()):
#                 foreignkey_field = required_table.objects.filter(name=row[column])[0]
#                 setattr(obj, column, foreignkey_field)
#             else:
#                 print(column)
#                 setattr(obj, column, row[column])
        
#         # Save the object to the database
#         obj.save()

#     return HttpResponse("Import Successful!")

def import_csv(request, table_name):
    required_table = apps.get_model(app_label='main', model_name=table_name)
    queryset = required_table.objects.all()

    csv_file_path = os.path.join(MEDIA_ROOT, 'file.csv')
    df = pandas.read_csv(csv_file_path, header=0)

    if required_table == MasterInventory:
        for _, row in df.iterrows():
            existing_record = required_table.objects.filter(
                
                asset_code=row['asset_code'], 
                equipment_id=row['equipment_id'], 
                equipment_name=row['equipment_name'], 
                employee_id=row['employee_id'], 
                employee_name=row['employee_name'], 
                warranty_start_date=row['warranty_start_date'], 
                warranty_end_date=row['warranty_end_date'], 
                purchase_order_number=row['purchase_order_number'],
            ).first()

            if existing_record:
                continue

            new_record = required_table(
                asset_code=row['asset_code'], 
                equipment_id=row['equipment_id'], 
                equipment_name=row['equipment_name'], 
                employee_id=row['employee_id'], 
                employee_name=row['employee_name'], 
                warranty_start_date=row['warranty_start_date'], 
                warranty_end_date=row['warranty_end_date'], 
                purchase_order_number=row['purchase_order_number'], 
            )
            new_record.save()


def export_to_csv(request, table_name):
    required_table = apps.get_model(app_label='main', model_name=table_name)
    queryset = required_table.objects.all()
    if table_name == "masterinventory":
        table = InventoryTable(queryset)
    if table_name == "equipmentmaster":
        table = EquipmentTable(queryset)
    if table_name == "equipmentcategory":
        table = EquipmentCategoriesTable(queryset)
    if table_name == "employeemaster":
        table = EmployeeTable(queryset)
    if table_name == "purchaserequests":
        table = PurchaseRequestsTable(queryset)
    if table_name == "purchaseorders":
        table = PurchaseOrdersTable(queryset)
    if table_name == "vendordetails":
        table = VendorsTable(queryset)
    if table_name == "invoicemaster":
        table = InvoicesTable(queryset)
    # i = 0
    # csv_file = os.path.join(MEDIA_ROOT, ''+table_name + '_' + i)
    
    # while (os.path.exists(csv_file)):
    #     i += 1
    #     csv_file = os.path.join(MEDIA_ROOT, ''+table_name + '_' + i)

    # if not os.path.exists(csv_file):
    #     f = open(csv_file, "a")
    #     line = ""
    #     for column in table.columns:
    #         line = column + ", "
    #     f.append(line)


    # return render(request, )

    response = HttpResponse(content_type='text/csv')  
    response['Content-Disposition'] = 'attachment; filename="file.csv"'  
    writer = csv.writer(response)
    columnslst = []
    for column in table.columns:
        columnslst.append(column)
    writer.writerow(columnslst)  
    for row in table.rows:
        row_lst = []
        row_lst = list(row)
        writer.writerow(row_lst)
    return response

# @login_required
def add_new(request, table_name):
    required_table = apps.get_model(app_label='main', model_name=table_name)
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    # print(user_profile.status)
    context_add_new = {
                    'table_name': table_name,
                    'required_table': required_table,
                    "table_verbose_name_plural": required_table._meta.verbose_name_plural[4:],
                    "table_verbose_name_singular": required_table._meta.verbose_name,
                    # 'form': form,
                    'status': user_profile.status
                }
    if request.method == 'POST':
        new_audit_log = AuditLog(name=user, action="added a new object", subject=table_name)
        new_audit_log.save()
    if table_name == "masterinventory":
        if request.method == 'POST':
            form = MasterInventoryForm(request.POST)

            if form.is_valid():
                cleaned_form = form.cleaned_data
                asset_code = cleaned_form['asset_code']
                equipment_id = cleaned_form['equipment_id']
                equipment_name = EquipmentMaster.objects.get(name=cleaned_form['equipment_name'], equipment_id = cleaned_form['equipment_id'])
                employee_id = cleaned_form['employee_id']
                employee_name = cleaned_form['employee_name']
                warranty_start_date = cleaned_form['warranty_start_date']
                warranty_end_date = cleaned_form['warranty_end_date']
                purchase_order_number = cleaned_form['purchase_order_number']

                master_inventory = MasterInventory(asset_code=asset_code, equipment_id=equipment_id, equipment_name=equipment_name, employee_id=employee_id, employee_name=employee_name, warranty_start_date=warranty_start_date, warranty_end_date=warranty_end_date, purchase_order_number=purchase_order_number)
                master_inventory.save()
                return HttpResponseRedirect('/table/'+table_name)
        else:
            form = MasterInventoryForm()
        
        context_add_new["form"] = form
        
        return render(request, 'main/add_new.html', context_add_new)
    if user_profile.status != 0:
        if table_name == "equipmentmaster":
            if request.method == 'POST':
                form = EquipmentMasterForm(request.POST)

                if form.is_valid():
                    equipment_objects = EquipmentMaster.objects.all()
                    if len(equipment_objects) != 0:
                        previous_object = EquipmentMaster.objects.filter()[len(EquipmentMaster.objects.filter())-1]
                        previous_object_id = previous_object.equipment_id
                        equipment_id = generate(EquipmentMaster.objects.all(), previous_object_id, 'EQUIPMENT')
                    else:
                        equipment_id = 'EQUIPMENT-000000'
                    cleaned_form = form.cleaned_data
                    equipment_type = cleaned_form['equipment_type']
                    name = cleaned_form['name']
                    ram = cleaned_form['ram']
                    storage = cleaned_form['storage']
                    display_size = cleaned_form['display_size']
                    paper_size = cleaned_form['paper_size']
                    operating_system = cleaned_form['operating_system']

                    equipment_master = EquipmentMaster(equipment_id=equipment_id, equipment_type=equipment_type, name=name, ram=ram, storage=storage, display_size=display_size, paper_size=paper_size, operating_system=operating_system)
                    equipment_master.save()
                    return HttpResponseRedirect('/table/'+table_name)
            else:
                form = EquipmentMasterForm()

            context_add_new["form"] = form

            return render(request, 'main/add_new.html', context_add_new)

        elif table_name == "equipmentcategory":
            if request.method == 'POST':
                # print("hi")
                form = EquipmentCategoryForm(request.POST)

                if form.is_valid():
                    cleaned_form = form.cleaned_data
                    name = cleaned_form['name']
                    description = cleaned_form['description']

                    equipment_categories = EquipmentCategory(name=name, description=description)
                    equipment_categories.save()
                    return HttpResponseRedirect('/table/'+table_name)
            else:
                form = EquipmentCategoryForm()

            context_add_new["form"] = form

            return render(request, 'main/add_new.html', context_add_new)

        elif table_name == "employeemaster":
            if request.method == 'POST':
                form = EmployeeMasterForm(request.POST)
                
                if form.is_valid():
                    cleaned_form = form.cleaned_data
                    employee_id = cleaned_form['employee_id']
                    name = cleaned_form['name']
                    email_id = cleaned_form['email_id']

                    employee_master = EmployeeMaster(name=name, employee_id=employee_id, email_id=email_id)
                    employee_master.save()
                    return HttpResponseRedirect('/table/'+table_name)
            else:
                form = EmployeeMasterForm()
            
            context_add_new["form"] = form

            return render(request, 'main/add_new.html', context_add_new)

        elif table_name == "purchaserequests":
            if request.method == 'POST':
                form = PurchaseRequestsForm(request.POST)
                
                if form.is_valid():
                    purchase_request_objects = PurchaseRequests.objects.all()
                    if len(purchase_request_objects) != 0:
                        previous_object = PurchaseRequests.objects.filter()[len(PurchaseRequests.objects.filter())-1]
                        # print("previous_object = ", previous_object)
                        previous_object_id = previous_object.purchase_request_number
                        # print("previous_object_id_exterior = ", previous_object_id)
                        # print(previous_object_id)
                        purchase_request_number = generate(PurchaseRequests.objects.all(), previous_object_id, 'PURCHASE-REQUEST')
                        # print()
                    else:
                        purchase_request_number = 'PURCHASE-REQUEST-000001'
                    cleaned_form = form.cleaned_data
                    equipment_master = cleaned_form['equipment_master']
                    # purchase_request_number = cleaned_form['purchase_request_number']
                    purchase_request_date = cleaned_form['purchase_request_date']
                    # is_visible = cleaned_form['is_visible']

                    purchase_requests = PurchaseRequests(equipment_master=equipment_master, purchase_request_number=purchase_request_number, purchase_request_date=purchase_request_date)
                    purchase_requests.save()
                    return HttpResponseRedirect('/table/'+table_name)
            else:
                form = PurchaseRequestsForm()
            
            context_add_new["form"] = form

            return render(request, 'main/add_new.html', context_add_new)

        elif table_name == "purchaseorders":
            if request.method == 'POST':
                form = PurchaseOrdersForm(request.POST)
                if form.is_valid():
                    purchase_order_objects = PurchaseOrders.objects.all()
                    if len(purchase_order_objects) != 0:
                        previous_object = PurchaseOrders.objects.filter()[len(PurchaseOrders.objects.filter())-1]
                        previous_object_id = previous_object.purchase_order_number
                        purchase_order_number = generate(PurchaseOrders.objects.all(), previous_object_id, 'PURCHASE-ORDERS')
                    else:
                        purchase_order_number = 'PURCHASE-ORDERS-000000'
                    cleaned_form = form.cleaned_data
                    equipment_master = cleaned_form['equipment_master']
                    purchase_order_date = cleaned_form['purchase_order_date']
                    amount = cleaned_form['amount']
                    vendor = cleaned_form['vendor']
                    # is_visible = cleaned_form['is_visible']

                    purchase_orders = PurchaseOrders(equipment_master=equipment_master, purchase_order_number=purchase_order_number, purchase_order_date=purchase_order_date, amount=amount, vendor=vendor)
                    purchase_orders.save()
                    return HttpResponseRedirect('/table/'+table_name)
            else:
                form = PurchaseOrdersForm()
            
            context_add_new["form"] = form

            return render(request, 'main/add_new.html', context_add_new)

        elif table_name == "vendordetails":
            if request.method == 'POST':
                form = VendorsForm(request.POST)
                if form.is_valid():
                    previous_vendor_object = VendorDetails.objects.filter()[len(VendorDetails.objects.filter())-1]
                    previous_vendor_object_id = previous_vendor_object.vendor_id
                    vendor_id = generate(VendorDetails.objects.all(), previous_vendor_object_id, 'VENDOR')
                    # print(previous_vendor_object[len(previous_vendor_object)-1])
                    cleaned_form = form.cleaned_data
                    
                    # print('Vendor id: ' + vendor_id)
                    # print(VendorsForm.Meta.fields)
                    vendor_name = cleaned_form['vendor_name']
                    phone_number = cleaned_form['phone_number']
                    email_id = cleaned_form['email_id']
                    address = cleaned_form['address']
                    # is_visible = cleaned_form['is_visible']
                    vendor_details = VendorDetails(vendor_id=vendor_id, vendor_name=vendor_name, phone_number=phone_number, email_id=email_id, address=address)
                    vendor_details.save()
                    return HttpResponseRedirect('/table/'+table_name)
            else:
                form = VendorsForm()
            
            context_add_new["form"] = form

            return render(request, 'main/add_new.html', context_add_new)

        elif table_name == "invoicemaster":
            if request.method == 'POST':
                form = InvoiceForm(request.POST)
                if form.is_valid():
                    if len(InvoiceMaster.objects.all()) != 0:
                        previous_invoice_object = InvoiceMaster.objects.filter()[len(InvoiceMaster.objects.filter())-1]
                        previous_invoice_object_id = previous_invoice_object.invoice_number
                        invoice_number = generate(InvoiceMaster.objects.all(), previous_invoice_object_id, 'INVOICE')
                    else:
                        invoice_number = 'INVOICE-000001'
                    cleaned_form = form.cleaned_data
                    # invoice_number = cleaned_form['invoice_number']
                    equipment = cleaned_form['equipment']
                    quantity = cleaned_form['quantity']
                    delivery_challan = cleaned_form['delivery_challan']
                    delivery_challan_date = cleaned_form['delivery_challan_date']
                    vendor = cleaned_form['vendor']
                    invoice_details = InvoiceMaster(invoice_number=invoice_number, equipment=equipment, quantity=quantity, delivery_challan=delivery_challan, delivery_challan_date=delivery_challan_date, vendor=vendor)
                    invoice_details.save()
                    return HttpResponseRedirect('/table/'+table_name)
            else:
                form = InvoiceForm()
            
            context_add_new["form"] = form

            return render(request, 'main/add_new.html', context_add_new)
# @login_required        
def delete(request, table_name, pk):
    required_table = apps.get_model(app_label='main', model_name=table_name)
    object_to_delete = required_table.objects.get(id=pk)
    user = request.user
    if request.method == 'POST':
        new_audit_log = AuditLog(name=user, action="deleted an object", subject=table_name)
        new_audit_log.save()
    object_to_delete.delete()

    return HttpResponseRedirect('/table/'+table_name)
# @login_required
def update_object(request, table_name, pk):
    user = request.user
    # print("hiiiwfvnw")
    # print([f for f in EquipmentMaster._meta.get_fields() if not f.auto_created])
    if request.method == 'POST':
        required_table = apps.get_model(app_label='main', model_name=table_name)
        previous = {}
        # print(required_table.objects.get(pk=pk))
        for field in required_table._meta.get_fields():
            # print(field.name)
            value = getattr(required_table.objects.get(pk=pk), field.name)
            # print("printing valueeee", value)
            previous[field.name] = value
            # print(type(value))
            additional_info="Previous: \n\t"+json.dumps(previous, cls=ModelEncoder)
            # print(field.name, value)
                
        # new_audit_log = AuditLog(name=user, action="updated an object", subject=table_name, additional_info="Previous: \n\t"+json.dumps(previous, cls=ModelEncoder))
        # new_audit_log.save()
    if table_name == "masterinventory":
        required_table = apps.get_model(app_label='main', model_name=table_name)
        object = required_table.objects.get(pk=pk)

        form = MasterInventoryForm(request.POST or None, instance=object)

        if form.is_valid():
            current = {}
            for field in list(form.fields.keys()):
                value = form.cleaned_data[field]
                current[field] = value.__str__()
                # print("hiiiii", field, value)
            form.save()
            additional_info += "\nCurrent: \n\t"+json.dumps(current, cls=ModelEncoder)
            new_audit_log = AuditLog(name=user, action="updated an object", subject=table_name, additional_info=additional_info)
            new_audit_log.save()

            return HttpResponseRedirect('/table/'+table_name+'/')

        return render(request, 'main/update_object.html', {
            'object': object,
            'form': form,
            'table_name': table_name
        })
    if table_name == "equipmentmaster":
        required_table = apps.get_model(app_label='main', model_name=table_name)
        object = required_table.objects.get(pk=pk)


        form = EquipmentMasterUpdateForm(request.POST or None, instance=object)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/table/'+table_name+'/')

        return render(request, 'main/update_object.html', {
            'object': object,
            'form': form,
            'table_name': table_name
        })

    if table_name == "equipmentcategory":
        required_table = apps.get_model(app_label='main', model_name=table_name)
        object = required_table.objects.get(pk=pk)


        form = EquipmentCategoryForm(request.POST or None, instance=object)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/table/'+table_name+'/')

        return render(request, 'main/update_object.html', {
            'object': object,
            'form': form,
            'table_name': table_name
        })

    if table_name == "employeemaster":
        required_table = apps.get_model(app_label='main', model_name=table_name)
        
        object = required_table.objects.get(pk=pk)


        form = EmployeeMasterForm(request.POST or None, instance=object)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/table/'+table_name+'/')

        return render(request, 'main/update_object.html', {
            'object': object,
            'form': form,
            'table_name': table_name
        })

    if table_name == "purchaserequests":
        required_table = apps.get_model(app_label='main', model_name=table_name)
        
        object = required_table.objects.get(pk=pk)


        form = PurchaseRequestsUpdateForm(request.POST or None, instance=object)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/table/'+table_name+'/')

        return render(request, 'main/update_object.html', {
            'object': object,
            'form': form,
            'table_name': table_name
        })

    if table_name == "vendordetails":
        required_table = apps.get_model(app_label='main', model_name=table_name)
        
        object = required_table.objects.get(pk=pk)


        form = VendorsUpdateForm(request.POST or None, instance=object)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/table/'+table_name+'/')

        return render(request, 'main/update_object.html', {
            'object': object,
            'form': form,
            'table_name': table_name
        })

    if table_name == "invoicemaster":
        required_table = apps.get_model(app_label='main', model_name=table_name)
        
        object = required_table.objects.get(pk=pk)


        form = InvoiceUpdateForm(request.POST or None, instance=object)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/table/'+table_name+'/')

        return render(request, 'main/update_object.html', {
            'object': object,
            'form': form,
            'table_name': table_name
        })

    if table_name == "purchaseorders":
        required_table = apps.get_model(app_label='main', model_name=table_name)
        
        object = required_table.objects.get(pk=pk)


        form = PurchaseOrdersUpdateForm(request.POST or None, instance=object)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/table/'+table_name+'/')

        return render(request, 'main/update_object.html', {
            'object': object,
            'form': form,
            'table_name': table_name
        })

# @login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    status = "User"
    if (user_profile.status == 1):
        status = "Manager"
    else:
        status = "Admin"
    return render(request, 'main/profile.html', {
        'name': request.user.username,
        'status': status
    })

@login_required
def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))