from django.urls import reverse
from .basecase import BaseCase


class BusinessProfileViewTest(BaseCase):

    def test_business_profile_view_with_business_user(self):
        """Test the business profile view which login as business user is rendered."""
        # login as business 1
        login_successful = self.client.login(username=self.business1.username, password="password123")
        self.assertTrue(login_successful)
        url = reverse('b2d:business_profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'b2d/business_create.html')

    def test_business_profile_view_without_business_user(self):
        """Test the business profile view which not login as business user is redirect."""
        url = reverse('b2d:business_profile')
        response = self.client.get(url)
        # Not authentication should redirect
        self.assertEqual(response.status_code, 302)
        # Investor user should redirect
        login_successful = self.client.login(username=self.investor1.username, password="password123")
        self.assertTrue(login_successful)
        self.assertEqual(response.status_code, 302)

    def test_business_profile_view_context(self):
        """Test business profile view return correct business information context"""
        self.client.login(username=self.business1.username, password="password123")
        url = reverse('b2d:business_profile')
        response = self.client.get(url)

        self.assertEqual(response.context['business_name'], self.business1.name)
        self.assertEqual(response.context['business_description'], self.business1.description)
        self.assertEqual(response.context['pitch_data'], [])
        self.assertEqual(response.context['team_members_data'], [])
        self.assertEqual(response.context['selected_category'], self.business1.category.id)
        self.assertEqual(response.context['youtube_video_url'], '')
        self.assertEqual(response.context['youtube_video_embed'], '')
