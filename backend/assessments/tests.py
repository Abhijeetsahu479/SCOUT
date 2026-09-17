from io import BytesIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core import mail
from django.db import IntegrityError
from django.test import TestCase, override_settings
from reportlab.pdfbase import pdfmetrics
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .email_service import (
	PDF_FONT_NAME,
	generate_assessment_pdf,
	send_assessment_report_email,
)
from .models import Assessment, AssessmentReport, Lead
from .services import (
	calculate_department_analysis,
	calculate_readiness_score,
	calculate_roi_estimate,
	generate_quick_wins,
	generate_recommendations,
	get_readiness_level,
)


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


def assessment_payload(email="api@example.com"):
	return {
		"name": "API User",
		"email": email,
		"company_name": "API Company",
		"designation": "Founder",
		"industry": "technology",
		"company_size": "11-50",
		"departments": ["sales_crm"],
		"automation_level": "partially_automated",
		"repetitive_activities": ["reporting", "data_entry"],
		"workflow_notes": "Weekly reporting is manual.",
		"challenges": ["time_consuming", "manual_data"],
		"challenge_notes": "Approvals take time.",
	}


def create_lead(**overrides):
	data = {
		"name": "Test Lead",
		"email": "lead@example.com",
		"company_name": "Test Company",
		"designation": "Manager",
		"industry": "technology",
		"company_size": "11-50",
	}
	data.update(overrides)
	return Lead.objects.create(**data)


class LeadModelTests(TestCase):

	def test_lead_required_fields_are_stored(self):
		lead = create_lead()

		self.assertEqual(lead.name, "Test Lead")
		self.assertEqual(lead.email, "lead@example.com")
		self.assertEqual(lead.company_name, "Test Company")
		self.assertEqual(lead.designation, "Manager")
		self.assertEqual(lead.industry, "technology")
		self.assertEqual(lead.company_size, "11-50")

	def test_lead_email_is_unique(self):
		create_lead()

		with self.assertRaises(IntegrityError):
			create_lead(name="Second Lead")


class AssessmentReportModelTests(TestCase):

	def test_report_requires_one_lead_and_stores_report_fields(self):
		lead = create_lead()
		report = AssessmentReport.objects.create(
			lead=lead,
			overall_score=72,
			department_scores={"Sales & CRM": {"score": 80}},
			should_automate=["Reporting"],
			should_not_automate=["Complex approvals"],
			estimated_hours_saved_monthly=20,
			estimated_cost_saved_monthly_inr=10000,
			ai_summary="Ready for automation.",
			raw_ai_response={"source": "test"},
		)

		self.assertEqual(lead.assessment_report, report)
		self.assertEqual(report.overall_score, 72)
		self.assertEqual(report.department_scores["Sales & CRM"]["score"], 80)
		self.assertEqual(report.estimated_hours_saved_monthly, 20)
		self.assertEqual(report.raw_ai_response["source"], "test")

	def test_report_lead_relationship_is_one_to_one(self):
		lead = create_lead()
		AssessmentReport.objects.create(lead=lead)

		with self.assertRaises(IntegrityError):
			AssessmentReport.objects.create(lead=lead)


@override_settings(
	EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
	DEFAULT_FROM_EMAIL="no-reply@scout.test",
	LEAD_NOTIFICATION_EMAIL="internal@scout.test",
)
class AssessmentAPITests(TestCase):

	def setUp(self):
		self.client = APIClient()

	@patch("assessments.views.send_assessment_report_email")
	def test_valid_assessment_post_creates_assessment_and_report_data(
		self,
		send_report,
	):
		response = self.client.post(
			"/api/assessments/",
			assessment_payload(),
			format="json",
		)

		self.assertEqual(response.status_code, 201)
		self.assertEqual(Assessment.objects.count(), 1)
		self.assertEqual(Lead.objects.count(), 1)
		self.assertEqual(AssessmentReport.objects.count(), 1)
		self.assertIn("readiness_score", response.data)
		self.assertIn("readiness_level", response.data)
		self.assertIn("department_analysis", response.data)
		self.assertIn("quick_wins", response.data)
		self.assertIn("recommendations", response.data)
		self.assertIn("roi_estimate", response.data)
		send_report.assert_called_once()

	def test_missing_email_returns_400(self):
		payload = assessment_payload()
		payload.pop("email")

		response = self.client.post(
			"/api/assessments/",
			payload,
			format="json",
		)

		self.assertEqual(response.status_code, 400)
		self.assertIn("email", response.data["details"])

	def test_invalid_email_returns_400(self):
		payload = assessment_payload(email="not-an-email")

		response = self.client.post(
			"/api/assessments/",
			payload,
			format="json",
		)

		self.assertEqual(response.status_code, 400)
		self.assertIn("email", response.data["details"])

	@patch("assessments.views.send_assessment_report_email")
	def test_duplicate_assessment_email_reuses_existing_lead(
		self,
		send_report,
	):
		first = self.client.post(
			"/api/assessments/",
			assessment_payload(email="duplicate@example.com"),
			format="json",
		)
		second = self.client.post(
			"/api/assessments/",
			assessment_payload(email="duplicate@example.com"),
			format="json",
		)

		self.assertEqual(first.status_code, 201)
		self.assertEqual(second.status_code, 201)
		self.assertEqual(Assessment.objects.count(), 2)
		self.assertEqual(Lead.objects.count(), 1)
		self.assertFalse(second.data["lead_created"])
		self.assertEqual(send_report.call_count, 2)


class FullReportAPITests(TestCase):

	def setUp(self):
		self.client = APIClient()
		self.user = get_user_model().objects.create_user(
			username="report-user",
			password="test-password",
		)
		self.token = Token.objects.create(user=self.user)
		self.assessment = Assessment.objects.create(
			**assessment_payload(email="report@example.com")
		)
		self.lead = create_lead(
			email=self.assessment.email,
			name=self.assessment.name,
			company_name=self.assessment.company_name,
		)
		self.report = AssessmentReport.objects.create(
			lead=self.lead,
			overall_score=72,
		)

	def test_full_report_without_token_returns_401(self):
		response = self.client.get(
			f"/api/report/{self.assessment.id}/"
		)

		self.assertEqual(response.status_code, 401)

	def test_full_report_with_invalid_token_returns_401(self):
		response = self.client.get(
			f"/api/report/{self.assessment.id}/",
			HTTP_AUTHORIZATION="Token invalid-token",
		)

		self.assertEqual(response.status_code, 401)

	def test_full_report_with_valid_token_returns_complete_json(self):
		self.client.credentials(
			HTTP_AUTHORIZATION=f"Token {self.token.key}"
		)

		response = self.client.get(
			f"/api/report/{self.assessment.id}/"
		)

		self.assertEqual(response.status_code, 200)
		for key in (
			"readiness_score",
			"readiness_level",
			"department_analysis",
			"quick_wins",
			"recommendations",
			"roi_estimate",
			"lead_id",
			"report_id",
			"assessment_report",
		):
			self.assertIn(key, response.data)

	def test_full_report_invalid_id_returns_json_404(self):
		self.client.credentials(
			HTTP_AUTHORIZATION=f"Token {self.token.key}"
		)

		response = self.client.get("/api/report/999999/")

		self.assertEqual(response.status_code, 404)
		self.assertEqual(
			response.data,
			{"success": False, "error": "Assessment not found."},
		)


class HealthAPITests(TestCase):

	def test_health_is_public_and_returns_exact_json(self):
		response = self.client.get("/api/health/")

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response["Content-Type"], "application/json")
		self.assertEqual(response.json(), {"status": "ok"})


class BusinessLogicTests(TestCase):

	def make_assessment(self, **overrides):
		data = assessment_payload(email="logic@example.com")
		data.update(overrides)
		return Assessment(**data)

	def test_readiness_score_uses_current_inputs_and_caps_at_100(self):
		assessment = self.make_assessment(
			automation_level="highly_automated",
			repetitive_activities=["a", "b", "c", "d", "e"],
			departments=["a", "b", "c", "d"],
			challenges=["a", "b", "c", "d", "e"],
			workflow_notes="Present",
		)

		self.assertEqual(calculate_readiness_score(assessment), 100)

	def test_readiness_level_thresholds(self):
		self.assertEqual(get_readiness_level(0), "Early Stage")
		self.assertEqual(get_readiness_level(39), "Early Stage")
		self.assertEqual(get_readiness_level(40), "Developing")
		self.assertEqual(get_readiness_level(59), "Developing")
		self.assertEqual(get_readiness_level(60), "Ready")
		self.assertEqual(get_readiness_level(79), "Ready")
		self.assertEqual(get_readiness_level(80), "Highly Ready")
		self.assertEqual(get_readiness_level(100), "Highly Ready")

	def test_department_analysis_known_department(self):
		analysis = calculate_department_analysis(
			self.make_assessment(
				departments=["sales_crm"],
				repetitive_activities=["reporting"],
				challenges=["errors"],
				workflow_notes="Manual process",
			)
		)

		self.assertEqual(analysis[0]["department"], "Sales & CRM")
		self.assertEqual(analysis[0]["score"], 80)
		self.assertIn("CRM data entry", analysis[0]["opportunities"])

	def test_department_analysis_unknown_department_has_fallback(self):
		analysis = calculate_department_analysis(
			self.make_assessment(departments=["legal"])
		)

		self.assertEqual(analysis[0]["department"], "Legal")
		self.assertIn("Workflow automation", analysis[0]["opportunities"])

	def test_quick_wins_map_and_deduplicate_recommendations(self):
		quick_wins = generate_quick_wins(
			self.make_assessment(
				repetitive_activities=["reporting"],
				challenges=["time_consuming", "reporting"],
			)
		)

		titles = [item["title"] for item in quick_wins]
		self.assertIn("Automate recurring reports", titles)
		self.assertEqual(len(titles), len(set(titles)))

	def test_quick_wins_are_limited_to_six(self):
		quick_wins = generate_quick_wins(
			self.make_assessment(
				repetitive_activities=[
					"data_entry", "reporting", "documents", "email", "data_processing",
				],
				challenges=[
					"time_consuming", "manual_data", "communication", "errors", "slow_process",
				],
			)
		)

		self.assertLessEqual(len(quick_wins), 6)

	def test_recommendations_include_activity_challenge_and_department_strategy(self):
		recommendations = generate_recommendations(
			self.make_assessment(
				repetitive_activities=["reporting"],
				challenges=["errors"],
				departments=["sales_crm"],
			)
		)

		areas = [item["area"] for item in recommendations]
		self.assertIn("reporting", areas)
		self.assertIn("errors", areas)
		self.assertIn("department_strategy", areas)

	def test_recommendations_are_unique_and_limited_to_eight(self):
		recommendations = generate_recommendations(
			self.make_assessment(
				repetitive_activities=[
					"data_entry", "reporting", "documents", "email", "data_processing",
				],
				challenges=[
					"time_consuming", "manual_data", "communication", "errors", "slow_process",
				],
				departments=["sales_crm"],
			)
		)

		texts = [item["recommendation"] for item in recommendations]
		self.assertEqual(len(texts), len(set(texts)))
		self.assertLessEqual(len(recommendations), 8)

	def test_roi_calculation_matches_current_formula(self):
		roi = calculate_roi_estimate(
			self.make_assessment(
				repetitive_activities=["reporting"],
				challenges=["errors"],
				departments=["sales_crm"],
			)
		)

		self.assertEqual(roi["estimated_hours_saved_monthly"], 17)
		self.assertEqual(roi["estimated_monthly_savings"], 8500)
		self.assertEqual(roi["estimated_annual_savings"], 102000)
		self.assertEqual(roi["estimated_implementation_cost"], 100000)
		self.assertEqual(roi["estimated_roi_percentage"], 2)


class PDFGenerationTests(TestCase):

	def test_pdf_generation_returns_valid_pdf_bytes(self):
		assessment = Assessment(**assessment_payload(email="pdf@example.com"))

		pdf_file = generate_assessment_pdf(
			assessment=assessment,
			readiness_score=72,
			readiness_level="Ready",
			department_analysis=[],
			quick_wins=[],
			recommendations=[],
			roi_estimate={},
		)

		self.assertGreater(pdf_file.getbuffer().nbytes, 0)
		self.assertTrue(pdf_file.getvalue().startswith(b"%PDF"))

	def test_pdf_renders_quick_wins_recommendations_and_currency(self):
		from pypdf import PdfReader

		assessment = Assessment(**assessment_payload(email="pdf-text@example.com"))
		pdf_file = generate_assessment_pdf(
			assessment=assessment,
			readiness_score=72,
			readiness_level="Ready",
			quick_wins=[
				{
					"title": "Automate recurring reports",
					"impact": "High",
					"source": "repetitive_activity",
				}
			],
			recommendations=[
				{
					"recommendation": "Use form automation to reduce manual data entry.",
					"impact": "High",
					"area": "data_entry",
				}
			],
			roi_estimate={
				"estimated_hourly_cost": 500,
				"estimated_monthly_savings": 12000,
				"estimated_annual_savings": 144000,
				"estimated_implementation_cost": 100000,
				"estimated_roi_percentage": 44,
			},
		)

		text = "\n".join(
			page.extract_text() or ""
			for page in PdfReader(pdf_file).pages
		)

		self.assertIn("Automate recurring reports", text)
		self.assertIn("Impact: High", text)
		self.assertIn("Use form automation to reduce manual data entry.", text)
		self.assertIn("Area: data_entry", text)
		self.assertNotIn("'title':", text)
		self.assertNotIn("Recommendation\n", text)
		self.assertIn("500", text)
		self.assertIn("12,000", text)
		self.assertIn("1,44,000", text)
		self.assertIn(
			PDF_FONT_NAME,
			pdfmetrics.getRegisteredFontNames(),
		)
		self.assertGreater(
			pdfmetrics.getFont(PDF_FONT_NAME).face.charWidths.get(
				ord("₹"),
				0,
			),
			0,
		)
