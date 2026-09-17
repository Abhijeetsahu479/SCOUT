# ============================================================
# SCOUT AI
# Assessment API Views
# ============================================================
#
# This file handles:
#
# 1. Assessment creation
# 2. Assessment listing
# 3. Assessment detail
# 4. Lead creation
# 5. Lead update
# 6. UTM tracking
# 7. Consent tracking
# 8. IP address tracking
# 9. Readiness score calculation
# 10. Readiness level calculation
# 11. Department analysis
# 12. Quick wins
# 13. Recommendations
# 14. ROI calculation
# 15. AssessmentReport creation/update
# 16. PDF report email
#
# IMPORTANT:
# There is NO HTML report email in this file.
#
# ============================================================


# ============================================================
# DJANGO IMPORTS
# ============================================================

from django.db import transaction
from django.utils import timezone


# ============================================================
# DJANGO REST FRAMEWORK IMPORTS
# ============================================================

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


# ============================================================
# LOCAL MODEL IMPORTS
# ============================================================

from .models import (
    Assessment,
    Lead,
    AssessmentReport,
)


# ============================================================
# SERIALIZER IMPORTS
# ============================================================

from .serializers import (
    AssessmentSerializer,
)


# ============================================================
# SERVICE IMPORTS
# ============================================================
#
# IMPORTANT:
# These functions should already exist in your project.
#
# ============================================================

from .services import (
    calculate_readiness_score,
    get_readiness_level,
    calculate_department_analysis,
    generate_quick_wins,
    generate_recommendations,
    calculate_roi_estimate,
)


# ============================================================
# EMAIL SERVICE
# ============================================================
#
# This function should generate and attach the PDF.
#
# Make sure your email service does NOT contain:
#
# html_content = f""" ... """
#
# and does NOT contain:
#
# email.attach_alternative(...)
#
# ============================================================

from .email_service import (
    send_assessment_report_email,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================


def safe_list(value):
    """
    Convert incoming value into a safe list.

    Examples:

    None
        -> []

    []
        -> []

    ["HR", "Finance"]
        -> ["HR", "Finance"]

    "HR"
        -> ["HR"]

    This prevents JSONField related errors.
    """

    if value is None:
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, tuple):
        return list(value)

    if isinstance(value, str):

        if not value.strip():
            return []

        return [value]

    return []


# ============================================================


def safe_text(value, default=""):
    """
    Convert incoming value into safe text.
    """

    if value is None:
        return default

    return str(value).strip()


# ============================================================


def safe_dict(value):
    """
    Convert incoming value into dictionary.
    """

    if isinstance(value, dict):
        return value

    return {}


# ============================================================


def get_client_ip(request):
    """
    Get client IP address.

    Supports normal requests and reverse proxy environments.
    """

    forwarded_for = request.META.get(
        "HTTP_X_FORWARDED_FOR"
    )

    if forwarded_for:

        ip = forwarded_for.split(",")[0].strip()

        if ip:
            return ip

    return request.META.get(
        "REMOTE_ADDR"
    )


# ============================================================


def get_utm_data(request):
    """
    Read UTM/source information from request.

    Supported fields:

    utm_source
    utm_medium
    utm_campaign
    """

    return {
        "utm_source": safe_text(
            request.data.get(
                "utm_source",
                ""
            )
        ),

        "utm_medium": safe_text(
            request.data.get(
                "utm_medium",
                ""
            )
        ),

        "utm_campaign": safe_text(
            request.data.get(
                "utm_campaign",
                ""
            )
        ),
    }


# ============================================================


def get_consent_value(request):
    """
    Read consent value from request.

    Supports:

    True
    False
    "true"
    "false"
    "1"
    "0"
    "yes"
    "no"
    """

    value = request.data.get(
        "consent_given",
        False
    )

    if isinstance(value, bool):
        return value

    if isinstance(value, str):

        value_lower = value.lower().strip()

        if value_lower in [
            "true",
            "1",
            "yes",
            "y",
            "on",
        ]:
            return True

        if value_lower in [
            "false",
            "0",
            "no",
            "n",
            "off",
            "",
        ]:
            return False

    if isinstance(value, int):

        return bool(value)

    return False


# ============================================================


def get_roi_value(
    roi_estimate,
    *keys,
    default=0,
):
    """
    Safely get a value from ROI result.

    This supports multiple possible key names
    so the API does not break if the ROI service
    uses slightly different naming.
    """

    roi_estimate = safe_dict(
        roi_estimate
    )

    for key in keys:

        if key in roi_estimate:

            value = roi_estimate.get(
                key
            )

            if value is not None:

                return value

    return default


# ============================================================


def normalize_roi_estimate(
    roi_estimate
):
    """
    Normalize ROI calculation output.

    Existing ROI service can return keys such as:

    estimated_hours_saved_monthly
    estimated_monthly_savings
    estimated_annual_savings
    implementation_cost
    estimated_roi

    This function safely reads them.
    """

    roi_estimate = safe_dict(
        roi_estimate
    )

    hours_saved = get_roi_value(
        roi_estimate,
        "estimated_hours_saved_monthly",
        "hours_saved_monthly",
        "monthly_hours_saved",
        default=0,
    )

    monthly_savings = get_roi_value(
        roi_estimate,
        "estimated_monthly_savings",
        "monthly_savings",
        "estimated_cost_saved_monthly_inr",
        default=0,
    )

    annual_savings = get_roi_value(
        roi_estimate,
        "estimated_annual_savings",
        "annual_savings",
        default=0,
    )

    implementation_cost = get_roi_value(
        roi_estimate,
        "implementation_cost",
        "estimated_implementation_cost",
        default=0,
    )

    estimated_roi = get_roi_value(
        roi_estimate,
        "estimated_roi",
        "roi",
        default=0,
    )

    return {
        "estimated_hours_saved_monthly": hours_saved,
        "estimated_monthly_savings": monthly_savings,
        "estimated_annual_savings": annual_savings,
        "implementation_cost": implementation_cost,
        "estimated_roi": estimated_roi,
    }


# ============================================================


def build_lead_defaults(
    assessment,
    request,
):
    """
    Build Lead data from Assessment.

    This is the single source of truth for
    creating a new Lead.
    """

    utm_data = get_utm_data(
        request
    )

    consent_given = get_consent_value(
        request
    )

    client_ip = get_client_ip(
        request
    )

    departments = safe_list(
        getattr(
            assessment,
            "departments",
            []
        )
    )

    repetitive_activities = safe_list(
        getattr(
            assessment,
            "repetitive_activities",
            []
        )
    )

    challenges = safe_list(
        getattr(
            assessment,
            "challenges",
            []
        )
    )

    workflow_notes = safe_text(
        getattr(
            assessment,
            "workflow_notes",
            ""
        )
    )

    challenge_notes = safe_text(
        getattr(
            assessment,
            "challenge_notes",
            ""
        )
    )

    return {

        # ----------------------------------------------------
        # Basic information
        # ----------------------------------------------------

        "name": assessment.name,

        "email": assessment.email,

        # ----------------------------------------------------
        # Company information
        # ----------------------------------------------------

        "company_name": (
            assessment.company_name
        ),

        "designation": (
            assessment.designation
        ),

        "industry": (
            assessment.industry
        ),

        "company_size": (
            assessment.company_size
        ),

        # ----------------------------------------------------
        # Assessment information
        # ----------------------------------------------------

        "departments_selected": (
            departments
        ),

        "automation_level": (
            assessment.automation_level
        ),

        "repetitive_activities": (
            repetitive_activities
        ),

        "workflow_notes": (
            workflow_notes
        ),

        "challenges": (
            challenges
        ),

        "challenge_notes": (
            challenge_notes
        ),

        # ----------------------------------------------------
        # Additional notes
        # ----------------------------------------------------

        "additional_notes": (
            challenge_notes
        ),

        # ----------------------------------------------------
        # UTM
        # ----------------------------------------------------

        "utm_source": (
            utm_data["utm_source"]
        ),

        "utm_medium": (
            utm_data["utm_medium"]
        ),

        "utm_campaign": (
            utm_data["utm_campaign"]
        ),

        # ----------------------------------------------------
        # IP
        # ----------------------------------------------------

        "ip_address": client_ip,

        # ----------------------------------------------------
        # Consent
        # ----------------------------------------------------

        "consent_given": consent_given,
    }


# ============================================================


def update_existing_lead(
    lead,
    assessment,
    request,
):
    """
    Update existing Lead with latest Assessment data.
    """

    utm_data = get_utm_data(
        request
    )

    departments = safe_list(
        getattr(
            assessment,
            "departments",
            []
        )
    )

    repetitive_activities = safe_list(
        getattr(
            assessment,
            "repetitive_activities",
            []
        )
    )

    challenges = safe_list(
        getattr(
            assessment,
            "challenges",
            []
        )
    )

    workflow_notes = safe_text(
        getattr(
            assessment,
            "workflow_notes",
            ""
        )
    )

    challenge_notes = safe_text(
        getattr(
            assessment,
            "challenge_notes",
            ""
        )
    )

    # --------------------------------------------------------
    # Basic
    # --------------------------------------------------------

    lead.name = assessment.name

    lead.company_name = (
        assessment.company_name
    )

    lead.designation = (
        assessment.designation
    )

    # --------------------------------------------------------
    # Company
    # --------------------------------------------------------

    lead.industry = (
        assessment.industry
    )

    lead.company_size = (
        assessment.company_size
    )

    # --------------------------------------------------------
    # Departments
    # --------------------------------------------------------

    lead.departments_selected = (
        departments
    )

    # --------------------------------------------------------
    # Automation
    # --------------------------------------------------------

    lead.automation_level = (
        assessment.automation_level
    )

    # --------------------------------------------------------
    # Repetitive activities
    # --------------------------------------------------------

    lead.repetitive_activities = (
        repetitive_activities
    )

    # --------------------------------------------------------
    # Workflow
    # --------------------------------------------------------

    lead.workflow_notes = (
        workflow_notes
    )

    # --------------------------------------------------------
    # Challenges
    # --------------------------------------------------------

    lead.challenges = (
        challenges
    )

    lead.challenge_notes = (
        challenge_notes
    )

    # --------------------------------------------------------
    # Additional notes
    # --------------------------------------------------------

    lead.additional_notes = (
        challenge_notes
    )

    # --------------------------------------------------------
    # UTM
    # --------------------------------------------------------

    if utm_data["utm_source"]:

        lead.utm_source = (
            utm_data["utm_source"]
        )

    if utm_data["utm_medium"]:

        lead.utm_medium = (
            utm_data["utm_medium"]
        )

    if utm_data["utm_campaign"]:

        lead.utm_campaign = (
            utm_data["utm_campaign"]
        )

    # --------------------------------------------------------
    # IP
    # --------------------------------------------------------

    client_ip = get_client_ip(
        request
    )

    if client_ip:

        lead.ip_address = client_ip

    # --------------------------------------------------------
    # Consent
    # --------------------------------------------------------

    if "consent_given" in request.data:

        lead.consent_given = (
            get_consent_value(request)
        )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    lead.save()

    return lead


# ============================================================


def create_or_update_lead(
    assessment,
    request,
):
    """
    Create a Lead if email does not exist.

    Otherwise update existing Lead.
    """

    lead, created = (
        Lead.objects.get_or_create(
            email=assessment.email,
            defaults=build_lead_defaults(
                assessment,
                request,
            ),
        )
    )

    if not created:

        lead = update_existing_lead(
            lead=lead,
            assessment=assessment,
            request=request,
        )

    return lead, created


# ============================================================


def calculate_assessment_results(
    assessment
):
    """
    Run all SCOUT AI calculations.

    Returns one dictionary.
    """

    # --------------------------------------------------------
    # Readiness score
    # --------------------------------------------------------

    score = calculate_readiness_score(
        assessment
    )

    # --------------------------------------------------------
    # Readiness level
    # --------------------------------------------------------

    level = get_readiness_level(
        score
    )

    # --------------------------------------------------------
    # Department analysis
    # --------------------------------------------------------

    department_analysis = (
        calculate_department_analysis(
            assessment
        )
    )

    # --------------------------------------------------------
    # Quick wins
    # --------------------------------------------------------

    quick_wins = generate_quick_wins(
        assessment
    )

    # --------------------------------------------------------
    # Recommendations
    # --------------------------------------------------------

    recommendations = (
        generate_recommendations(
            assessment
        )
    )

    # --------------------------------------------------------
    # ROI
    # --------------------------------------------------------

    roi_estimate = calculate_roi_estimate(
        assessment
    )

    # --------------------------------------------------------
    # Return
    # --------------------------------------------------------

    return {
        "score": score,

        "level": level,

        "department_analysis": (
            department_analysis
        ),

        "quick_wins": (
            quick_wins
        ),

        "recommendations": (
            recommendations
        ),

        "roi_estimate": (
            roi_estimate
        ),
    }


# ============================================================


def create_or_update_assessment_report(
    lead,
    results,
):
    """
    Create or update AssessmentReport.
    """

    score = results["score"]

    level = results["level"]

    department_analysis = (
        results["department_analysis"]
    )

    quick_wins = (
        results["quick_wins"]
    )

    recommendations = (
        results["recommendations"]
    )

    roi_estimate = normalize_roi_estimate(
        results["roi_estimate"]
    )

    # --------------------------------------------------------
    # Update or create
    # --------------------------------------------------------

    report, created = (
        AssessmentReport.objects.update_or_create(

            lead=lead,

            defaults={

                # --------------------------------------------
                # Score
                # --------------------------------------------

                "overall_score": score,

                # --------------------------------------------
                # Department analysis
                # --------------------------------------------

                "department_scores": (
                    department_analysis
                    or {}
                ),

                # --------------------------------------------
                # Automation
                # --------------------------------------------

                "should_automate": (
                    quick_wins
                    or []
                ),

                "should_not_automate": [],

                # --------------------------------------------
                # ROI
                # --------------------------------------------

                "estimated_hours_saved_monthly": int(
                    roi_estimate.get(
                        "estimated_hours_saved_monthly",
                        0
                    )
                    or 0
                ),

                "estimated_cost_saved_monthly_inr": (
                    roi_estimate.get(
                        "estimated_monthly_savings",
                        0
                    )
                    or 0
                ),

                # --------------------------------------------
                # AI summary
                # --------------------------------------------

                "ai_summary": (
                    f"Readiness Level: {level}"
                ),

                # --------------------------------------------
                # Raw result
                # --------------------------------------------

                "raw_ai_response": {

                    "readiness_score": (
                        score
                    ),

                    "readiness_level": (
                        level
                    ),

                    "department_analysis": (
                        department_analysis
                    ),

                    "quick_wins": (
                        quick_wins
                    ),

                    "recommendations": (
                        recommendations
                    ),

                    "roi_estimate": (
                        results[
                            "roi_estimate"
                        ]
                    ),
                },
            },
        )
    )

    return report, created


# ============================================================


def get_lead_report_status(
    lead,
):
    """Return a readable report status for a lead."""

    if not lead:
        return "Not sent"

    if lead.full_report_sent:
        return "Full report sent"

    if lead.prelim_report_sent:
        return "Preliminary report sent"

    return "Not sent"


def build_response_data(
    assessment,
    results,
    lead,
    report,
):
    """
    Build final API response.
    """

    data = AssessmentSerializer(
        assessment
    ).data

    # --------------------------------------------------------
    # Calculation results
    # --------------------------------------------------------

    data["readiness_score"] = (
        results["score"]
    )

    data["readiness_level"] = (
        results["level"]
    )

    data["department_analysis"] = (
        results["department_analysis"]
    )

    data["quick_wins"] = (
        results["quick_wins"]
    )

    data["recommendations"] = (
        results["recommendations"]
    )

    data["roi_estimate"] = (
        results["roi_estimate"]
    )

    # --------------------------------------------------------
    # IDs
    # --------------------------------------------------------

    data["lead_id"] = str(
        lead.id
    )

    data["report_id"] = str(
        report.id
    )

    # --------------------------------------------------------
    # Lead status
    # --------------------------------------------------------

    data["lead_created"] = (
        False
    )

    if lead:

        data["lead_created"] = (
            True
        )

    return data


# ============================================================
# ASSESSMENT LIST / CREATE VIEW
# ============================================================


class AssessmentListCreateView(
    APIView
):
    """
    GET:
        Return all assessments.

    POST:
        Create assessment,
        calculate readiness,
        create/update lead,
        create/update report,
        send PDF report.
    """

    # ========================================================
    # GET
    # ========================================================

    def get(
        self,
        request,
    ):
        """
        Return all assessments.
        """

        assessments = (
            Assessment.objects.all()
            .order_by("-created_at")
        )

        serializer = AssessmentSerializer(
            assessments,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    # ========================================================
    # POST
    # ========================================================

    def post(
        self,
        request,
    ):
        """
        Create a new assessment.
        """

        # ----------------------------------------------------
        # SERIALIZE INPUT
        # ----------------------------------------------------

        serializer = AssessmentSerializer(
            data=request.data
        )

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if not serializer.is_valid():

            return Response(
                {
                    "success": False,
                    "error": "Validation failed.",
                    "details": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ----------------------------------------------------
        # DATABASE TRANSACTION
        # ----------------------------------------------------

        try:

            with transaction.atomic():

                # ============================================
                # CREATE ASSESSMENT
                # ============================================

                assessment = serializer.save()

                # ============================================
                # CALCULATIONS
                # ============================================

                results = (
                    calculate_assessment_results(
                        assessment
                    )
                )

                # ============================================
                # CREATE / UPDATE LEAD
                # ============================================

                lead, lead_created = (
                    create_or_update_lead(
                        assessment=assessment,
                        request=request,
                    )
                )

                # ============================================
                # CREATE / UPDATE REPORT
                # ============================================

                report, report_created = (
                    create_or_update_assessment_report(
                        lead=lead,
                        results=results,
                    )
                )

        # ----------------------------------------------------
        # DATABASE / CALCULATION ERROR
        # ----------------------------------------------------

        except Exception as error:

            print(
                "Assessment processing failed:",
                error,
            )

            return Response(
                {
                    "success": False,
                    "error": (
                        "Assessment processing failed."
                    ),
                    "details": str(error),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # ====================================================
        # SEND CUSTOMER PDF REPORT
        # ====================================================

        email_sent = False

        try:

            send_assessment_report_email(

                assessment=assessment,
                lead=lead,

                readiness_score=(
                    results["score"]
                ),

                readiness_level=(
                    results["level"]
                ),

                department_analysis=(
                    results[
                        "department_analysis"
                    ]
                ),

                quick_wins=(
                    results["quick_wins"]
                ),

                recommendations=(
                    results[
                        "recommendations"
                    ]
                ),

                roi_estimate=(
                    results["roi_estimate"]
                ),
            )

            # -----------------------------------------------
            # Email success
            # -----------------------------------------------

            email_sent = True

            lead.full_report_sent = True

            lead.full_report_sent_at = (
                timezone.now()
            )

            lead.save(
                update_fields=[
                    "full_report_sent",
                    "full_report_sent_at",
                ]
            )

            print(
                "Assessment PDF report email sent successfully"
            )

        # ----------------------------------------------------
        # EMAIL ERROR
        # ----------------------------------------------------

        except Exception as error:

            print(
                "Assessment PDF report email failed:",
                error,
            )

        # ====================================================
        # BUILD RESPONSE
        # ====================================================

        response_data = (
            build_response_data(
                assessment=assessment,
                results=results,
                lead=lead,
                report=report,
            )
        )

        # ----------------------------------------------------
        # Additional metadata
        # ----------------------------------------------------

        response_data["success"] = True

        response_data["lead_created"] = (
            lead_created
        )

        response_data["report_created"] = (
            report_created
        )

        response_data["email_sent"] = (
            email_sent
        )

        # ====================================================
        # RETURN
        # ====================================================

        return Response(
            response_data,
            status=status.HTTP_201_CREATED,
        )


# ============================================================
# ASSESSMENT DETAIL VIEW
# ============================================================


class AssessmentDetailView(
    APIView
):
    """
    GET:
        Return one assessment with calculated results.
    """

    # ========================================================
    # GET
    # ========================================================

    def get(
        self,
        request,
        pk,
    ):
        """
        Get assessment by primary key.
        """

        # ----------------------------------------------------
        # FIND ASSESSMENT
        # ----------------------------------------------------

        try:

            assessment = (
                Assessment.objects.get(
                    pk=pk
                )
            )

        except Assessment.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "error": (
                        "Assessment not found."
                    ),
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # ----------------------------------------------------
        # CALCULATE RESULTS
        # ----------------------------------------------------

        try:

            results = (
                calculate_assessment_results(
                    assessment
                )
            )

        except Exception as error:

            print(
                "Assessment calculation failed:",
                error,
            )

            return Response(
                {
                    "success": False,
                    "error": (
                        "Unable to calculate assessment results."
                    ),
                    "details": str(error),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # ----------------------------------------------------
        # SERIALIZE
        # ----------------------------------------------------

        data = AssessmentSerializer(
            assessment
        ).data

        # ----------------------------------------------------
        # RESULTS
        # ----------------------------------------------------

        data["readiness_score"] = (
            results["score"]
        )

        data["readiness_level"] = (
            results["level"]
        )

        data["department_analysis"] = (
            results[
                "department_analysis"
            ]
        )

        data["quick_wins"] = (
            results["quick_wins"]
        )

        data["recommendations"] = (
            results[
                "recommendations"
            ]
        )

        data["roi_estimate"] = (
            results["roi_estimate"]
        )

        # ----------------------------------------------------
        # Lead information
        # ----------------------------------------------------

        try:

            lead = Lead.objects.get(
                email=assessment.email
            )

            data["lead_id"] = str(
                lead.id
            )

            data["full_report_sent"] = (
                lead.full_report_sent
            )

            data["full_report_sent_at"] = (
                lead.full_report_sent_at
            )

            # -----------------------------------------------
            # Lead information
            # -----------------------------------------------

            data["lead"] = {

                "id": str(
                    lead.id
                ),

                "name": lead.name,

                "email": lead.email,

                "company_name": (
                    lead.company_name
                ),

                "designation": (
                    lead.designation
                ),

                "industry": (
                    lead.industry
                ),

                "company_size": (
                    lead.company_size
                ),

                "departments": (
                    lead.departments_selected
                ),

                "automation_level": (
                    lead.automation_level
                ),

                "repetitive_activities": (
                    lead.repetitive_activities
                ),

                "workflow_notes": (
                    lead.workflow_notes
                ),

                "challenges": (
                    lead.challenges
                ),

                "challenge_notes": (
                    lead.challenge_notes
                ),

                "consent_given": (
                    lead.consent_given
                ),

                "utm_source": (
                    lead.utm_source
                ),

                "utm_medium": (
                    lead.utm_medium
                ),

                "utm_campaign": (
                    lead.utm_campaign
                ),

                "ip_address": (
                    lead.ip_address
                ),

                "created_at": (
                    lead.created_at
                ),

                "report_status": (
                    get_lead_report_status(
                        lead
                    )
                ),
            }

        except Lead.DoesNotExist:

            data["lead_id"] = None

            data["lead"] = None

        # ----------------------------------------------------
        # Assessment report
        # ----------------------------------------------------

        try:

            report = (
                AssessmentReport.objects.get(
                    lead__email=assessment.email
                )
            )

            data["report_id"] = str(
                report.id
            )

            data["assessment_report"] = {

                "id": str(
                    report.id
                ),

                "overall_score": (
                    report.overall_score
                ),

                "department_scores": (
                    report.department_scores
                ),

                "should_automate": (
                    report.should_automate
                ),

                "should_not_automate": (
                    report.should_not_automate
                ),

                "estimated_hours_saved_monthly": (
                    report.estimated_hours_saved_monthly
                ),

                "estimated_cost_saved_monthly_inr": (
                    str(
                        report.estimated_cost_saved_monthly_inr
                    )
                ),

                "ai_summary": (
                    report.ai_summary
                ),

                "generated_at": (
                    report.generated_at
                ),
            }

        except AssessmentReport.DoesNotExist:

            data["report_id"] = None

            data["assessment_report"] = None

        # ----------------------------------------------------
        # Success
        # ----------------------------------------------------

        data["success"] = True

        return Response(
            data,
            status=status.HTTP_200_OK,
        )


# ============================================================
# FULL REPORT VIEW
# ============================================================


class FullReportView(
    AssessmentDetailView
):
    """
    Token-protected alias for the project brief's full report API.
    """

    authentication_classes = [
        TokenAuthentication,
    ]
    permission_classes = [
        IsAuthenticated,
    ]


# ============================================================
# OPTIONAL HEALTH CHECK
# ============================================================
#
# This endpoint can be used to check whether the
# Django backend is running.
#
# URL example:
#
# /api/health/
#
# ============================================================


class HealthCheckView(
    APIView
):
    """
    Simple backend health check.
    """

    def get(
        self,
        request,
    ):
        return Response(
            {
                "status": "ok",
            },
            status=status.HTTP_200_OK,
        )


# ============================================================
# OPTIONAL LEAD LIST VIEW
# ============================================================
#
# Useful for testing Lead data from API.
#
# ============================================================


class LeadListView(
    APIView
):
    """
    Return leads.

    This is mainly useful for development/admin
    testing.
    """

    def get(
        self,
        request,
    ):
        """
        Return latest leads.
        """

        leads = (
            Lead.objects.all()
            .order_by("-created_at")
        )

        data = []

        for lead in leads:

            data.append({

                "id": str(
                    lead.id
                ),

                "name": lead.name,

                "email": lead.email,

                "company_name": (
                    lead.company_name
                ),

                "designation": (
                    lead.designation
                ),

                "industry": (
                    lead.industry
                ),

                "company_size": (
                    lead.company_size
                ),

                "departments": (
                    lead.departments_selected
                ),

                "automation_level": (
                    lead.automation_level
                ),

                "repetitive_activities": (
                    lead.repetitive_activities
                ),

                "workflow_notes": (
                    lead.workflow_notes
                ),

                "challenges": (
                    lead.challenges
                ),

                "challenge_notes": (
                    lead.challenge_notes
                ),

                "additional_notes": (
                    lead.additional_notes
                ),

                "consent_given": (
                    lead.consent_given
                ),

                "utm_source": (
                    lead.utm_source
                ),

                "utm_medium": (
                    lead.utm_medium
                ),

                "utm_campaign": (
                    lead.utm_campaign
                ),

                "ip_address": (
                    lead.ip_address
                ),

                "created_at": (
                    lead.created_at
                ),

                "report_status": (
                    get_lead_report_status(
                        lead
                    )
                ),

                "full_report_sent": (
                    lead.full_report_sent
                ),

                "full_report_sent_at": (
                    lead.full_report_sent_at
                ),
            })

        return Response(
            {
                "success": True,
                "count": len(data),
                "leads": data,
            },
            status=status.HTTP_200_OK,
        )


# ============================================================
# OPTIONAL LEAD DETAIL VIEW
# ============================================================


class LeadDetailView(
    APIView
):
    """
    Return one Lead using UUID.
    """

    def get(
        self,
        request,
        pk,
    ):
        """
        Get lead.
        """

        try:

            lead = Lead.objects.get(
                pk=pk
            )

        except Lead.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "error": "Lead not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # ----------------------------------------------------
        # Base lead
        # ----------------------------------------------------

        data = {

            "id": str(
                lead.id
            ),

            "name": lead.name,

            "email": lead.email,

            "company_name": (
                lead.company_name
            ),

            "designation": (
                lead.designation
            ),

            "industry": (
                lead.industry
            ),

            "company_size": (
                lead.company_size
            ),

            "departments": (
                lead.departments_selected
            ),

            "automation_level": (
                lead.automation_level
            ),

            "repetitive_activities": (
                lead.repetitive_activities
            ),

            "workflow_notes": (
                lead.workflow_notes
            ),

            "challenges": (
                lead.challenges
            ),

            "challenge_notes": (
                lead.challenge_notes
            ),

            "additional_notes": (
                lead.additional_notes
            ),

            "consent_given": (
                lead.consent_given
            ),

            "utm_source": (
                lead.utm_source
            ),

            "utm_medium": (
                lead.utm_medium
            ),

            "utm_campaign": (
                lead.utm_campaign
            ),

            "ip_address": (
                lead.ip_address
            ),

            "created_at": (
                lead.created_at
            ),

            "report_status": (
                get_lead_report_status(
                    lead
                )
            ),

            "prelim_report_sent": (
                lead.prelim_report_sent
            ),

            "full_report_sent": (
                lead.full_report_sent
            ),

            "full_report_sent_at": (
                lead.full_report_sent_at
            ),
        }

        # ----------------------------------------------------
        # Assessment Report
        # ----------------------------------------------------

        try:

            report = (
                AssessmentReport.objects.get(
                    lead=lead
                )
            )

            data["assessment_report"] = {

                "id": str(
                    report.id
                ),

                "overall_score": (
                    report.overall_score
                ),

                "department_scores": (
                    report.department_scores
                ),

                "should_automate": (
                    report.should_automate
                ),

                "should_not_automate": (
                    report.should_not_automate
                ),

                "estimated_hours_saved_monthly": (
                    report.estimated_hours_saved_monthly
                ),

                "estimated_cost_saved_monthly_inr": (
                    str(
                        report.estimated_cost_saved_monthly_inr
                    )
                ),

                "ai_summary": (
                    report.ai_summary
                ),

                "generated_at": (
                    report.generated_at
                ),
            }

        except AssessmentReport.DoesNotExist:

            data["assessment_report"] = None

        # ----------------------------------------------------
        # Success
        # ----------------------------------------------------

        data["success"] = True

        return Response(
            data,
            status=status.HTTP_200_OK,
        )


# ============================================================
# END OF VIEWS.PY
# ============================================================