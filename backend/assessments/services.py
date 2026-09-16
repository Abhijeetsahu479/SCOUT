# =========================================================
# READINESS SCORE ENGINE
# =========================================================

def calculate_readiness_score(assessment):
    score = 0

    automation_scores = {
        "mostly_manual": 10,
        "partially_automated": 18,
        "somewhat_automated": 24,
        "highly_automated": 30,
    }

    score += automation_scores.get(
        assessment.automation_level,
        10,
    )

    activity_count = len(assessment.repetitive_activities or [])
    score += min(activity_count * 5, 20)

    department_count = len(assessment.departments or [])
    score += min(department_count * 5, 15)

    challenge_count = len(assessment.challenges or [])
    score += min(challenge_count * 5, 20)

    if assessment.workflow_notes:
        score += 15
    else:
        score += 5

    return min(score, 100)


def get_readiness_level(score):
    if score >= 80:
        return "Highly Ready"

    if score >= 60:
        return "Ready"

    if score >= 40:
        return "Developing"

    return "Early Stage"


# =========================================================
# DEPARTMENT ANALYSIS ENGINE
# =========================================================

DEPARTMENT_ANALYSIS = {
    "hr_payroll": {
        "name": "HR & Payroll",
        "opportunities": [
            "Employee data entry",
            "Payroll processing",
            "HR reporting",
            "Employee onboarding",
        ],
    },
    "sales_crm": {
        "name": "Sales & CRM",
        "opportunities": [
            "Lead management",
            "CRM data entry",
            "Sales reporting",
            "Follow-up automation",
        ],
    },
    "finance_accounting": {
        "name": "Finance & Accounting",
        "opportunities": [
            "Invoice processing",
            "Expense management",
            "Financial reporting",
            "Document processing",
        ],
    },
    "operations": {
        "name": "Operations",
        "opportunities": [
            "Process tracking",
            "Task automation",
            "Operations reporting",
            "Workflow automation",
        ],
    },
    "it": {
        "name": "IT",
        "opportunities": [
            "Ticket management",
            "System monitoring",
            "IT reporting",
            "User support automation",
        ],
    },
    "customer_support": {
        "name": "Customer Support",
        "opportunities": [
            "Ticket classification",
            "Customer response automation",
            "Support reporting",
            "FAQ automation",
        ],
    },
    "marketing": {
        "name": "Marketing",
        "opportunities": [
            "Campaign reporting",
            "Lead tracking",
            "Content workflows",
            "Marketing analytics",
        ],
    },
}


def calculate_department_analysis(assessment):
    analysis = []

    departments = assessment.departments or []
    activity_count = len(assessment.repetitive_activities or [])
    challenge_count = len(assessment.challenges or [])

    for department in departments:
        department_info = DEPARTMENT_ANALYSIS.get(
            department,
            {
                "name": department.replace("_", " ").title(),
                "opportunities": [
                    "Workflow automation",
                    "Data processing",
                    "Reporting automation",
                ],
            },
        )

        score = 40

        score += min(activity_count * 10, 20)
        score += min(challenge_count * 10, 20)

        if assessment.workflow_notes:
            score += 20

        score = min(score, 100)

        analysis.append(
            {
                "department": department_info["name"],
                "score": score,
                "opportunities": department_info["opportunities"],
            }
        )

    return analysis


# =========================================================
# QUICK WINS + RECOMMENDATIONS ENGINE
# =========================================================

ACTIVITY_RECOMMENDATIONS = {
    "data_entry": {
        "quick_win": "Automate repetitive data entry tasks",
        "recommendation": (
            "Use form automation, OCR, or workflow automation "
            "to reduce manual data entry."
        ),
        "impact": "High",
    },
    "reporting": {
        "quick_win": "Automate recurring reports",
        "recommendation": (
            "Create automated dashboards and scheduled reports "
            "instead of preparing reports manually."
        ),
        "impact": "High",
    },
    "documents": {
        "quick_win": "Automate document processing",
        "recommendation": (
            "Use document extraction and classification "
            "to reduce manual document handling."
        ),
        "impact": "High",
    },
    "email": {
        "quick_win": "Automate repetitive email workflows",
        "recommendation": (
            "Use automated email triggers, templates, "
            "and workflow rules for repetitive communication."
        ),
        "impact": "Medium",
    },
    "data_processing": {
        "quick_win": "Streamline data processing",
        "recommendation": (
            "Automate repetitive data transformation "
            "and validation workflows."
        ),
        "impact": "High",
    },
}


CHALLENGE_RECOMMENDATIONS = {
    "time_consuming": {
        "quick_win": (
            "Identify and automate the most "
            "time-consuming workflows"
        ),
        "recommendation": (
            "Prioritize high-volume repetitive "
            "processes for automation."
        ),
        "impact": "High",
    },
    "manual_data": {
        "quick_win": "Reduce manual data handling",
        "recommendation": (
            "Introduce automated data capture, "
            "validation, and synchronization."
        ),
        "impact": "High",
    },
    "communication": {
        "quick_win": "Automate repetitive communication",
        "recommendation": (
            "Use automated notifications, email workflows, "
            "and communication templates."
        ),
        "impact": "Medium",
    },
    "errors": {
        "quick_win": "Reduce manual errors",
        "recommendation": (
            "Add automated validation and workflow checks "
            "to reduce human errors."
        ),
        "impact": "High",
    },
    "slow_process": {
        "quick_win": "Improve slow business processes",
        "recommendation": (
            "Map the workflow and automate repetitive "
            "approval and processing steps."
        ),
        "impact": "High",
    },
}


def generate_quick_wins(assessment):
    quick_wins = []

    activities = assessment.repetitive_activities or []
    challenges = assessment.challenges or []

    for activity in activities:
        recommendation = ACTIVITY_RECOMMENDATIONS.get(activity)

        if recommendation:
            quick_wins.append(
                {
                    "title": recommendation["quick_win"],
                    "impact": recommendation["impact"],
                    "source": "repetitive_activity",
                }
            )

    for challenge in challenges:
        recommendation = CHALLENGE_RECOMMENDATIONS.get(challenge)

        if recommendation:
            quick_wins.append(
                {
                    "title": recommendation["quick_win"],
                    "impact": recommendation["impact"],
                    "source": "challenge",
                }
            )

    # Remove duplicate quick wins
    unique_quick_wins = []
    seen_titles = set()

    for item in quick_wins:
        if item["title"] not in seen_titles:
            unique_quick_wins.append(item)
            seen_titles.add(item["title"])

    return unique_quick_wins[:6]


def generate_recommendations(assessment):
    recommendations = []

    activities = assessment.repetitive_activities or []
    challenges = assessment.challenges or []
    departments = assessment.departments or []

    for activity in activities:
        recommendation = ACTIVITY_RECOMMENDATIONS.get(activity)

        if recommendation:
            recommendations.append(
                {
                    "recommendation": recommendation["recommendation"],
                    "impact": recommendation["impact"],
                    "area": activity,
                }
            )

    for challenge in challenges:
        recommendation = CHALLENGE_RECOMMENDATIONS.get(challenge)

        if recommendation:
            recommendations.append(
                {
                    "recommendation": recommendation["recommendation"],
                    "impact": recommendation["impact"],
                    "area": challenge,
                }
            )

    if departments:
        recommendations.append(
            {
                "recommendation": (
                    "Start with one high-impact workflow "
                    "in each selected department and measure "
                    "the automation outcome."
                ),
                "impact": "High",
                "area": "department_strategy",
            }
        )

    # Remove duplicates
    unique_recommendations = []
    seen_recommendations = set()

    for item in recommendations:
        text = item["recommendation"]

        if text not in seen_recommendations:
            unique_recommendations.append(item)
            seen_recommendations.add(text)

    return unique_recommendations[:8]
def calculate_roi_estimate(assessment):
    """
    Estimate potential ROI based on repetitive activities,
    challenges, and selected departments.

    This is an indicative estimate, not a financial guarantee.
    """

    activity_hours = {
        "data_entry": 20,
        "reporting": 16,
        "documents": 18,
        "email": 12,
        "data_processing": 20,
    }

    challenge_hours = {
        "time_consuming": 12,
        "manual_data": 15,
        "communication": 10,
        "errors": 8,
        "slow_process": 14,
    }

    # Assumption:
    # Average employee/process cost = ₹500 per hour
    hourly_cost = 500

    activities = assessment.repetitive_activities or []
    challenges = assessment.challenges or []
    departments = assessment.departments or []

    estimated_hours = 0

    # Hours from repetitive activities
    for activity in activities:
        estimated_hours += activity_hours.get(activity, 10)

    # Hours from challenges
    for challenge in challenges:
        estimated_hours += challenge_hours.get(challenge, 8)

    # Department complexity adjustment
    department_bonus = min(len(departments) * 5, 20)

    estimated_hours += department_bonus

    # Automation can realistically recover around 60% of
    # the identified manual effort.
    estimated_hours_saved = round(
        estimated_hours * 0.60
    )

    estimated_monthly_savings = (
        estimated_hours_saved * hourly_cost
    )

    estimated_annual_savings = (
        estimated_monthly_savings * 12
    )

    # Indicative implementation cost assumption
    estimated_implementation_cost = 100000

    if estimated_implementation_cost > 0:
        estimated_roi_percentage = round(
            (
                (
                    estimated_annual_savings
                    - estimated_implementation_cost
                )
                / estimated_implementation_cost
            )
            * 100
        )
    else:
        estimated_roi_percentage = 0

    return {
        "estimated_hours_saved_monthly": estimated_hours_saved,
        "estimated_hourly_cost": hourly_cost,
        "estimated_monthly_savings": estimated_monthly_savings,
        "estimated_annual_savings": estimated_annual_savings,
        "estimated_implementation_cost": estimated_implementation_cost,
        "estimated_roi_percentage": estimated_roi_percentage,
        "assumptions": {
            "hourly_cost": (
                "₹500 estimated average hourly cost"
            ),
            "automation_recovery": (
                "60% of identified manual effort"
            ),
            "implementation_cost": (
                "₹100,000 indicative implementation cost"
            ),
        },
    }

from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.utils.html import escape


def _format_department_analysis_text(department_analysis):
    if not department_analysis:
        return "No department analysis available."

    lines = []
    for item in department_analysis:
        department = item.get("department", "Department")
        score = item.get("score", 0)
        opportunities = item.get("opportunities", []) or []

        lines.append(f"{department} - Score: {score}/100")
        for opportunity in opportunities:
            lines.append(f"  - {opportunity}")

    return "\n".join(lines)


def _format_quick_wins_text(quick_wins):
    if not quick_wins:
        return "No quick wins available."

    lines = []
    for item in quick_wins:
        title = item.get("title", "Quick win")
        impact = item.get("impact", "")
        lines.append(f"- {title} | Impact: {impact}")

    return "\n".join(lines)


def _format_recommendations_text(recommendations):
    if not recommendations:
        return "No recommendations available."

    lines = []
    for item in recommendations:
        recommendation = item.get("recommendation", "")
        impact = item.get("impact", "")
        area = item.get("area", "")
        lines.append(
            f"- {recommendation} | Area: {area} | Impact: {impact}"
        )

    return "\n".join(lines)


def _format_department_analysis_html(department_analysis):
    if not department_analysis:
        return "<p>No department analysis available.</p>"

    blocks = []
    for item in department_analysis:
        department = escape(str(item.get("department", "Department")))
        score = escape(str(item.get("score", 0)))
        opportunities = item.get("opportunities", []) or []

        opportunity_items = "".join(
            f"<li>{escape(str(opportunity))}</li>"
            for opportunity in opportunities
        )

        blocks.append(
            f"""
            <div class="analysis-card" style="
                margin:10px 0;
                padding:18px;
                background:#f5f8f9;
                border-radius:10px;
            ">
                <strong>{department}</strong>
                <p style="margin:8px 0;">
                    Readiness Score:
                    <strong>{score}/100</strong>
                </p>
                <p><strong>Opportunities:</strong></p>
                <ul>{opportunity_items}</ul>
            </div>
            """
        )

    return "".join(blocks)


def _format_quick_wins_html(quick_wins):
    if not quick_wins:
        return "<p>No quick wins available.</p>"

    blocks = []
    for item in quick_wins:
        title = escape(str(item.get("title", "")))
        impact = escape(str(item.get("impact", "")))

        blocks.append(
            f"""
            <div class="quick-win-card" style="
                margin:10px 0;
                padding:18px;
                background:#eef8f2;
                border-radius:10px;
            ">
                <strong>{title}</strong>
                <p style="margin:8px 0 0;">
                    Impact:
                    <strong>{impact}</strong>
                </p>
            </div>
            """
        )

    return "".join(blocks)


def _format_recommendations_html(recommendations):
    if not recommendations:
        return "<p>No recommendations available.</p>"

    blocks = []
    for item in recommendations:
        recommendation = escape(str(item.get("recommendation", "")))
        impact = escape(str(item.get("impact", "")))
        area = escape(str(item.get("area", "")))

        blocks.append(
            f"""
            <div class="recommendation-card" style="
                margin:10px 0;
                padding:18px;
                background:#f5f8f9;
                border-radius:10px;
            ">
                <p style="margin:0;">{recommendation}</p>
                <p style="margin:8px 0 0;">
                    Area: <strong>{area}</strong><br>
                    Impact: <strong>{impact}</strong>
                </p>
            </div>
            """
        )

    return "".join(blocks)


from django.core.mail import EmailMultiAlternatives, send_mail
from django.utils.html import escape


def send_assessment_report(
    assessment,
    readiness_score,
    readiness_level,
    department_analysis,
    quick_wins,
    recommendations,
    roi_estimate,
):
    """Send the complete SCOUT AI assessment report by email."""

    roi_estimate = roi_estimate or {}

    recipient = getattr(assessment, "email", "")
    if not recipient:
        raise ValueError("Assessment email address is required.")

    subject = "SCOUT AI - Your AI Automation Readiness Report"

    # =====================================================
    # ROI DATA
    # =====================================================

    monthly_savings = roi_estimate.get(
        "estimated_monthly_savings", 0
    )

    annual_savings = roi_estimate.get(
        "estimated_annual_savings", 0
    )

    hours_saved = roi_estimate.get(
        "estimated_hours_saved_monthly", 0
    )

    hourly_cost = roi_estimate.get(
        "estimated_hourly_cost", 0
    )

    implementation_cost = roi_estimate.get(
        "estimated_implementation_cost", 0
    )

    roi_percentage = roi_estimate.get(
        "estimated_roi_percentage", 0
    )

    # =====================================================
    # ASSESSMENT DATA
    # =====================================================

    name = str(
        getattr(assessment, "name", "there")
    )

    company = str(
        getattr(assessment, "company_name", "-")
    )

    designation = str(
        getattr(assessment, "designation", "-")
    )

    industry = str(
        getattr(assessment, "industry", "-")
    )

    company_size = str(
        getattr(assessment, "company_size", "-")
    )

    # =====================================================
    # FORMAT DATA
    # =====================================================

    department_text = _format_department_analysis_text(
        department_analysis
    )

    quick_wins_text = _format_quick_wins_text(
        quick_wins
    )

    recommendations_text = _format_recommendations_text(
        recommendations
    )

    department_html = _format_department_analysis_html(
        department_analysis
    )

    quick_wins_html = _format_quick_wins_html(
        quick_wins
    )

    recommendations_html = _format_recommendations_html(
        recommendations
    )

    # =====================================================
    # SAFE HTML VALUES
    # =====================================================

    safe_name = escape(name)
    safe_company = escape(company)
    safe_designation = escape(designation)
    safe_industry = escape(industry)
    safe_company_size = escape(company_size)
    safe_readiness_level = escape(
        str(readiness_level)
    )

    # =====================================================
    # PLAIN TEXT EMAIL
    # =====================================================

    text_content = f"""
SCOUT AI
AI AUTOMATION READINESS REPORT

Hello {name},

Thank you for completing the SCOUT AI assessment.

COMPANY DETAILS
---------------
Company: {company}
Designation: {designation}
Industry: {industry}
Company Size: {company_size}

READINESS
---------
Score: {readiness_score}/100
Level: {readiness_level}

ESTIMATED BUSINESS IMPACT
-------------------------
Monthly Savings: ₹{monthly_savings:,}
Annual Savings: ₹{annual_savings:,}
Hours Saved / Month: {hours_saved}
Hourly Cost: ₹{hourly_cost:,}
Implementation Cost: ₹{implementation_cost:,}
Estimated ROI: {roi_percentage}%

DEPARTMENT ANALYSIS
-------------------
{department_text}

QUICK WINS
----------
{quick_wins_text}

RECOMMENDATIONS
---------------
{recommendations_text}

IMPORTANT
---------
ROI figures are indicative estimates based on the assessment inputs
and are not a financial guarantee.

SCOUT AI
Your automation journey starts here.
"""

    # =====================================================
    # HTML EMAIL
    # =====================================================

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>SCOUT AI Report</title>
    <style>
        @page {{
            size: A4;
            margin: 0;
        }}

        body {{
            padding: 0;
        }}

        .report-shell {{
            width: 750px;
            margin: 0 auto;
        }}

        .report-section,
        .readiness-card,
        .impact-table,
        .analysis-card,
        .quick-win-card,
        .recommendation-card,
        .important-note,
        .report-footer-note {{
            page-break-inside: avoid;
        }}

        h2 {{
            page-break-after: avoid;
        }}
    </style>
</head>

<body style="
    margin:0;
    padding:30px;
    background:#f5f7f9;
    font-family:Arial,Helvetica,sans-serif;
    color:#20394B;
        {{

        }}
    max-width:750px;
        h2 {{
    background:#ffffff;
        }}
    overflow:hidden;
    border:1px solid #e5e7eb;
">

    <div style="
        background:#2C485E;
        padding:30px;
        color:#ffffff;
    ">
        <h1 style="margin:0;font-size:28px;">
            SCOUT AI
        </h1>

        <p style="
            margin:8px 0 0;
            color:#64C786;
        ">
            AI Automation Readiness Report
        </p>
    </div>

    <div class="report-section" style="padding:35px;">

        <h2>Hello {safe_name},</h2>

        <p style="
            color:#607D8B;
            line-height:1.6;
        ">
            Thank you for completing the SCOUT AI assessment.
            Your automation readiness report is ready.
        </p>

        <h2 style="margin-top:35px;">
            Company Details
        </h2>

        <table width="100%"
               cellpadding="8"
               cellspacing="0"
               style="border-collapse:collapse;">

            <tr>
                <td><strong>Company</strong></td>
                <td>{safe_company}</td>
            </tr>

            <tr>
                <td><strong>Designation</strong></td>
                <td>{safe_designation}</td>
            </tr>

            <tr>
                <td><strong>Industry</strong></td>
                <td>{safe_industry}</td>
            </tr>

            <tr>
                <td><strong>Company Size</strong></td>
                <td>{safe_company_size}</td>
            </tr>

        </table>

        <div class="readiness-card" style="
            margin-top:25px;
            padding:25px;
            background:#f5f8f9;
            border-radius:12px;
            text-align:center;
        ">

            <p style="
                margin:0;
                font-size:13px;
                color:#607D8B;
            ">
                AUTOMATION READINESS
            </p>

            <div style="
                margin-top:10px;
                font-size:42px;
                font-weight:bold;
                color:#64C786;
            ">
                {readiness_score}/100
            </div>

            <p style="
                margin:8px 0 0;
                font-weight:bold;
            ">
                {safe_readiness_level}
            </p>

        </div>

        <h2 style="margin-top:35px;">
            Estimated Business Impact
        </h2>

        <table class="impact-table" width="100%"
               cellpadding="12"
               cellspacing="0"
               style="
                    border-collapse:collapse;
                    background:#f8fafb;
               ">

            <tr>
                <td>Hours Saved / Month</td>
                <td align="right">
                    <strong>{hours_saved}</strong>
                </td>
            </tr>

            <tr>
                <td>Hourly Cost</td>
                <td align="right">
                    <strong>₹{hourly_cost:,}</strong>
                </td>
            </tr>

            <tr>
                <td>Monthly Savings</td>
                <td align="right">
                    <strong>₹{monthly_savings:,}</strong>
                </td>
            </tr>

            <tr>
                <td>Annual Savings</td>
                <td align="right">
                    <strong>₹{annual_savings:,}</strong>
                </td>
            </tr>

            <tr>
                <td>Implementation Cost</td>
                <td align="right">
                    <strong>₹{implementation_cost:,}</strong>
                </td>
            </tr>

            <tr>
                <td>Estimated ROI</td>
                <td align="right">
                    <strong>{roi_percentage}%</strong>
                </td>
            </tr>

        </table>

        <h2 style="margin-top:35px;">
            Department Analysis
        </h2>

        {department_html}

        <h2 style="margin-top:35px;">
            Quick Wins
        </h2>

        {quick_wins_html}

        <h2 style="margin-top:35px;">
            Recommended Next Steps
        </h2>

        {recommendations_html}

        <div style="
            margin-top:40px;
            padding:18px;
            background:#fff8e6;
            border-radius:10px;
            font-size:13px;
            color:#6b5b35;
        ">

            <strong>Important:</strong>

            ROI figures are indicative estimates based on
            the assessment inputs and are not a financial guarantee.

        </div>

        <div style="
            margin-top:40px;
            padding-top:20px;
            border-top:1px solid #ddd;
            color:#777;
            font-size:13px;
        ">

            <strong>SCOUT AI</strong>

            <p>
                Your automation journey starts here.
            </p>

        </div>

    </div>

    <div style="
        background:#2C485E;
        padding:20px;
        text-align:center;
        color:#ffffff;
    ">
        SCOUT AI · CodeGrameen
    </div>

</div>

</body>
</html>
"""

    # =====================================================
    # SEND USER REPORT
    # =====================================================

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient],
    )

    email.attach_alternative(
        html_content,
        "text/html"
    )

    email.send(
        fail_silently=False
    )

    print(
        f"Assessment report email sent successfully to {recipient}"
    )

    # =====================================================
    # INTERNAL ALERT EMAIL
    # =====================================================

    try:

        send_mail(
            subject="SCOUT AI - New Assessment Lead",

            message=f"""
A new SCOUT AI assessment has been submitted.

Name:
{name}

Email:
{recipient}

Company:
{company}

Designation:
{designation}

Industry:
{industry}

Company Size:
{company_size}

Readiness Score:
{readiness_score}/100

Readiness Level:
{readiness_level}

Assessment ID:
{assessment.id}
""",

            from_email=None,

            recipient_list=[
                "abhijeetsahu479@gmail.com"
            ],

            fail_silently=False,
        )

        print(
            "Internal alert email sent successfully"
        )

    except Exception as error:

        print(
            "Internal alert email failed:",
            error
        )