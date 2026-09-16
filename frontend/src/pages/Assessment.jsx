import { useState } from "react"
import WizardLayout from "../components/wizard/WizardLayout"
import { assessmentSteps } from "../data/assessmentSteps"

const industries = [
  { id: "technology", icon: "💻", name: "Technology" },
  { id: "manufacturing", icon: "🏭", name: "Manufacturing" },
  { id: "finance", icon: "💰", name: "Finance" },
  { id: "retail", icon: "🛍️", name: "Retail" },
  { id: "healthcare", icon: "🏥", name: "Healthcare" },
  { id: "logistics", icon: "📦", name: "Logistics" },
  { id: "education", icon: "🎓", name: "Education" },
  { id: "other", icon: "◈", name: "Other" },
]

const companySizes = [
  { id: "1-10", number: "01", title: "1–10" },
  { id: "11-50", number: "02", title: "11–50" },
  { id: "51-200", number: "03", title: "51–200" },
  { id: "201-500", number: "04", title: "201–500" },
  { id: "500+", number: "05", title: "500+" },
]

const departments = [
  {
    id: "hr_payroll",
    number: "01",
    icon: "👥",
    name: "HR & Payroll",
    description: "People, attendance & payroll",
  },
  {
    id: "finance_accounting",
    number: "02",
    icon: "💰",
    name: "Finance & Accounting",
    description: "Invoices, payments & reporting",
  },
  {
    id: "sales_crm",
    number: "03",
    icon: "📈",
    name: "Sales & CRM",
    description: "Leads, follow-ups & CRM",
  },
  {
    id: "customer_support",
    number: "04",
    icon: "🎧",
    name: "Customer Support",
    description: "Tickets, queries & service",
  },
  {
    id: "inventory_logistics",
    number: "05",
    icon: "📦",
    name: "Inventory & Logistics",
    description: "Stock, orders & movement",
  },
  {
    id: "marketing",
    number: "06",
    icon: "📣",
    name: "Marketing",
    description: "Campaigns, content & leads",
  },
  {
    id: "operations_production",
    number: "07",
    icon: "⚙️",
    name: "Operations & Production",
    description: "Processes & production",
  },
  {
    id: "procurement",
    number: "08",
    icon: "🛒",
    name: "Procurement",
    description: "Purchasing & vendor workflows",
  },
  {
    id: "it_helpdesk",
    number: "09",
    icon: "💻",
    name: "IT Helpdesk",
    description: "Support requests & IT workflows",
  },
  {
    id: "compliance_reporting",
    number: "10",
    icon: "📋",
    name: "Compliance & Reporting",
    description: "Compliance, audits & reports",
  },
]

const automationLevels = [
  {
    id: "mostly_manual",
    icon: "📝",
    title: "Mostly Manual",
    description:
      "Most processes are handled manually.",
  },
  {
    id: "partially_automated",
    icon: "⚙️",
    title: "Partially Automated",
    description:
      "Some workflows already use automation.",
  },
  {
    id: "highly_automated",
    icon: "🤖",
    title: "Highly Automated",
    description:
      "Most important workflows are automated.",
  },
]

const repetitiveActivities = [
  {
    id: "data_entry",
    icon: "⌨️",
    name: "Data Entry",
  },
  {
    id: "reporting",
    icon: "📊",
    name: "Reporting",
  },
  {
    id: "email_communication",
    icon: "✉️",
    name: "Email & Communication",
  },
  {
    id: "customer_queries",
    icon: "🎧",
    name: "Customer Queries",
  },
  {
    id: "approvals",
    icon: "✅",
    name: "Approvals",
  },
  {
    id: "documents",
    icon: "📄",
    name: "Document Processing",
  },
  {
    id: "followups",
    icon: "🔔",
    name: "Follow-ups",
  },
  {
    id: "other",
    icon: "◈",
    name: "Other",
  },
]

const challenges = [
  {
    id: "time_consuming",
    number: "01",
    icon: "⏱️",
    name: "Time-consuming tasks",
    description: "Too much time spent on routine work",
  },
  {
    id: "repetitive_work",
    number: "02",
    icon: "🔁",
    name: "Repetitive work",
    description: "The same tasks are repeated frequently",
  },
  {
    id: "manual_data",
    number: "03",
    icon: "📋",
    name: "Manual data handling",
    description: "Data is entered or moved manually",
  },
  {
    id: "errors_rework",
    number: "04",
    icon: "⚠️",
    name: "Errors & rework",
    description: "Mistakes create additional manual work",
  },
  {
    id: "slow_processes",
    number: "05",
    icon: "🐌",
    name: "Slow processes",
    description: "Workflows take longer than expected",
  },
  {
    id: "poor_visibility",
    number: "06",
    icon: "👁️",
    name: "Poor visibility",
    description: "Difficult to track work and performance",
  },
  {
    id: "scalability",
    number: "07",
    icon: "📈",
    name: "Scalability issues",
    description: "Current processes struggle as work grows",
  },
  {
    id: "communication",
    number: "08",
    icon: "💬",
    name: "Communication gaps",
    description: "Information gets delayed or missed",
  },
]

function ReviewSection({ title, children }) {
  return (
    <section className="rounded-2xl border border-[#20394B]/10 bg-white p-5 shadow-sm sm:p-6">

      <div className="mb-5 flex items-center gap-3">

        <span className="h-px w-6 bg-[#64C786]/40" />

        <h2 className="text-xs font-bold uppercase tracking-[0.18em] text-[#20394B]/90">
          {title}
        </h2>

      </div>

      {children}

    </section>
  )
}


function ReviewItem({ label, value }) {
  return (
    <div>

      <p className="text-[10px] font-semibold uppercase tracking-[0.15em] text-[#20394B]/85">
        {label}
      </p>

      <p className="mt-2 break-words text-sm font-medium text-[#20394B]/85">
        {value || "Not provided"}
      </p>

    </div>
  )
}


function ReviewTags({ items }) {
  return (
    <div className="flex flex-wrap gap-2">

      {items.length > 0 ? (
        items.map((item) => (
          <span
            key={item}
            className="rounded-full border border-[#64C786]/35 bg-[#64C786]/10 px-3 py-2 text-xs font-medium text-[#2C8F59]"
          >
            {item}
          </span>
        ))
      ) : (
        <span className="text-xs text-[#20394B]/70">
          None selected
        </span>
      )}

    </div>
  )
}


function AssessmentResult({ result }) {
  const score = result?.readiness_score ?? 0
  const level = result?.readiness_level || "Early Stage"

  const roi = result?.roi_estimate || {}
  const departments = result?.department_analysis || []
  const quickWins = result?.quick_wins || []
  const recommendations = result?.recommendations || []

  const money = (value) =>
    `₹${Number(value || 0).toLocaleString("en-IN")}`

  return (
    <main className="min-h-screen bg-[#F7F9F8] text-[#20394B]">

      {/* Header */}
      <header className="border-b border-[#20394B]/10 bg-[#2C485E]">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-5 py-4 sm:px-8">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center overflow-hidden rounded-xl bg-white p-1">
              <img
                src="/logo.jpg"
                alt="CodeGrameen"
                className="h-full w-full object-contain"
              />
            </div>

            <div>
              <p className="text-sm font-bold text-white">
                CodeGrameen
              </p>
              <p className="text-[10px] font-semibold uppercase tracking-[0.18em] text-[#64C786]">
                SCOUT AI
              </p>
            </div>
          </div>

          <div className="rounded-full border border-[#64C786]/40 bg-[#64C786]/10 px-4 py-2 text-[10px] font-semibold uppercase tracking-[0.16em] text-[#64C786]">
            Assessment Complete
          </div>
        </div>
      </header>

      <section className="mx-auto max-w-7xl px-5 py-8 sm:px-8 lg:py-10">

        {/* Hero */}
        <div className="mb-8">
          <p className="text-xs font-bold uppercase tracking-[0.22em] text-[#2C8F59]">
            SCOUT Assessment Report
          </p>

          <h1 className="mt-3 text-3xl font-bold tracking-tight text-[#20394B] sm:text-4xl">
            Your AI Automation Readiness Report
          </h1>

          <p className="mt-3 max-w-2xl text-sm leading-6 text-[#20394B]/65 sm:text-base">
            SCOUT has analyzed your business information,
            workflows and challenges to identify practical
            automation opportunities and estimated business impact.
          </p>
        </div>

        {/* Top metrics */}
        <div className="grid gap-5 lg:grid-cols-3">

          {/* Score */}
          <div className="rounded-3xl border border-[#20394B]/10 bg-white p-6 shadow-[0_18px_55px_rgba(32,57,75,0.08)]">
            <div className="flex items-center justify-between gap-5">
              <div>
                <p className="text-xs font-bold uppercase tracking-[0.15em] text-[#20394B]/50">
                  Readiness
                </p>

                <h2 className="mt-2 text-2xl font-bold text-[#20394B]">
                  {level}
                </h2>

                <p className="mt-2 text-sm text-[#20394B]/55">
                  AI automation readiness
                </p>
              </div>

              <div className="flex h-24 w-24 shrink-0 items-center justify-center rounded-full border-[8px] border-[#64C786]/20">
                <div className="text-center">
                  <p className="text-2xl font-bold text-[#20394B]">
                    {score}
                  </p>
                  <p className="text-[10px] font-semibold text-[#20394B]/50">
                    / 100
                  </p>
                </div>
              </div>
            </div>

            <div className="mt-6 h-2 overflow-hidden rounded-full bg-[#20394B]/10">
              <div
                className="h-full rounded-full bg-[#64C786] transition-all duration-700"
                style={{ width: `${Math.min(Math.max(score, 0), 100)}%` }}
              />
            </div>
          </div>

          {/* Monthly savings */}
          <MetricCard
            label="Estimated Monthly Savings"
            value={money(roi.estimated_monthly_savings)}
            description="Potential monthly savings from identified automation opportunities."
          />

          {/* Annual savings */}
          <div className="rounded-3xl bg-[#20394B] p-6 shadow-[0_18px_55px_rgba(32,57,75,0.14)]">
            <p className="text-xs font-bold uppercase tracking-[0.15em] text-white/50">
              Estimated Annual Savings
            </p>

            <p className="mt-4 text-3xl font-bold text-white">
              {money(roi.estimated_annual_savings)}
            </p>

            <div className="mt-4 inline-flex rounded-full bg-[#64C786]/15 px-3 py-1.5 text-xs font-bold text-[#78D99A]">
              {roi.estimated_roi_percentage || 0}% estimated ROI
            </div>
          </div>
        </div>

        {/* ROI details */}
        <ReportSection
          eyebrow="ROI ESTIMATE"
          title="Potential Business Impact"
        >
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <MetricCard
              label="Hours Saved / Month"
              value={`${roi.estimated_hours_saved_monthly || 0} hrs`}
            />

            <MetricCard
              label="Hourly Cost"
              value={money(roi.estimated_hourly_cost)}
            />

            <MetricCard
              label="Implementation Cost"
              value={money(roi.estimated_implementation_cost)}
            />

            <MetricCard
              label="Estimated ROI"
              value={`${roi.estimated_roi_percentage || 0}%`}
            />
          </div>

          <div className="mt-5 rounded-2xl bg-[#F7F9F8] p-5">
            <p className="text-sm font-semibold text-[#20394B]">
              Important
            </p>

            <p className="mt-2 text-xs leading-6 text-[#20394B]/60">
              ROI figures are indicative estimates based on SCOUT assumptions.
              Actual savings and implementation costs may vary depending on
              workflows, tools, team size and implementation approach.
            </p>
          </div>
        </ReportSection>

        {/* Department analysis */}
        <ReportSection
          eyebrow="DEPARTMENT ANALYSIS"
          title="Automation Opportunities"
        >
          {departments.length === 0 ? (
            <EmptyReport text="No department analysis available." />
          ) : (
            <div className="grid gap-5 md:grid-cols-2">
              {departments.map((department, index) => (
                <div
                  key={index}
                  className="rounded-2xl border border-[#20394B]/10 bg-[#F7F9F8] p-5"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <h3 className="text-lg font-bold text-[#20394B]">
                        {department.department}
                      </h3>
                      <p className="mt-1 text-xs text-[#20394B]/50">
                        Automation opportunity score
                      </p>
                    </div>

                    <span className="rounded-full bg-[#64C786]/15 px-3 py-1.5 text-xs font-bold text-[#2C8F59]">
                      {department.score}/100
                    </span>
                  </div>

                  <div className="mt-5 h-2 overflow-hidden rounded-full bg-[#20394B]/10">
                    <div
                      className="h-full rounded-full bg-[#64C786]"
                      style={{
                        width: `${Math.min(Math.max(department.score || 0, 0), 100)}%`,
                      }}
                    />
                  </div>

                  <p className="mt-5 text-xs font-bold uppercase tracking-[0.12em] text-[#20394B]/50">
                    Key Opportunities
                  </p>

                  <ul className="mt-3 space-y-2">
                    {(department.opportunities || []).map(
                      (opportunity, opportunityIndex) => (
                        <li
                          key={opportunityIndex}
                          className="flex gap-2 text-sm text-[#20394B]/65"
                        >
                          <span className="text-[#64C786]">●</span>
                          <span>{opportunity}</span>
                        </li>
                      )
                    )}
                  </ul>
                </div>
              ))}
            </div>
          )}
        </ReportSection>

        {/* Quick wins */}
        <ReportSection
          eyebrow="QUICK WINS"
          title="Start With These Opportunities"
        >
          {quickWins.length === 0 ? (
            <EmptyReport text="No quick wins identified yet." />
          ) : (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {quickWins.map((item, index) => (
                <div
                  key={index}
                  className="rounded-2xl border border-[#20394B]/10 bg-white p-5"
                >
                  <div className="flex items-center justify-between gap-3">
                    <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-[#64C786]/15 text-sm font-bold text-[#2C8F59]">
                      {index + 1}
                    </span>

                    <span className="rounded-full bg-[#F7F9F8] px-3 py-1 text-[10px] font-bold uppercase tracking-wide text-[#20394B]/55">
                      {item.impact || "Medium"} Impact
                    </span>
                  </div>

                  <h3 className="mt-5 text-sm font-semibold leading-6 text-[#20394B]">
                    {item.title}
                  </h3>
                </div>
              ))}
            </div>
          )}
        </ReportSection>

        {/* Recommendations */}
        <ReportSection
          eyebrow="RECOMMENDATIONS"
          title="Recommended Next Steps"
        >
          {recommendations.length === 0 ? (
            <EmptyReport text="No recommendations available yet." />
          ) : (
            <div className="space-y-3">
              {recommendations.map((item, index) => (
                <div
                  key={index}
                  className="flex gap-4 rounded-2xl border border-[#20394B]/10 bg-white p-5"
                >
                  <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-[#20394B] text-xs font-bold text-white">
                    {index + 1}
                  </span>

                  <div>
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="rounded-full bg-[#64C786]/15 px-3 py-1 text-[10px] font-bold uppercase tracking-wide text-[#2C8F59]">
                        {item.impact || "Medium"} Impact
                      </span>

                      {item.area && (
                        <span className="text-[10px] font-medium text-[#20394B]/40">
                          {item.area}
                        </span>
                      )}
                    </div>

                    <p className="mt-3 text-sm leading-6 text-[#20394B]/70">
                      {item.recommendation}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </ReportSection>

        {/* Footer */}
        <div className="mt-10 rounded-3xl bg-[#2C485E] p-8 text-center">
          <p className="text-xs font-bold uppercase tracking-[0.2em] text-[#64C786]">
            SCOUT AI
          </p>

          <h2 className="mt-3 text-2xl font-bold text-white">
            Your automation journey starts here.
          </h2>

          <p className="mx-auto mt-3 max-w-xl text-sm leading-6 text-white/60">
            Use this assessment as a starting point to prioritize
            high-impact automation opportunities.
          </p>
        </div>

      </section>
    </main>
  )
}


function ReportSection({ eyebrow, title, children }) {
  return (
    <section className="mt-8 rounded-3xl border border-[#20394B]/10 bg-white p-6 shadow-sm sm:p-7">
      <div className="mb-6">
        <p className="text-xs font-bold uppercase tracking-[0.18em] text-[#2C8F59]">
          {eyebrow}
        </p>

        <h2 className="mt-2 text-2xl font-bold text-[#20394B]">
          {title}
        </h2>
      </div>

      {children}
    </section>
  )
}


function MetricCard({ label, value, description }) {
  return (
    <div className="rounded-2xl border border-[#20394B]/10 bg-[#F7F9F8] p-5">
      <p className="text-xs font-medium text-[#20394B]/50">
        {label}
      </p>

      <p className="mt-2 text-2xl font-bold text-[#20394B]">
        {value}
      </p>

      {description && (
        <p className="mt-2 text-xs leading-5 text-[#20394B]/50">
          {description}
        </p>
      )}
    </div>
  )
}


function EmptyReport({ text }) {
  return (
    <div className="rounded-2xl border border-dashed border-[#20394B]/15 bg-[#F7F9F8] p-8 text-center">
      <p className="text-sm text-[#20394B]/50">
        {text}
      </p>
    </div>
  )
}


function Assessment() {
  const [currentStep, setCurrentStep] = useState(1)

const [formData, setFormData] = useState({
  name: "",
  email: "",
  companyName: "",
  designation: "",
  industry: "",
  companySize: "",
  departments: [],

  automationLevel: "",
  repetitiveActivities: [],
  workflowNotes: "",

  challenges: [],
  challengeNotes: "",
})
  const [errors, setErrors] = useState({})

  const currentStepData = assessmentSteps[currentStep - 1]
  const [assessmentResult, setAssessmentResult] = useState(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  // -------------------------
  // INPUT CHANGE
  // -------------------------

  const handleChange = (event) => {
  const { name, value } = event.target

  if ((name === "workflowNotes" || name === "challengeNotes") && value.length > 500) {
    return
  }

  setFormData((previous) => ({
    ...previous,
    [name]: value,
  }))

  setErrors((previous) => ({
    ...previous,
    [name]: "",
  }))
} 

  // -------------------------
  // INDUSTRY
  // -------------------------

  const handleIndustrySelect = (industryId) => {
    setFormData((previous) => ({
      ...previous,
      industry: industryId,
    }))

    setErrors((previous) => ({
      ...previous,
      industry: "",
    }))
  }

  // -------------------------
  // COMPANY SIZE
  // -------------------------

  const handleCompanySizeSelect = (sizeId) => {
    setFormData((previous) => ({
      ...previous,
      companySize: sizeId,
    }))

    setErrors((previous) => ({
      ...previous,
      companySize: "",
    }))
  }

  // -------------------------
  // DEPARTMENT MULTI SELECT
  // -------------------------

  const handleDepartmentToggle = (departmentId) => {
    setFormData((previous) => {
      const isSelected = previous.departments.includes(departmentId)

      if (isSelected) {
        return {
          ...previous,
          departments: previous.departments.filter(
            (id) => id !== departmentId
          ),
        }
      }

      return {
        ...previous,
        departments: [...previous.departments, departmentId],
      }
    })

    setErrors((previous) => ({
      ...previous,
      departments: "",
    }))
  }

  
  // -------------------------
  // STEP 1 VALIDATION
  // -------------------------

  const validateStepOne = () => {
    const newErrors = {}

    if (!formData.name.trim()) {
      newErrors.name = "Please enter your full name."
    }

    if (!formData.email.trim()) {
      newErrors.email = "Please enter your work email."
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = "Please enter a valid email address."
    }

    if (!formData.companyName.trim()) {
      newErrors.companyName = "Please enter your company name."
    }

    if (!formData.designation.trim()) {
      newErrors.designation = "Please enter your designation."
    }

    setErrors(newErrors)

    return Object.keys(newErrors).length === 0
  }

  // -------------------------
  // STEP 2 VALIDATION
  // -------------------------

  const validateStepTwo = () => {
    const newErrors = {}

    if (!formData.industry) {
      newErrors.industry = "Please select your industry."
    }

    if (!formData.companySize) {
      newErrors.companySize = "Please select your company size."
    }

    setErrors(newErrors)

    return Object.keys(newErrors).length === 0
  }

  // -------------------------
  // STEP 3 VALIDATION
  // -------------------------

  const validateStepThree = () => {
    const newErrors = {}

    if (formData.departments.length === 0) {
      newErrors.departments =
        "Please select at least one department."
    }

    setErrors(newErrors)

    return Object.keys(newErrors).length === 0
  }

const handleAutomationLevelSelect = (level) => {
  setFormData((previous) => ({
    ...previous,
    automationLevel: level,
  }))

  setErrors((previous) => ({
    ...previous,
    automationLevel: "",
  }))
}

const handleActivityToggle = (activityId) => {
  setFormData((previous) => {
    const alreadySelected =
      previous.repetitiveActivities.includes(activityId)

    if (alreadySelected) {
      return {
        ...previous,
        repetitiveActivities:
          previous.repetitiveActivities.filter(
            (id) => id !== activityId
          ),
      }
    }

    return {
      ...previous,
      repetitiveActivities: [
        ...previous.repetitiveActivities,
        activityId,
      ],
    }
  })

  setErrors((previous) => ({
    ...previous,
    repetitiveActivities: "",
  }))
}

const handleChallengeToggle = (challengeId) => {
  setFormData((previous) => {
    const alreadySelected =
      previous.challenges.includes(challengeId)

    if (alreadySelected) {
      return {
        ...previous,
        challenges: previous.challenges.filter(
          (id) => id !== challengeId
        ),
      }
    }

    return {
      ...previous,
      challenges: [
        ...previous.challenges,
        challengeId,
      ],
    }
  })

  setErrors((previous) => ({
    ...previous,
    challenges: "",
  }))
}

const validateStepFour = () => {
  const newErrors = {}

  if (!formData.automationLevel) {
    newErrors.automationLevel =
      "Please select your current automation level."
  }

  if (formData.repetitiveActivities.length === 0) {
    newErrors.repetitiveActivities =
      "Please select at least one activity."
  }

  setErrors(newErrors)

  return Object.keys(newErrors).length === 0
} 

const validateStepFive = () => {
  const newErrors = {}

  if (formData.challenges.length === 0) {
    newErrors.challenges =
      "Please select at least one challenge."
  }

  setErrors(newErrors)

  return Object.keys(newErrors).length === 0
}

const getIndustryName = () => {
  const selected = industries.find(
    (item) => item.id === formData.industry
  )

  return selected?.name || "Not selected"
}

const getCompanySizeName = () => {
  const selected = companySizes.find(
    (item) => item.id === formData.companySize
  )

  return selected?.title
    ? `${selected.title} employees`
    : "Not selected"
}

const getAutomationLevelName = () => {
  const selected = automationLevels.find(
    (item) => item.id === formData.automationLevel
  )

  return selected?.title || "Not selected"
}

const getDepartmentNames = () => {
  return formData.departments
    .map((id) => {
      const department = departments.find(
        (item) => item.id === id
      )

      return department?.name
    })
    .filter(Boolean)
}

const getActivityNames = () => {
  return formData.repetitiveActivities
    .map((id) => {
      const activity = repetitiveActivities.find(
        (item) => item.id === id
      )

      return activity?.name
    })
    .filter(Boolean)
}

const getChallengeNames = () => {
  return formData.challenges
    .map((id) => {
      const challenge = challenges.find(
        (item) => item.id === id
      )

      return challenge?.name
    })
    .filter(Boolean)
}
  // -------------------------
  // NEXT
  // -------------------------

  const handleNext = async () => {
    if (currentStep === 1 && !validateStepOne()) return
    if (currentStep === 2 && !validateStepTwo()) return
    if (currentStep === 3 && !validateStepThree()) return
    if (currentStep === 4 && !validateStepFour()) return
    if (currentStep === 5 && !validateStepFive()) return

    if (currentStep === assessmentSteps.length) {
      try {
        setIsSubmitting(true)

        const response = await fetch(
          "http://127.0.0.1:8000/api/assessments/",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              name: formData.name,
              email: formData.email,
              company_name: formData.companyName,
              designation: formData.designation,
              industry: formData.industry,
              company_size: formData.companySize,
              departments: formData.departments,
              automation_level: formData.automationLevel,
              repetitive_activities: formData.repetitiveActivities,
              workflow_notes: formData.workflowNotes,
              challenges: formData.challenges,
              challenge_notes: formData.challengeNotes,
            }),
          }
        )

        const data = await response.json()

        if (!response.ok) {
          console.error("SCOUT API Error:", data)
          alert("Assessment submit nahi hua. Please try again.")
          return
        }

        console.log("SCOUT Assessment Result:", data)
        setAssessmentResult(data)
      } catch (error) {
        console.error("SCOUT Network Error:", error)
        alert(
          "Backend se connection nahi ho pa raha. Django server check karein."
        )
      } finally {
        setIsSubmitting(false)
      }

      return
    }

    setCurrentStep((previous) => previous + 1)
    window.scrollTo({ top: 0, behavior: "smooth" })
  }

  // -------------------------
  // BACK
  // -------------------------

  const handleBack = () => {
    if (currentStep > 1) {
      setCurrentStep((previous) => previous - 1)
      window.scrollTo({ top: 0, behavior: "smooth" })
    }
  }

  if (assessmentResult) {
    return <AssessmentResult result={assessmentResult} />
  }

  // -------------------------
  // INPUT STYLE
  // -------------------------

  const inputClass = (fieldName) => {
    const hasError = errors[fieldName]

    return `
      mt-2
      w-full
      rounded-2xl
      border
      bg-white
      px-4
      py-4
      text-sm
      text-[#20394B]
      outline-none
      transition
      duration-300
      placeholder:text-[#20394B]/20
      ${
        hasError
          ? "border-red-400/60 focus:border-red-400"
          : "border-[#20394B]/10 focus:border-[#64C786]/60 focus:bg-[#F1F6F3]"
      }
    `
  }

  return (
    <WizardLayout
      currentStep={currentStep}
      onBack={handleBack}
      onNext={handleNext}
      isFirstStep={currentStep === 1}
      isLastStep={currentStep === assessmentSteps.length}
      isSubmitting={isSubmitting}
    >
      {/* ================= HEADER ================= */}

      <div className="mb-8">
        <p className="text-xs font-bold uppercase tracking-[0.25em] text-[#2C8F59]">
          Step {String(currentStep).padStart(2, "0")} / 06
        </p>

        <div className="mt-4 flex items-center gap-2">
          <span className="h-1.5 w-7 rounded-full bg-[#64C786]" />
          <span className="text-[10px] font-bold uppercase tracking-[0.18em] text-[#20394B]/75">
            SCOUT AI Assessment
          </span>
        </div>

        <h1 className="mt-3 text-3xl font-bold tracking-tight text-[#20394B] sm:text-4xl">
          {currentStepData.title}
        </h1>

        <p className="mt-3 max-w-xl text-sm leading-6 text-[#20394B]/55 sm:text-base">
          {currentStepData.description}
        </p>
      </div>

      {/* ==================================================
          STEP 1
      ================================================== */}

      {currentStep === 1 && (
        <div className="grid gap-6 sm:grid-cols-2">

          {/* Name */}
          <div>
            <label className="text-sm font-medium text-[#20394B]/90">
              Full name
              <span className="ml-1 text-[#64C786]">*</span>
            </label>

            <input
              name="name"
              type="text"
              value={formData.name}
              onChange={handleChange}
              placeholder="e.g. Abhijeet Sahu"
              className={inputClass("name")}
            />

            {errors.name && (
              <p className="mt-2 text-xs text-red-400">
                {errors.name}
              </p>
            )}
          </div>

          {/* Email */}
          <div>
            <label className="text-sm font-medium text-[#20394B]/90">
              Work email
              <span className="ml-1 text-[#64C786]">*</span>
            </label>

            <input
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="you@company.com"
              className={inputClass("email")}
            />

            {errors.email && (
              <p className="mt-2 text-xs text-red-400">
                {errors.email}
              </p>
            )}
          </div>

          {/* Company */}
          <div>
            <label className="text-sm font-medium text-[#20394B]/90">
              Company name
              <span className="ml-1 text-[#64C786]">*</span>
            </label>

            <input
              name="companyName"
              type="text"
              value={formData.companyName}
              onChange={handleChange}
              placeholder="e.g. CodeGrameen"
              className={inputClass("companyName")}
            />

            {errors.companyName && (
              <p className="mt-2 text-xs text-red-400">
                {errors.companyName}
              </p>
            )}
          </div>

          {/* Designation */}
          <div>
            <label className="text-sm font-medium text-[#20394B]/90">
              Your designation
              <span className="ml-1 text-[#64C786]">*</span>
            </label>

            <input
              name="designation"
              type="text"
              value={formData.designation}
              onChange={handleChange}
              placeholder="e.g. HR Manager"
              className={inputClass("designation")}
            />

            {errors.designation && (
              <p className="mt-2 text-xs text-red-400">
                {errors.designation}
              </p>
            )}
          </div>

        </div>
      )}

      {/* ==================================================
          STEP 2
      ================================================== */}

      {currentStep === 2 && (
        <div className="space-y-10">

          {/* INDUSTRY */}

          <div>
            <div className="mb-4">
              <h2 className="text-lg font-semibold">
                What industry are you in?
                <span className="ml-1 text-[#64C786]">*</span>
              </h2>

              <p className="mt-1 text-xs font-medium text-[#20394B]/70">
                Choose the option closest to your organisation.
              </p>
            </div>

            <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">

              {industries.map((industry) => {
                const selected =
                  formData.industry === industry.id

                return (
                  <button
                    key={industry.id}
                    type="button"
                    onClick={() =>
                      handleIndustrySelect(industry.id)
                    }
                    className={`
                      relative
                      min-h-[105px]
                      rounded-2xl
                      border
                      p-4
                      text-left
                      transition-all
                      duration-300
                      ${
                        selected
                          ? "border-[#64C786]/70 bg-[#64C786]/10"
                          : "border-[#20394B]/10 bg-[#F8FBF9] hover:border-[#20394B]/15 hover:bg-[#F1F6F3]"
                      }
                    `}
                  >
                    {selected && (
                      <span className="absolute right-3 top-3 flex h-5 w-5 items-center justify-center rounded-full bg-[#64C786] text-xs font-black text-[#173326]">
                        ✓
                      </span>
                    )}

                    <span className="text-2xl">
                      {industry.icon}
                    </span>

                    <p
                      className={`mt-3 text-xs font-medium ${
                        selected
                          ? "text-[#64C786]"
                          : "text-[#20394B]/65"
                      }`}
                    >
                      {industry.name}
                    </p>
                  </button>
                )
              })}

            </div>

            {errors.industry && (
              <p className="mt-3 text-xs text-red-400">
                {errors.industry}
              </p>
            )}
          </div>

          {/* COMPANY SIZE */}

          <div>
            <div className="mb-4">
              <h2 className="text-lg font-semibold">
                How large is your organisation?
                <span className="ml-1 text-[#64C786]">*</span>
              </h2>

              <p className="mt-1 text-xs font-medium text-[#20394B]/70">
                Select the approximate number of employees.
              </p>
            </div>

            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-5">

              {companySizes.map((size) => {
                const selected =
                  formData.companySize === size.id

                return (
                  <button
                    key={size.id}
                    type="button"
                    onClick={() =>
                      handleCompanySizeSelect(size.id)
                    }
                    className={`
                      relative
                      rounded-2xl
                      border
                      p-5
                      text-left
                      transition-all
                      duration-300
                      ${
                        selected
                          ? "border-[#64C786]/70 bg-[#64C786]/10"
                          : "border-[#20394B]/10 bg-[#F8FBF9] hover:border-[#20394B]/15 hover:bg-[#F1F6F3]"
                      }
                    `}
                  >
                    {selected && (
                      <span className="absolute right-3 top-3 flex h-5 w-5 items-center justify-center rounded-full bg-[#64C786] text-xs font-black text-[#173326]">
                        ✓
                      </span>
                    )}

                    <span className="text-[10px] font-semibold tracking-[0.2em] text-[#20394B]/55">
                      {size.number}
                    </span>

                    <p
                      className={`mt-2 text-xl font-semibold ${
                        selected
                          ? "text-[#64C786]"
                          : "text-[#20394B]"
                      }`}
                    >
                      {size.title}
                    </p>

                    <p className="mt-1 text-xs font-medium text-[#20394B]/65">
                      employees
                    </p>
                  </button>
                )
              })}

            </div>

            {errors.companySize && (
              <p className="mt-3 text-xs text-red-400">
                {errors.companySize}
              </p>
            )}
          </div>

        </div>
      )}

      {/* ==================================================
          STEP 3
      ================================================== */}

      {currentStep === 3 && (
        <div>

          {/* Heading */}

          <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">

            <div>
              <h2 className="text-lg font-semibold">
                Which teams should we assess?
                <span className="ml-1 text-[#64C786]">*</span>
              </h2>

              <p className="mt-1 max-w-xl text-xs font-medium leading-5 text-[#20394B]/90 sm:text-sm">
                Select every department where you'd like SCOUT
                to identify automation opportunities.
              </p>
            </div>

            {/* Counter */}

            <div className="rounded-full border border-[#64C786]/35 bg-[#64C786]/10 px-4 py-2">

              <span className="text-xs font-medium text-[#20394B]/75">
                Selected
              </span>

              <span className="ml-2 text-sm font-bold text-[#2C8F59]">
                {formData.departments.length}
              </span>

            </div>

          </div>

          {/* Department Cards */}

          <div className="grid gap-3 sm:grid-cols-2">

            {departments.map((department) => {
              const selected =
                formData.departments.includes(department.id)

              return (
                <button
                  key={department.id}
                  type="button"
                  onClick={() =>
                    handleDepartmentToggle(department.id)
                  }
                  aria-pressed={selected}
                  className={`
                    relative
                    rounded-2xl
                    border
                    p-5
                    text-left
                    transition-all
                    duration-300
                    ${
                      selected
                        ? "border-[#64C786]/70 bg-[#64C786]/10 shadow-[0_0_30px_rgba(100,199,134,0.07)]"
                        : "border-[#20394B]/10 bg-[#F8FBF9] hover:-translate-y-0.5 hover:border-[#20394B]/15 hover:bg-[#F1F6F3]"
                    }
                  `}
                >

                  <div className="flex items-start justify-between gap-4">

                    <div className="flex items-start gap-4">

                      {/* Icon */}

                      <div
                        className={`
                          flex
                          h-12
                          w-12
                          shrink-0
                          items-center
                          justify-center
                          rounded-xl
                          text-xl
                          ${
                            selected
                              ? "bg-[#64C786]/35"
                              : "bg-[#C9DBD0]"
                          }
                        `}
                      >
                        {department.icon}
                      </div>

                      {/* Text */}

                      <div>

                        <span className="text-[9px] font-bold tracking-[0.2em] text-[#20394B]">
                          {department.number}
                        </span>

                        <h3
                          className={`
                            mt-1
                            text-sm
                            font-semibold
                            ${
                              selected
                                ? "text-[#64C786]"
                                : "text-[#20394B]/85"
                            }
                          `}
                        >
                          {department.name}
                        </h3>

                        <p className="mt-1 text-xs leading-5 text-[#20394B]/65">
                          {department.description}
                        </p>

                      </div>

                    </div>

                    {/* Check */}

                    <div
                      className={`
                        flex
                        h-6
                        w-6
                        shrink-0
                        items-center
                        justify-center
                        rounded-full
                        border
                        text-xs
                        transition-all
                        ${
                          selected
                            ? "border-[#64C786] bg-[#64C786] text-[#173326]"
                            : "border-[#20394B]/10 text-transparent"
                        }
                      `}
                    >
                      ✓
                    </div>

                  </div>

                </button>
              )
            })}

          </div>

          {/* Error */}

          {errors.departments && (
            <p className="mt-4 text-xs text-red-400">
              {errors.departments}
            </p>
          )}

          {/* Helper */}

          <div className="mt-5 flex items-center gap-2 text-xs font-medium text-[#20394B]/85">
            <span className="text-[#64C786]">●</span>
            You can select multiple departments
          </div>

        </div>
      )}

    {/* ==================================================
    STEP 4 — WORKFLOW
================================================== */}

{currentStep === 4 && (
  <div className="space-y-10">

    {/* Automation Level */}

    <div>
      <div className="mb-5">
        <h2 className="text-lg font-semibold">
          How automated are your current workflows?
          <span className="ml-1 text-[#64C786]">*</span>
        </h2>

        <p className="mt-1 max-w-xl text-xs font-medium leading-5 text-[#20394B]/80 sm:text-sm">
          Tell SCOUT how much of your day-to-day work
          is already automated.
        </p>
      </div>

      <div className="grid gap-3 md:grid-cols-3">

        {automationLevels.map((level) => {
          const selected =
            formData.automationLevel === level.id

          return (
            <button
              key={level.id}
              type="button"
              onClick={() =>
                handleAutomationLevelSelect(level.id)
              }
              className={`
                relative
                rounded-2xl
                border
                p-5
                text-left
                transition-all
                duration-300
                ${
                  selected
                    ? "border-[#64C786]/70 bg-[#64C786]/10 shadow-[0_0_30px_rgba(100,199,134,0.07)]"
                    : "border-[#20394B]/10 bg-[#F8FBF9] hover:-translate-y-0.5 hover:border-[#20394B]/15 hover:bg-[#F1F6F3]"
                }
              `}
            >

              {selected && (
                <span className="absolute right-4 top-4 flex h-6 w-6 items-center justify-center rounded-full bg-[#64C786] text-xs font-black text-[#173326]">
                  ✓
                </span>
              )}

              <div className="text-2xl">
                {level.icon}
              </div>

              <h3
                className={`mt-4 text-sm font-semibold ${
                  selected
                    ? "text-[#64C786]"
                    : "text-[#20394B]/85"
                }`}
              >
                {level.title}
              </h3>

              <p className="mt-2 text-xs leading-5 text-[#20394B]/85">
                {level.description}
              </p>

            </button>
          )
        })}

      </div>

      {errors.automationLevel && (
        <p className="mt-3 text-xs text-red-400">
          {errors.automationLevel}
        </p>
      )}
    </div>


    {/* Repetitive Activities */}

    <div>
      <div className="mb-5 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">

        <div>
          <h2 className="text-lg font-semibold">
            Which activities consume the most time?
            <span className="ml-1 text-[#64C786]">*</span>
          </h2>

          <p className="mt-1 text-xs text-[#20394B]/70 sm:text-sm">
            Select all activities that frequently require
            manual effort.
          </p>
        </div>

        <div className="self-start rounded-full border border-[#20394B]/10 bg-[#F8FBF9] px-4 py-2">
          <span className="text-xs font-medium text-[#20394B]/75">
            Selected
          </span>

          <span className="ml-2 text-sm font-bold text-[#2C8F59]">
            {formData.repetitiveActivities.length}
          </span>
        </div>

      </div>


      <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">

        {repetitiveActivities.map((activity) => {
          const selected =
            formData.repetitiveActivities.includes(
              activity.id
            )

          return (
            <button
              key={activity.id}
              type="button"
              onClick={() =>
                handleActivityToggle(activity.id)
              }
              aria-pressed={selected}
              className={`
                relative
                min-h-[105px]
                rounded-2xl
                border
                p-4
                text-left
                transition-all
                duration-300
                ${
                  selected
                    ? "border-[#64C786]/70 bg-[#64C786]/10"
                    : "border-[#20394B]/10 bg-[#F8FBF9] hover:border-[#20394B]/15 hover:bg-[#F1F6F3]"
                }
              `}
            >

              {selected && (
                <span className="absolute right-3 top-3 flex h-5 w-5 items-center justify-center rounded-full bg-[#64C786] text-xs font-black text-[#173326]">
                  ✓
                </span>
              )}

              <span className="text-xl">
                {activity.icon}
              </span>

              <p
                className={`mt-3 text-xs font-medium ${
                  selected
                    ? "text-[#64C786]"
                    : "text-[#20394B]/75"
                }`}
              >
                {activity.name}
              </p>

            </button>
          )
        })}

      </div>

      {errors.repetitiveActivities && (
        <p className="mt-3 text-xs text-red-400">
          {errors.repetitiveActivities}
        </p>
      )}

    </div>


    {/* Additional Workflow Notes */}

    <div>

      <label
        htmlFor="workflowNotes"
        className="text-sm font-medium text-[#20394B]/75"
      >
        Tell us more about your workflow
        <span className="ml-2 text-xs font-medium text-[#20394B]/95">
          Optional
        </span>
      </label>

      <textarea
        id="workflowNotes"
        name="workflowNotes"
        value={formData.workflowNotes}
        onChange={handleChange}
        rows="5"
        placeholder="For example: Our team manually prepares weekly reports, follows up with customers by email, and enters data into multiple systems..."
        className="
          mt-3
          w-full
          resize-none
          rounded-2xl
          border
          border-[#20394B]/10
          bg-[#F8FBF9]
          px-4
          py-4
          text-sm
          leading-6
          text-[#20394B]
          outline-none
          transition
          duration-300
          placeholder:text-[#20394B]/75
          focus:border-[#64C786]/60
          focus:bg-[#F1F6F3]
          focus:ring-2
          focus:ring-[#64C786]/10
        "
      />

      <div className="mt-2 flex justify-between">
        <span className="text-[11px] font-medium text-[#20394B]/90">
          Your information helps SCOUT identify better
          automation opportunities.
        </span>

        <span className="text-[11px] text-[#20394B]/75">
          {formData.workflowNotes.length}/500
        </span>
      </div>

    </div>

  </div>
)}

{/* ==================================================
    STEP 5 — CHALLENGES
================================================== */}

{currentStep === 5 && (
  <div className="space-y-8">

    {/* Header */}

    <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">

      <div>
        <h2 className="text-lg font-semibold">
          What challenges are slowing your team down?
          <span className="ml-1 text-[#64C786]">*</span>
        </h2>

        <p className="mt-1 max-w-xl text-xs font-medium leading-5 text-[#20394B]/80 sm:text-sm">
          Select the problems your organisation faces most often.
        </p>
      </div>

      {/* Counter */}

      <div className="self-start rounded-full border border-[#64C786]/35 bg-[#64C786]/10 px-4 py-2">

        <span className="text-xs font-medium text-[#20394B]/75">
          Selected
        </span>

        <span className="ml-2 text-sm font-bold text-[#2C8F59]">
          {formData.challenges.length}
        </span>

      </div>

    </div>


    {/* Challenge Cards */}

    <div className="grid gap-3 sm:grid-cols-2">

      {challenges.map((challenge) => {
        const selected =
          formData.challenges.includes(challenge.id)

        return (
          <button
            key={challenge.id}
            type="button"
            onClick={() =>
              handleChallengeToggle(challenge.id)
            }
            aria-pressed={selected}
            className={`
              group
              relative
              overflow-hidden
              rounded-2xl
              border
              p-5
              text-left
              transition-all
              duration-300
              ${
                selected
                  ? "border-[#64C786]/70 bg-[#64C786]/10 shadow-[0_0_30px_rgba(100,199,134,0.07)]"
                  : "border-[#20394B]/10 bg-[#F8FBF9] hover:-translate-y-0.5 hover:border-[#20394B]/15 hover:bg-[#F1F6F3]"
              }
            `}
          >

            {/* Glow */}

            {selected && (
              <div className="pointer-events-none absolute -right-10 -top-10 h-28 w-28 rounded-full bg-[#64C786]/10 blur-2xl" />
            )}

            <div className="relative flex items-start justify-between gap-4">

              <div className="flex items-start gap-4">

                {/* Icon */}

                <div
                  className={`
                    flex
                    h-12
                    w-12
                    shrink-0
                    items-center
                    justify-center
                    rounded-xl
                    text-xl
                    transition-all
                    duration-300
                    ${
                      selected
                        ? "bg-[#64C786]/15"
                        : "bg-[#F1F6F3]"
                    }
                  `}
                >
                  {challenge.icon}
                </div>

                {/* Content */}

                <div>

                  <span className="text-[9px] font-medium tracking-[0.2em] text-[#20394B]/65">
                    {challenge.number}
                  </span>

                  <h3
                    className={`
                      mt-1
                      text-sm
                      font-semibold
                      ${
                        selected
                          ? "text-[#64C786]"
                          : "text-[#20394B]/85"
                      }
                    `}
                  >
                    {challenge.name}
                  </h3>

                  <p className="mt-1 text-xs leading-5 text-[#20394B]/75">
                    {challenge.description}
                  </p>

                </div>

              </div>


              {/* Check */}

              <div
                className={`
                  flex
                  h-6
                  w-6
                  shrink-0
                  items-center
                  justify-center
                  rounded-full
                  border
                  text-xs
                  transition-all
                  duration-300
                  ${
                    selected
                      ? "border-[#64C786] bg-[#64C786] text-[#173326]"
                      : "border-[#20394B]/10 text-transparent"
                  }
                `}
              >
                ✓
              </div>

            </div>

          </button>
        )
      })}

    </div>


    {/* Error */}

    {errors.challenges && (
      <p className="text-xs text-red-400">
        {errors.challenges}
      </p>
    )}


    {/* Additional Notes */}

    <div>

      <label
        htmlFor="challengeNotes"
        className="text-sm font-medium text-[#20394B]/75"
      >
        Anything else we should know?
        <span className="ml-2 text-xs font-normal text-[#20394B]/65">
          Optional
        </span>
      </label>

      <textarea
        id="challengeNotes"
        name="challengeNotes"
        value={formData.challengeNotes}
        onChange={handleChange}
        rows="4"
        placeholder="Tell us about any specific challenge, bottleneck or process that you would like SCOUT to consider..."
        className="
          mt-3
          w-full
          resize-none
          rounded-2xl
          border
          border-[#20394B]/10
          bg-[#F8FBF9]
          px-4
          py-4
          text-sm
          leading-6
          text-[#20394B]
          outline-none
          transition
          duration-300
          placeholder:text-[#20394B]/65
          focus:border-[#64C786]/60
          focus:bg-[#F1F6F3]
          focus:ring-2
          focus:ring-[#64C786]/10
        "
      />

      <div className="mt-2 flex justify-end">
        <span className="text-[11px] text-[#20394B]/65">
          {formData.challengeNotes.length}/500
        </span>
      </div>

    </div>

  </div>
)}

{/* ==================================================
    STEP 6 — REVIEW
================================================== */}

{currentStep === 6 && (
  <div className="space-y-6">

    {/* Intro */}

    <div className="rounded-2xl border border-[#64C786]/15 bg-[#64C786]/[0.03] p-5">

      <div className="flex items-start gap-4">

        <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-[#64C786]/10 text-lg text-[#64C786]">
          ✓
        </div>

        <div>
          <h2 className="text-sm font-semibold text-[#20394B]">
            Your assessment is ready
          </h2>

          <p className="mt-1 text-xs leading-5 text-[#20394B]/85">
            Review the information below before sending
            it to SCOUT AI.
          </p>
        </div>

      </div>

    </div>


    {/* ================= COMPANY ================= */}

    <ReviewSection title="Company">

      <div className="grid gap-5 sm:grid-cols-2">

        <ReviewItem
          label="Full name"
          value={formData.name}
        />

        <ReviewItem
          label="Work email"
          value={formData.email}
        />

        <ReviewItem
          label="Company"
          value={formData.companyName}
        />

        <ReviewItem
          label="Designation"
          value={formData.designation}
        />

      </div>

    </ReviewSection>


    {/* ================= BUSINESS ================= */}

    <ReviewSection title="Business Profile">

      <div className="grid gap-5 sm:grid-cols-2">

        <ReviewItem
          label="Industry"
          value={getIndustryName()}
        />

        <ReviewItem
          label="Company size"
          value={getCompanySizeName()}
        />

      </div>

    </ReviewSection>


    {/* ================= DEPARTMENTS ================= */}

    <ReviewSection title="Departments">

      <ReviewTags
        items={getDepartmentNames()}
      />

    </ReviewSection>


    {/* ================= WORKFLOW ================= */}

    <ReviewSection title="Workflow">

      <ReviewItem
        label="Current automation"
        value={getAutomationLevelName()}
      />

      <div className="mt-5">

        <p className="text-[10px] font-semibold uppercase tracking-[0.18em] text-[#20394B]/85">
          Time-consuming activities
        </p>

        <div className="mt-3">
          <ReviewTags
            items={getActivityNames()}
          />
        </div>

      </div>

      {formData.workflowNotes && (
        <div className="mt-5">

          <p className="text-[10px] font-semibold uppercase tracking-[0.18em] text-[#20394B]/85">
            Workflow notes
          </p>

          <p className="mt-2 rounded-xl border border-[#20394B]/5 bg-[#F8FBF9] p-4 text-sm leading-6 text-[#20394B]/75">
            {formData.workflowNotes}
          </p>

        </div>
      )}

    </ReviewSection>


    {/* ================= CHALLENGES ================= */}

    <ReviewSection title="Challenges">

      <ReviewTags
        items={getChallengeNames()}
      />

      {formData.challengeNotes && (
        <div className="mt-5">

          <p className="text-[10px] font-semibold uppercase tracking-[0.18em] text-[#20394B]/85">
            Additional challenge notes
          </p>

          <p className="mt-2 rounded-xl border border-[#20394B]/5 bg-[#F8FBF9] p-4 text-sm leading-6 text-[#20394B]/75">
            {formData.challengeNotes}
          </p>

        </div>
      )}

    </ReviewSection>


    {/* Final notice */}

    <div className="flex items-start gap-3 rounded-2xl border border-[#20394B]/5 bg-[#F8FBF9] p-4">

      <span className="mt-0.5 text-sm text-[#64C786]">
        ●
      </span>

      <p className="text-xs leading-5 text-[#20394B]/85">
        Your information will be used to prepare your
        SCOUT automation readiness assessment.
      </p>

    </div>

  </div>
)}

    </WizardLayout>
  )
}

export default Assessment