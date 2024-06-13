from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, UpdateView

# from rolepermissions.mixins import HasRoleMixin

from . import forms
from admin_panel.model.event import Event, EventsHashtag
from admin_panel.app import views as custom


class HasRoleMixin:
    pass


class EventCreate(HasRoleMixin, CreateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Event
    form_class = forms.EventForm
    template_name = "back/event/event_create.html"
    success_url = reverse_lazy("event:event-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EventCreate, self).get_context_data(object_list=object_list, **kwargs)
        context["event_hashtags"] = EventsHashtag.objects.all()
        # if not self.request.user.is_superuser:
        #     context['staff'] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        hashtags = request.POST.getlist("hashtag")
        del data["csrfmiddlewaretoken"]

        if not data["start_time"]:
            del data["start_time"]
        if not data["end_time"]:
            del data["end_time"]
        if data.get("hashtag"):
            del data["hashtag"]

        if data.get("is_published") == "on":
            data["is_published"] = True
        else:
            data["is_published"] = False

        if data.get("main_page") == "on":
            data["main_page"] = True
        else:
            data["main_page"] = False

        # data['region'] = Region.objects.get(id=int(data['region']))

        event = self.model.objects.create(**data)

        # image = request.FILES.get('image')
        # if image:
        #     event.image = image
        if request.LANGUAGE_CODE == "en":
            for hashtag in hashtags:
                if EventsHashtag.objects.filter(title_en=hashtag).exists():
                    tag = EventsHashtag.objects.get(title_en=hashtag)
                else:
                    tag = EventsHashtag.objects.create(title_en=hashtag)
                if tag not in event.hashtag.all():
                    event.hashtag.add(tag.id)

        elif request.LANGUAGE_CODE == "ru":
            for hashtag in hashtags:
                if EventsHashtag.objects.filter(title_ru=hashtag).exists():
                    tag = EventsHashtag.objects.get(title_ru=hashtag)
                else:
                    tag = EventsHashtag.objects.create(title_ru=hashtag)
                if tag not in event.hashtag.all():
                    event.hashtag.add(tag.id)

        elif request.LANGUAGE_CODE == "uz":
            for hashtag in hashtags:
                if EventsHashtag.objects.filter(title_uz=hashtag).exists():
                    tag = EventsHashtag.objects.get(title_uz=hashtag)
                else:
                    tag = EventsHashtag.objects.create(title_uz=hashtag)
                if tag not in event.hashtag.all():
                    event.hashtag.add(tag.id)
        event.save()

        return HttpResponseRedirect(self.success_url)


class EventList(HasRoleMixin, custom.CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Event
    template_name = "back/event/event_list.html"
    queryset = model.objects.all()


class EventUpdate(HasRoleMixin, UpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Event
    form_class = forms.EventForm
    context_object_name = "event"
    template_name = "back/event/event_update.html"
    success_url = reverse_lazy("event:event-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EventUpdate, self).get_context_data(object_list=object_list, **kwargs)
        context["event_hashtags"] = EventsHashtag.objects.all()
        # if not self.request.user.is_superuser:
        #     context['staff'] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        event = Event.objects.get(id=self.kwargs["pk"])
        hashtags = request.POST.getlist("hashtag")

        if not data["start_time"]:
            del data["start_time"]
        if not data["end_time"]:
            del data["end_time"]

        if data.get("is_published") == "on":
            event.is_published = True
        else:
            event.is_published = False

        if data.get("main_page") == "on":
            event.main_page = True
        else:
            event.main_page = False

        # data['region'] = Region.objects.get(id=int(data['region']))

        event.title_uz = data.get("title_uz")
        event.title_ru = data.get("title_ru")
        event.title_en = data.get("title_en")

        event.description_uz = data.get("description_uz")
        event.description_ru = data.get("description_ru")
        event.description_en = data.get("description_en")

        # event.address_uz = data.get('address_uz')
        # event.address_ru = data.get('address_ru')
        # event.address_en = data.get('address_en')

        # event.event_place_uz = data.get('event_place_uz')
        # event.event_place_ru = data.get('event_place_ru')
        # event.event_place_en = data.get('event_place_en')

        # event.link = data.get('link')
        # event.region = data.get('region')

        if not data["start_time"]:
            event.start_time = timezone.now()
        else:
            event.start_time = data.get("start_time")
        # event.end_time = data.get('start_time')

        if not data["end_time"]:
            event.end_time = timezone.now()
        else:
            event.end_time = data.get("end_time")
        # event.end_time = data.get('end_times')

        # image = request.FILES.get('image')
        # if image:
        #     event.image = image

        for i in event.hashtag.all():
            event.hashtag.remove(i)

        if request.LANGUAGE_CODE == "en":
            for hashtag in hashtags:
                if EventsHashtag.objects.filter(title_en=hashtag).exists():
                    tag = EventsHashtag.objects.get(title_en=hashtag)
                else:
                    tag = EventsHashtag.objects.create(title_en=hashtag)
                if tag not in event.hashtag.all():
                    event.hashtag.add(tag.id)

        elif request.LANGUAGE_CODE == "ru":
            for hashtag in hashtags:
                if EventsHashtag.objects.filter(title_ru=hashtag).exists():
                    tag = EventsHashtag.objects.get(title_ru=hashtag)
                else:
                    tag = EventsHashtag.objects.create(title_ru=hashtag)
                if tag not in event.hashtag.all():
                    event.hashtag.add(tag.id)

        elif request.LANGUAGE_CODE == "uz":
            for hashtag in hashtags:
                if EventsHashtag.objects.filter(title_uz=hashtag).exists():
                    tag = EventsHashtag.objects.get(title_uz=hashtag)
                else:
                    tag = EventsHashtag.objects.create(title_uz=hashtag)
                if tag not in event.hashtag.all():
                    event.hashtag.add(tag.id)

        event.save()

        return HttpResponseRedirect(self.success_url)


class EventDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Event
    success_url = reverse_lazy("event:event-list")


class EventsHashtagCreate(custom.CustomCreateView):
    model = EventsHashtag
    form_class = forms.EventHashtagForm
    template_name = "back/event/events_hashtag_create.html"
    success_url = reverse_lazy("event:hashtag-list")


class EventsHashtagUpdate(UpdateView):
    model = EventsHashtag
    form_class = forms.EventHashtagForm
    context_object_name = "object"
    template_name = "back/event/events_hashtag_update.html"
    success_url = reverse_lazy("event:hashtag-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        obj = self.model.objects.get(id=self.kwargs["pk"])

        obj.title_uz = data["title_uz"]
        obj.title_ru = data["title_ru"]
        obj.title_en = data["title_en"]

        obj.save()
        return HttpResponseRedirect(self.success_url)


class EventsHashtagList(custom.CustomListView):
    model = EventsHashtag
    template_name = "back/event/events_hashtag_list.html"
    queryset = model.objects.all()


class EventsHashtagDelete(custom.CustomDeleteView):
    model = EventsHashtag
    success_url = reverse_lazy("event:hashtag-list")
