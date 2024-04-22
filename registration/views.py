import json
from django.shortcuts import render
from django.db import IntegrityError
from django.http import JsonResponse
from django.core.serializers import serialize
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from matplotlib import use
from django.contrib.auth import authenticate, login
from registration.models import *


def register_user(req):
    """
    View function to handle user registration.

    Args:
        req (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: JSON response containing success or error message.
    """
    try:
        data = json.loads(req.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data provided"}, status=400)
    user_name = data.get('user_name')
    number = data.get('number')
    email = data.get('email')
    password = data.get('password')
    print(data)
    if user_name is None or number is None or len(number) < 10 or not number.isdigit() or not password:
        return JsonResponse({"error": "Invalid Number Or User Name"}, status=400)

    try:
        user_params = {
            'first_name': user_name,
            'username': number,
        }
        if email:
            user_params['email'] = email

        user = User.objects.create(**user_params)
        user.set_password(password)
        user.save()
        return JsonResponse({"message": "User Registered"}, status=201)
    except IntegrityError:
        return JsonResponse({"error": "User Already Exists"}, status=400)


def login_user(req):
    """
    View function to handle user login.

    Args:
        req (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: JSON response containing access token or error message.
    """
    try:
        data = json.loads(req.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data provided"}, status=400)
    user_name = data.get('user_name')
    password = data.get('password')
    user = authenticate(username=user_name, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return JsonResponse({"access_token": str(refresh.access_token), "refresh_token": str(refresh)})
    return JsonResponse({"error": "User Does Not Exist"}, status=400)


def contact_list_user(req):
    """
    View function to handle adding contacts to user's contact list.

    Args:
        req (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: JSON response containing success or error message.
    """
    
    try:
        data = json.loads(req.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data provided"}, status=400)
    name = data.get('name')
    number = data.get('number')
    email = data.get('email', None)

    try:
        user_params = {
            'name': name,
            'phone_number': number,
            'spam_likelihood': False,
        }
        if email:
            user_params['email'] = email
        contact = Contact(**user_params)
        contact.save()
        return JsonResponse({"message": "User Saved In Users Contact List"}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data provided"}, status=400)
