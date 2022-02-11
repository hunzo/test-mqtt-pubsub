import { useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  setInterval(() => {
    // console.log('test')
    getCounter()
  }, 2000)

  const getCounter = () => {
    // fetch('http://localhost:8081/api/get?key=test')
    fetch('http://localhost:8000/counter/show')
      .then((res) => res.json())
      .then((data) => setCount(data.count))
      .catch((e) => console.log(e))
  }

  const start = () => {
    // fetch('http://localhost:8081/api/get?key=test')
    fetch('http://localhost:8000/control/start')
      .then((res) => res.json())
      .then((data) => setCount(data.count))
      .catch((e) => console.log(e))
  }
  const stop = () => {
    // fetch('http://localhost:8081/api/get?key=test')
    fetch('http://localhost:8000/control/stop')
      .then((res) => res.json())
      .then((data) => setCount(data.count))
      .catch((e) => console.log(e))
  }

  const clear = () => {
    // fetch('http://localhost:8081/api/get?key=test')
    const q = prompt('reset counter')
    if (!q) {
      alert(`please type "yes" to reset counter`)
      return
    }
    fetch('http://localhost:8000/counter/clear', {
      method: 'DELETE',
    })
      .then((res) => res.json())
      .then((data) => setCount(data.count))
      .catch((e) => console.log(e))
  }

  const inc = () => {
    // fetch('http://localhost:8081/api/get?key=test')
    fetch('http://localhost:8000/counter/inc', {
      method: 'POST',
    })
      .then((res) => res.json())
      .then((data) => setCount(data.count))
      .catch((e) => console.log(e))
  }
  const dec = () => {
    // fetch('http://localhost:8081/api/get?key=test')
    fetch('http://localhost:8000/counter/dec', {
      method: 'POST',
    })
      .then((res) => res.json())
      .then((data) => setCount(data.count))
      .catch((e) => console.log(e))
  }

  return (
    <div className='App'>
      <button
        onClick={() => {
          start()
        }}
      >
        start
      </button>
      <button
        onClick={() => {
          stop()
        }}
      >
        stop
      </button>
      <button
        onClick={() => {
          clear()
        }}
      >
        clear
      </button>
      <button onClick={() => inc()}>+</button>
      <button onClick={() => dec()}>-</button>
      <div style={{ fontSize: '600px' }}>{count}</div>
    </div>
  )
}

export default App
