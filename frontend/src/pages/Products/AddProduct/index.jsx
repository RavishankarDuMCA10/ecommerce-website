import { Categories } from '@/constant/products.constant'
import { Formik, Form, Field, ErrorMessage } from 'formik'
import React, {useCallback, useState} from 'react'
import {useDropzone} from 'react-dropzone'
import { toast } from 'react-toastify'
import * as Yup from 'yup'
import { IoIosImages } from "react-icons/io";
import { IoCloudUploadOutline } from "react-icons/io5";
import { MdClose } from 'react-icons/md'
import AuthButton from '@/components/ui/AuthButton'
import { axiosClient } from '@/utils/axiosClient'



const AddProduct = () => {
    const [loading, setLoading] = useState(false)
    const validationSchema = Yup.object().shape({
        title: Yup.string().required("Title is required"),
        description: Yup.string().required("Product description is required"),
        price: Yup.number().required("Price is required").positive("Price must be positive"),
        category: Yup.string().required("Category is required").oneOf(Object.keys(Categories), "Choose Valid Category"),
        // stock: Yup.number().required("Stock is required").integer("Stock must be an integer").min(0, "Stock cannot be negative"),
        images: Yup.array(Yup.mixed()).required("Images are required")
    })

    const initialValues = {
        title: "",
        description: "",
        price: "",
        category: "",
        // stock: "",
        images:[]
    }

    const onSubmitHandler = async(values, helpers) => {
        try {
            setLoading(true)
            console.log(values)
            const formData = new FormData()
            formData.append("title", values.title)
            formData.append("description", values.description)
            formData.append("price", values.price)
            formData.append("category", values.category)
            values.images.forEach(img => formData.append('images', img));

            const response = await axiosClient.post("/product/add-product", formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                    'Authorization': 'Bearer ' + localStorage.getItem("token")
                }
            })
            const data = await response.data
            console.log(data)
            toast.success(data?.msg || "Product added successfully")
            helpers.resetForm()
        } catch (error) {
            toast.error(error?.response?.data?.detail || error.message)
        } finally {
            setLoading(false)
        }
    }
  return (
    <>
        <div className="py-10 rounded px-4 bg-gray-50 border border-gray-200">
            <h3 className="text-3xl font-semibold">Add Product</h3>
            <Formik
                initialValues={initialValues}
                validationSchema={validationSchema}
                onSubmit={onSubmitHandler}
            >
                {({values, setFieldValue}) => {
                return <Form>                    
                    <>
                        <div className="mb-3">
                            <label>Title
                                <Field type="text" 
                                className="w-full py-2 px-3 rounded bg-white border border-gray-200 outline-none"
                                placeholder='Enter Product Title' name='title' />
                                <ErrorMessage name='title' component="p" className='text-red-500 text-sm mt-1' />
                            </label>
                        </div>                        
                        <div className="mb-3">
                            <label>Category
                                <Field as="select" 
                                className="w-full py-2 px-3 rounded bg-white border border-gray-200 outline-none"
                                name='category'>
                                <option value="">Select</option>
                                {
                                    Object.keys(Categories).map((cur,i) => {
                                        return <option key={i} value={cur}>{cur}</option>
                                    })
                                }
                                </Field>
                                <ErrorMessage name='category' component="p" className='text-red-500 text-sm mt-1' />
                            </label>
                        </div>
                        <div className="mb-3">
                            <label>Description
                                <Field as="textarea" rows={5} 
                                className="w-full py-2 px-3 rounded bg-white border border-gray-200 outline-none"
                                placeholder='Enter Product Description' name='description' />
                                <ErrorMessage name='description' component="p" className='text-red-500 text-sm mt-1' />
                            </label>
                        </div>
                        <div className="mb-3">
                            <div>Product Images
                                <ProductImageComponent images={values.images} setImages={(images) => setFieldValue('images', images)} />
                                <ErrorMessage name='images' component="p" className='text-red-500 text-sm mt-1' />
                            </div>
                        </div>
                        <div className="mb-3">
                            <label>Price (in &#8377;)
                                <Field type="text" 
                                onInput={(e) => {
                                    e.target.value = e.target.value.replace(/[^0-9.]/g, '')
                                }}
                                className="w-full py-2 px-3 rounded bg-white border border-gray-200 outline-none"
                                placeholder='Enter Product Price' name='price' />
                                <ErrorMessage name='price' component="p" className='text-red-500 text-sm mt-1' />
                            </label>
                        </div>
                        <div className="mb-3">
                            <AuthButton text={'Add Product'} loading={loading} />
                        </div>
                    </>                    
                </Form>
                }}
            </Formik>
        </div>
    </>
  )
}

export default AddProduct

const ProductImageComponent = ({images, setImages}) => {
    // const [images, setImages] = useState([])
    const onDrop = useCallback(acceptedFiles => {
        if (acceptedFiles.length > 5) {
            toast.error("You can only upload up to 5 images")
            return
        }
        // Do something with the files
        setImages(acceptedFiles)
        console.log(acceptedFiles)
    }, [])
    const {getRootProps, getInputProps, isDragActive} = useDropzone({
        onDrop,
        multiple: true,
        maxFiles:5,
        accept: {
            'image/jpeg': ['.jpeg', '.jpg'],
            'image/png': ['.png']
        }
    })

    const deleteImage = (idx) => {
        let all_images = images.filter((_, i) => i != idx)
        setImages(all_images)
    }

    return <>
        {images && images.length > 0 ? <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 mx-auto gap-x-3 gap-y-2">
                {
                    images.map((cur,i) => {
                        return <div key={i} className="w-full relative h-[200px] p-2 rounded-sm">
                            <img src={URL.createObjectURL(cur)} alt={i+1} className='w-full h-full object-cover' />
                            <button onClick={() => deleteImage(i)} className='p-2 absolute right-0 top-0 text-xl bg-blue-500 cursor-pointer text-white rounded-full'>
                                <MdClose />
                            </button>
                        </div>
                    })
                }
            </div>
        </> : <div {...getRootProps()} className='border w-full min-h-44 flex justify-center items-center border-dashed border-blue-500 bg-white'>
        <input {...getInputProps()} />
        {
            isDragActive ?
            <div className="flex items-center justify-center flex-col">
                <IoCloudUploadOutline className="text-6xl text-blue-500" />
                <p className="text-center">Uploading ...</p>
            </div> :
            <div className='flex items-center justify-center flex-col'>
                <IoIosImages className="text-6xl text-blue-500" />
                <p className="text-center">Upload Images</p>
            </div>
        }
        </div>}
    </>
}