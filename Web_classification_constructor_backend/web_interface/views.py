from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .forms import Form1

# Create your views here.


@csrf_exempt
# @login_required
@require_http_methods(["GET", "POST"])
def post_form_1(request):
    form_1 = Form1(request.POST)
    field_1 = ""
    field_2 = ""
    field_3 = ""
    if form_1.is_valid():
        field_1 = form_1.cleaned_data["field_1"]
        field_2 = form_1.cleaned_data["field_2"]
        field_3 = form_1.cleaned_data["field_3"]
        response = {"form_1": form_1,
                    "data": {"field_1": field_1, "field_2": field_2, "field_3": field_3}}
        print(response["data"])
        return response
    response = {"form_1": form_1,
                "data": {"field_1": field_1, "field_2": field_2, "field_3": field_3}}
    print(response)
    return response


@csrf_exempt
# @login_required
@require_http_methods(["GET", "POST"])
def button_click_tracking(request):
    if "button exit" in request.POST.keys():
        return redirect("/logout")
    if "button send" in request.POST.keys():
        response = post_form_1(request)
        return render(request, "form_1.html", response)
    else:
        form_1 = Form1(request.POST)
        response = {"form_1": form_1,
                    "data": None}
        return render(request, "form_1.html", response)