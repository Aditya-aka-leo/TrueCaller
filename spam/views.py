from django.shortcuts import render
import json
from django.http import JsonResponse
from spam.models import *


def update_spam_likelihood(req):
    """
    View function to update the spam likelihood of a user in the global contacts list.

    Args:
        req (HttpRequest): The HTTP request object containing JSON data with user's number and spam likelihood.

    Returns:
        JsonResponse: JSON response containing success or error message.
    """
    try:
        data = json.loads(req.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data provided"}, status=400)
    
    number = data.get('number')
    spam_likelihood = data.get('spam_likelihood')
    
    try:
        contacts = Global_Contacts.objects.filter(phone_number=number)
        if contacts.exists():
            for contact in contacts:
                contact.spam_likelihood = spam_likelihood
                contact.save()
            return JsonResponse({"message": "Spam Likelihood Updated"}, status=202)
        else:
            return JsonResponse({"error": "User not found"}, status=404)
    except Global_Contacts.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def create_user_global_list(req):
    """
    View function to create a user entry in the global contacts list.

    Args:
        req (HttpRequest): The HTTP request object containing JSON data with user's name, number, email, and spam likelihood.

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
    spam_likelihood = data.get('spam_likelihood', False)
    
    try:
        user_params = {
            'name': name,
            'phone_number': number,
            'spam_likelihood': spam_likelihood
        }
        if email:
            user_params['email'] = email
        
        Global_Contacts.objects.create(**user_params)
        
        return JsonResponse({"message": "User Entered Into Global Db"}, status=202)
       
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
