import React from 'react'
import { Link, NavLink } from 'react-router'
import logo from '../assets/logo.png'

const NavBar = () => {
  return (
    <div className='navbar'>
      <img src={logo} alt="Company Logo" />
      <div className='navbar-link'>
        <Link to='/'>Home</Link>
        <Link to='/upload'>Upload</Link>
      </div>
    </div>
  )
}

export default NavBar
