from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    message = 'Este usuario no tiene permiso para realizar esta acción.'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True

        if request.user.type == 0:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        return False


class IsTeacherOrIsStudent(permissions.BasePermission):
    message = 'Para realizar esta acción el usuario debe ser Docente o Estudiante.'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.type == 0:
            return True

        if request.user.type == 1:
            return True

        if request.user.type == 2:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        return False


class IsTeacher(permissions.BasePermission):
    message = 'No tiene los suficientes permisos para realizar esta acción.'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

        return False

    def has_object_permission(self, request, view, obj):

        if request.user.type == 0:
            return True

        if request.user.type == 1:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        return False


class IsOwnerAndTeacher(permissions.BasePermission):
    message = 'Este usuario no tiene permiso para realizar esta acción.'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if (obj.owner == request.user) and (request.user.type == 1):
            return True

        if request.user.type == 0:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        return False


class IsOwnerAndStudent(permissions.BasePermission):
    message = 'Este usuario no tiene permiso para realizar esta acción.'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if (obj.owner == request.user) and (request.user.type == 2):
            return True

        if request.user.type == 0:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        return False
