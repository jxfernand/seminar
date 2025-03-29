import os
from django.conf import settings
from django.shortcuts import render
from django.shortcuts import redirect


def seminar_page(request):
    if not hasattr(settings, "STATIC_URL") or not settings.STATIC_URL:
        return render(request, 'seminar/seminar_page.html', {'css_files': [], 'js_files': []}, {"google_maps_api_key": settings.GOOGLE_MAPS_API_KEY})

    static_dir = settings.STATIC_URL[0]  # This might be empty

    css_path = os.path.join(static_dir, 'css')
    js_path = os.path.join(static_dir, 'js')

    css_files = [f"css/{file}" for file in os.listdir(css_path)] if os.path.exists(css_path) else []
    js_files = [f"js/{file}" for file in os.listdir(js_path)] if os.path.exists(js_path) else []

    return render(request, 'seminar/seminar_page.html', {'css_files': css_files, 'js_files': js_files})