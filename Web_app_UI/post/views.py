import base64
import json
import django
import requests
from django.http import HttpResponse
from django.middleware.csrf import CsrfViewMiddleware
from django.shortcuts import redirect, render


# Create your views here.


def post_request(request):
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
        url = "http://127.0.0.1:8001/api/posts"

        response = requests.get(url, headers=headers)
        data = response.json()
        category = data['data']['category']
        user_profile = data['data']['user_profile']
        request_user = data['data']['request_user']
        data = {"category": category, "user_profile": user_profile, "request_user": request_user}
        return render(request, "post.html", data)

    if request.method == "POST":
        if request.FILES.get('image') is not None:
            image = request.FILES.get('image')
            image_data = image.read()
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            caption = request.POST['Title']
            content = request.POST['message']
            category = request.POST.getlist('select[]')

            url = "http://127.0.0.1:8001/api/posts"

            data = {
                "Title": caption,
                "message": content,
                "select[]": category,
                "image": image_base64
            }
            response = requests.post(url, data=json.dumps(data), headers=headers)

            if response.status_code == 201:
                return redirect('home')
            elif response.status_code == 400:
                return render(request, "post.html", {"error": response.text.strip("{}")})

        elif request.FILES.get('image') is None:
            caption = request.POST['Title']
            content = request.POST['message']
            category = request.POST.getlist('select[]')

            url = "http://127.0.0.1:8001/api/posts"

            data = {
                "Title": caption,
                "message": content,
                "select[]": category,
            }
            response = requests.post(url, data=json.dumps(data), headers=headers)

            if response.status_code == 201:
                return redirect('home')
            elif response.status_code == 400:
                return render(request, "post.html", {"error": response.text.strip("{}")})

    return render(request, "post.html")


def post_details(request, slug):

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
        url = f"http://127.0.0.1:8001/api/posts/{slug}"

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            post = data['data']['post']
            profile_s = data['data']['profile_s']
            profile_user = data['data']['profile_user']
            user = data['data']['user']
            data = {"post": post, "profile_s": profile_s, "profile_user": profile_user, "user": user }
            return render(request, "details.html", data)
        else:
            return redirect('home')

    if request.method == "POST":
        is_delete = request.POST.get("delete")
        if is_delete:
            url = f"http://127.0.0.1:8001/api/posts/{slug}:delete"
            response = requests.delete(url, headers=headers)
            if response.status_code == 200:
                return redirect('home')
            else:
                error_message = f"Hata kodu: {response.status_code}"
                return HttpResponse(error_message, status=response.status_code)

    return redirect('details', slug=slug)