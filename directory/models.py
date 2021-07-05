from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator


class Subject(models.Model):
    title = models.CharField(_("Title"), max_length=128)

    def __str__(self) -> str:
        return f"{self.title}"


class Teacher(models.Model):
    phone_regex_validator = RegexValidator(regex=r'\+?[\d]{3}-[\d]{3}-[\d]{3}-[\d]{3}', message=_(
        "Phone number must be entered in the format: '+111-222-333-444'."))

    first_name = models.CharField(_("First Name"), max_length=128)
    last_name = models.CharField(_("Last Name"), max_length=128)
    profile_picture = models.ImageField(
        _("Profile Picture"), upload_to="teacher_profiles", null=True, blank=True)
    email_address = models.EmailField(_("Email Address"), unique=True)
    phone_number = models.CharField(_("Phone Number"), validators=[
                                    phone_regex_validator], max_length=17)
    room_number = models.CharField(_("Room Number"), max_length=8)
    subjects = models.ManyToManyField(Subject,  related_name=_(
        "Teachers"), related_query_name="teachers", verbose_name=_("Subjects"))

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    

    class Meta:
        ordering = ('first_name', 'last_name', )
