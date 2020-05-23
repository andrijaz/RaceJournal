from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permision to only allow owners of an object to edit it
    """
    # Korisno kad se dodaju korisnici i njihovi objekti(trofeji, rekordi, itd)
    # https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/
    pass
