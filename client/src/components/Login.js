import React, { useState } from "react";
import {Form, Button} from 'react-bootstrap'
import { Link } from "react-router-dom";
import {useForm} from 'react-hook-form'
import { login } from "../auth";
import { useNavigate } from 'react-router-dom';
 
const LoginPage=()=>{

    const{register, handleSubmit, reset, formState:{errors}}=useForm()

    const history=useNavigate()

    const loginUser=(data)=>{
        console.log(data)


        const requestOptions={
            method:"POST",
            headers:{
                'content-type':'application/json'
            },
            body:JSON.stringify(data)
        }
        fetch('/token',requestOptions)
        .then(res=>res.json())
        .then(data=>{
            console.log(data.access_token)
            login(data.access_token)

            history('/');
        })
        reset()
    }
    return (
        <div className="container">
        <div className="form">
            <h1>Login Page</h1>
            <form>
                {/* <Form.Group>
                    <Form.Label>
                        Username
                    </Form.Label>
                    <Form.Control type="text" placeholder="Your username"
                   {...register('username',{required:true, maxLength:80})}
                    />
                </Form.Group>
                {errors.username && <p style={{color:'red'}}><small>Username is required</small></p>}
                {errors.username?.type==="maxLength"&&<p style={{color:'red'}}><small>Username should have maximum 80 characters </small></p>}
                <br></br> */}
                <Form.Group>
                    <Form.Label>
                        Email
                    </Form.Label>
                    <Form.Control type="email" placeholder="Your email"
                     {...register('email',{required:true, maxLength:80})}
                    />
                </Form.Group>
                {errors.email && <p style={{color:'red'}}><small>Email is required</small></p>}
                <br></br>
                <Form.Group>
                    <Form.Label>
                        Password
                    </Form.Label>
                    <Form.Control type="password" placeholder="Your password"
                    {...register('password',{required:true, minLength:8})}
                    />
                </Form.Group>
                {errors.password && <p style={{color:'red'}}><small>Password is required</small></p>}
                {errors.password?.type==="maxLength"&&<p style={{color:'red'}}><small>Password should have minimum 8 characters </small></p>}
                <br></br>
                <Form.Group>
                    <Button as="sub" variant="primary" onClick={handleSubmit(loginUser)}>
                        Login
                    </Button>
                </Form.Group>
                <br></br>
                <Form.Group>
                    <small>Do not have an account?<Link to="/signup">Create One</Link></small>
                </Form.Group>
            </form>
        </div>
    </div>
    )
}

export default LoginPage