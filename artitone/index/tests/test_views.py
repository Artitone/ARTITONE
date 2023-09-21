
from django.urls import reverse
from django.test.client import RequestFactory

from index.tests.unittest_setup import TestCase
from index.views.home import home


class IndexTest(TestCase):

    def setUp(self):
        super().setUp()
        self.client.login(email="vangogh@gmail.com", password="where_is_my_ear")

    def test_index(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
    
    def test_search_by_keyword(self):
        data = {}
        response = self.client.get(reverse("home"), data)
        artworks = response.context['page_obj'].object_list
        self.assertEqual(len(artworks), 2)

        data['keyword'] = "Artwork"
        response = self.client.get(reverse("home"), data)
        artworks = response.context['page_obj'].object_list
        self.assertEqual(len(artworks), 1)

        data['keyword'] = "lala"
        response = self.client.get(reverse("home"), data)
        artworks = response.context['page_obj'].object_list
        self.assertEqual(len(artworks), 1)

        data['keyword'] = "lalaLalala"
        response = self.client.get(reverse("home"), data)
        artworks = response.context['page_obj'].object_list
        self.assertEqual(len(artworks), 0)
        
    def test_search_by_tags(self):
        data = {}
        response = self.client.get(reverse("home"), data)
        artworks = response.context['page_obj'].object_list
        self.assertEqual(len(artworks), 2)

        data['keyword'] = "Minimalism"
        response = self.client.get(reverse("home"), data)
        artworks = response.context['page_obj'].object_list
        self.assertEqual(len(artworks), 1)

        data['keyword'] = "Minimalist"
        response = self.client.get(reverse("home"), data)
        artworks = response.context['page_obj'].object_list
        self.assertEqual(len(artworks), 0)
    
    def test_search_by_color_pallete(self):
        data = {}
        response = self.client.get(reverse("home"), data)
        artworks = response.context['page_obj'].object_list
        self.assertEqual(len(artworks), 2)

        data['color'] = "modern"
        response = self.client.get(reverse("home"), data)
        artworks = response.context['page_obj'].object_list
        self.assertEqual(len(artworks), 1)

        data['color'] = "contemporary"
        response = self.client.get(reverse("home"), data)
        artworks = response.context['page_obj'].object_list
        self.assertEqual(len(artworks), 0)

    def test_search_by_category(self):
        data = {}
        response = self.client.get(reverse("home"), data)
        artworks = response.context['page_obj'].object_list
        self.assertEqual(len(artworks), 2)

        data['category'] = "Sculpture"
        response = self.client.get(reverse("home"), data)
        artworks = response.context['page_obj'].object_list
        self.assertEqual(len(artworks), 1)

        data['category'] = "Wall Arts"
        response = self.client.get(reverse("home"), data)
        artworks = response.context['page_obj'].object_list
        self.assertEqual(len(artworks), 0)