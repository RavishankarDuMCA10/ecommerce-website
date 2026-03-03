import React from 'react'
import { AuthContextProvider } from '@/context/AuthContext'

const MainContext = ({children}) => {
  return (
    <AuthContextProvider>
      {children}
    </AuthContextProvider>
  )
}

export default MainContext