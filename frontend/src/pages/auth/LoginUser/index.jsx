import React, { useState } from 'react'
import Logo from '@/components/ui/Logo'
import AuthButton from '@/components/ui/AuthButton'
import { FaEye, FaEyeSlash } from 'react-icons/fa'

const LoginUser = () => {

  const [isLoading, setIsLoading] = useState(false)
  const [isHide, setIsHide] = useState(true)

  return (
    <>
      <div className="min-h-[60vh] flex items-center justify-center">
        <div className="w-[96%] mx-auto lg:1/2 xl:w-1/3 p-4 lg:px-10 rounded border border-gray-100 shadow">
          <div className="mb-3 w-full flex justify-center">
            <Logo className={'mx-auto block'} />
          </div>
          <div className="mb-3">
            <label htmlFor="name">Name <span className="text-red-500">*</span></label>
            <input id='name' type="text" className="w-full py-2 px-2 rounded outline-none bg-gray-50 border border-gray-200" placeholder='Enter You Name' />
          </div>
          <div className="mb-3">
            <label htmlFor="email">Email <span className="text-red-500">*</span></label>
            <input id='email' type="email" className="w-full py-2 px-2 rounded outline-none bg-gray-50 border border-gray-200" placeholder='Enter Your Email' />
          </div>
          <div className="mb-3">
            <label htmlFor="password">Password <span className="text-red-500">*</span></label>
            <div className="w-full px-2 rounded outline-none bg-gray-50 border border-gray-200 flex justify-between items-center">
              <input id='password' type={isHide ? "password" : "text"} className='w-full py-2 outline-none' placeholder='Enter Your Password' />
              <button onClick={()=>setIsHide(!isHide)} type='button' className='text-xl'>
                {isHide ? <FaEye /> : <FaEyeSlash />}
              </button>
            </div>            
          </div>
          <div className="mb-3">
            <AuthButton
              isLoading={isLoading}
              text="Login"
            />
          </div>
        </div>
      </div>
    </>
  )
}

export default LoginUser