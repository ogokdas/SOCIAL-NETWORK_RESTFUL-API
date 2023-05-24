import django
from django.shortcuts import render, redirect
import requests
from django.middleware.csrf import CsrfViewMiddleware


def categories(request, slug):
        session_id = request.session.get('session_id', None)
        csrftoken = django.middleware.csrf.get_token(request)

        if not session_id:
            return redirect('login')

        headers = {
            "Cookie": f"sessionid={session_id}; csrftoken={csrftoken}",
            "X-CSRFToken": csrftoken,
            "Content-Type": "application/json"
        }

        url = f"http://127.0.0.1:8001/api/categories/{slug}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            kategoriler = data['data']['kategoriler']
            posts = data['data']['posts']
            profile__ = data['data']['profile__']
            profile = data['data']['profile']
            count = data['data']['count']
            user = data['data']['user']

            context = {"kategoriler": kategoriler, "posts": posts, "profile__": profile__, "profile": profile, "count": count, "user": user, "request_user": user}
            return render(request, "category.html", context)
        else:
            return redirect('login')