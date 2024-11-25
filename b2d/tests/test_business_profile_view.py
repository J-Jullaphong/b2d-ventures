from django.urls import reverse
from .basecase import BaseCase


class BusinessProfileViewTest(BaseCase):

    def test_business_profile_view_accessible_for_business(self):
        """Test that the business profile view is accessible for logged-in business owner."""
        self.client.login(username=self.business1.username, password="#Password1234")
        url = reverse('b2d:business_profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'b2d/business_create.html')

    def test_business_profile_view_forbidden_for_non_business(self):
        """Test that the business profile view is forbidden for non-business users."""
        self.client.logout()
        url = reverse('b2d:business_profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_business_profile_view_context(self):
        """Test business profile view return correct business information context"""
        self.client.login(username=self.business1.username, password="#Password1234")
        url = reverse('b2d:business_profile')
        response = self.client.get(url)

        self.assertEqual(response.context['business_name'], self.business1.name)
        self.assertEqual(response.context['business_description'], self.business1.description)
        self.assertEqual(response.context['pitch_data'], [])
        self.assertEqual(response.context['team_members_data'], [])
        self.assertListEqual(
            list(response.context['selected_category']),
            list(self.business1.category.values_list('id', flat=True))
        )
        self.assertEqual(response.context['youtube_video_url'], '')
        self.assertEqual(response.context['youtube_video_embed'], '')
