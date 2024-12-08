import json
from urllib.parse import urlparse

from django.conf import settings
from django.core.files.base import ContentFile
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View

from ..models import Business, Category
from ..utils import upload_file, get_file


class BusinessProfileView(View):
    """View to manage business profile creation and updates."""
    template_name = 'b2d/business_create.html'

    def get(self, request):
        """Handles the GET request to display the business profile form."""
        try:
            business = Business.objects.get(id=request.user.id)
        except Business.DoesNotExist:
            messages.error(request, "Access restricted. Business profile page is for business owners only.")
            return redirect("b2d:home")

        pitch_data = self.load_json_file(f"business_docs/{business.id}/pitches.json", default=[])

        team_members_data = self.load_json_file(f"business_docs/{business.id}/team_members.json", default=[])
        youtube_video_data = self.load_json_file(f"business_docs/{business.id}/youtube_video.json", default={})

        youtube_video_url = youtube_video_data.get('url', '')
        youtube_video_embed = self.get_youtube_embed_url(youtube_video_url)

        context = {
            'business_name': business.name,
            'business_description': business.description,
            'pitch_data': pitch_data,
            'team_members_data': team_members_data,
            'categories': Category.objects.all(),
            'selected_category': business.category.values_list('id', flat=True),
            'photo1_url': self.get_photo_url(business.id, "photo1"),
            'photo2_url': self.get_photo_url(business.id, "photo2"),
            'photo3_url': self.get_photo_url(business.id, "photo3"),
            'youtube_video_url': youtube_video_url,
            'youtube_video_embed': youtube_video_embed,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Handles the POST request to update business profile information."""
        business = Business.objects.get(id=request.user.id)
        business.name = request.POST.get('businessName', business.name)
        business.description = request.POST.get('businessDescription', business.description)
        category_ids = request.POST.getlist('category[]')
        if category_ids:
            business.category.set(Category.objects.filter(id__in=category_ids))
        business.save()

        self.handle_pitch_data(request, business.id)
        self.handle_team_members(request, business.id)
        self.handle_photos(request, business.id)
        self.handle_youtube_video(request, business.id)

        messages.success(request, "Business profile updated successfully.")
        return redirect('b2d:business_profile')

    def handle_pitch_data(self, request, business_id):
        """Handles pitch data update with dynamic reindexing, including optional photo upload."""
        pitch_data = []
        index = 0

        while True:
            topic = request.POST.get(f'topic_{index}')
            details = request.POST.get(f'details_{index}')
            photo = request.FILES.get(f'photo_{index}')

            if topic is None and details is None:
                break
            if topic and details:
                photo_key = f"business_docs/{business_id}/pitches/pitch_{topic}.jpg"
                if photo:
                    upload_file(photo, photo_key)
                pitch_data.append({
                    "topic": topic,
                    "details": details,
                    "photo_url": f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{photo_key}"
                })
            index += 1

        self.save_json_file(pitch_data,
                            f"business_docs/{business_id}/pitches.json")

    def handle_team_members(self, request, business_id):
        """Handles team members data update with explicit indexing."""
        team_members_data = []
        index = 0

        while True:
            name = request.POST.get(f'memberName_{index}')
            work_as = request.POST.get(f'workAs_{index}')
            photo = request.FILES.get(f'uploadFile_{index}')

            if name is None and work_as is None:
                break
            if name and work_as:
                photo_key = f"business_docs/{business_id}/team_members/{name}.jpg"
                if photo:
                    upload_file(photo, photo_key)
                team_members_data.append({
                    "name": name,
                    "work_as": work_as,
                    "photo_url": f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{photo_key}"
                })
            index += 1

        self.save_json_file(team_members_data, f"business_docs/{business_id}/team_members.json")

    def handle_photos(self, request, business_id):
        """Handles uploading of business photos."""
        for i in range(1, 4):
            photo = request.FILES.get(f'photo{i}')
            if photo:
                photo_key = f"business_docs/{business_id}/photo{i}.jpg"
                upload_file(photo, photo_key)

    def handle_youtube_video(self, request, business_id):
        """Handles YouTube video data update."""
        youtube_video_url = request.POST.get('videoEmbed')
        if youtube_video_url:
            youtube_video_data = {'url': youtube_video_url}
            self.save_json_file(youtube_video_data, f"business_docs/{business_id}/youtube_video.json")

    def get_photo_url(self, business_id, photo_name):
        """Constructs the photo URL."""
        return f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/business_docs/{business_id}/{photo_name}.jpg"

    def get_youtube_embed_url(self, url):
        """Parses and returns the YouTube embed URL."""
        parsed_url = urlparse(url)
        host = parsed_url.hostname
        if host and (host == "youtube.com" or host == "www.youtube.com"):
            return url.replace("watch?v=", "embed/")
        elif host and (host == "youtu.be" or host == "www.youtu.be"):
            video_id = parsed_url.path.split('/')[-1]
            return f"https://www.youtube.com/embed/{video_id}"
        return url

    def load_json_file(self, file_key, default=None):
        """Loads JSON content from S3."""
        content = get_file(file_key)
        return json.loads(content) if content else default

    def save_json_file(self, data, file_key):
        """Saves JSON content to S3."""
        json_content = json.dumps(data, indent=4).encode('utf-8')
        file = ContentFile(json_content)
        upload_file(file, file_key)
