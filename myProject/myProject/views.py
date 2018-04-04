from django.http import HttpResponse


# ========================================================================================
# For rendering the page
def redirect(request):
    html = "<html><script>window.location.href = 'http://127.0.0.1:8000/foodApp/';</script></html>"
    return HttpResponse(html)
