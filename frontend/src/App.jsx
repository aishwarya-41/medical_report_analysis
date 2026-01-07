import { useState } from 'react'
import './App.css'
import { Route, Routes } from 'react-router'
import HomePage from './pages/HomePage'
import UploadPage from './pages/UploadPage'
import ReportPage from './pages/ReportPage'
import AskPage from './pages/AskPage'

function App() {
  return (
    <>
      <Routes>
        <Route index element={<HomePage/>}/>
        <Route path="/upload" element={<UploadPage/>}/>
        <Route path="/report" element={<ReportPage/>}/>
        <Route path="/ask" element={<AskPage/>}/>
      </Routes>
    </>
  )
}

export default App
