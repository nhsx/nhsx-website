from django import forms
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.rich_text import get_rich_text_editor_widget
from wagtail.images.widgets import AdminImageChooser

from ..service import _user_profiles, _users, _authors


image_widget = AdminImageChooser(
    choose_one_text=_('Choose a photo'),
    choose_another_text=_('Choose a different photo')
)


class AuthorForm(forms.ModelForm):

    """
        Form used by admins to register a new author with profile
    """

    class Meta:
        model = _user_profiles.__model__
        # fields = ('first_name', 'last_name')
        exclude = ('user', )

    email = forms.EmailField(required=False, label=_('Email'))
    first_name = forms.CharField(required=True, label=_('First Name'))
    last_name = forms.CharField(required=True, label=_('Last Name'))

    field_order = ['email', 'first_name', 'last_name']

    def clean_email(self):

        email = self.cleaned_data['email']

        users_query = _users.find(**{'email': email})
        if self.instance.user is not None:
            users_query = users_query.exclude(pk=self.instance.user.pk)
        if users_query.exists():
            self.add_error('email', forms.ValidationError(
                _("A user with that username already exists."),
                code='duplicate_username',
            ))

        if email is None or email == '':
            count = _authors.count()
            email = f"dummy-email-{count}@example.net"
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo'].widget = image_widget
        self.fields['bio'].widget = get_rich_text_editor_widget('default')
        self.fields['short_bio'].widget = get_rich_text_editor_widget('default')
