# vms
1. Navigate to vms\Vendor_Management_System_project/settings.py file
in database change your database name and password

2.Here i have attached vms.sql file just import in your database and 

run the server python manage.py runserver

3. if you dont want to import database just type following commands
-  python manage.py makemigrations
-  python manage.py migrate



API Endpoints
1. Vendor Profile Management
List all vendors or create a new vendor:

Endpoint: /api/vendors/
Method: GET (list all vendors) or POST (create a new vendor)
Retrieve, update, or delete a specific vendor:

Endpoint: /api/vendors/{vendor_id}/
Methods: GET (retrieve), PUT (update), DELETE (delete)
2. Purchase Order Tracking
List all purchase orders or create a new purchase order:

Endpoint: /api/purchase_orders/
Method: GET (list all purchase orders) or POST (create a new purchase order)
Retrieve, update, or delete a specific purchase order:

Endpoint: /api/purchase_orders/{po_id}/
Methods: GET (retrieve), PUT (update), DELETE (delete)
3. Historical Performance Model
Update vendor performance metrics:
Endpoint: /api/update_vendor_performance_metrics/{vendor_id}/
Method: POST (update vendor performance metrics)
4. Vendor Performance
Show vendor performance metrics:
Endpoint: /api/show_vendor_performance/{vendor_id}/
Method: GET (retrieve vendor performance metrics)


After this if you have any type of issue feel free to contact me
