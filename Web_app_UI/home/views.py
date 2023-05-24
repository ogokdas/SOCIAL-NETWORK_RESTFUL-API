import django
from django.shortcuts import render, redirect
import requests
from django.middleware.csrf import CsrfViewMiddleware


def home(request):
    session_id = request.session.get('session_id', '')
    csrftoken = django.middleware.csrf.get_token(request)

    if not session_id:
        return redirect('login')

    headers = {
        "Cookie": f"sessionid={session_id}; csrftoken={csrftoken}",
        "X-CSRFToken": csrftoken,
        "Content-Type": "application/json"
    }

    query = request.POST.get('profile_s', '')
    like = request.POST.get('like')
    post_id = request.POST.get('post_id')

    context = {"like": like, "post_id": post_id, "profile_s": query}

    url = "http://127.0.0.1:8001/api/home"
    response = requests.post(url, headers=headers, json=context)

    data_post = {}
    if response.status_code == 200:
        data_ = response.json()
        profile_results = data_['data']['profile_results']
        user_results = data_['data']['user_results']
        data_post = {"profile_results": profile_results, "user_results": user_results}

    url = "http://127.0.0.1:8001/api/home"
    response = requests.get(url, headers=headers)

    data_get = {}
    if response.status_code == 200:
        data = response.json()
        kategoriler = data['data']['kategoriler']
        category_counts = data['data']['category_counts']
        post = data['data']['post']
        user_profile = data['data']['user_profile']
        likedPost = data['data']['likedPost']
        profiles_ = data['data']['profiles_']
        users = data['data']['users']
        request_user = data['data']['request_user']

        data_get = {"kategoriler": kategoriler, "post": post, "category_counts": category_counts,
                    "user_profile": user_profile,
                    "likedPost": likedPost, "profiles_": profiles_, "users": users, "request_user": request_user}

    return render(request, "index.html", {**data_get, **data_post})