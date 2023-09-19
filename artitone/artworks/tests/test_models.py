from artworks.tests.unittest_setup import TestCase

# Create your tests here.


class ArtworksTest(TestCase):
    def test_artwork_details(self):
        self.assertEqual(self.artwork.artist.user_name, "Van Gogh")
        self.assertEqual(self.artwork.title, self.title)
        self.assertEqual(self.artwork.category, self.category)
        self.assertEqual(self.artwork.price, self.price)
        self.assertEqual(self.artwork.texture, self.texture)
        self.assertEqual(self.artwork.content, self.content)
        self.assertEqual(self.artwork.pictures.all()[0], self.picture)

    def test_category_detail(self):
        self.assertEqual(self.category.name, "Painting")

    def test_taggit_tags_detail(self):
        self.assertEqual(self.artwork.tags.all()[0].name, "Minimalism")

    def test_taggit_colors_detail(self):
        self.assertEqual(self.artwork.colors.all()[0].name, "#ffffff")
