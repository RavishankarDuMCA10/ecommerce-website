import React from 'react'
import { Routes, Route } from 'react-router-dom'
import LoginUser from '@/pages/auth/LoginUser'
import Dashboard from '@/pages/Dashboard'
import CartPage from '@/pages/CartPage'
import AddProduct from '@/pages/Products/AddProduct'
import AllProducts from '@/pages/Products/AllProducts'
import MainLayout from '@/layout/MainLayout'
import HomePage from '@/pages/HomePage'
import RegisterUser from '@/pages/auth/RegisterUser'
import AuthLayout from '@/layout/AuthLayout'
import ProtectedLayout from '@/layout/ProtectedLayout'
import ProfileUser from '@/pages/auth/ProfileUser'
import { ROLE_TYPE } from './constant/auth.constant'
import RoleLayout from './layout/RoleLayout'
import OrderPage from './pages/Orders'
import ProductPage from './pages/ProductPage'
import WishListPage from './pages/WishListPage'

const App = () => {
  return (
    <>
    <Routes>
      <Route path='/' Component={MainLayout} > 
        <Route index Component={HomePage} />
        <Route path='/cart' Component={CartPage} />   
        <Route path='/product/:slug' Component={ProductPage} />

        <Route Component={ProtectedLayout}>                    
          <Route path='/dashboard' Component={Dashboard} />
          <Route path='/profile' Component={ProfileUser} />

          {/* Buyer routes */}
          <Route element={<RoleLayout role={ROLE_TYPE.BUYER} />}>
            <Route path='/orders' Component={OrderPage} />
            <Route path='/wishlist' Component={WishListPage} />
          </Route>

          {/* /** Seller routes */        }
          <Route element={<RoleLayout role={ROLE_TYPE.SELLER} />}>
            <Route path='/add-product' Component={AddProduct} />
            <Route path='/all-products' Component={AllProducts} />
          </Route>
        </Route>
      </Route>
      
      <Route Component={AuthLayout}>
        <Route path='/login' Component={LoginUser} />
        <Route path='/register' Component={RegisterUser} />
      </Route>
    </Routes>
    </>
  )
}

export default App