import { useAuthContext } from '@/context/AuthContext';
import { axiosClient } from '@/utils/axiosClient';
import React, {useCallback, useState} from 'react'
import {useDropzone} from 'react-dropzone'
import { CgSpinner } from 'react-icons/cg';
import { FaCamera } from "react-icons/fa";
import { FiUploadCloud } from "react-icons/fi";
import { toast } from 'react-toastify';



const AvatarComponent = () => {
    const [loading, setLoading] = useState(false)
    const { user, fetchUserProfile } = useAuthContext() 
    const onDrop = useCallback(async(acceptedFiles) => {
        
        try {
            setLoading(true)
            const formData = new FormData()
            formData.append("avatar", acceptedFiles[0])
            const response = await axiosClient.put("/auth/update-avatar", formData, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem("token")}`,
                }
            })
            const data = await response.data
            console.log(data)
            await fetchUserProfile()
            toast.success("Avatar updated successfully")
        } catch (error) {
         toast.error(error.response.data.detail || error.message)   
        } finally {
            setLoading(false)
        }
    }, [])
    const {getRootProps, getInputProps, isDragActive} = useDropzone({
        onDrop,
        multiple: false,
        accept: {
        'image/jpeg': ['.jpeg', '.jpg'],
        'image/png': ['.png'],
        }
    })
    const sample_uri = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRa_-ZfHzpnSe1itLoQTiHP8QpQbhOMBNSjr_9zEDoq16reWgqs72wq_kk&s"
  return (
    <div>
        <div {...getRootProps()} className='w-[200px] relative h-[200px] border border-gray-200 rounded-full p-1 mx-auto flex items-center justify-center'>
            <input {...getInputProps()} />
            {
                isDragActive ?
                <>
                <div className="flex items-center flex-col gap-y-2">
                    <FiUploadCloud className="text-4xl text-blue-600" />
                    <p>Upload Image ...</p>
                </div>
                </> :
                <>
                { loading ? <>
                    <CgSpinner className='text-4xl animate-spin' />
                </>
                : <img src={user.avatar?.image_uri ?? sample_uri} alt="avatar" className='w-full h-full rounded-full object-cover' />}
                </>                
            }
            <button className='p-1 text-xl rounded-full bg-blue-600 absolute -right-2 bottom-10 text-white'>
                <FaCamera />
            </button>
        </div>
    </div>
  )
}

export default AvatarComponent