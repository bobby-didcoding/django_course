from django.conf import settings

def project_context(request):
    return {
        "installed_apps": settings.INSTALLED_APPS,
    }