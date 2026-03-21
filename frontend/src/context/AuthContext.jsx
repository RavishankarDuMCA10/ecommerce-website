import React, { createContext, useContext, useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { removeUser, setUser, UserSlicePath } from '@/redux/slice/user.slice'
import axios from 'axios'
import { axiosClient } from '@/utils/axiosClient'
import { toast } from 'react-toastify'
import { useNavigate } from 'react-router-dom'
import LoaderComponent from '@/components/ui/LoaderComponent'

const AuthContext = createContext({
  user: null,
  fetchUserProfile: () => {},
  logoutUser: () => {},
})

export const useAuthContext = () => useContext(AuthContext)


export const AuthContextProvider = ({children}) => {

    const user = useSelector(UserSlicePath)
    const dispatch = useDispatch()
    const [loading, setLoading] = useState(true)
    const navigate = useNavigate()

    /*
    * # Fetch user profile
    * - if token exist
    */
    const fetchUserProfile = async() => {
      try{
        const token = localStorage.getItem("token") || ""
        if (!token) return
        const response = await axiosClient.get("/auth/profile", {
          headers: {
            'Authorization': 'Bearer ' + token
          }
        })
        const data = response.data
        // console.log(data)
        dispatch(setUser(data))
      } catch (error) {
        toast.error(error.response.data.details || error.message)
      } finally {
        setLoading(false)
      }
    }

    useEffect(() => {
      fetchUserProfile()
    }, [])

    /**
     * # Logout user
     */
    const logoutUser=() => {
      localStorage.removeItem("token")
      dispatch(removeUser)
      toast.success("Logout successful")
      navigate('/')
    }

    if (loading) {
      return <div className='h-screen flex justify-center items-center'>
        <LoaderComponent />
      </div>
    }
  return (
    <AuthContext.Provider value={{ user, logoutUser, fetchUserProfile }}>
      {children}
    </AuthContext.Provider>
  )
}