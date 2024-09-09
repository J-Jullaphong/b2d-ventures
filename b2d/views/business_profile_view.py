import json

from django.conf import settings
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.views import View

from ..models import Business, Category
from ..utils import upload_file, get_file


class BusinessProfileView(View):
    template_name = 'b2d/business_create.html'

    def get(self, request):
        business = Business.objects.get(id=request.user.id)
        pitch_file_key = f"business_docs/{business.id}/pitches.json"
        team_file_key = f"business_docs/{business.id}/team_members.json"

        pitch_content = get_file(pitch_file_key)
        team_content = get_file(team_file_key)

        pitch_data = json.loads(pitch_content) if pitch_content else []
        team_members_data = json.loads(team_content) if team_content else []

        photo1_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/business_docs/{business.id}/photo1.jpg"
        photo2_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/business_docs/{business.id}/photo2.jpg"
        photo3_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/business_docs/{business.id}/photo3.jpg"

        youtube_video_key = f"business_docs/{business.id}/youtube_video.json"
        youtube_video_content = get_file(youtube_video_key)
        youtube_video_data = json.loads(
            youtube_video_content) if youtube_video_content else {}
        youtube_video_url = youtube_video_data.get('url', '')
        youtube_video_embed = youtube_video_url
        if "youtube.com" in youtube_video_url:
            youtube_video_embed = youtube_video_url.replace("watch?v=",
                                                            "embed/")
        elif "youtu.be" in youtube_video_url:
            video_id = youtube_video_url.split('/')[-1]
            youtube_video_embed = f"https://www.youtube.com/embed/{video_id}"

        context = {
            'business_name': business.name,
            'business_description': business.description,
            'pitch_data': pitch_data,
            'team_members_data': team_members_data,
            'categories': Category.objects.all(),
            'selected_category': business.category.id if business.category else None,
            'photo1_url': photo1_url,
            'photo2_url': photo2_url,
            'photo3_url': photo3_url,
            'youtube_video_url': youtube_video_url,
            'youtube_video_embed': youtube_video_embed
        }

        return render(request, self.template_name, context)

    def post(self, request):
        business = Business.objects.get(id=request.user.id)
        business_name = request.POST.get('businessName')
        business_description = request.POST.get('businessDescription')
        category_id = request.POST.get('category')

        if business_name:
            business.name = business_name
        if business_description:
            business.description = business_description
        if category_id:
            business.category = Category.objects.get(id=category_id)

        business.save()

        topics = request.POST.getlist('topic[]')
        details = request.POST.getlist('details[]')

        if (topics and details) and (len(topics) == len(details)):
            pitch_data = [{"topic": topic, "details": detail} for topic, detail
                          in zip(topics, details) if topic and detail]
            pitch_json_content = json.dumps(pitch_data, indent=4).encode(
                'utf-8')
            pitch_file = ContentFile(pitch_json_content)
            pitch_file_key = f"business_docs/{business.id}/pitches.json"
            upload_file(pitch_file, pitch_file_key)

        member_names = request.POST.getlist('memberName[]')
        work_as_roles = request.POST.getlist('workAs[]')
        photos = request.FILES.getlist('uploadFile[]')

        if member_names and work_as_roles:
            team_members_data = []
            for index, (name, work_as) in enumerate(
                    zip(member_names, work_as_roles)):
                if not name:
                    continue
                photo = photos[index] if index < len(photos) else None
                photo_key = f"business_docs/{business.id}/team_members/{index}.jpg"
                if photo:
                    upload_file(photo, photo_key)

                team_members_data.append({
                    "number": index,
                    "name": name,
                    "work_as": work_as,
                    "photo_url": f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{photo_key}"
                })

            team_json_content = json.dumps(team_members_data, indent=4).encode(
                'utf-8')
            team_file = ContentFile(team_json_content)
            team_file_key = f"business_docs/{business.id}/team_members.json"
            upload_file(team_file, team_file_key)

        photos = {
            'photo1': request.FILES.get('photo1'),
            'photo2': request.FILES.get('photo2'),
            'photo3': request.FILES.get('photo3')
        }

        for i, photo in photos.items():
            if photo:
                photo_key = f"business_docs/{business.id}/{i}.jpg"
                upload_file(photo, photo_key)

        youtube_video_url = request.POST.get('videoEmbed')
        if youtube_video_url:
            youtube_video_data = {'url': youtube_video_url}
            youtube_video_json_content = json.dumps(youtube_video_data,
                                                    indent=4).encode('utf-8')
            youtube_video_file = ContentFile(youtube_video_json_content)
            youtube_video_key = f"business_docs/{business.id}/youtube_video.json"
            upload_file(youtube_video_file, youtube_video_key)

        return redirect('b2d:business-profile')
