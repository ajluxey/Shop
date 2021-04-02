from django.shortcuts import redirect


def redirect_to_shop(request):
    return redirect('catalog', permanent=True)