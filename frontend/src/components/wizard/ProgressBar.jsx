import { assessmentSteps } from "../../data/assessmentSteps"

function ProgressBar({ currentStep }) {
  return (
    <div className="w-full">

      {/* ================= TOP INFO ================= */}
      <div className="
        mb-6
        flex
        items-start
        justify-between
      ">

        <div>

          <p className="
            text-[10px]
            font-bold
            uppercase
            tracking-[0.2em]
            text-[#2C8F59]
          ">
            SCOUT AI Assessment
          </p>

          <p className="
            mt-1
            text-xs
            font-medium
            text-[#20394B]/90
          ">
            Complete your business assessment
          </p>

        </div>


        {/* Counter */}
        <div className="
          rounded-full
          border
          border-[#64C786]/40
          bg-[#64C786]/10
          px-4
          py-2
          text-xs
          font-semibold
          text-[#2C8F59]
        ">
          <span className="font-bold text-[#2C8F59]">
            {String(currentStep).padStart(2, "0")}
          </span>

          <span className="mx-1 text-[#20394B]/60">
            /
          </span>

          <span className="text-[#20394B]/75">
            {String(assessmentSteps.length).padStart(2, "0")}
          </span>
        </div>

      </div>


      {/* ================= PROGRESS ================= */}
      <div className="
        relative
        flex
        items-center
        justify-between
      ">

        {/* Background Line */}
        <div className="
          absolute
          left-0
          right-0
          top-1/2
          h-1
          -translate-y-1/2
          rounded-full
          bg-[#20394B]/35
        " />


        {/* Completed Line */}
        <div
          className="
            absolute
            left-0
            top-1/2
            h-1
            -translate-y-1/2
            rounded-full
            bg-[#64C786]
            transition-all
            duration-500
          "
          style={{
            width:
              assessmentSteps.length > 1
                ? `${((currentStep - 1) / (assessmentSteps.length - 1)) * 100}%`
                : "0%",
          }}
        />


        {/* Steps */}
        {assessmentSteps.map((step) => {

          const completed = step.id < currentStep
          const active = step.id === currentStep

          return (
            <div
              key={step.id}
              className="
                relative
                z-10
                flex
                flex-col
                items-center
              "
            >

              {/* Circle */}
              <div
                className={`
                  flex
                  h-9
                  w-9
                  items-center
                  justify-center
                  rounded-full
                  border
                  text-[11px]
                  font-semibold
                  transition-all
                  duration-500

                  ${
                    completed
                      ? `
                        border-[#64C786]
                        bg-[#64C786]
                        text-[#173326]
                        shadow-[0_5px_18px_rgba(100,199,134,0.20)]
                      `
                      : active
                        ? `
                          border-[#64C786]
                          bg-white
                          text-[#2C8F59]
                          shadow-[0_0_0_5px_rgba(100,199,134,0.10)]
                        `
                        : `
                          border-[#20394B]/25
                          bg-[#E8EFEB]
                          text-[#20394B]/80
                        `
                  }
                `}
              >

                {completed ? "✓" : String(step.id).padStart(2, "0")}

              </div>


              {/* Label */}
              <span
                className={`
                  mt-3
                  hidden
                  whitespace-nowrap
                  text-[9px]
                  font-semibold
                  uppercase
                  tracking-[0.12em]
                  sm:block

                  ${
                    active
                      ? "text-[#2C8F59]"
                      : completed
                        ? "text-[#20394B]/70"
                        : "text-[#20394B]/75"
                  }
                `}
              >
                {step.label}
              </span>

            </div>
          )
        })}

      </div>

    </div>
  )
}

export default ProgressBar