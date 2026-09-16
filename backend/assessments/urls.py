from django.urls import path

from .views import AssessmentListCreateView, AssessmentDetailView


urlpatterns = [
    path(
        "",
        AssessmentListCreateView.as_view(),
        name="assessment-list-create",
    ),
    path(
        "<int:pk>/",
        AssessmentDetailView.as_view(),
        name="assessment-detail",
    ),
]