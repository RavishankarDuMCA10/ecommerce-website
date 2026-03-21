import React, {useEffect, useState} from 'react'
import * as yup from "yup"
import { Formik, Form, Field, ErrorMessage } from 'formik'
import { ROLE_TYPE } from '@/constant/auth.constant'
import { useAuthContext } from '@/context/AuthContext'
import AuthButton from '@/components/ui/AuthButton'
import { toast } from 'react-toastify'
import axios from 'axios'
import { axiosClient } from '@/utils/axiosClient'


const BasicDetails = () => {
    const {user, fetchUserProfile} = useAuthContext()
    const [loading, setLoading] = useState(false)
    const [initialValues, setInitialValues] = useState({
        name: user.name,
        email: user.email,
        role: user.role,
    })

    const validationSchema = yup.object().shape({
        name: yup.string().required("Name is Required"),
        email: yup.string(),
        role: yup.string()
    })

    const onSubmitHandler = async(values, _) => {
        try {
            setLoading(true)
            const response = await axiosClient.put("/auth/update-basic-details", values, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem("token")}`,
                }
            })
            const data = await response.data
            toast.success(data.message)
            console.log(values)
            await fetchUserProfile()
        } catch (error) {
            toast.error(error.response?.data?.detail || error.message)
        }finally {
            setLoading(false)
        }
    }
    useEffect(() => {
        setInitialValues({
            name: user.name,
            email: user.email,
            role: user.role,
        })
    }, [user])
  return (
    <>
    <h2 className='text-xl font-bold'>Basic Details : </h2>
    <Formik initialValues={initialValues} validationSchema={validationSchema} onSubmit={onSubmitHandler}>
        <Form>
            <div className='mb-3'>
                <label htmlFor='name'>Name <span className='text-red-500'>*</span></label>
                <Field type="text" placeholder='Enter your name' id='name' name='name' className='w-full py-2 px-3 rounded bg-gray-50 border border-gray-200 outline-none' />
                <ErrorMessage name="name" component={'p'} className="text-red-500 text-sm" />
            </div>
            <div className='mb-3'>
                <label htmlFor='email'>Email <span className='text-red-500'>*</span></label>
                <input value={initialValues.email} readOnly type="email" placeholder='Enter your email' id='email' name='email' className='w-full py-2 px-3 rounded bg-gray-50 border border-gray-200 outline-none' />
                <ErrorMessage name="email" component={'p'} className="text-red-500 text-sm" />
            </div>
            <div className='mb-3'>
                <label htmlFor='role'>Role <span className='text-red-500'>*</span></label>
                <select value={initialValues.role} readOnly type="text" placeholder='Enter your role' id='role' name='role' className='w-full py-2 px-3 rounded bg-gray-50 border border-gray-200 outline-none'>
                    {Object.values(ROLE_TYPE).map((role, index) => {
                        return <option key={index} defaultChecked={role == initialValues.role} value={role}>{role}</option>
                    })}
                </select>
                <ErrorMessage name="role" component={'p'} className="text-red-500 text-sm" />
            </div>
            <div className="mb-3">
                <AuthButton className={''} text={'Update'} />
            </div>
        </Form>
    </Formik>
    </>
  )
}

export default BasicDetails