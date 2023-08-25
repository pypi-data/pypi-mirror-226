# pylint: disable=unused-argument
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsBudgetOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.has_access(request.user, request.method not in SAFE_METHODS)


class CanAccessBudgetShare(BasePermission):
    SHARED_USER_PERMISSIONS = SAFE_METHODS + ('DELETE',)

    def has_object_permission(self, request, view, obj):
        return (
            obj.user == request.user and request.method in self.SHARED_USER_PERMISSIONS
            or obj.budget.user == request.user
        )


class IsPayeeOwner(IsBudgetOwner):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.budget)


class IsPaymentOwner(IsBudgetOwner):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.payee.budget)
