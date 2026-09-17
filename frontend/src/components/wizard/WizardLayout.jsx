import ProgressBar from "./ProgressBar"

function WizardLayout({
  currentStep,
  children,
  onBack,
  onNext,
  isFirstStep,
  isLastStep,
  isSubmitting = false,
}) {
  const buttonText = isSubmitting
    ? "Generating Report..."
    : isLastStep
      ? "Submit Assessment"
      : "Continue"

  return (
    <main className="min-h-screen bg-[#F7F9F8] text-[#20394B]">

      {/* ================= HEADER ================= */}
      <header className="border-b border-[#20394B]/10 bg-[#20394B] shadow-sm">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-5 py-3 sm:px-8 lg:px-10">

          {/* Brand */}
          <a href="/" className="flex items-center">
            <img
              src="/logo.jpg"
              alt="CodeGrameen"
              className="h-20 w-44 object-contain"
            />
          </a>

          {/* Header badge */}
          <div className="rounded-full border border-[#64C786]/40 bg-[#64C786]/10 px-4 py-2 text-[10px] font-semibold uppercase tracking-[0.18em] text-[#64C786]">
            AI Assessment
          </div>

        </div>
      </header>


      {/* ================= CONTENT ================= */}
      <section className="mx-auto max-w-6xl px-5 pb-12 pt-8 sm:px-8 sm:pt-10 lg:px-10">

        <ProgressBar currentStep={currentStep} />

        {/* Main form area */}
        <div className="mt-8 grid gap-8 lg:grid-cols-[minmax(0,1fr)_260px] lg:items-start">

          {/* Form card */}
          <div className="rounded-[24px] border border-[#20394B]/10 bg-white p-6 shadow-[0_18px_55px_rgba(32,57,75,0.08)] sm:p-8 lg:p-9">
            {children}
          </div>


          {/* Right information panel */}
          <aside className="hidden lg:block lg:pt-8">

            <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-[#64C786]">
              SCOUT AI
            </p>

            <h3 className="mt-3 text-2xl font-semibold leading-tight text-[#20394B]">
              Understand your business.
              <br />
              Unlock what's possible.
            </h3>

            <p className="mt-4 text-sm leading-6 text-[#20394B]/90">
              Help us understand your organisation so SCOUT can identify
              practical opportunities for AI-powered automation.
            </p>

            <div className="mt-6 space-y-4">

              {[
                "Tailored to your business",
                "Actionable recommendations",
                "Focus on real impact",
              ].map((item) => (
                <div
                  key={item}
                  className="flex items-center gap-3"
                >
                  <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-[#64C786] text-[10px] font-bold text-white">
                    ✓
                  </span>

                  <span className="text-xs font-medium text-[#20394B]/90">
                    {item}
                  </span>
                </div>
              ))}

            </div>

          </aside>

        </div>


        {/* ================= NAVIGATION ================= */}
        <div className="mt-6 flex items-center justify-between">

          {/* Back button */}
          <button
            type="button"
            onClick={onBack}
            disabled={isFirstStep || isSubmitting}
            className={
              isFirstStep || isSubmitting
                ? "cursor-not-allowed rounded-full px-5 py-3 text-sm font-medium text-[#20394B]/45"
                : "rounded-full px-5 py-3 text-sm font-medium text-[#20394B]/60 transition-all hover:bg-[#20394B]/5 hover:text-[#20394B]"
            }
          >
            ← Back
          </button>


          {/* Continue / Submit button */}
          <button
            type="button"
            onClick={onNext}
            disabled={isSubmitting}
            className={
              isSubmitting
                ? "flex cursor-not-allowed items-center gap-3 rounded-full bg-[#64C786] px-7 py-3.5 text-sm font-semibold text-[#173326] opacity-70"
                : "group flex items-center gap-3 rounded-full bg-[#64C786] px-7 py-3.5 text-sm font-semibold text-[#173326] shadow-[0_8px_25px_rgba(100,199,134,0.20)] transition-all duration-300 hover:-translate-y-0.5 hover:bg-[#78D99A] hover:shadow-[0_12px_30px_rgba(100,199,134,0.25)] active:translate-y-0"
            }
          >

            {isSubmitting && (
              <span className="h-4 w-4 animate-spin rounded-full border-2 border-[#173326]/30 border-t-[#173326]" />
            )}

            <span>
              {buttonText}
            </span>

            {!isSubmitting && (
              <span className="transition-transform duration-300 group-hover:translate-x-1">
                →
              </span>
            )}

          </button>

        </div>

      </section>

    </main>
  )
}

export default WizardLayout