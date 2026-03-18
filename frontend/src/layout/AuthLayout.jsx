import LoaderComponent from '@/components/ui/LoaderComponent'
import { UserSlicePath } from '@/redux/slice/user.slice'
import React, { useEffect, useState } from 'react'
import { useSelector } from 'react-redux'
import { useNavigate } from 'react-router-dom'

const AuthLayout = ({children}) => {
    const user = useSelector(UserSlicePath)
    const [loading, setLoading] = useState(true)
    const navigate = useNavigate()

    useEffect(() => {
        if (user) {
            navigate("/dashboard")
            return <></>
        }
    }, [user])

    if (loading) {
        return <div className='h-screen flex justify-center items-center'>
            <LoaderComponent />
        </div>
    }
  return (
    <>
        {children}
    </>
  )
}

export default AuthLayout