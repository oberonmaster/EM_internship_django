from rest_framework import generics, permissions
from .models import Video
from .serializers import VideoSerializer
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Like, Video
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .models import Video
from django.contrib.auth import get_user_model
from .serializers import UserLikeStatSerializer
from django.db.models import Sum, Subquery, OuterRef, IntegerField
from rest_framework.permissions import IsAdminUser


class VideoListAPIView(generics.ListAPIView):
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_staff:
            return Video.objects.all()
        elif user.is_authenticated:
            return Video.objects.filter(Q(is_published=True) | Q(owner=user))
        return Video.objects.filter(is_published=True)


class VideoDetailAPIView(generics.RetrieveAPIView):
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_staff:
            return Video.objects.all()
        elif user.is_authenticated:
            return Video.objects.filter(Q(is_published=True) | Q(owner=user))
        return Video.objects.filter(is_published=True)


class VideoLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, video_id):
        try:
            video = Video.objects.select_for_update().get(id=video_id)
        except Video.DoesNotExist:
            return Response({'detail': 'Видео не найдено'}, status=404)

        # Проверка доступа
        if not video.is_published and video.owner != request.user and not request.user.is_staff:
            return Response({'detail': 'Нет доступа'}, status=403)

        like, created = Like.objects.get_or_create(user=request.user, video=video)

        if created:
            video.total_likes = Video.objects.filter(id=video.id).annotate(cnt=models.Count('like')).first().cnt
            video.save()
            return Response({'detail': 'Лайк добавлен'}, status=201)
        else:
            like.delete()
            video.total_likes = Video.objects.filter(id=video.id).annotate(cnt=models.Count('like')).first().cnt
            video.save()
            return Response({'detail': 'Лайк удалён'}, status=204)



class VideoIDsAPIView(APIView):
    permission_classes = [IsAdminUser]  # Только staff-пользователи

    def get(self, request):
        ids = list(Video.objects.filter(is_published=True).values_list('id', flat=True))
        return Response({'ids': ids})



User = get_user_model()


class StatsGroupByAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        queryset = (
            User.objects
            .filter(video__is_published=True)
            .annotate(likes_sum=Sum('video__total_likes'))
            .values('username', 'likes_sum')
            .order_by('-likes_sum')
        )
        return Response(UserLikeStatSerializer(queryset, many=True).data)


class StatsSubqueryAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        video_likes = (
            Video.objects
            .filter(is_published=True, owner=OuterRef('pk'))
            .values('owner')
            .annotate(likes_sum=Sum('total_likes'))
            .values('likes_sum')
        )

        queryset = (
            User.objects
            .annotate(likes_sum=Subquery(video_likes, output_field=IntegerField()))
            .filter(likes_sum__isnull=False)
            .values('username', 'likes_sum')
            .order_by('-likes_sum')
        )

        return Response(UserLikeStatSerializer(queryset, many=True).data)
