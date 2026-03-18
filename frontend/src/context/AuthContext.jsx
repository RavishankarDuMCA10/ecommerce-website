import React, { createContext, useContext, useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { setUser, UserSlicePath } from '@/redux/slice/user.slice'
import axios from 'axios'
import { axiosClient } from '@/utils/axiosClient'
import { toast } from 'react-toastify'

const AuthContext = createContext()

export const useAuthContext = () => useContext(AuthContext)

export const AuthContextProvider = ({children}) => {

    const user = useSelector(UserSlicePath)
    const dispatch = useDispatch()

    const fetchUSerProfile = async() => {
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
      }
    }

    useEffect(() => {
      fetchUSerProfile()
    }, [])
  return (
    <AuthContext.Provider value={{ user }}>
      {children}
    </AuthContext.Provider>
  )
}