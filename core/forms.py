from django import forms
from django.contrib.auth import authenticate, get_user_model, password_validation

class PasswordResetForm(forms.Form):
    serial_number = forms.CharField(max_length=255, label="serial_number", widget=forms.TextInput(attrs={'autocomplete': "serial_number"}))


    def get_users(self, serial_number):
        serial_number_field_name = UserModel.get_serial_number_field()
        active_users = UserModel._default_manager.filter(
            **{
                "%s__iexact" % serial_number_field_name: serial_number,
                "is_active": True,
            }
        )
        return (
            u
            for u in active_users
            if u.has_usable_password()
            and _unicode_ci_compare(serial_number, getattr(u, serial_number_field_name))
        )


    def save(
        self,
        domain_override=None,
        use_https=False,
        request=None,
    ):
        serial_number = self.cleaned_data["serial_number"]
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        serial_number_field_name = UserModel.get_serial_number_field()
        for user in self.get_users(serial_number):
            user_serial_number = getattr(user, serial_number_field_name)
            context = {
                "serial_number": user_serial_number,
                "domain": domain,
                "site_name": site_name,
                "user": user,
                "protocol": "https" if use_https else "http",
            }
