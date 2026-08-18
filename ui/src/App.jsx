import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  // 1. Initialize our state with default safety values
  const [config, setConfig] = useState({
    cooldown_seconds: 1.5,
    pinch_threshold: 0.05,
    volume_sensitivity: 0.02,
    swipe_sensitivity: 0.15
  })
  
  const [statusMessage, setStatusMessage] = useState("")

  // 2. Fetch the actual database values on boot
  useEffect(() => {
    axios.get('http://localhost:5000/api/config')
      .then(response => {
        setConfig(response.data)
      })
      .catch(error => console.error("Could not fetch config:", error))
  }, [])

  // 3. Handle the slider movement
  const handleSliderChange = (event) => {
    const { name, value } = event.target
    setConfig(prevConfig => ({
      ...prevConfig,
      [name]: parseFloat(value)
    }))
  }

  // 4. Send the updated state back to Express
  const syncSettings = () => {
    setStatusMessage("Syncing...")
    axios.post('http://localhost:5000/api/config', config)
      .then(response => {
        setStatusMessage("✅ Live with Vision Engine!")
        setTimeout(() => setStatusMessage(""), 3000) // Clear message after 3 seconds
      })
      .catch(error => {
        console.error(error)
        setStatusMessage("❌ Sync Failed.")
      })
  }

  return (
    <div className="dashboard">
      <h1>Gesture Control Panel</h1>
      <p className="subtitle">Tune your spatial tracking parameters</p>

      <div className="control-group">
        <label>
          Action Cooldown ({config.cooldown_seconds}s)
          <input 
            type="range" name="cooldown_seconds" 
            min="0.5" max="5.0" step="0.1" 
            value={config.cooldown_seconds} onChange={handleSliderChange} 
          />
        </label>

        <label>
          Joystick Volume Sensitivity ({config.volume_sensitivity})
          <input 
            type="range" name="volume_sensitivity" 
            min="0.01" max="0.10" step="0.01" 
            value={config.volume_sensitivity} onChange={handleSliderChange} 
          />
        </label>

        <label>
          Track Swipe Distance ({config.swipe_sensitivity})
          <input 
            type="range" name="swipe_sensitivity" 
            min="0.05" max="0.40" step="0.01" 
            value={config.swipe_sensitivity} onChange={handleSliderChange} 
          />
        </label>
        
        <label>
          Pinch Activation Threshold ({config.pinch_threshold})
          <input 
            type="range" name="pinch_threshold" 
            min="0.02" max="0.10" step="0.01" 
            value={config.pinch_threshold} onChange={handleSliderChange} 
          />
        </label>
      </div>

      <button className="sync-btn" onClick={syncSettings}>
        Sync Settings
      </button>

      {statusMessage && <p className="status">{statusMessage}</p>}
    </div>
  )
}

export default App