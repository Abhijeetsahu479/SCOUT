from django.contrib import admin

from .models import Assessment, Lead, AssessmentReport


# =====================================================
# ASSESSMENT ADMIN
# =====================================================

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):

    # =========================
    # LIST VIEW
    # =========================
    list_display = (
        "company_name",
        "name",
        "email",
        "industry",
        "company_size",
        "automation_level",
        "workflow_options",
        "workflow_answer",
        "selected_challenges",
        "challenge_answer",
        "created_at",
    )

    # =========================
    # FILTERS
    # =========================
    list_filter = (
        "industry",
        "company_size",
        "automation_level",
        "created_at",
    )

    # =========================
    # SEARCH
    # =========================
    search_fields = (
        "company_name",
        "name",
        "email",
        "designation",
    )

    # =========================
    # ORDERING
    # =========================
    ordering = ("-created_at",)

    # =========================
    # DATE NAVIGATION
    # =========================
    date_hierarchy = "created_at"

    # =========================
    # NUMBER OF RECORDS
    # =========================
    list_per_page = 25

    # =========================
    # READ-ONLY FIELDS
    # =========================
    readonly_fields = (
        "created_at",
    )

    # =========================
    # WORKFLOW OPTIONS
    # =========================
    @admin.display(description="Workflow Options")
    def workflow_options(self, assessment):
        return ", ".join(
            assessment.repetitive_activities or []
        ) or "-"

    # =========================
    # WORKFLOW NOTES
    # =========================
    @admin.display(description="Workflow Notes")
    def workflow_answer(self, assessment):
        return assessment.workflow_notes or "-"

    # =========================
    # CHALLENGES
    # =========================
    @admin.display(description="Challenges")
    def selected_challenges(self, assessment):
        return ", ".join(
            assessment.challenges or []
        ) or "-"

    # =========================
    # CHALLENGE NOTES
    # =========================
    @admin.display(description="Challenge Notes")
    def challenge_answer(self, assessment):
        return assessment.challenge_notes or "-"


# =====================================================
# LEAD ADMIN
# =====================================================

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):

    list_display = (
        "company_name",
        "name",
        "email",
        "designation",
        "industry",
        "company_size",
        "consent_given",
        "full_report_sent",
        "full_report_sent_at",
        "created_at",
    )

    list_filter = (
        "industry",
        "company_size",
        "consent_given",
        "full_report_sent",
        "created_at",
    )

    search_fields = (
        "company_name",
        "name",
        "email",
        "designation",
    )

    ordering = ("-created_at",)

    date_hierarchy = "created_at"

    list_per_page = 25

    readonly_fields = (
        "id",
        "created_at",
        "full_report_sent_at",
    )


# =====================================================
# ASSESSMENT REPORT ADMIN
# =====================================================

@admin.register(AssessmentReport)
class AssessmentReportAdmin(admin.ModelAdmin):

    list_display = (
        "lead",
        "overall_score",
        "estimated_hours_saved_monthly",
        "estimated_cost_saved_monthly_inr",
        "generated_at",
    )

    list_filter = (
        "generated_at",
    )

    search_fields = (
        "lead__name",
        "lead__email",
        "lead__company_name",
    )

    ordering = ("-generated_at",)

    date_hierarchy = "generated_at"

    list_per_page = 25

    readonly_fields = (
        "id",
        "generated_at",
    )