from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from ..models import Business, FundRaising
import json

from ..utils import check_file_exist, get_file


class BusinessDetailView(DetailView):
    model = Business
    template_name = 'b2d/business_detail.html'
    context_object_name = 'business'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        business = self.object

        pitch_file_key = f"business_docs/{business.id}/pitches.json"
        team_file_key = f"business_docs/{business.id}/team_members.json"

        pitch_content = get_file(pitch_file_key)
        team_content = get_file(team_file_key)

        pitch_data = json.loads(pitch_content) if pitch_content else []
        team_members_data = json.loads(team_content) if team_content else []

        photo1_key = f"business_docs/{business.id}/photo1.jpg"
        photo2_key = f"business_docs/{business.id}/photo2.jpg"
        photo3_key = f"business_docs/{business.id}/photo3.jpg"

        photo1_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{photo1_key}" if check_file_exist(photo1_key) else None
        photo2_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{photo2_key}" if check_file_exist(photo2_key) else None
        photo3_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{photo3_key}" if check_file_exist(photo3_key) else None

        youtube_video_key = f"business_docs/{business.id}/youtube_video.json"
        youtube_video_content = get_file(youtube_video_key)
        youtube_video_data = json.loads(youtube_video_content) if youtube_video_content else {}
        youtube_video_url = youtube_video_data.get('url', '')
        youtube_video_embed = youtube_video_url
        if "youtube.com" in youtube_video_url:
            youtube_video_embed = youtube_video_url.replace("watch?v=", "embed/")
        elif "youtu.be" in youtube_video_url:
            video_id = youtube_video_url.split('/')[-1]
            youtube_video_embed = f"https://www.youtube.com/embed/{video_id}"

        context.update({
            'pitch_data': pitch_data,
            'team_members_data': team_members_data,
            'photo1_url': photo1_url,
            'photo2_url': photo2_url,
            'photo3_url': photo3_url,
            'youtube_video_embed': youtube_video_embed,
            'fundraisings': FundRaising.objects.filter(business=business)
        })

        return context
