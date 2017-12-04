from rest_framework.permissions import BasePermission
from .models import Tweet

class IsOwner(BasePermission):
  """
  Class used to determine if user owns some requested object.
  See e.g. views.py for usage.
  """  
  def has_object_permission(self, request, view, obj):
    return obj.owner == request.user
