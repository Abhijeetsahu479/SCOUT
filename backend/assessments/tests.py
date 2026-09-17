from io import BytesIO
from unittest.mock import patch

from django.core import mail
from django.test import TestCase, override_settings

from .email_service import send_assessment_report_email
from .models import Assessment, Lead


@override_settings(
	EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
	DEFAULT_FROM_EMAIL="no-reply@scout.test",
	LEAD_NOTIFICATION_EMAIL="abhijeetsahu479@gmail.com",
)
class AssessmentEmailTests(TestCase):

	@patch(
		"assessments.email_service.generate_assessment_pdf",
		return_value=BytesIO(b"test-pdf"),
	)
	def test_sends_pdf_to_user_and_lead_details_to_internal_inbox(
		self,
		generate_pdf,
	):
		assessment = Assessment.objects.create(
			name="Abhijeet Sahu",
			email="user@example.com",
			company_name="Example Co",
			designation="Founder",
			industry="technology",
			company_size="11-50",
			departments=["sales_crm"],
			automation_level="partially_automated",
			repetitive_activities=["reporting"],
			workflow_notes="Weekly reporting is manual.",
			challenges=["repetitive_work"],
			challenge_notes="Approvals take time.",
		)

		lead = Lead.objects.create(
			name=assessment.name,
			email=assessment.email,
			company_name=assessment.company_name,
			designation=assessment.designation,
			industry=assessment.industry,
			company_size=assessment.company_size,
			departments_selected=assessment.departments,
			automation_level=assessment.automation_level,
			repetitive_activities=assessment.repetitive_activities,
			workflow_notes=assessment.workflow_notes,
			challenges=assessment.challenges,
			challenge_notes=assessment.challenge_notes,
			consent_given=True,
			utm_source="google",
			utm_medium="cpc",
			utm_campaign="spring_campaign",
			ip_address="203.0.113.42",
			full_report_sent=True,
		)

		send_assessment_report_email(
			assessment=assessment,
			lead=lead,
			readiness_score=72,
			readiness_level="Growing",
			department_analysis=[],
			quick_wins=[],
			recommendations=[],
			roi_estimate={},
		)

		self.assertEqual(len(mail.outbox), 2)
		self.assertEqual(mail.outbox[0].to, ["user@example.com"])
		self.assertEqual(
			mail.outbox[1].to,
			["abhijeetsahu479@gmail.com"],
		)
		self.assertEqual(
			mail.outbox[0].attachments[0][0],
			f"SCOUT_AI_Automation_Readiness_Report_{assessment.id}.pdf",
		)
		self.assertIn(
			"Your Automation Readiness Report is attached",
			mail.outbox[0].body,
		)
		self.assertIn("user@example.com", mail.outbox[1].body)
		self.assertIn("Example Co", mail.outbox[1].body)
		self.assertIn("Consent: Yes", mail.outbox[1].body)
		self.assertIn("UTM Source: google", mail.outbox[1].body)
		self.assertIn("UTM Medium: cpc", mail.outbox[1].body)
		self.assertIn("UTM Campaign: spring_campaign", mail.outbox[1].body)
		self.assertIn("IP Address: 203.0.113.42", mail.outbox[1].body)
		self.assertIn("Report Status: Full report sent", mail.outbox[1].body)
		generate_pdf.assert_called_once()

# Create your tests here.
