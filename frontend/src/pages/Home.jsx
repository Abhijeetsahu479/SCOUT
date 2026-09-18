function Home({ onStart }) {
  return (
    <main className="min-h-screen bg-white text-[#12304A]">

      {/* =====================================================
          HEADER
      ===================================================== */}
      <header className="border-b border-[#E5E9ED] bg-[#294B63]">

        <div className="mx-auto flex h-24 max-w-7xl items-center justify-between px-6">

          {/* LOGO */}
          <a href="/" className="flex items-center">
            <img
              src="/logo.jpg"
              alt="CodeGrameen"
              className="h-20 w-44 object-contain"
            />
          </a>

          {/* HEADER CTA */}
          <button
            type="button"
            onClick={onStart}
            className="hidden rounded-full bg-[#65D391] px-7 py-3.5 text-sm font-bold text-[#12304A] shadow-md transition duration-300 hover:bg-[#7BE0A3] hover:shadow-lg lg:block"
          >
            AI ASSESSMENT →
          </button>

          {/* MOBILE CTA */}
          <button
            type="button"
            onClick={onStart}
            className="rounded-full bg-[#65D391] px-5 py-2.5 text-sm font-bold text-[#12304A] lg:hidden"
          >
            Start
          </button>

        </div>

      </header>


      {/* =====================================================
          HERO SECTION
      ===================================================== */}
      <section className="relative overflow-hidden bg-white">

        {/* SOFT GREEN BACKGROUND */}
        <div className="pointer-events-none absolute right-0 top-0 h-96 w-96 rounded-full bg-[#65D391] opacity-10 blur-3xl" />

        <div className="mx-auto max-w-7xl px-6 py-20 lg:py-28">

          <div className="grid items-center gap-14 lg:grid-cols-2">


            {/* =================================================
                LEFT CONTENT
            ================================================= */}
            <div>

              {/* SCOUT BADGE */}
              <div className="mb-7 inline-flex items-center gap-2 rounded-full border border-[#65D391] bg-[#F0FBF4] px-4 py-2">

                <span className="h-2 w-2 rounded-full bg-[#20A761]" />

                <span className="text-xs font-bold uppercase tracking-widest text-[#159453]">
                  SCOUT AI
                </span>

              </div>


              {/* MAIN HEADING */}
              <h1 className="max-w-2xl text-5xl font-bold leading-tight tracking-tight text-[#12304A] md:text-6xl lg:text-7xl">

                Discover where your

                <span className="block text-[#20A761]">
                  business
                </span>

                is ready for AI.

              </h1>


              {/* DESCRIPTION */}
              <p className="mt-7 max-w-2xl text-base leading-7 text-[#4F687A] md:text-lg md:leading-8">
                SCOUT analyzes your business processes, repetitive work,
                challenges and automation readiness to identify practical
                opportunities for AI-powered transformation.
              </p>


              {/* BUTTONS */}
              <div className="mt-8 flex flex-col gap-4 sm:flex-row sm:items-center">

                <button
                  type="button"
                  onClick={onStart}
                  className="rounded-full bg-[#294B63] px-8 py-4 text-sm font-bold text-white shadow-lg transition duration-300 hover:bg-[#1D3B50] hover:shadow-xl"
                >
                  Start Assessment →
                </button>

                <button
                  type="button"
                  onClick={() =>
                    document.getElementById("how-it-works")?.scrollIntoView({
                      behavior: "smooth",
                    })
                  }
                  className="rounded-full border border-[#294B63] bg-white px-8 py-4 text-sm font-semibold text-[#294B63] transition duration-300 hover:bg-[#294B63] hover:text-white"
                >
                  See How It Works
                </button>

              </div>


              {/* TIME */}
              <p className="mt-3 text-sm text-[#526B7A]">
                Takes approximately 5–7 minutes
              </p>


              {/* FEATURES */}
              <div className="mt-10 flex flex-wrap gap-x-8 gap-y-4">

                <div className="flex items-center gap-2">
                  <span className="font-bold text-[#20A761]">
                    ✓
                  </span>

                  <span className="text-sm text-[#4F687A]">
                    Business-focused
                  </span>
                </div>


                <div className="flex items-center gap-2">
                  <span className="font-bold text-[#20A761]">
                    ✓
                  </span>

                  <span className="text-sm text-[#4F687A]">
                    Actionable insights
                  </span>
                </div>


                <div className="flex items-center gap-2">
                  <span className="font-bold text-[#20A761]">
                    ✓
                  </span>

                  <span className="text-sm text-[#4F687A]">
                    ROI-oriented
                  </span>
                </div>

              </div>

            </div>


            {/* =================================================
                RIGHT DASHBOARD
            ================================================= */}
            <div>

              <div className="rounded-3xl border border-[#DCE4E9] bg-white p-6 shadow-xl md:p-8">

                {/* DASHBOARD HEADER */}
                <div className="flex items-center justify-between">

                  <div>

                    <p className="text-xs font-bold uppercase tracking-widest text-[#526B7A]">
                      SCOUT Dashboard
                    </p>

                    <h2 className="mt-2 text-lg font-semibold text-[#12304A]">
                      AI Readiness Snapshot
                    </h2>

                  </div>


                  {/* LIVE */}
                  <div className="rounded-full bg-[#EFFAF3] px-4 py-2">

                    <span className="text-xs font-bold text-[#159453]">
                      ● LIVE
                    </span>

                  </div>

                </div>


                {/* SCORE CARD */}
                <div className="mt-7 rounded-2xl border border-[#E1E7EB] bg-[#FAFCFD] p-6">

                  <p className="text-sm text-[#526B7A]">
                    Example readiness score
                  </p>


                  <div className="mt-2 flex items-end justify-between">

                    <div>

                      <span className="text-6xl font-bold text-[#12304A]">
                        78
                      </span>

                      <span className="ml-2 text-sm text-[#526B7A]">
                        / 100
                      </span>

                    </div>


                    {/* STATUS */}
                    <div className="rounded-xl bg-[#EFFAF3] px-5 py-3 text-center">

                      <p className="text-xs uppercase tracking-wider text-[#526B7A]">
                        Status
                      </p>

                      <p className="mt-1 text-sm font-bold text-[#159453]">
                        AI Ready
                      </p>

                    </div>

                  </div>


                  {/* PROGRESS */}
                  <div className="mt-6 h-3 overflow-hidden rounded-full bg-[#E3E8EC]">

                    <div className="h-full w-3/4 rounded-full bg-[#20B464]" />

                  </div>

                </div>


                {/* STATS */}
                <div className="mt-4 grid grid-cols-2 gap-4">

                  {/* AUTOMATION */}
                  <div className="rounded-2xl border border-[#E1E7EB] bg-white p-5">

                    <p className="text-xs font-semibold uppercase tracking-wider text-[#526B7A]">
                      Automation
                    </p>

                    <p className="mt-2 text-base font-bold text-[#12304A]">
                      12 opportunities
                    </p>

                  </div>


                  {/* POTENTIAL */}
                  <div className="rounded-2xl border border-[#E1E7EB] bg-white p-5">

                    <p className="text-xs font-semibold uppercase tracking-wider text-[#526B7A]">
                      Potential
                    </p>

                    <p className="mt-2 text-base font-bold text-[#20A761]">
                      High impact
                    </p>

                  </div>

                </div>


                {/* INSIGHT */}
                <div className="mt-4 rounded-2xl border border-[#B9EFD0] bg-[#F1FBF5] p-5">

                  <div className="flex gap-4">

                    {/* ICON */}
                    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-white text-lg text-[#20A761] shadow-sm">
                      ✦
                    </div>


                    <div>

                      <p className="text-sm font-bold text-[#12304A]">
                        What SCOUT helps uncover
                      </p>

                      <p className="mt-1 text-sm leading-6 text-[#526B7A]">
                        Where automation can reduce repetitive work,
                        improve efficiency and create measurable business value.
                      </p>

                    </div>

                  </div>

                </div>

              </div>

            </div>

          </div>


          {/* BOTTOM LINE */}
          <div className="mt-16 border-t border-[#E5EAEE] pt-7">

            <p className="text-center text-xs font-semibold uppercase tracking-widest text-[#526B7A]">
              AI-powered business transformation
            </p>

          </div>

        </div>

      </section>


      {/* =====================================================
          HOW IT WORKS
      ===================================================== */}
      <section
        id="how-it-works"
        className="border-t border-[#E5EAEE] bg-[#F7F9FA]"
      >

        <div className="mx-auto max-w-7xl px-6 py-16 lg:py-20">

          <div className="max-w-2xl">
            <p className="text-xs font-bold uppercase tracking-widest text-[#159453]">
              HOW SCOUT WORKS
            </p>

            <h2 className="mt-3 text-3xl font-bold tracking-tight text-[#12304A] md:text-4xl">
              From assessment to practical next steps.
            </h2>

            <p className="mt-4 text-base leading-7 text-[#4F687A]">
              SCOUT turns your business inputs into a clear view of where
              automation can create measurable value.
            </p>
          </div>

          <div className="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
            {[
              {
                number: "01",
                title: "Complete Assessment",
                description:
                  "Tell us about your company, departments, workflows and challenges.",
              },
              {
                number: "02",
                title: "Check Readiness",
                description:
                  "Get an automation readiness score based on your submitted information.",
              },
              {
                number: "03",
                title: "Find Opportunities",
                description:
                  "Identify departments and workflows where automation can help.",
              },
              {
                number: "04",
                title: "Get Recommendations",
                description:
                  "Receive quick wins, recommendations and indicative ROI estimates.",
              },
              {
                number: "05",
                title: "Receive Your Report",
                description:
                  "Get your SCOUT assessment report and PDF through the existing workflow.",
              },
            ].map((step) => (
              <article
                key={step.number}
                className="rounded-2xl border border-[#DCE4E9] bg-white p-5 shadow-sm"
              >
                <p className="text-xs font-bold tracking-[0.2em] text-[#20A761]">
                  STEP {step.number}
                </p>

                <h3 className="mt-5 text-base font-bold leading-6 text-[#12304A]">
                  {step.title}
                </h3>

                <p className="mt-3 text-sm leading-6 text-[#526B7A]">
                  {step.description}
                </p>
              </article>
            ))}
          </div>

          <div className="mt-10">
            <button
              type="button"
              onClick={onStart}
              className="rounded-full bg-[#294B63] px-7 py-3.5 text-sm font-bold text-white shadow-md transition duration-300 hover:bg-[#1D3B50] hover:shadow-lg"
            >
              Start Assessment →
            </button>
          </div>

        </div>

      </section>


      {/* =====================================================
          FOOTER
      ===================================================== */}
      <footer className="border-t border-[#E2E7EA] bg-[#F7F9FA]">

        <div className="mx-auto flex max-w-7xl flex-col gap-2 px-6 py-6 text-center text-sm text-[#526B7A] sm:flex-row sm:items-center sm:justify-between">

          <span>
            Powered by CodeGrameen
          </span>

          <span>
            SCOUT AI Assessment • 2026
          </span>

        </div>

      </footer>

    </main>
  )
}

export default Home