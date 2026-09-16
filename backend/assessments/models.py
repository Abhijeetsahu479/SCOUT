import uuid

from django.db import models


# =========================================================
# ASSESSMENT
# =========================================================

class Assessment(models.Model):

    # -------------------------
    # Basic Information
    # -------------------------

    name = models.CharField(
        max_length=100
    )

    email = models.EmailField()

    company_name = models.CharField(
        max_length=200
    )

    designation = models.CharField(
        max_length=100
    )

    # -------------------------
    # Company Information
    # -------------------------

    industry = models.CharField(
        max_length=100
    )

    company_size = models.CharField(
        max_length=100
    )

    departments = models.JSONField(
        default=list,
        blank=True
    )

    # -------------------------
    # Automation Information
    # -------------------------

    automation_level = models.CharField(
        max_length=100,
        blank=True
    )

    repetitive_activities = models.JSONField(
        default=list,
        blank=True
    )

    workflow_notes = models.TextField(
        blank=True,
        max_length=500
    )

    # -------------------------
    # Challenges
    # -------------------------

    challenges = models.JSONField(
        default=list,
        blank=True
    )

    challenge_notes = models.TextField(
        blank=True,
        max_length=500
    )

    # -------------------------
    # Created Date
    # -------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Assessment"
        verbose_name_plural = "Assessment submissions"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.company_name} - {self.name}"


# =========================================================
# LEAD
# =========================================================

class Lead(models.Model):

    # -------------------------
    # Primary Key
    # -------------------------

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # -------------------------
    # Basic User Information
    # -------------------------

    name = models.CharField(
        max_length=200
    )

    email = models.EmailField(
        unique=True,
        db_index=True
    )

    # -------------------------
    # Company Information
    # -------------------------

    company_name = models.CharField(
        max_length=300
    )

    designation = models.CharField(
        max_length=200
    )

    industry = models.CharField(
        max_length=100
    )

    company_size = models.CharField(
        max_length=50
    )

    # -------------------------
    # Assessment Information
    # -------------------------

    departments_selected = models.JSONField(
        default=list,
        blank=True
    )

    automation_level = models.CharField(
        max_length=100,
        blank=True
    )

    repetitive_activities = models.JSONField(
        default=list,
        blank=True
    )

    workflow_notes = models.TextField(
        blank=True
    )

    challenges = models.JSONField(
        default=list,
        blank=True
    )

    challenge_notes = models.TextField(
        blank=True
    )

    # -------------------------
    # Additional Notes
    # -------------------------

    additional_notes = models.TextField(
        blank=True
    )

    # -------------------------
    # UTM / Marketing Tracking
    # -------------------------

    utm_source = models.CharField(
        max_length=200,
        blank=True
    )

    utm_medium = models.CharField(
        max_length=200,
        blank=True
    )

    utm_campaign = models.CharField(
        max_length=200,
        blank=True
    )

    # -------------------------
    # IP Address
    # -------------------------

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    # -------------------------
    # Consent
    # -------------------------

    consent_given = models.BooleanField(
        default=False
    )

    # -------------------------
    # Created Date
    # -------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # -------------------------
    # Report Status
    # -------------------------

    prelim_report_sent = models.BooleanField(
        default=False
    )

    full_report_sent = models.BooleanField(
        default=False
    )

    full_report_sent_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Lead"
        verbose_name_plural = "Leads"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.company_name}"


# =========================================================
# ASSESSMENT REPORT
# =========================================================

class AssessmentReport(models.Model):

    # -------------------------
    # Primary Key
    # -------------------------

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # -------------------------
    # Lead Relationship
    # -------------------------

    lead = models.OneToOneField(
        Lead,
        on_delete=models.CASCADE,
        related_name="assessment_report"
    )

    # -------------------------
    # Overall Readiness Score
    # -------------------------

    overall_score = models.IntegerField(
        default=0
    )

    # -------------------------
    # Department Analysis
    # -------------------------

    department_scores = models.JSONField(
        default=dict,
        blank=True
    )

    # -------------------------
    # Automation Recommendations
    # -------------------------

    should_automate = models.JSONField(
        default=list,
        blank=True
    )

    should_not_automate = models.JSONField(
        default=list,
        blank=True
    )

    # -------------------------
    # ROI / Business Impact
    # -------------------------

    estimated_hours_saved_monthly = models.IntegerField(
        default=0
    )

    estimated_cost_saved_monthly_inr = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    # -------------------------
    # AI Report
    # -------------------------

    ai_summary = models.TextField(
        blank=True
    )

    raw_ai_response = models.JSONField(
        default=dict,
        blank=True
    )

    # -------------------------
    # Generated Date
    # -------------------------

    generated_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Assessment Report"
        verbose_name_plural = "Assessment Reports"
        ordering = ["-generated_at"]

    def __str__(self):
        return (
            f"{self.lead.company_name} - "
            f"{self.overall_score}/100"
        )