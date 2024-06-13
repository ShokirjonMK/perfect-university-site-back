from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView
from admin_panel.app import views as custom
from admin_panel.model import contact
from . import forms


class HasRoleMixin:
    pass


class ContactList(HasRoleMixin, ListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = contact.Contact
    template_name = "back/contact/contact_list.html"
    queryset = model.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ContactList, self).get_context_data(object_list=object_list)
        objects = self.queryset

        q = self.request.GET.get("q")
        if q:
            objects = self.model.objects.filter(title__icontains=q)

        page = self.request.GET.get("page", 1)
        paginator = Paginator(objects, 12)

        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)

        context["objects"] = objects

        return context


class ContactUpdate(HasRoleMixin, UpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = contact.Contact
    template_name = "back/contact/contact_update.html"
    form_class = forms.ContactForm
    success_url = reverse_lazy("contact:contact-list")

    def get(self, request, pk):
        context = {
            "contact": self.model.objects.get(id=self.kwargs["pk"]),
            "status": contact.STATUS,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        contact = self.model.objects.get(id=self.kwargs["pk"])
        contact.status = self.request.POST.get("status")
        contact.save()
        return HttpResponseRedirect(self.success_url)


class ContactDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = contact.Contact
    success_url = reverse_lazy("contact:contact-list")
