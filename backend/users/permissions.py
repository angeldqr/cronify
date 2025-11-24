from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Permiso personalizado para verificar si el usuario es administrador.
    Solo permite acceso a usuarios autenticados con is_admin=True.
    """
    
    def has_permission(self, request, view):
        # Verificar que el usuario esté autenticado y sea admin
        return (
            request.user 
            and request.user.is_authenticated 
            and getattr(request.user, 'is_admin', False)
        )
    
    message = 'No tienes permisos de administrador para realizar esta acción.'


class IsAdminOrReadOnly(BasePermission):
    """
    Permiso que permite lectura a cualquier usuario autenticado,
    pero solo admins pueden modificar (POST, PUT, PATCH, DELETE).
    """
    
    def has_permission(self, request, view):
        # Permitir lectura a usuarios autenticados
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return request.user and request.user.is_authenticated
        
        # Solo admins pueden modificar
        return (
            request.user 
            and request.user.is_authenticated 
            and getattr(request.user, 'is_admin', False)
        )
    
    message = 'Solo los administradores pueden realizar esta acción.'
