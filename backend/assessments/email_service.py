from io import BytesIO
from pathlib import Path

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)


PDF_FONT_NAME = "ScoutUnicode"


def _register_pdf_font():
    """Register a Unicode font so PDF text includes the rupee symbol."""
    if PDF_FONT_NAME in pdfmetrics.getRegisteredFontNames():
        return

    font_path = Path("C:/Windows/Fonts/arial.ttf")
    if font_path.exists():
        pdfmetrics.registerFont(
            TTFont(PDF_FONT_NAME, str(font_path))
        )
        return

    fallback_path = Path("C:/Windows/Fonts/Nirmala.ttc")
    if fallback_path.exists():
        pdfmetrics.registerFont(
            TTFont(
                PDF_FONT_NAME,
                str(fallback_path),
                subfontIndex=0,
            )
        )
        return

    raise FileNotFoundError(
        "A Unicode TrueType font is required for PDF currency rendering."
    )


def _format_currency(value):
    """Format an integer-like value with Indian grouping and rupees."""
    try:
        amount = int(value or 0)
    except (TypeError, ValueError):
        amount = 0

    sign = "-" if amount < 0 else ""
    digits = str(abs(amount))

    if len(digits) > 3:
        last_three = digits[-3:]
        remaining = digits[:-3]
        groups = []

        while remaining:
            groups.insert(0, remaining[-2:])
            remaining = remaining[:-2]

        digits = ",".join(groups + [last_three])

    return f"{sign}₹{digits}"


# =========================================================
# PDF REPORT GENERATOR
# =========================================================

def generate_assessment_pdf(
    assessment,
    readiness_score,
    readiness_level,
    department_analysis=None,
    quick_wins=None,
    recommendations=None,
    roi_estimate=None,
):
    """
    Generate professional SCOUT AI PDF report
    and return PDF as BytesIO.
    """

    department_analysis = department_analysis or []
    quick_wins = quick_wins or []
    recommendations = recommendations or []
    roi_estimate = roi_estimate or {}

    _register_pdf_font()

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title="SCOUT AI Automation Readiness Report",
        author="SCOUT AI - CodeGrameen",
    )

    styles = getSampleStyleSheet()

    # =====================================================
    # CUSTOM STYLES
    # =====================================================

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontName=PDF_FONT_NAME,
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#294B63"),
        alignment=TA_CENTER,
        spaceAfter=8,
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontName=PDF_FONT_NAME,
        fontSize=11,
        textColor=colors.HexColor("#4CAF7A"),
        alignment=TA_CENTER,
        spaceAfter=20,
    )

    section_style = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontName=PDF_FONT_NAME,
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#294B63"),
        spaceBefore=12,
        spaceAfter=8,
    )

    normal_style = ParagraphStyle(
        "NormalCustom",
        parent=styles["Normal"],
        fontName=PDF_FONT_NAME,
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#333333"),
    )

    small_style = ParagraphStyle(
        "Small",
        parent=styles["Normal"],
        fontName=PDF_FONT_NAME,
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#666666"),
    )

    score_style = ParagraphStyle(
        "Score",
        parent=styles["Normal"],
        fontName=PDF_FONT_NAME,
        fontSize=30,
        textColor=colors.HexColor("#4CAF7A"),
        alignment=TA_CENTER,
    )

    level_style = ParagraphStyle(
        "Level",
        parent=styles["Normal"],
        fontName=PDF_FONT_NAME,
        fontSize=11,
        textColor=colors.HexColor("#294B63"),
        alignment=TA_CENTER,
    )

    # =====================================================
    # STORY
    # =====================================================

    story = []

    # =====================================================
    # HEADER
    # =====================================================

    header_data = [
        [
            Paragraph(
                "<b>SCOUT AI</b>",
                ParagraphStyle(
                    "HeaderTitle",
                    parent=styles["Normal"],
                    fontSize=24,
                    textColor=colors.white,
                    fontName=PDF_FONT_NAME,
                ),
            )
        ],
        [
            Paragraph(
                "AI Automation Readiness Report",
                ParagraphStyle(
                    "HeaderSub",
                    parent=styles["Normal"],
                    fontSize=10,
                    textColor=colors.HexColor("#8FE0B0"),
                    fontName=PDF_FONT_NAME,
                ),
            )
        ],
    ]

    header_table = Table(
        header_data,
        colWidths=[174 * mm],
    )

    header_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.HexColor("#294B63"),
                ),
                ("LEFTPADDING", (0, 0), (-1, -1), 15),
                ("RIGHTPADDING", (0, 0), (-1, -1), 15),
                ("TOPPADDING", (0, 0), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ]
        )
    )

    story.append(header_table)
    story.append(Spacer(1, 15))

    # =====================================================
    # GREETING
    # =====================================================

    story.append(
        Paragraph(
            f"Hello <b>{assessment.name}</b>,",
            ParagraphStyle(
                "Greeting",
                parent=normal_style,
                fontSize=14,
                fontName=PDF_FONT_NAME,
                textColor=colors.HexColor("#183B56"),
                spaceAfter=8,
            ),
        )
    )

    story.append(
        Paragraph(
            "Thank you for completing the SCOUT AI assessment. "
            "Your automation readiness report is ready.",
            normal_style,
        )
    )

    story.append(Spacer(1, 15))

    # =====================================================
    # COMPANY DETAILS
    # =====================================================

    story.append(
        Paragraph(
            "Company Details",
            section_style,
        )
    )

    company_data = [
        ["Name", str(assessment.name or "Not provided")],
        ["Email", str(assessment.email or "Not provided")],
        [
            "Company",
            str(assessment.company_name or "Not provided"),
        ],
        [
            "Designation",
            str(assessment.designation or "Not provided"),
        ],
        [
            "Industry",
            str(assessment.industry or "Not provided"),
        ],
        [
            "Company Size",
            str(assessment.company_size or "Not provided"),
        ],
    ]

    company_table = Table(
        company_data,
        colWidths=[45 * mm, 129 * mm],
    )

    company_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#F2F6F8"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#294B63"),
                ),
                ("FONTNAME", (0, 0), (0, -1), PDF_FONT_NAME),
                ("FONTNAME", (1, 0), (1, -1), PDF_FONT_NAME),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D9E2E7")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    story.append(company_table)

    # =====================================================
    # AUTOMATION READINESS
    # =====================================================

    story.append(
        Paragraph(
            "Automation Readiness",
            section_style,
        )
    )

    score_table = Table(
        [
            [
                Paragraph(
                    f"{readiness_score}/100",
                    score_style,
                )
            ],
            [
                Paragraph(
                    f"<b>{readiness_level}</b>",
                    level_style,
                )
            ],
        ],
        colWidths=[174 * mm],
    )

    score_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.HexColor("#F4F8F9"),
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.6,
                    colors.HexColor("#DCE7EA"),
                ),
                ("TOPPADDING", (0, 0), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ]
        )
    )

    story.append(score_table)

    # =====================================================
    # BUSINESS IMPACT / ROI
    # =====================================================

    story.append(
        Paragraph(
            "Estimated Business Impact",
            section_style,
        )
    )

    hours_saved = roi_estimate.get(
        "estimated_hours_saved_monthly",
        roi_estimate.get("hours_saved_monthly", 0),
    )

    hourly_cost = roi_estimate.get(
        "hourly_cost",
        500,
    )

    monthly_savings = roi_estimate.get(
        "estimated_monthly_savings",
        roi_estimate.get("monthly_savings", 0),
    )

    annual_savings = roi_estimate.get(
        "estimated_annual_savings",
        roi_estimate.get("annual_savings", 0),
    )

    implementation_cost = roi_estimate.get(
        "implementation_cost",
        0,
    )

    roi = roi_estimate.get(
        "roi_percentage",
        roi_estimate.get("roi", 0),
    )

    roi_data = [
        ["Hours Saved / Month", str(hours_saved)],
        ["Hourly Cost", _format_currency(hourly_cost)],
        ["Monthly Savings", _format_currency(monthly_savings)],
        ["Annual Savings", _format_currency(annual_savings)],
        ["Implementation Cost", _format_currency(implementation_cost)],
        [
            "Estimated ROI",
            f"{roi_estimate.get('estimated_roi_percentage', roi)}%",
        ],
    ]

    roi_table = Table(
        roi_data,
        colWidths=[85 * mm, 89 * mm],
    )

    roi_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.HexColor("#F7F9FA"),
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, -1),
                    PDF_FONT_NAME,
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#294B63"),
                ),
                ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.HexColor("#D9E2E7"),
                ),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    story.append(roi_table)

    # =====================================================
    # DEPARTMENT ANALYSIS
    # =====================================================

    if department_analysis:

        story.append(
            Paragraph(
                "Department Analysis",
                section_style,
            )
        )

        for department in department_analysis:

            if not isinstance(department, dict):
                continue

            department_name = department.get(
                "department",
                "Department",
            )

            department_score = department.get(
                "score",
                department.get("readiness_score", 0),
            )

            opportunities = department.get(
                "opportunities",
                [],
            )

            dept_content = [
                [
                    Paragraph(
                        f"<b>{department_name}</b>",
                        normal_style,
                    ),
                    Paragraph(
                        f"<b>{department_score}/100</b>",
                        normal_style,
                    ),
                ]
            ]

            if opportunities:

                opportunity_text = "<b>Opportunities:</b><br/>"

                for opportunity in opportunities:
                    opportunity_text += (
                        f"• {opportunity}<br/>"
                    )

                dept_content.append(
                    [
                        Paragraph(
                            opportunity_text,
                            normal_style,
                        ),
                        "",
                    ]
                )

            dept_table = Table(
                dept_content,
                colWidths=[140 * mm, 34 * mm],
            )

            dept_table.setStyle(
                TableStyle(
                    [
                        (
                            "BACKGROUND",
                            (0, 0),
                            (-1, -1),
                            colors.HexColor("#F4F8F9"),
                        ),
                        (
                            "SPAN",
                            (0, 1),
                            (1, 1),
                        )
                        if opportunities
                        else (
                            "SPAN",
                            (0, 0),
                            (0, 0),
                        ),
                        (
                            "GRID",
                            (0, 0),
                            (-1, -1),
                            0.4,
                            colors.HexColor("#DCE7EA"),
                        ),
                        (
                            "LEFTPADDING",
                            (0, 0),
                            (-1, -1),
                            8,
                        ),
                        (
                            "RIGHTPADDING",
                            (0, 0),
                            (-1, -1),
                            8,
                        ),
                        (
                            "TOPPADDING",
                            (0, 0),
                            (-1, -1),
                            7,
                        ),
                        (
                            "BOTTOMPADDING",
                            (0, 0),
                            (-1, -1),
                            7,
                        ),
                    ]
                )
            )

            story.append(dept_table)
            story.append(Spacer(1, 7))

    # =====================================================
    # QUICK WINS
    # =====================================================

    if quick_wins:

        story.append(
            Paragraph(
                "Recommended Quick Wins",
                section_style,
            )
        )

        for index, item in enumerate(quick_wins, start=1):

            if not isinstance(item, dict):
                title = str(item)
                impact = ""
            else:
                title = item.get("title", "Quick win")
                impact = item.get("impact", "")

            story.append(
                Paragraph(
                    f"<b>{index}. {title}</b>",
                    normal_style,
                )
            )

            if impact:
                story.append(
                    Paragraph(
                        f"Impact: {impact}",
                        normal_style,
                    )
                )

            story.append(Spacer(1, 4))

    # =====================================================
    # RECOMMENDATIONS
    # =====================================================

    if recommendations:

        story.append(
            Paragraph(
                "Automation Recommendations",
                section_style,
            )
        )

        for index, item in enumerate(recommendations, start=1):

            if isinstance(item, dict):

                recommendation = item.get(
                    "recommendation",
                    "",
                )
                impact = item.get("impact", "")
                area = item.get("area", "")

                story.append(
                    Paragraph(
                        f"<b>{index}. {recommendation}</b>",
                        normal_style,
                    )
                )

                if impact:
                    story.append(
                        Paragraph(
                            f"Impact: {impact}",
                            normal_style,
                        )
                    )

                if area:
                    story.append(
                        Paragraph(
                            f"Area: {area}",
                            normal_style,
                        )
                    )

            else:

                story.append(
                    Paragraph(
                        f"• {item}",
                        normal_style,
                    )
                )

            story.append(Spacer(1, 5))

    # =====================================================
    # FOOTER / DISCLAIMER
    # =====================================================

    story.append(Spacer(1, 15))

    footer_box = Table(
        [
            [
                Paragraph(
                    "<b>SCOUT AI · CodeGrameen</b><br/>"
                    "This assessment provides indicative automation "
                    "readiness and business impact estimates based "
                    "on the information submitted.",
                    small_style,
                )
            ]
        ],
        colWidths=[174 * mm],
    )

    footer_box.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.HexColor("#F1F7F4"),
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#CFE5D8"),
                ),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )

    story.append(footer_box)

    # =====================================================
    # BUILD PDF
    # =====================================================

    doc.build(story)

    buffer.seek(0)

    return buffer


# =========================================================
# SEND REPORT EMAIL
# =========================================================

def send_assessment_report_email(
    assessment,
    readiness_score,
    readiness_level,
    department_analysis=None,
    quick_wins=None,
    recommendations=None,
    roi_estimate=None,
    lead=None,
):
    """
    Send SCOUT AI assessment report as PDF attachment and internal lead notification.
    """

    from django.conf import settings
    from django.core.mail import EmailMultiAlternatives

    from .models import Lead

    recipient = assessment.email
    subject = "SCOUT AI - Your Automation Readiness Report"

    pdf_file = generate_assessment_pdf(
        assessment=assessment,
        readiness_score=readiness_score,
        readiness_level=readiness_level,
        department_analysis=department_analysis,
        quick_wins=quick_wins,
        recommendations=recommendations,
        roi_estimate=roi_estimate,
    )

    text_content = f"""
Hello {assessment.name},

Thank you for completing the SCOUT AI assessment.

Your Automation Readiness Report is attached to this email as a PDF.


Regards,
SCOUT AI
CodeGrameen
"""

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient],
    )

    pdf_filename = (
        "SCOUT_AI_Automation_Readiness_Report_"
        f"{assessment.id}.pdf"
    )

    email.attach(
        pdf_filename,
        pdf_file.getvalue(),
        "application/pdf",
    )

    email.send(fail_silently=False)

    print(f"PDF report sent successfully to {recipient}")

    if lead is None:
        lead = Lead.objects.filter(email=assessment.email).first()

    consent_value = "Yes" if lead and lead.consent_given else "No"
    utm_source = getattr(lead, "utm_source", "-") if lead else "-"
    utm_medium = getattr(lead, "utm_medium", "-") if lead else "-"
    utm_campaign = getattr(lead, "utm_campaign", "-") if lead else "-"
    ip_address = getattr(lead, "ip_address", "-") if lead and lead.ip_address else "-"
    created_at = getattr(lead, "created_at", assessment.created_at) if lead else assessment.created_at

    if lead and lead.full_report_sent:
        report_status = "Full report sent"
    elif lead and lead.prelim_report_sent:
        report_status = "Preliminary report sent"
    else:
        report_status = "Not sent"

    try:
        send_mail(
            subject="SCOUT AI - New Assessment Lead",
            message=f"""
A new SCOUT AI assessment has been submitted.

Name: {assessment.name}
Email: {assessment.email}
Company: {assessment.company_name}
Designation: {assessment.designation}
Industry: {assessment.industry}
Company Size: {assessment.company_size}
Departments: {assessment.departments}
Automation Level: {assessment.automation_level}
Repetitive Activities: {assessment.repetitive_activities}
Workflow Notes: {assessment.workflow_notes or '-'}
Challenges: {assessment.challenges}
Challenge Notes: {assessment.challenge_notes or '-'}
Consent: {consent_value}
UTM Source: {utm_source}
UTM Medium: {utm_medium}
UTM Campaign: {utm_campaign}
IP Address: {ip_address}
Created At: {created_at}
Report Status: {report_status}
Readiness Score: {readiness_score}/100
Readiness Level: {readiness_level}
Assessment ID: {assessment.id}
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.LEAD_NOTIFICATION_EMAIL],
            fail_silently=False,
        )

        print("Internal lead notification sent successfully")

    except Exception as error:
        print("Internal lead notification failed:", error)