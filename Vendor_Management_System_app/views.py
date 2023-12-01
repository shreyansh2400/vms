from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone as tz
from rest_framework import status
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404
from django.db.models import Avg, F




# 1. Vendor Profile Management:

@api_view(['GET', 'POST'])
def vendor_list(request, vendor_id=None):
    if request.method == 'GET':
        if vendor_id:
            # Retrieve a specific vendor's details
            try:
                vendor = Vendor.objects.get(id=vendor_id)
                serializer = VendorSerializer(vendor)
                return Response({
                    'success': True,
                    'message': 'Vendor fetched successfully',
                    'data': serializer.data
                })
            except Vendor.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'Vendor not found',
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            # List all vendors
            vendors = Vendor.objects.all()
            serializer = VendorSerializer(vendors, many=True)
            return Response({
                'success': True,
                'message': 'Vendors fetched successfully',
                'data': serializer.data
            })

    elif request.method == 'POST':
        # Create a new vendor
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            vendor = serializer.save()
            return Response({
                'success': True,
                'message': 'Vendor added successfully',
                'data': VendorSerializer(vendor).data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'message': 'Error occurred while adding vendor',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        # Update a vendor's details
        try:
            vendor = Vendor.objects.get(id=vendor_id)
        except Vendor.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Vendor not found',
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = VendorSerializer(instance=vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Vendor updated successfully',
                'data': VendorSerializer(vendor).data
            })
        else:
            return Response({
                'success': False,
                'message': 'Error occurred while updating vendor',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Delete a vendor
        try:
            vendor = Vendor.objects.get(id=vendor_id)
            vendor.delete()
            return Response({
                'success': True,
                'message': 'Vendor deleted successfully'
            })
        except Vendor.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Vendor not found',
            }, status=status.HTTP_404_NOT_FOUND)


# 2. Purchase Order Tracking:
    
@api_view(['GET', 'POST'])
def purchase_order_tracking(request, po_id=None):
    if request.method == 'GET':
        if po_id:
            try:
                purchase_order = PurchaseOrder.objects.get(id=po_id)
                serializer = PurchaseOrderSerializer(purchase_order)
                return Response({
                    'success': True,
                    'message': 'Purchase Order fetched successfully',
                    'data': serializer.data
                })
            except PurchaseOrder.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'Purchase Order not found',
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            purchase_orders = PurchaseOrder.objects.all()
            serializer = PurchaseOrderSerializer(purchase_orders, many=True)
            return Response({
                'success': True,
                'message': 'Purchase Orders fetched successfully',
                'data': serializer.data
            })

    elif request.method == 'POST':
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            purchase_order = serializer.save()
            return Response({
                'success': True,
                'message': 'Purchase Order added successfully',
                'data': PurchaseOrderSerializer(purchase_order).data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'message': 'Error occurred while adding Purchase Order',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        try:
            purchase_order = PurchaseOrder.objects.get(id=po_id)
        except PurchaseOrder.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Purchase Order not found',
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = PurchaseOrderSerializer(instance=purchase_order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Purchase Order updated successfully',
                'data': PurchaseOrderSerializer(purchase_order).data
            })
        else:
            return Response({
                'success': False,
                'message': 'Error occurred while updating Purchase Order',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            purchase_order = PurchaseOrder.objects.get(id=po_id)
            purchase_order.delete()
            return Response({
                'success': True,
                'message': 'Purchase Order deleted successfully'
            })
        except PurchaseOrder.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Purchase Order not found',
            }, status=status.HTTP_404_NOT_FOUND)
            
            
# 3. Historical Performance Model

@api_view(['POST'])
def update_vendor_performance_metrics(request,id):
    vendorId = get_object_or_404(Vendor, id=id)

    # On-Time Delivery Rate
    completed_pos = PurchaseOrder.objects.filter(vendor=id, status='completed')
    total_completed_pos = completed_pos.count()
    on_time_deliveries = PurchaseOrder.objects.filter(id=id,status='completed',delivery_date__lte=tz.now()).count()
    on_time_delivery_rate = on_time_deliveries / total_completed_pos if total_completed_pos > 0 else 0


    # # Quality Rating Average
    quality_rating_avg = completed_pos.exclude(quality_rating__isnull=True).aggregate(avg_rating=Avg('quality_rating'))['avg_rating'] or 0

    # Average Response Time
    response_times = completed_pos.filter(acknowledgment_date__isnull=False).annotate(response_time=F('acknowledgment_date') - F('issue_date')).aggregate(avg_response_time=Avg('response_time'))['avg_response_time']
    average_response_time = response_times.total_seconds() if response_times else 0

    # Fulfilment Rate
    successful_fulfillments = completed_pos.filter(issue_date__lte=F('acknowledgment_date'))
    fulfillment_rate = successful_fulfillments.count() / total_completed_pos if total_completed_pos > 0 else 0
    
    vendorPerformanceMetrics = HistoricalPerformance(vendor=vendorId,date=tz.now(),on_time_delivery_rate=on_time_delivery_rate,quality_rating_avg=quality_rating_avg,average_response_time=average_response_time,fulfillment_rate=fulfillment_rate)
    vendorPerformanceMetrics.save()
    
    return Response({
                'success': True,
                'message': 'vendorPerformanceMetrics added successfully',
            }, status=status.HTTP_201_CREATED)
    
    
@api_view(['GET'])
def show_vendor_performance(request, id):
    vendor_list = HistoricalPerformance.objects.filter(id=id).values()

    alldata = []

    for vendor in vendor_list:
        user_info = {
            'id': vendor['id'],
            'vendor': vendor['vendor_id'],
            'date': vendor['date'],
            'on_time_delivery_rate': vendor['on_time_delivery_rate'],
            'quality_rating_avg': vendor['quality_rating_avg'],
            'average_response_time': vendor['average_response_time'],
            'fulfillment_rate': vendor['fulfillment_rate'],
        }
        alldata.append(user_info)

    return Response({"data": alldata, "message": "SUCCESS", "status": 200}, status=200)
