import React from 'react'
import { Link } from 'react-router-dom'
import { FiShoppingBag } from "react-icons/fi";

const Logo  = () => {
  return (
    <>
        <Link to={'/'} className="flex title-font font-medium items-center text-gray-900 mb-4 md:mb-0">
            <span className="text-black text-3xl">
                <FiShoppingBag />
            </span>                
            <span className="ml-3 text-xl">Ecom</span>
        </Link>
    </>
  )
}

export default Logo