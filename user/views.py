from django.shortcuts import render, redirect
from django.contrib.auth import login
from core.api import FT_API
from django.conf import settings
from .models import User
from core.models import Campus, Cursus
# Create your views here.


def intra_login(request):
    if request.GET.get('code'):
        api = FT_API(api_uid=settings.FT_AUTH_API_UID,
                     api_secret=settings.FT_AUTH_API_SECRET,
                     grant_type='authorization_code',
                     redirect_uri=settings.FT_AUTH_REDIRECT_URI,
                     code=request.GET.get('code'))
        me = api.get_me()
        user, created = User.objects.update_or_create(
            ft_id=me['id'], defaults={'username': me['login'], 'email': me['email']})
        if created:
            cursus_list = []
            campus_list = []
            for campus_data in me['campus']:
                campus_obj, campus_created = Campus.objects.get_or_create(
                    ft_id=campus_data['id'])
                if campus_created:
                    campus_obj.name = campus_data['name']
                    campus_obj.country = campus_data['country']
                    campus_obj.city = campus_data['city']
                    campus_obj.save()
                campus_list.append(campus_obj)
            for cursus in me['cursus_users']:
                cursus_data = cursus['cursus']
                cursus_obj, cursus_created = Cursus.objects.get_or_create(
                    ft_id=cursus_data['id'])
                if cursus_created:
                    cursus_obj.name = cursus_data['name']
                    cursus_obj.slug = cursus_data['slug']
                    cursus_obj.ft_created_at = api.parse_date(
                        cursus_data['created_at'])
                    cursus_obj.save()
                cursus_list.append(cursus_obj)
            user.campus.set(campus_list)
            user.cursus.set(cursus_list)
            user.save()
        login(request, user)
    return None
