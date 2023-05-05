from shared.permissions.app import AppBasePermission


class APIPermission(AppBasePermission):
    def has_permission(self, request, view):
        return self.is_auth(request)

    def has_object_permission(self, request, view, obj):
        return super(APIPermission, self).has_object_permission(request, view, obj)
