import React from 'react'
import { Link } from 'react-router-dom'
import { GrArchlinux } from "react-icons/gr";

const Logo  = () => {
  return (
    <>
        <Link to={'/'} className="flex title-font font-medium items-center text-gray-900 mb-4 md:mb-0">
            <span className="text-xl p-4 bg-black rounded-full text-white">
                <GrArchlinux />
            </span>                
            <span className="ml-3 text-xl">Arc-com</span>
        </Link>
    </>
  )
}

export default Logo