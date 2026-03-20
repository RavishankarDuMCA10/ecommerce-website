import React from 'react'
import { Routes, Route } from 'react-router-dom'
import LoginUser from '@/pages/auth/LoginUser'
import Dashboard from '@/pages/Dashboard'
import CartPage from '@/pages/CartPage'
import MainLayout from '@/layout/MainLayout'
import HomePage from '@/pages/HomePage'
import RegisterUser from '@/pages/auth/RegisterUser'
import AuthLayout from '@/layout/AuthLayout'
import ProtectedLayout from '@/layout/ProtectedLayout'
import ProfileUser from '@/pages/auth/ProfileUser'

const App = () => {
  return (
    <>
    <Routes>
      <Route path='/' Component={MainLayout} > 
        <Route index Component={HomePage} />
        <Route path='/cart' Component={CartPage} />        
        <Route Component={ProtectedLayout}>
          <Route path='/dashboard' Component={Dashboard} />
          <Route path='/profile' Component={ProfileUser} />
        </Route>
      </Route>
      
      <Route Component={AuthLayout}>
        <Route path='/login' Component={LoginUser} />
        <Route path='/register' Component={RegisterUser} />
      </Route>
    </Routes>
    </>
  )
}

export default App