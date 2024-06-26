from datetime import date
import logging

from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import transaction

from profiles.models.customer import Customer
from profiles.models.user import User
from profiles.models.user import UserType

_is_alpha = RegexValidator(
    regex=r"^[a-zA-Z]+$",
    message="Only upper and lower case English alphabet characters are allowed.",
)


class CustomerCreationForm(UserCreationForm):
    user_name = forms.CharField(required=True)
    first_name = forms.CharField(required=True, validators=[_is_alpha])
    last_name = forms.CharField(required=True, validators=[_is_alpha])
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={"type": "date", "max": date.today()}),
    )
    photo = forms.ImageField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email",)

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.type = UserType.CUSTOMER
        if commit:
            user.save()
            Customer.objects.create(
                user=user,
                user_name=self.cleaned_data.get("user_name"),
                first_name=self.cleaned_data.get("first_name"),
                last_name=self.cleaned_data.get("last_name"),
                date_of_birth=self.cleaned_data.get("date_of_birth"),
                photo=self.cleaned_data.get("photo"),
            )
        return user

    def clean(self):
        super(CustomerCreationForm, self).clean()
        date_of_birth = self.cleaned_data.get("date_of_birth")
        today = date.today()
        if date_of_birth > today:
            raise ValidationError("Date of birth must be in the past")
        return self.cleaned_data


""" CustomerChangeForm

This form is for edit Customer profile.
"""


class CustomerChangeForm(UserChangeForm):
    password = None

    class Meta(UserChangeForm.Meta):
        model = Customer
        fields = (
            "user_name",
            "first_name",
            "last_name",
            "date_of_birth",
            "photo",
            "description",
        )
        widgets = {"date_of_birth": forms.DateInput(attrs={"type": "date", "max": date.today()})}

    @transaction.atomic
    def save(self, commit=True):
        user = self.instance
        customer = Customer.objects.get(pk=user)

        if self.is_valid():
            customer.user_name = self.cleaned_data.get("user_name")
            customer.first_name = self.cleaned_data.get("first_name")
            customer.last_name = self.cleaned_data.get("last_name")
            customer.date_of_birth = self.cleaned_data.get("date_of_birth")
            customer.photo = self.cleaned_data.get("photo")
            customer.description = self.cleaned_data.get("description")
            customer.save()
        else:
            logger = logging.getLogger(__name__)
            logger.error(self.errors)

    def clean(self):
        cleaned_data = super(CustomerChangeForm, self).clean()
        date_of_birth = cleaned_data.get("date_of_birth")
        today = date.today()
        if date_of_birth > today:
            raise ValidationError("Date of birth must be in the past")
        return cleaned_data
