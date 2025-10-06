from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado para permitir que solo los dueños de un objeto
    puedan editarlo. Los demás solo podrán leerlo.
    """

    def has_object_permission(self, request, view, obj):
        # Los permisos de lectura (GET, HEAD, OPTIONS) se permiten a cualquier solicitud.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Los permisos de escritura (PUT, PATCH, DELETE) solo se permiten
        # si el usuario que hace la petición es el mismo que el creador del evento.
        # Esto aplica al 'obj' que es la instancia del Evento.
        return obj.creador == request.user

