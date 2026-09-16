from rest_framework import serializers
from .models import Assessment


class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = [
            "id",
            "name",
            "email",
            "company_name",
            "designation",
            "industry",
            "company_size",
            "departments",
            "automation_level",
            "repetitive_activities",
            "workflow_notes",
            "challenges",
            "challenge_notes",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]