from django.shortcuts import render
from django.utils.timezone import now
from django.views import View

from admin_panel.model import ministry as about
from admin_panel.model import press_service as press
from admin_panel.model import event
from admin_panel.model import activity


class Index(View):
    def get(self, request):
        event_count = event.Event.objects.count()
        # library_count = activity.Library.objects.count()
        # activity_count = activity.Activity.objects.count()
        news_count = press.News.objects.count()
        photo_gallery_count = press.PhotoGallery.objects.count()
        video_gallery_count = press.VideoGallery.objects.count()
        media_count = photo_gallery_count + video_gallery_count
        staff_count = about.Staff.objects.count()
        job_count = activity.Job.objects.count()
        department_count = about.Department.objects.count()

        latest_news = press.News.objects.all().filter(is_published=True).order_by("-publish_date")[:5]
        popular_news = press.News.objects.filter(is_published=True).order_by("-views")[:5]
        latest_events = event.Event.objects.all().filter(is_published=True).order_by("-start_time")[:5]

        context = {
            "event_count": event_count,
            "news_count": news_count,
            "media_count": media_count,
            "staff_count": staff_count,
            "department_count": department_count,
            "job_count": job_count,
            # 'library_count': library_count,
            # 'activity_count': activity_count,
            "latest_events": latest_events,
            "latest_news": latest_news,
            "popular_news": popular_news,
            "now": now(),
        }
        return render(request, "back/index.html", context)
