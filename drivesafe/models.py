from django.db import models
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone





def validate_pdf_file(value):
    if not value.name.lower().endswith('.pdf'):
        raise ValidationError('Only PDF files are allowed.')

def validate_jpg_file(value):
    if not value.name.lower().endswith('.jpg'):
        raise ValidationError('Only JPG files are allowed.')

def validate_txt_file(value):
    if not value.name.lower().endswith('.txt'):
        raise ValidationError('Only TXT files are allowed.')

class UploadedFiles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to='pdfs/', validators=[FileExtensionValidator(['pdf']), validate_pdf_file], blank=True, null=True)
    jpg_file = models.FileField(upload_to='jpgs/', validators=[FileExtensionValidator(['jpg']), validate_jpg_file], blank=True, null=True)
    txt_file = models.FileField(upload_to='txts/', validators=[FileExtensionValidator(['txt']), validate_txt_file], blank=True, null=True)
    last_updated = models.DateTimeField(default=timezone.now)
    update_seen = models.BooleanField(default=True)

    LOCATION_CHOICES = [
        ('Central Grounds', 'Central Grounds'),
        ('North Grounds', 'North Grounds'),
        ('The Corner', 'The Corner'),
        ('Jefferson Park Avenue', 'Jefferson Park Avenue'),
        ('Emmet Street', 'Emmet Street'),
    ]

    location = models.CharField(max_length=50, choices=LOCATION_CHOICES, default='Central Grounds', blank=True)
    car_color = models.CharField(max_length=100, default= '', blank=True)
    car_model = models.CharField(max_length=100, default= '', blank=True)
    car_identifying_features = models.CharField(max_length=100, default= '', blank=True)
    driver_details = models.CharField(max_length=300, default= '', blank=True)
    additional_information = models.CharField(max_length=300, default= '', blank=True)
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    admin_response = models.CharField(max_length=400, null=True, default='')

    def delete(self, *args, **kwargs):
        # Delete all associated files
        for field in [self.pdf_file, self.jpg_file, self.txt_file]:
            try:
                field.delete(save=False)
            except ValueError:
                pass  # Handle the case where the file doesn't exist

        super().delete(*args, **kwargs)



class ReportingForm(ModelForm):
    class Meta:
        model = UploadedFiles
        fields = ['pdf_file', 'jpg_file', 'txt_file', 'location', 'car_color', 'car_model', 'car_identifying_features', 'driver_details', 'additional_information']
       # fields = ['pdf_file', 'jpg_file', 'location', 'car_color', 'car_model', 'car_identifying_features', 'driver_details', 'additional_information']
        labels = {
            'pdf_file': 'PDF File',
            'jpg_file': 'JPG File',
            'txt_file': 'TXT File',
            'location': 'Location',
            'car_color': 'Car Color',
            'car_model': 'Car Model',
            'car_identifying_features': 'Car Identifying Features',
            'driver_details': 'Driver Details',
            'additional_information': 'Additional Information',
        }


class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Your existing file fields and other fields

    STATUS_CHOICES = [
        ('New', 'New'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')