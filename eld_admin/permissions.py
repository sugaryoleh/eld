from django.contrib.auth.models import User, Group
from rest_framework.permissions import BasePermission


class IsDriver(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Drivers')


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Managers')


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Admins')


class IsStuff(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Managers') or request.user.groups.filter(name='Admins')

