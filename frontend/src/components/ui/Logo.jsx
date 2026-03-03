import React from 'react'
import { Link } from 'react-router-dom'
import { GiGoat } from "react-icons/gi";

const Logo  = () => {
  return (
    <>
        <Link to={'/'} className="flex title-font font-medium items-center text-gray-900 mb-4 md:mb-0">
            <span className="text-xl p-4 bg-black rounded-full text-white">
                <GiGoat className='text-2xl' />
            </span>                
            <span className="ml-3 text-xl">EcomFarm</span>
        </Link>
    </>
  )
}

export default Logo