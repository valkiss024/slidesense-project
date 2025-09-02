from django.core.exceptions import ValidationError
from django.test import TestCase

from .factories import PresentationFactory
from ..models import Presentation


class PresentationModelTest(TestCase):
    def test_model_Presentation(self):
        """Tests model creation and instance type"""
        pres = PresentationFactory(title='Example Title')
        self.assertEqual(str(pres), 'Example Title')
        self.assertIsInstance(pres, Presentation)

    def test_default_values(self):
        """Tests the values for default fields (favorited, last_analyzed_at, uploaded_at"""
        pres = PresentationFactory()
        self.assertFalse(pres.favourited)
        self.assertIsNone(pres.last_analyzed_at)
        self.assertIsNotNone(pres.uploaded_at)

    def test_dynamic_traits(self):
        """Tests dynamically changing fields"""
        pres_1 = PresentationFactory(with_analysis=True)
        pres_2 = PresentationFactory(favourited_true=True)
        self.assertIsNotNone(pres_1.last_analyzed_at)
        self.assertTrue(pres_2.favourited)

    def test_title_min_length(self):
        """Tests min length (3) validation for the presentation title"""
        pres = PresentationFactory(title="AA", domain="Test Domain", target_audience="Test audience")
        self.assertRaises(ValidationError, pres.full_clean)

    def test_title_unique(self):
        """Tests the uniqueness of the title field"""
        PresentationFactory(title="Not Unique")
        duplicate = Presentation(title="Not Unique", domain="Test Domain", target_audience="Test audience")
        self.assertRaises(ValidationError, duplicate.full_clean)

    def test_title_domain_target_audience_max_length(self):
        """Tests max length validation for the presentation title, domain and target audience"""
        pres = PresentationFactory(
            title="a" * 51,
            domain="a" * 31,
            target_audience="a" * 31,
        )
        with self.assertRaises(ValidationError) as ex:
            pres.full_clean()  # Call to handle validation errors manually

        self.assertIn("title", ex.exception.message_dict)
        self.assertIn("domain", ex.exception.message_dict)
        self.assertIn("target_audience", ex.exception.message_dict)

    def test_domain_target_audience_required(self):
        """Tests domain and target audience cannot be none"""
        pres = PresentationFactory(
            domain="",
            target_audience="",
        )
        with self.assertRaises(ValidationError) as ex:
            pres.full_clean()  # Call to handle validation errors manually

        self.assertIn("domain", ex.exception.message_dict)
        self.assertIn("target_audience", ex.exception.message_dict)
