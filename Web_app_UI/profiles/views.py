import base64
import json
import django
from django.contrib.sites import requests
from django.shortcuts import render, redirect
import requests


# Create your views here.


def profile_request(request):
    session_id = request.session.get('session_id', '')
    csrftoken = django.middleware.csrf.get_token(request)

    if not session_id:
        return redirect('login')

    headers = {
        "Cookie": f"sessionid={session_id}; csrftoken={csrftoken}",
        "X-CSRFToken": csrftoken,
        "Content-Type": "application/json"
    }

    if request.method == "GET":
        url = "http://127.0.0.1:8001/api/profiles"

        response = requests.get(url, headers=headers)
        data_ = response.json()
        user_profile = data_['data']['user_profile']
        user_object = data_['data']['user_object']
        data = {"user_object": user_object, "user_profile": user_profile, "request_user":user_object }
        return render(request, "profile.html", data)


def profiledetail_request(request, slug):
    session_id = request.session.get('session_id', '')
    csrftoken = django.middleware.csrf.get_token(request)

    if not session_id:
        return redirect('login')

    headers = {
        "Cookie": f"sessionid={session_id}; csrftoken={csrftoken}",
        "X-CSRFToken": csrftoken,
        "Content-Type": "application/json"
    }

    if request.method == "GET":
        url = f"http://127.0.0.1:8001/api/profiles/{slug}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data_ = response.json()
            profiledetail = data_['context']['profiledetail']
            posts = data_['context']['posts']
            postliked = data_['context']['postliked']
            users = data_['context']['users']
            user_profile = data_['context']['user_profile']
            data = {"profiledetail": profiledetail, "posts": posts, "postliked": postliked, "users": users, "user_profile": user_profile, "request_user": user_profile}

            return render(request, "profile_detail.html", data)

        else:
            pass


def settings_request(request):
    session_id = request.session.get('session_id', '')
    csrftoken = django.middleware.csrf.get_token(request)

    if not session_id:
        return redirect('login')

    headers = {
        "Cookie": f"sessionid={session_id}; csrftoken={csrftoken}",
        "X-CSRFToken": csrftoken,
        "Content-Type": "application/json"
    }

    if request.method == "GET":
        url = f"http://127.0.0.1:8001/api/profiles:setting"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data_ = response.json()
            profile = data_['data']['profile']
            data = {"profile": profile}
            return render(request, "settings.html", data)
        else:
            pass

    if request.method == 'POST':
        if request.FILES.get('profileImage_name') is None:
            job = request.POST['job_name']
            location = request.POST['location_name']
            data = {"job_name": job, "location_name": location}

            url = f"http://127.0.0.1:8001/api/profiles:setting"
            response = requests.put(url, data=json.dumps(data), headers=headers)

            if response.status_code == 200:
                return redirect('profile')
            else:
                return redirect('settings')

        elif request.FILES.get('profileImage_name') is not None:
            image = request.FILES.get('profileImage_name')
            image_data = image.read()
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            job = request.POST['job_name']
            location = request.POST['location_name']
            data = {"profileImage_name": image_base64, "job_name": job, "location_name": location}

            url = f"http://127.0.0.1:8001/api/profiles:setting"
            response = requests.put(url, data=json.dumps(data), headers=headers)

            if response.status_code == 200:
                return redirect('profile')
            else:
                return redirect('settings')