import React from 'react'
import { Link } from 'react-router-dom'
import { PiShoppingCartThin } from "react-icons/pi";
import Logo from '@/components/ui/Logo';

const Header = () => {
  return (
    <>
    <header className="text-gray-600 body-font">
        <div className="container mx-auto flex flex-wrap p-5 flex-col md:flex-row items-center">
            <Logo />
            <nav className="md:ml-auto flex flex-wrap items-center text-base justify-center">
                <Link to={'/'} className="mr-5 hover:text-gray-900">Home</Link>
                <Link to={'/about'} className="mr-5 hover:text-gray-900">About</Link>
                <Link to={'/login'} className="mr-5 hover:text-gray-900">Login</Link>
            </nav>
            <Link to={'/cart'} className="p-3 text-xl bg-rose-500 text-white rounded-full">
                <PiShoppingCartThin /> 
            </Link>
        </div>
    </header>

    </>
  )
}

export default Header