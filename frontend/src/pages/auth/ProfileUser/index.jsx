import React from 'react'
import AvatarComponent from './components/AvatarComponent'
import BasicDetails from './components/BasicDetails'
import AccountType from './components/AccountType'

const ProfileUser = () => {
  return (
    <>
      <AvatarComponent />
      <div className="lg w-1/2 mx-auto">
        <BasicDetails />
        <AccountType />
      </div>      
    </>
  )
}

export default ProfileUser