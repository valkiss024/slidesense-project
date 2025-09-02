from django.core.validators import MinLengthValidator
from django.db import models


# The Presentation class encapsulates all information of a presentation uploaded by the user
class Presentation(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    last_analyzed_at = models.DateTimeField(default=None, blank=True, null=True)
    title = models.CharField(max_length=50,
                             validators=[MinLengthValidator(3,
                                                            message="Title must be at least 3 characters long")],
                             unique=True)
    # pptx_file = models.FileField(upload_to=get_user_presentation_path,
    #                             validators=[FileExtensionValidator(allowed_extensions=['pptx'],
    #                                                                message='Only .pptx files are allowed')])
    domain = models.CharField(max_length=30)
    target_audience = models.CharField(max_length=30)
    favourited = models.BooleanField(default=False)

    def __str__(self):
        return self.title
