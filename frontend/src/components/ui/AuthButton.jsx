import React from 'react'
import clsx from 'clsx'
import { CgSpinner } from 'react-icons/cg'
import { IoIosArrowRoundForward } from "react-icons/io";

const AuthButton = ({
    isLoading = false,
    text,
    className
}) => {
  return (
    <button disabled={isLoading} type={isLoading?'button':'submit'} className={clsx("w-full py-3 rounded bg-black text-white outline-none cursor-pointer disabled:cursor-no-drop flex items-center justify-center gap-x-1", className, "disabled:bg-gray-800")}>
        <span>{text}</span> {
            isLoading ? <CgSpinner className='animate-spin'/> : <IoIosArrowRoundForward className='text-xl' />
        }
    </button>
  )
}

export default AuthButton