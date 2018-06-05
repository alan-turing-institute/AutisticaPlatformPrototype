from io import BytesIO

from django.test import TestCase, Client
from django.core.management import call_command
from django.conf import settings
from openhumans.models import OpenHumansMember
import markdown
import vcr


class IndexPageTestCase(TestCase):
    """
    Test cases for the index page.
    """

    def setUp(self):
        """
        Set up the app for following tests.
        """
        settings.DEBUG = True

    def test_index_page_content(self):
        """
        Test whether content is rendered properly.
        """
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)


class LoginTestCase(TestCase):
    """
    Test the login logic of the OH API
    """

    def setUp(self):
        settings.DEBUG = True
        settings.OPENHUMANS_APP_BASE_URL = "http://127.0.0.1"

    @vcr.use_cassette('main/tests/fixtures/token_exchange_valid.yaml',
                      record_mode='none')
    def test_complete(self):
        c = Client()
        self.assertEqual(0,
                         OpenHumansMember.objects.all().count())
        response = c.get("/complete", {'code': 'mytestcode'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/overview")
        self.assertEqual(1,
                         OpenHumansMember.objects.all().count())

    def test_complete_unauthenticated(self):
        """
        Tests making a get request to complete
        when not authenticated.
        """
        with self.assertLogs(logger='main.views', level='DEBUG') as log:
            c = Client()
            self.assertEqual(0,
                             OpenHumansMember.objects.all().count())
            response = c.get("/complete", {'code': 'mytestcode'})
        self.assertIn(
                    "Invalid code exchange. User returned to start page.",
                    log.output[len(log.output)-1])
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/")

    def test_log_out_logged_out(self):
        """
        Tests logout function
        """
        c = Client()
        response = c.get('/logout')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/")

    def test_overview_logged_out(self):
        """
        Tests overview function when logged out
        """
        c = Client()
        response = c.get("/overview")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/")

    def test_log_out(self):
        """
        Tests logout function
        """
        data = {"access_token": 'foo',
                "refresh_token": 'bar',
                "expires_in": 36000}
        self.oh_member = OpenHumansMember.create(oh_id='1234567890abcdef',
                                                 data=data)
        self.oh_member.save()
        self.user = self.oh_member.user
        self.user.set_password('foobar')
        self.user.save()
        c = Client()
        c.login(username=self.user.username, password='foobar')
        response = c.post('/logout')
        self.assertEqual(response.wsgi_request.user.username, '')
        self.assertRedirects(response, "/")

    def test_delete_single_logged_out(self):
        c = Client()
        response = c.get("/delete/1")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/")

    @vcr.use_cassette('main/tests/fixtures/delete_single.yaml',
                      record_mode='none')
    def test_delete_single(self):
        data = {"access_token": 'foo',
                "refresh_token": 'bar',
                "expires_in": 36000}
        self.oh_member = OpenHumansMember.create(oh_id='1234567890abcdef',
                                                 data=data)
        self.oh_member.save()
        self.user = self.oh_member.user
        self.user.set_password('foobar')
        self.user.save()
        c = Client()
        c.login(username=self.user.username, password='foobar')

        response = c.get("/delete/1337", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/list.html')


class UploadTestCase(TestCase):
    def setUp(self):
        # set up project
        settings.DEBUG = True
        # settings.OPENHUMANS_APP_BASE_URL = "http://127.0.0.1"

        # set up user
        data = {"access_token": 'foo',
                "refresh_token": 'bar',
                "expires_in": 36000}
        self.oh_member = OpenHumansMember.create(oh_id='1234567890abcdef',
                                                 data=data)
        self.oh_member.save()
        self.user = self.oh_member.user
        self.user.set_password('foobar')
        self.user.save()

    def test_get_upload(self):
        c = Client()
        c.login(username=self.user.username, password='foobar')
        response = c.get("/upload/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/upload.html')

    def test_upload_logged_out(self):
        c = Client()
        response = c.get("/upload/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    @vcr.use_cassette('main/tests/fixtures/upload_file.yaml',
                      record_mode='none')
    def test_post_upload(self):
        c = Client()
        c.login(username=self.user.username, password='foobar')
        test_file = BytesIO(b'mybinarydata')
        test_file.name = 'myimage.jpg'
        response = c.post("/complete/",
                          {'file_1': test_file},
                          follow=True)
        self.assertRedirects(response,
                             "/overview",
                             status_code=302)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/overview.html')
