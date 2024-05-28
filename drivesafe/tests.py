from django.test import TestCase, Client
from django.urls import reverse
from .models import UploadedFiles, ReportingForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
# # Create your tests here.

class LoginUserTests(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(username='staffuser', email='staff@example.com',
                                                   password='password', is_staff=True)
        self.regular_user = User.objects.create_user(username='regularuser', email='regularuser@example.com',
                                                   password='password', is_staff=False)
        self.client = Client()
        pass

    def tearDown(self):
        self.staff_user.delete()
        self.regular_user.delete()

    def test_staff_redirect_to_admin_home(self):
        self.client.login(username='staffuser', password='password')
        response = self.client.get(reverse('drivesafe:login_redirect'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('drivesafe:admin_home'))
        pass
#
    def test_regular_user_redirect(self):
        self.client.login(username='regularuser', password='password')
        response = self.client.get(reverse('drivesafe:login_redirect'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('drivesafe:regular_user_home'))
        pass
    def test_anon_user(self):
        response = self.client.get(reverse('drivesafe:anonymous_report'))
        self.assertEqual(response.status_code, 200)
        pass



class ReportingFormTests(TestCase):

   def test_valid_form(self):
        pdf_file = SimpleUploadedFile("test_pdf.pdf", b"file_content", content_type="application/pdf")
        jpg_file = SimpleUploadedFile("test_jpg.jpg", b"file_content", content_type="image/jpeg")
        txt_file = SimpleUploadedFile("test_txt.txt", b"file_content", content_type="text/plain")
        data = {
            'pdf_file': pdf_file,
            'jpg_file': jpg_file,
            'txt_file': txt_file,
            'location': 'Central Grounds',
            'car_color': 'Red',
            'car_model': 'Toyota',
            'car_identifying_features': 'None',
            'driver_details': 'John Doe',
            'additional_information': 'None',
        }
        form = ReportingForm(data, {'pdf_file': pdf_file, 'jpg_file': jpg_file, 'txt_file': txt_file})
        self.assertTrue(form.is_valid())
        pass

   # def test_invalid_form(self):
   #     pdf_file = SimpleUploadedFile("test_pdf.pdf", b"file_content", content_type="application/pdf")
   #     jpg_file = SimpleUploadedFile("test_jpg.jpg", b"file_content", content_type="image/jpeg")
   #     txt_file = SimpleUploadedFile("test_txt.txt", b"file_content", content_type="text/plain")
   #     data = {
   #         'pdf_file': pdf_file,
   #         'jpg_file': jpg_file,
   #         'txt_file': txt_file,
   #         'location': 'Central Grounds',
   #         'car_color': '',
   #         'car_model': 'Toyota',
   #         'car_identifying_features': '',
   #         'driver_details': 'John Doe',
   #         'additional_information': '',
   #     }
   #     form = ReportingForm(data, {'pdf_file': pdf_file, 'jpg_file': jpg_file, 'txt_file': txt_file})
   #     self.assertFalse(form.is_valid())
   #     pass


class StatusUpdateTest(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(username='staffuser', email='staff@example.com',
                                                   password='password', is_staff=True)
        self.submission = UploadedFiles.objects.create(
            user=self.staff_user,
            pdf_file='sample.pdf',
            jpg_file='sample.jpg',
            txt_file='sample.txt',
            location='Central Grounds',
            car_color='Red',
            car_model='Toyota',
            car_identifying_features='None',
            driver_details='John Doe',
            additional_information='None',
            status='New'
        )
    def tearDown(self):
        self.staff_user.delete()
        self.submission.delete()
    # def test_status_update_complete(self):
    #     self.client.login(username='staffuser', password='password')
    #     response = self.client.post(reverse('drivesafe:update_status', args=[self.submission.pk]), {'status': 'Completed'})
    #     updated_submission = UploadedFiles.objects.get(pk=self.submission.pk)
    #     self.assertEqual(updated_submission.status, 'Completed')
    #
    # def test_status_update_in_progress(self):
    #     self.client.login(username='staffuser', password='password')
    #     response = self.client.post(reverse('drivesafe:update_status', args=[self.submission.pk]), {'status': 'In Progress'})
    #     updated_submission = UploadedFiles.objects.get(pk=self.submission.pk)
    #     self.assertEqual(updated_submission.status, 'In Progress')



class ViewSubmissions(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(username='staffuser', email='staff@example.com',
                                                   password='password', is_staff=True)
        self.regular_user = User.objects.create_user(username='regularuser', email='regularuser@example.com',
                                                     password='password', is_staff=False)
        self.submission = UploadedFiles.objects.create(
            user=self.regular_user,
            pdf_file='sample.pdf',
            jpg_file='sample.jpg',
            txt_file='sample.txt',
            location='Central Grounds',
            car_color='Red',
            car_model='Toyota',
            car_identifying_features='None',
            driver_details='John Doe',
            additional_information='None',
            status='New',
        )
        self.client = Client()
        pass

    def tearDown(self):
        self.staff_user.delete()
        self.regular_user.delete()
        self.submission.delete()

    # def test_view_own_submission(self):
    #     self.client.login(username='regularuser', password='password')
    #     response = self.client.get(reverse('drivesafe:user_submissions'))
    #     self.assertEqual(response.status_code, 200)
    #     form_exists = UploadedFiles.objects.filter(user=self.regular_user).exists()
    #     self.assertTrue(form_exists)
    #     self.assertContains(response, 'sample.pdf')
    #
    # def test_staff_view_submissions(self):
    #     self.client.login(username='staffuser', password='password')
    #     response = self.client.get(reverse('drivesafe:submissions'))
    #     self.assertEquals(response.status_code, 200)
    #     form_exists = UploadedFiles.objects.filter(user=self.regular_user).exists()
    #     self.assertTrue(form_exists)
    #     self.assertContains(response, 'sample.pdf')
