import LoaderComponent from '@/components/ui/LoaderComponent'
import { UserSlicePath } from '@/redux/slice/user.slice'
import React, { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Outlet, useNavigate, Link } from 'react-router-dom'
import { Sidebar, Menu, MenuItem, SubMenu } from 'react-pro-sidebar';
import { setToggle, SidebarSlicePath } from '@/redux/slice/sidebar.slice'


const ProtectedLayout = () => {
    const user = useSelector(UserSlicePath)
    const [loading, setLoading] = useState(true)
    const navigate = useNavigate()

    const dispatch = useDispatch()
    const { isToggle, isCollapse } = useSelector(SidebarSlicePath)

    useEffect(() => {
        if (!user) {            
            navigate("/login")            
        } else {
            setLoading(false)
        }
    }, [user])

    if (loading) {
        return <div className='h-screen flex justify-center items-center'>
            <LoaderComponent />
        </div>
    }
  return (
    <>
        <div className="flex items-start">
            <Sidebar collapsed={isCollapse} toggled={isToggle} onBackdropClick={() => dispatch(setToggle())} breakPoint='md'>
                <Menu
                className='h-screen bg-white border-none'
                    menuItemStyles={{
                    button: {
                        // the active class will be added automatically by react router
                        // so we can use it to style the active menu item
                        [`&.active`]: {
                        backgroundColor: '#13395e',
                        color: '#b6c8d9',
                        },
                    },
                    }}
                >
                    <MenuItem component={<Link to="/dashboard" />}> Dashboard</MenuItem>
                    <MenuItem component={<Link to="/profile" />}> Profile</MenuItem>
                </Menu>
            </Sidebar>
            <main className="px-4 w-full">
                <Outlet />
            </main>            
        </div>        
    </>
  )
}

export default ProtectedLayout