import django
from django.contrib.sites import requests
from django.shortcuts import render, redirect
import requests
from django.middleware import csrf


# Create your views here.
def login_request(request):
    session_id = request.session.get('session_id', None)
    if session_id:
        return redirect('home')

    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        data = {'username': username, 'password': password}

        url = "http://127.0.0.1:8001/api/accounts/login/"
        response = requests.post(url, data=data)

        if response.status_code == 200:
            # Login success
            session_id = response.cookies["sessionid"]
            csrftoken = response.cookies["csrftoken"]

            request.session['session_id'] = session_id
            request.session['csrf_token'] = csrf.get_token(request)

            return redirect('home')
        else:
            # Login failed
            return render(request, "login.html", {"error": response.text.strip("{}")})

    return render(request, "login.html")


def logout_request(request):
    session_id = request.session.get('session_id', None)
    csrftoken = django.middleware.csrf.get_token(request)

    headers = {
        "Cookie": f"sessionid={session_id}; csrftoken={csrftoken}",
        "X-CSRFToken": csrftoken,
        "Content-Type": "application/json"
    }
    url = "http://127.0.0.1:8001/api/accounts/logout/"
    response = requests.post(url, headers=headers)

    if session_id:
        del request.session['session_id']
    return redirect('login')


def register_request(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        name = request.POST["name"]
        surname = request.POST["surname"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]

        data = {'username': username, 'password': password, 'email': email, 'name': name, 'surname': surname,
                'repassword': repassword}

        url = "http://127.0.0.1:8001/api/accounts/register/"
        response = requests.post(url, data=data)

        if response.status_code == 201:
            # Register success
            session_id = response.cookies["sessionid"]
            csrftoken = response.cookies["csrftoken"]

            request.session['session_id'] = session_id
            request.session['csrf_token'] = csrf.get_token(request)

            headers = {
                "Cookie": f"sessionid={session_id}; csrftoken={csrftoken}",
                "X-CSRFToken": csrftoken,
                "Content-Type": "application/json"
            }

            return redirect('settings')
        else:
            # Register failed
            return render(request, "register.html", {"error": response.text.strip("{}")})

    else:
        session_id = request.session.get('session_id', None)
        csrftoken = django.middleware.csrf.get_token(request)

        if session_id:

            headers = {
                "Cookie": f"sessionid={session_id}; csrftoken={csrftoken}",
                "X-CSRFToken": csrftoken,
                "Content-Type": "application/json"
            }

            url = "http://127.0.0.1:8001/api/accounts/register/"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                user_profile = data['data']['user_profile']
                request_user = data['data']['request_user']

                context = {"user_profile": user_profile, "request_user": request_user}
                return render(request, "register.html", context)

        else:
            return render(request, "register.html")