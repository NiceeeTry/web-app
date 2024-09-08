import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useAuth, logout } from "../auth";




const LoggedOutLinks=()=>{
  return(
    <>
       <li className="nav-item">
        <Link className="nav-link active" to="/">Posts</Link>
        </li>
      <li className="nav-item">
          <Link className="nav-link active" to="/">Home</Link>
        </li>
        <li className="nav-item">
          <Link className="nav-link active" to="/signup">Sign Up</Link>
        </li>
        <li className="nav-item">
          <Link className="nav-link active" to="/login">Login</Link>
        </li>
    </>
  )
}

const NavBar =()=>{
const [user, setUser]=useState('')
const [logged]=useAuth();


    useEffect(
      ()=>{
        const token=localStorage.getItem('REACT_TOKEN_AUTH_KEY');
        const requestOptions={
            method:'GET',
            headers:{
                'content-type':'application/json',
                'Authorization':`Bearer ${JSON.parse(token)}`
            }
  
        }
        fetch('/users',requestOptions)
        .then(res=>res.json())
        .then(data=>{
            console.log(data)
            setUser(data)
        })
        .catch(err=>console.log(err))
      },[]
  );



  const LoggedInLinks=()=>{
    return(
        <>
        <li className="nav-item">
        <Link className="nav-link active" to="/">Posts</Link>
        </li>
        <li className="nav-item">
            <Link className="nav-link active" to="/">Home</Link>
          </li>
        <li className="nav-item">
            <Link className="nav-link active" to="/create_post">Create Post</Link>
          </li>
  
          <li className="nav-item">
            <Link className="nav-link active" to="/liked">My Favorites</Link>
          </li>
  
        <li className="nav-item">
            <a className="nav-link active" href="#" onClick={()=>{logout()}}>Log Out</a>
          </li>

          <li className="nav-item">
            <div className="nav-link active"><i>User:</i> <strong><abbr title="User">{user.username}</abbr></strong></div>
          </li>
        </>
        
        
    )
  }




    return (
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
  <div className="container-fluid">
    <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span className="navbar-toggler-icon"></span>
    </button>
    <div className="collapse navbar-collapse" id="navbarNav">
      <ul className="navbar-nav">
        {logged?<LoggedInLinks/>:<LoggedOutLinks/>}
      </ul>
    </div>
  </div>
</nav>
    )   
}

export default NavBar