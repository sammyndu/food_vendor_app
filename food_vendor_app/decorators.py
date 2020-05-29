from rest_framework import permissions
# from rest_framework.exceptions import APIException
# from order.models import Order
# from notification.models import Notification
# from django.http import HttpResponseBadRequest, HttpResponseForbidden, Http404
# from rest_framework import status

class CustomerPermission(permissions.BasePermission):
    """
    Global permission check for blacklisted IPs.
    """

    def has_permission(self, request, view):
        return request.user.is_customer

class VendorPermission(permissions.BasePermission):
    """
    Global permission check for blacklisted IPs.
    """

    def has_permission(self, request, view):
        return request.user.is_vendor


# company_id = view.kwargs.get('company_id')

# class SubmitNotificationPermission(permissions.BasePermission):
#     """
#     Global permission check for blacklisted IPs.
#     """

#     def has_permission(self, request, view):

#         user = request.user
#         try:
#             order = Order.objects.get(pk=request.data['order_id'])
#         except Order.DoesNotExist:
#             return False

#         vendor_id = order.vendor_id
#         customer_id = order.customer_id

#         if user.id != vendor_id and user.id != customer_id:
#             return False

#         return True

# class GetNotificationPermission(permissions.BasePermission):
#     """
#     Global permission check for blacklisted IPs.
#     """

#     def has_permission(self, request, view):

#         notification_id = view.kwargs.get('pk')


#         user = request.user
#         try:
#             notification = Notification.objects.get(pk=notification_id)
#         except Notification.DoesNotExist:
#             return False

#         try:
#             order = Order.objects.get(pk=notification.order_id)
#         except Order.DoesNotExist:
#             return False

#         vendor_id = order.vendor_id
#         customer_id = order.customer_id

#         vendor_id = order.vendor_id
#         customer_id = order.customer_id

#         if user.id != vendor_id and user.id != customer_id:
#             return False

#         return True


