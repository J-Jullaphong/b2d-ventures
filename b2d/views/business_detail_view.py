import json

from django.conf import settings
from django.shortcuts import render
from django.views.generic import DetailView

from ..models import Business, FundRaising
from ..utils import check_file_exist, get_file


class BusinessDetailView(DetailView):
    """View for displaying detailed information about a specific business."""
    template_name = 'b2d/business_detail.html'
    context_object_name = 'business'

    def get(self, request, *args, **kwargs):
        """
        Provides context data to the business detail template including pitch data, team members, photos,
        embedded YouTube videos, and the business's fundraising campaigns.
        """
        try:
            business = Business.objects.get(id=self.kwargs['pk'])
        except Business.DoesNotExist:
            return render(request, "b2d/404.html", status=404)

        # Paths to pitch and team members JSON files
        pitch_file_key = f"business_docs/{business.id}/pitches.json"
        team_file_key = f"business_docs/{business.id}/team_members.json"

        # Get pitch and team members data from JSON files
        pitch_content = get_file(pitch_file_key)
        team_content = get_file(team_file_key)
        pitch_data = json.loads(pitch_content) if pitch_content else []
        team_members_data = json.loads(team_content) if team_content else []

        # Paths to business photos
        photo1_key = f"business_docs/{business.id}/photo1.jpg"
        photo2_key = f"business_docs/{business.id}/photo2.jpg"
        photo3_key = f"business_docs/{business.id}/photo3.jpg"

        # Get URLs for photos if they exist
        photo1_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{photo1_key}" if check_file_exist(photo1_key) else None
        photo2_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{photo2_key}" if check_file_exist(photo2_key) else None
        photo3_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{photo3_key}" if check_file_exist(photo3_key) else None

        # Get YouTube video data
        youtube_video_key = f"business_docs/{business.id}/youtube_video.json"
        youtube_video_content = get_file(youtube_video_key)
        youtube_video_data = json.loads(youtube_video_content) if youtube_video_content else {}
        youtube_video_url = youtube_video_data.get('url', '')

        # Transform YouTube URL into an embeddable format
        youtube_video_embed = youtube_video_url
        if "youtube.com" in youtube_video_url:
            youtube_video_embed = youtube_video_url.replace("watch?v=", "embed/")
        elif "youtu.be" in youtube_video_url:
            video_id = youtube_video_url.split('/')[-1]
            youtube_video_embed = f"https://www.youtube.com/embed/{video_id}"

        context = {
            'business': business,
            'pitch_data': pitch_data,
            'team_members_data': team_members_data,
            'photo1_url': photo1_url,
            'photo2_url': photo2_url,
            'photo3_url': photo3_url,
            'youtube_video_embed': youtube_video_embed,
            'fundraisings': FundRaising.objects.filter(business=business)
        }

        return render(request, self.template_name, context)
