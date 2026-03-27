import LoaderComponent from '@/components/ui/LoaderComponent'
import { axiosClient } from '@/utils/axiosClient'
import React, { useEffect, useState } from 'react'
import { toast } from 'react-toastify'
import moment from 'moment'
import { IoMdTrash } from 'react-icons/io'

const WishListPage = () => {

    const [loading, setLoading] = useState(false)
    const [products, setProducts] = useState([])
    const fetchAllProducts = async () => {
        try {
            setProducts([])
            console.log("fetchAllProducts call started")
            const response = await axiosClient.get("/wishlist/get", {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem("token")}`
                }
            })
            const data = await response.data
            console.log("fetchAllProducts response data:", data)
            setProducts(data)
            setLoading(false)
        } catch (error) {
            toast.error(error?.response?.data?.detail || error.message)
        } finally {
            setLoading(false)
        }
    }

    if(loading) {
        return <div className='flex items-center justify-center min-h-56'>
            <LoaderComponent />
        </div>
    }

    useEffect(() => {
        fetchAllProducts()
    }, [])
  return (
    <>
        <section className="text-gray-600 body-font">
            <div className="container px-5 py-24 mx-auto">
                <div className="flex flex-wrap -m-4">
                    {
                        products.length > 0 ? <>
                            {products.map((cur, i) => (
                                <Card fetchAllProducts={fetchAllProducts} key={i} product={cur} />
                            ))}

                        </> : <>
                            <h3 className="text-4xl w-full font-bold text-center">
                                No Products Found
                            </h3>
                        </>
                    }      
                </div>
            </div>
        </section>

    </>
  )
}

export default WishListPage

const Card = ({ product, fetchAllProducts }) => {
    
    const [loading, setLoading] = useState(false)
    const deleteHandler = async() => {
        try {
            setLoading(true)
            console.log("deleteHandler call started")
            const response = await axiosClient.delete(`/wishlist/delete/${product.id}`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem("token")}`
                }
            })
            console.log("deleteHandler response data:", response.data)
            const data = await response.data
            await fetchAllProducts()
            toast.success(data.msg)

        } catch (error) {
            toast.error(error?.response?.data?.detail || error.message)
        } finally {
            setLoading(false)
        }
    }
    return <>
        <div className="p-4 md:w-1/3">
            <div className="h-full border-2 border-gray-200 border-opacity-60 rounded-lg overflow-hidden">
            <img
                className="lg:h-48 md:h-36 w-full object-cover object-center"
                src={product.image || "https://dummyimage.com/720x400"}
                alt={product.name}
            />
            <div className="px-6 pt-5">
                <h2 className="tracking-widest text-xs title-font font-medium text-gray-400 mb-1">
                {product.category}
                </h2>
                <h1 className="title-font text-lg font-medium text-gray-900 mb-3">
                {product.title}
                </h1>
                <p className="leading-relaxed mb-3">
                {product.description}
                </p>
                <p className="leading-relaxed mb-3">
                    Price (in &#8377;) {product.price}
                </p>                
                <div className="mb-3 flex items-center justify-between">     
                    <p className="text-zinc-500text-sm">
                        {moment(product.created_at).format("LLL")}
                    </p>
                    <button disabled={loading} onClick={deleteHandler} className="text-2xl rounded-full bg-red-500 p-2 cursor-pointer text-white disabled:bg-black">
                        <IoMdTrash />
                    </button>
                </div>                       
            </div>
            </div>
        </div>
    </>
}