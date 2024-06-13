from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = "news"

urlpatterns = [
    path("yangiliklar/", login_required(views.NewsList.as_view()), name="news-list"),
    path("yangiliklar/create/", login_required(views.NewsCreate.as_view()), name="news-create"),
    path("yangiliklar/update/<int:pk>/", login_required(views.NewsUpdate.as_view()), name="news-update"),
    path("yangiliklar/delete/<int:pk>/", login_required(views.NewsDelete.as_view()), name="news-delete"),
    path(
        "yangiliklar/image/delete/<int:pk>/",
        login_required(views.PhotoGallaeryImageDeleteView.as_view()),
        name="photo-image-delete",
    ),
    path("maqsadlar/", login_required(views.ObjectiveList.as_view()), name="objective-list"),
    path("maqsadlar/create/", login_required(views.ObjectiveCreate.as_view()), name="objective-create"),
    path("maqsadlar/update/<int:pk>/", login_required(views.ObjectiveUpdate.as_view()), name="objective-update"),
    path("maqsadlar/delete/<int:pk>/", login_required(views.ObjectiveDelete.as_view()), name="objective-delete"),


    path("category/", login_required(views.NewsCategoryList.as_view()), name="category-list"),
    path("category/create/", login_required(views.NewsCategoryCreate.as_view()), name="category-create"),
    path("category/update/<int:pk>/", login_required(views.NewsCategoryUpdate.as_view()), name="category-update"),
    path("category/delete/<int:pk>/", login_required(views.NewsCategoryDelete.as_view()), name="category-delete"),
    path("hashtag/", login_required(views.NewsHashtagList.as_view()), name="hashtag-list"),
    path("hashtag/create/", login_required(views.NewsHashtagCreate.as_view()), name="hashtag-create"),
    path("hashtag/update/<int:pk>/", login_required(views.NewsHashtagUpdate.as_view()), name="hashtag-update"),
    path("hashtag/delete/<int:pk>/", login_required(views.NewsHashtagDelete.as_view()), name="hashtag-delete"),
    # path('elonlar/', login_required(views.ElonlarList.as_view()), name='elonlar-list'),
    # path('elonlar/create/', login_required(views.ElonlarCreate.as_view()), name='elonlar-create'),
    # path('elonlar/update/<int:pk>/', login_required(views.ElonlarUpdate.as_view()), name='elonlar-update'),
    # path('elonlar/delete/<int:pk>/', login_required(views.ElonlarDelete.as_view()), name='elonlar-delete'),
    path("faq/", login_required(views.FAQList.as_view()), name="faq-list"),
    path("faq/create/", login_required(views.FAQCreate.as_view()), name="faq-create"),
    path("faq/update/<int:pk>/", login_required(views.FAQUpdate.as_view()), name="faq-update"),
    path("faq/delete/<int:pk>/", login_required(views.FAQDelete.as_view()), name="faq-delete"),
]
