import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import Assessment, Lead, AssessmentReport


# =====================================================
# ADMIN HELPERS
# =====================================================


def format_admin_value(value):
    """Return CSV-friendly values for list/dict/bool fields."""
    if value is None:
        return ""

    if isinstance(value, bool):
        return "Yes" if value else "No"

    if isinstance(value, (list, tuple)):
        return ", ".join(str(item) for item in value)

    if isinstance(value, dict):
        return ", ".join(
            f"{key}: {val}" for key, val in value.items()
        )

    return str(value)


def get_lead_report_status(lead):
    """Return a readable report status for admin display."""
    if getattr(lead, "full_report_sent", False):
        return "Full report sent"

    if getattr(lead, "prelim_report_sent", False):
        return "Preliminary report sent"

    return "Not sent"


def get_lead_readiness_score(lead):
    """Return related overall readiness score for a lead."""
    report = getattr(lead, "assessment_report", None)
    if report is None:
        return "-"

    return report.overall_score


def get_lead_readiness_level(lead):
    """Return related readiness level for a lead."""
    report = getattr(lead, "assessment_report", None)
    if report is None:
        return "-"

    summary = report.ai_summary or ""
    if "Readiness Level:" in summary:
        return summary.split("Readiness Level:")[-1].strip()

    return "-"


# =====================================================
# ASSESSMENT ADMIN
# =====================================================

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
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

    list_filter = (
        "industry",
        "company_size",
        "automation_level",
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
    )

    fieldsets = (
        (
            "Lead Information",
            {
                "fields": (
                    "name",
                    "email",
                    "company_name",
                    "designation",
                    "industry",
                    "company_size",
                )
            },
        ),
        (
            "Assessment Information",
            {
                "fields": (
                    "departments",
                    "automation_level",
                    "repetitive_activities",
                    "workflow_notes",
                    "challenges",
                    "challenge_notes",
                )
            },
        ),
        (
            "Meta",
            {
                "fields": (
                    "id",
                    "created_at",
                )
            },
        ),
    )

    @admin.display(description="Workflow Options")
    def workflow_options(self, assessment):
        return ", ".join(
            assessment.repetitive_activities or []
        ) or "-"

    @admin.display(description="Workflow Notes")
    def workflow_answer(self, assessment):
        return assessment.workflow_notes or "-"

    @admin.display(description="Challenges")
    def selected_challenges(self, assessment):
        return ", ".join(
            assessment.challenges or []
        ) or "-"

    @admin.display(description="Challenge Notes")
    def challenge_answer(self, assessment):
        return assessment.challenge_notes or "-"


# =====================================================
# LEAD ADMIN
# =====================================================

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "email",
        "company_name",
        "industry",
        "company_size",
        "readiness_score",
        "readiness_level",
        "report_status",
        "created_at",
    )

    list_filter = (
        "industry",
        "company_size",
        "automation_level",
        "consent_given",
        "full_report_sent",
        "created_at",
    )

    search_fields = (
        "name",
        "email",
        "company_name",
        "designation",
        "industry",
    )

    ordering = ("-created_at",)

    date_hierarchy = "created_at"

    list_per_page = 25

    readonly_fields = (
        "id",
        "created_at",
        "full_report_sent_at",
        "readiness_score",
        "readiness_level",
        "report_status",
    )

    fieldsets = (
        (
            "Lead Information",
            {
                "fields": (
                    "name",
                    "email",
                    "company_name",
                    "designation",
                    "industry",
                    "company_size",
                )
            },
        ),
        (
            "Assessment Information",
            {
                "fields": (
                    "departments_selected",
                    "automation_level",
                    "repetitive_activities",
                    "workflow_notes",
                    "challenges",
                    "challenge_notes",
                )
            },
        ),
        (
            "Assessment Results",
            {
                "fields": (
                    "readiness_score",
                    "readiness_level",
                )
            },
        ),
        (
            "Tracking Information",
            {
                "fields": (
                    "consent_given",
                    "utm_source",
                    "utm_medium",
                    "utm_campaign",
                    "ip_address",
                    "created_at",
                )
            },
        ),
        (
            "Report Information",
            {
                "fields": (
                    "report_status",
                    "prelim_report_sent",
                    "full_report_sent",
                    "full_report_sent_at",
                )
            },
        ),
    )

    actions = ["export_selected_leads_as_csv"]

    @admin.display(description="Readiness Score")
    def readiness_score(self, obj):
        return get_lead_readiness_score(obj)

    @admin.display(description="Readiness Level")
    def readiness_level(self, obj):
        return get_lead_readiness_level(obj)

    @admin.display(description="Report Status")
    def report_status(self, obj):
        return get_lead_report_status(obj)

    def export_selected_leads_as_csv(self, request, queryset):
        """Export selected leads as CSV from admin."""
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            'attachment; filename="scout_ai_leads_'
            f'{__import__("datetime").datetime.now().strftime("%Y-%m-%d")}.csv"'
        )

        csv_headers = [
            "ID",
            "Name",
            "Email",
            "Company Name",
            "Designation",
            "Industry",
            "Company Size",
            "Departments",
            "Automation Level",
            "Repetitive Activities",
            "Workflow Notes",
            "Challenges",
            "Challenge Notes",
            "Consent",
            "UTM Source",
            "UTM Medium",
            "UTM Campaign",
            "IP Address",
            "Readiness Score",
            "Readiness Level",
            "Report Status",
            "Full Report Sent",
            "Full Report Sent At",
            "Created At",
        ]

        writer = csv.writer(response)
        writer.writerow(csv_headers)

        for lead in queryset:
            report = getattr(lead, "assessment_report", None)
            writer.writerow(
                [
                    str(lead.id),
                    lead.name,
                    lead.email,
                    lead.company_name,
                    lead.designation,
                    lead.industry,
                    lead.company_size,
                    format_admin_value(lead.departments_selected),
                    lead.automation_level,
                    format_admin_value(lead.repetitive_activities),
                    lead.workflow_notes,
                    format_admin_value(lead.challenges),
                    lead.challenge_notes,
                    "Yes" if lead.consent_given else "No",
                    lead.utm_source,
                    lead.utm_medium,
                    lead.utm_campaign,
                    lead.ip_address or "",
                    report.overall_score if report else "",
                    get_lead_readiness_level(lead),
                    get_lead_report_status(lead),
                    "Yes" if lead.full_report_sent else "No",
                    lead.full_report_sent_at.isoformat() if lead.full_report_sent_at else "",
                    lead.created_at.isoformat() if lead.created_at else "",
                ]
            )

        return response

    export_selected_leads_as_csv.short_description = "Export selected leads as CSV"


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