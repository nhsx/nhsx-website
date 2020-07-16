from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView
from django.utils.crypto import get_random_string
from django.shortcuts import redirect, reverse
from django.http import Http404
from django.utils.translation import ugettext_lazy as _

from .forms import AuthorForm
from ..service import _authors, _user_profiles

_template_prefix = "authors/admin/"


####################################################################################################
# Authors
####################################################################################################


class AuthorBaseView(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "add_link": "authors_admin:create",
                "add_text": "Create new author",
                "title": "Authors",
            }
        )
        return context


class AuthorIndexView(AuthorBaseView, ListView):
    template_name = "{}index.html".format(_template_prefix)
    paginate_by = 20
    context_object_name = "objects"
    page_kwarg = "p"

    def get_queryset(self):
        return _authors.all()


class AuthorCreateView(AuthorBaseView, CreateView):
    template_name = "{}form.html".format(_template_prefix)
    form_class = AuthorForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"title": "Adding new author account"})
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        self.object = _authors.create(password=get_random_string(), **data)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse("authors_admin:index")


class AuthorUpdateView(AuthorBaseView, UpdateView):
    model = _user_profiles.__model__
    template_name = "{}form.html".format(_template_prefix)
    form_class = AuthorForm
    user_fields = ["first_name", "last_name", "email"]

    def form_valid(self, form):
        data = form.cleaned_data

        user = form.instance.user
        for field in self.user_fields:
            setattr(user, field, data[field])
        user.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("authors_admin:index")

    def get_object(self):
        queryset = self.get_queryset()
        slug = self.kwargs.get(self.slug_url_kwarg)
        if slug is not None:
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{"user__{}".format(slug_field): slug})
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(
                _("No results found matching the query")
                % {"verbose_name": queryset.model._meta.verbose_name}
            )
        return obj

    def get_initial(self):
        initial = super().get_initial()
        user = self.object.user
        for field in self.user_fields:
            initial.update({field: getattr(user, field)})

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"title": "Editing author account"})
        return context
