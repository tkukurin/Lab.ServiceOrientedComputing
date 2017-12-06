from django.contrib.auth.models import User
from rest_framework import permissions
from .models import Tweet

class IsOwner(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    return obj.owner == request.user

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
      if request.method in permissions.SAFE_METHODS:
        return True
      if isinstance(obj, User):
        return obj == request.user
      return obj.owner == request.user
