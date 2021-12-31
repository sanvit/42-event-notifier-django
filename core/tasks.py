from config.celery import app as celery_app
from .models import *
from .api import FT_API
from django.conf import settings

EVENT_KEYS = ['ft_id', 'name', 'description', 'location', 'kind', 'max_people',
              'nbr_subscribers', 'begin_at', 'end_at', 'ft_created_at', 'ft_updated_at']
THEME_KEYS = ['ft_id', 'name', 'ft_created_at', 'ft_updated_at']


@celery_app.task
def run_periodic_checks():
    load_events.apply_async()


@celery_app.task
def load_events():
    ft_api = FT_API(api_uid=settings.FT_API_UID,
                    api_secret=settings.FT_API_SECRET)
    events = ft_api.get_events()
    for event in events:
        campus_list = []
        cursus_list = []
        theme_list = []
        for campus_id in event['campus_ids']:
            campus_obj, campus_created = Campus.objects.get_or_create(
                ft_id=campus_id)
            if campus_created:
                campus_data = ft_api.get_campus(campus_id)
                campus_obj.name = campus_data['name']
                campus_obj.country = campus_data['country']
                campus_obj.city = campus_data['city']
                campus_obj.save()
            campus_list.append(campus_obj)
        for cursus_id in event['cursus_ids']:
            cursus_obj, cursus_created = Cursus.objects.get_or_create(
                ft_id=cursus_id)
            if cursus_created:
                cursus_data = ft_api.get_cursus(cursus_id)
                cursus_obj.name = cursus_data['name']
                cursus_obj.slug = cursus_data['slug']
                cursus_obj.ft_created_at = ft_api.parse_date(
                    cursus_data['created_at'])
                cursus_obj.save()
            cursus_list.append(cursus_obj)
        for theme in event['themes']:
            theme.update({'ft_id': theme['id'], 'ft_created_at': ft_api.parse_date(
                event['created_at']), 'ft_updated_at': ft_api.parse_date(event['updated_at'])})
            theme_data = {key: theme.get(key) for key in THEME_KEYS}
            theme_obj, theme_created = Theme.objects.update_or_create(
                ft_id=theme['id'], defaults=theme_data)
            theme_list.append(theme_obj)
        event.update({'ft_id': event['id'], 'ft_created_at': ft_api.parse_date(event['created_at']), 'ft_updated_at': ft_api.parse_date(
            event['updated_at'])})
        event_data = {key: event.get(key) for key in EVENT_KEYS}
        event_obj, event_created = Event.objects.update_or_create(
            ft_id=event['id'], defaults=event_data)
        event_obj.campus.set(campus_list)
        event_obj.cursus.set(cursus_list)
        event_obj.theme.set(theme_list)
        if event_created:
            event_created_handler(event_obj.id)


@celery_app.task
def event_created_handler(event_id):
    event = Event.objects.get(id=event_id)
    pass
