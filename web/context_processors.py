from django.conf import settings

def settings_context_processor(request):
    return {"PROJECT_NAME": settings.PROJECT_NAME,
            "SHORT_PROJECT_NAME": settings.SHORT_PROJECT_NAME}
