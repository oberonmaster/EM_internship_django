from django.urls import path
from .views import (VideoListAPIView,
                    VideoDetailAPIView,
                    VideoLikeAPIView,
                    VideoIDsAPIView,
                    StatsGroupByAPIView,
                    StatsSubqueryAPIView,
                    )

urlpatterns = [
    path('videos/', VideoListAPIView.as_view(), name='video-list'),
    path('videos/<int:pk>/', VideoDetailAPIView.as_view(), name='video-detail'),
    path('videos/<int:video_id>/likes/', VideoLikeAPIView.as_view(), name='video-like'),
    path('videos/ids/', VideoIDsAPIView.as_view(), name='video-ids'),
    path('videos/statistics-group-by/', StatsGroupByAPIView.as_view(), name='video-stat-group'),
    path('videos/statistics-subquery/', StatsSubqueryAPIView.as_view(), name='video-stat-subquery'),

]
