
from django.db.models import Q
from dal_select2.views import Select2QuerySetView


class AuthorAutocomplete(Select2QuerySetView):

    def get_queryset(self):
        from modules.users.service import _authors, _users

        if not self.request.user.is_authenticated:
            return []

        if not self.request.user.has_perm('wagtailadmin.access_admin'):
            return []

        # Disabling this because sometimes a user will need to be added as an author before they
        # have been given the group permssions
        # qs = _authors.all()

        qs = _users.all()

        if self.q:
            if ' ' in self.q:
                full = self.q.split(' ')
                firstname = full[0]
                lastname = full[-1]
                qs = qs.filter(
                    first_name__istartswith=firstname, last_name__istartswith=lastname
                ).order_by('first_name')
            else:
                qs = qs.filter(
                    Q(first_name__istartswith=self.q) | Q(last_name__istartswith=self.q)
                ).order_by('first_name')

        return qs
