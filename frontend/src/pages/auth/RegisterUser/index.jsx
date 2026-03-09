import React, { useState } from 'react'
import Logo from '@/components/ui/Logo'
import AuthButton from '@/components/ui/AuthButton'
import { FaEye, FaEyeSlash } from 'react-icons/fa'
import { Link } from 'react-router-dom'
import {Formik, Form, Field, ErrorMessage} from 'formik'
import * as yup from 'yup'
import { ROLE_TYPE } from '@/constant/auth.constant'
import { axiosClient } from '@/utils/axiosClient'
import { toast } from 'react-toastify'

const RegisterUser = () => {

  const [isLoading, setIsLoading] = useState(false)
  const [isHide, setIsHide] = useState(true)

  const validationSchema = yup.object({
    name: yup.string().required('Name is required'),
    email: yup.string().email('Invalid email format').required('Email must be a proper email'),
    password: yup.string().min(6, 'Password must be at least 6 characters').required('Password is required'),
    role: yup.string().required('Role is required').oneOf(Object.values(ROLE_TYPE), 'Role must be either buyer or seller')
  })

  const onSubmitHandler = async (value, helpers) => {
    try {
      setIsLoading(true)
      const response = await axiosClient.post("/auth/register", value)
      const data = response.data
      // console.log(data)
      toast.success(data.message || "Registration successful")
      helpers.resetForm()
    } catch (error) {
      // console.log(error)
      toast.error(error.response.data.details || error.message)
    } finally {
      setIsLoading(false)
    }
  }

  const initialValues={name:'', email:'', password:'', role:ROLE_TYPE.BUYER}

  return (
    <>
    <Formik validationSchema={validationSchema} onSubmit={onSubmitHandler} initialValues={initialValues}>
      <Form className="min-h-screen flex items-center justify-center">
        <div className="w-[96%] mx-auto lg:1/2 xl:w-1/3 p-4 lg:px-10 rounded border border-gray-100 shadow">
          <div className="mb-3 w-full flex justify-center">
            <Logo className={'mx-auto block'} />
          </div>
          <div className="mb-3">
            <label htmlFor="name">Name <span className="text-red-500">*</span></label>
            <Field name='name' id='name' type="text" className="w-full py-2 px-2 rounded outline-none bg-gray-50 border border-gray-200" placeholder='Enter You Name' />
            <ErrorMessage name='name' component={'p'} className='text-red-500' />
          </div>
          <div className="mb-3">
            <label htmlFor="email">Email <span className="text-red-500">*</span></label>
            <Field name='email' id='email' type="email" className="w-full py-2 px-2 rounded outline-none bg-gray-50 border border-gray-200" placeholder='Enter Your Email' />
            <ErrorMessage name='email' component={'p'} className='text-red-500' />
          </div>
          <div className="mb-3">
            <label htmlFor="password">Password <span className="text-red-500">*</span></label>
            <div className="w-full px-2 rounded outline-none bg-gray-50 border border-gray-200 flex justify-between items-center">
              <Field name='password' id='password' type={isHide ? "password" : "text"} className='w-full py-2 outline-none' placeholder='Enter Your Password' />
              <button onClick={()=>setIsHide(!isHide)} type='button' className='text-xl'>
                {isHide ? <FaEye /> : <FaEyeSlash />}
              </button>
            </div>
            <ErrorMessage name='password' component={'p'} className='text-red-500' />            
          </div>
          <div className="mb-3">
            <label htmlFor="Role">Role <span className="text-red-500">*</span></label>
            <Field as='select' name='role' id='role' className="w-full py-2 px-2 rounded outline-none bg-gray-50 border border-gray-200">
              {
                Object.values(ROLE_TYPE).map((cur, i) =>{
                  return <option key={i} value={cur} className='capitalize'>{cur}</option>
                })
              }
            </Field>
            <ErrorMessage name='role' component={'p'} className='text-red-500' />
          </div>
          <div className="mb-3">
            <AuthButton
              isLoading={isLoading}
              text="Register"
            />
          </div>
          <div className='mb-3 flex justify-center items-center gap-x-6'>
            <div className='w-full h-[0.1000px] bg-gray-400'></div>
            <div className=''>OR</div>
            <div className='w-full h-[0.1000px] bg-gray-400'></div>
          </div>
          <div className="mb-3 text-center">
            <p>
              Already Have An Account ? <Link to={'/login'} className='text-red-600'>Login</Link>
            </p>
          </div>
        </div>
      </Form>
      </Formik>
    </>
  )
}

export default RegisterUser