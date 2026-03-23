import React from 'react'
import { FaTrash } from "react-icons/fa";
import AddAddressModel from './AddAddressModel';
import { useAuthContext } from '@/context/AuthContext';
import { axiosClient } from '@/utils/axiosClient';
import { toast } from 'react-toastify';


const UserAddress = () => {
    const {user, fetchUserProfile} = useAuthContext()
    const address = [
        {
            "id": 1,
            "address": "Deoria"
        },
        {
            "id": 2,
            "address": "Gorakhpur"
        }
    ]

    const deleteAddressHandler = async(id) => {
        try {
            if(!confirm("Are you sure you want to delete this address?")) return
            const response = await axiosClient.delete("/auth/delete-address/"+id, {                
                headers: {  'Authorization': `Bearer ${localStorage.getItem("token")}` }
            })
            const data = await response.data
            console.log("data:", data)
            toast.success(data)
            await fetchUserProfile()
        } catch (error) {
            toast.error(error.response.data.detail || error.message)
        }
    }
  return (
    <>
        <div className="py-10">
            <div className="flex mb-4 items-center justify-between">
                <h4 className='text-2xl font-bold mb-4'>Address</h4>                
                 <AddAddressModel />
            </div>
            
            <div className="flex flex-col gap-y-3">
                {
                    user && user.address && user.address.length > 0 ? user.address.map((cur, i) => {
                        return <div key={i} className='w-full py-2 rounded- px-2 bg-gray-100 border border-gray-200 flex items-center justify-between'>
                            <div className="flex flex-col">
                                <h3 className='text-xl font-bold'>Address {i + 1}</h3>
                                <p className='text-xl text-zinc-600'>{
                                    cur.landmark + ", " + cur.city + ", " + cur.state + ", " + cur.country + " - " + cur.pin_code
                            }</p>
                            </div>
                            <div className="flex items-center gap-x-3">
                                <button 
                                onClick={()=>deleteAddressHandler(cur._id)}
                                >
                                    <FaTrash className='text-red-500' />
                                </button>                                
                            </div>
                            
                        </div>
                    }) : <p className='text-center py-5 border border-gray-200 bg-gray-100'>No addresses found</p>
                }
            </div>
        </div>
    </>
  )
}

export default UserAddress