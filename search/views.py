from django.http import JsonResponse
from spam.models import *
from registration.models import *
from django.contrib.auth.models import User
import json

def search(req):
    """
    View function to handle search functionality based on name or number.

    Args:
        req (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: JSON response containing search results or error message.
    """
    if req.method != 'GET':
        return JsonResponse({"error": "Only GET method is supported"}, status=405)

    name = req.GET.get('name')
    number = req.GET.get('number')

    if not name and not number:
        return JsonResponse({"error": "Name or number not provided"}, status=400)

    data_list = []

    try:
        if name:
            # Search by name
            name_query = name.lower()
            contacts_starting_with_query = Contact.objects.filter(name__istartswith=name_query)
            for contact in contacts_starting_with_query:
                user = User.objects.filter(username=contact.phone_number).first()
                contact_info = {
                    "name": contact.name,
                    "phone_number": contact.phone_number,
                    "spam_likelihood": contact.spam_likelihood
                }
                if user:
                    contact_info['email'] = contact.email
                data_list.append(contact_info)

            global_contacts_starting_with_query = Global_Contacts.objects.filter(name__istartswith=name_query)
            for contact in global_contacts_starting_with_query:
                user = User.objects.filter(username=contact.phone_number).first()
                contact_info = {
                    "name": contact.name,
                    "phone_number": contact.phone_number,
                    "spam_likelihood": contact.spam_likelihood
                }
                if user:
                    contact_info['email'] = contact.email
                data_list.append(contact_info)

            global_contacts_containing_query = Global_Contacts.objects.filter(name__icontains=name_query).exclude(name__istartswith=name_query)
            for contact in global_contacts_containing_query:
                user = User.objects.filter(username=contact.phone_number).first()
                contact_info = {
                    "name": contact.name,
                    "phone_number": contact.phone_number,
                    "spam_likelihood": contact.spam_likelihood
                }
                if user:
                    contact_info['email'] = contact.email
                data_list.append(contact_info)

        if number:
            # Search by number
            contacts_query = Contact.objects.filter(phone_number=number)
            for contact in contacts_query:
                user = User.objects.filter(username=contact.phone_number).first()
                contact_info = {
                    "name": contact.name,
                    "phone_number": contact.phone_number,
                    "spam_likelihood": contact.spam_likelihood
                }
                if user:
                    contact_info['email'] = contact.email
                data_list.append(contact_info)
            if(data_list != []):
                return JsonResponse({"data": data_list})
            global_contacts_query = Global_Contacts.objects.filter(phone_number=number)
            for contact in global_contacts_query:
                user = User.objects.filter(username=contact.phone_number).first()
                contact_info = {
                    "name": contact.name,
                    "phone_number": contact.phone_number,
                    "spam_likelihood": contact.spam_likelihood
                }
                if user:
                    contact_info['email'] = contact.email
                data_list.append(contact_info)

        return JsonResponse({"data": data_list})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
