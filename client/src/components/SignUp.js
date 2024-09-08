import React, {useState, useEffect} from "react";
import { Form , Button, Alert} from "react-bootstrap";
import { Link } from "react-router-dom";
import {useForm} from 'react-hook-form'

const SignUpPage=()=>{
    const[groups,setGroups]=useState([]);

    const {register, watch, handleSubmit, reset, formState:{errors}}=useForm('');
    const [show, setShow]=useState(true)
    const [serverResponse, setServerResponse]=useState('')


    useEffect(
        ()=>{
            fetch('/groups')
            .then(res=>res.json())
            .then(data=>{
                console.log(data)
                setGroups(data.groups)
            })
            .catch(err=>console.log(err))
        },[]
    );

    const submitForm=(data)=>{
        if(data.password===data.confirmPassword){

            const body={
                username:data.username,
                email:data.email,
                password:data.password,
                group:data.group
            }

            const requestOptions={
                method:"POST",
                headers:{
                    'content-type':'application/json'
                },
                body:JSON.stringify(body)
            }
            fetch('/users',requestOptions)
            .then(res=>res.json())
            .then(data=>{
                console.log(data)
                setServerResponse(data.message)
                console.log(serverResponse)

                setShow(true)
            })
            .catch(err=>console.log(err))
            reset()
        }
    else{
        alert("Passwords do not match")
    }
    }

    // const GettingGroups=()=>{
    //     useEffect(
    //         ()=>{
    //             fetch('/groups')
    //             .then(res=>res.json())
    //             .then(data=>{
    //                 console.log(data)
    //                 setGroups(data)
    //             })
    //             .catch(err=>console.log(err))
    //         },[]
    //     );
    // }
    // llll------------

    return (
        <div className="container">
            <div className="form">
                    {show?
                    <>
                     <Alert variant="success" onClose={() => setShow(false)} dismissible>
                    <p>
                        {serverResponse}
                    </p>
                    </Alert>
                    <h1>Sign Up Page</h1>
                    </>
                    :
                    <h1>Sign Up Page</h1>
                }
                <form>
                    <Form.Group>
                        <Form.Label>
                            Username
                        </Form.Label>
                        <Form.Control type="text" placeholder="Your username"
                        {...register("username",{required:true, maxLength:80})}
                        />
                
                    {errors.username && <p style={{color:"red"}}><small>Username is required</small></p>}
                
                    {errors.username?.type==="maxLength"&&<p style={{color:"red"}}><small>Max charachters should be 80</small></p>}
                    </Form.Group>
                    
                    <br></br>
                    <Form.Group>
                        <Form.Label>
                            Email
                        </Form.Label>
                        <Form.Control type="email" placeholder="Your email"
                        {...register("email",{required:true, maxLength:80})}
                        />
                    {errors.email && <p style={{color:"red"}}><small>Email is required</small></p>}
        
                    {errors.email?.type==="maxLength"&&<p style={{color:"red"}}><small>Max charachters should be 80</small></p>}
                    </Form.Group>
                    <br></br>
                    <Form.Group>
                        <Form.Label>
                            Groups
                        </Form.Label>
                        <Form.Control as="select" multiple {...register("group",{required:true})}>
                        
                        {groups.map((group, index) => <option value={group} >{group}</option>)}
                        </Form.Control>
                        {errors.group && <p style={{color:"red"}}><small>Group is required</small></p>}
                    </Form.Group>
                    <br></br>
                    <Form.Group>
                        <Form.Label>
                            Password
                        </Form.Label>
                        <Form.Control type="password" placeholder="Your password"
                        {...register("password",{required:true, minLength:8})}
                        />
    
                    {errors.password && <p style={{color:"red"}}><small>Password is required</small></p>}

                    {errors.password?.type==="minLength"&&<p style={{color:"red"}}><small>Min charachters should be 8</small></p>}
                    </Form.Group>
                    <br></br>
                    <Form.Group>
                        <Form.Label>
                           Confirm Password
                        </Form.Label>
                        <Form.Control type="password" placeholder="Your password"
                        {...register("confirmPassword",{required:true, minLength:8})}
                        />
                    
                    {errors.confirmPassword && <p style={{color:"red"}}><small>confirmPassword is required</small></p>}
                
                    {errors.confirmPassword?.type==="minLength"&&<p style={{color:"red"}}><small>Min charachters should be 8</small></p>}
                    </Form.Group>
                    <br></br>
                    <Form.Group>
                        <Button as="sub" variant="primary" onClick={handleSubmit(submitForm)}>
                            SignUp
                        </Button>
                    </Form.Group>
                    <br></br>
                    <Form.Group>
                        <small>Already have an account?<Link to="/login">Log In</Link></small>
                    </Form.Group>
                </form>
            </div>
        </div>
    )
}

export default SignUpPage