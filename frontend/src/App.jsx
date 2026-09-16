import { useState } from "react"
import Home from "./pages/Home"
import Assessment from "./pages/Assessment"

function App() {
  const [showAssessment, setShowAssessment] = useState(false)

  if (showAssessment) {
    return <Assessment />
  }

  return (
    <Home onStart={() => setShowAssessment(true)} />
  )
}

export default App
