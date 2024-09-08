import React from "react";
import { Form, Button } from "react-bootstrap";
import {useForm} from 'react-hook-form'



const CreatePostPage=()=>{

    const{register, handleSubmit, reset, formState:{errors}}=useForm()

    const createPost = (data)=>{
        console.log(data)

        const token=localStorage.getItem('REACT_TOKEN_AUTH_KEY');
        const requestOptions={
            method:'POST',
            headers:{
                'content-type':'application/json',
                'Authorization':`Bearer ${JSON.parse(token)}`
            },
            body:JSON.stringify(data)

        }
        fetch('/posts',requestOptions)
        .then(res=>res.json())
        .then(data=>{
            reset()
        })
        .catch(err=>console.log(err))
    }

    return (
        <div className="container">
            <h1>Create a Post</h1>
            <form>
                <Form.Group>
                    <Form.Label>Title</Form.Label>
                    <Form.Control type="text"
                        {...register('title',{required:true, maxLength:50})}
                    />
                </Form.Group>
                {errors.title && <p style={{color:'red'}}><small>Title is required</small></p>}
                {errors.title?.type==="maxLength"&&<p style={{color:'red'}}><small>Title should be less than 50 characters </small></p>}
                <Form.Group>
                    <Form.Label>Description</Form.Label>
                    <Form.Control as="textarea" rows={5}
                        {...register('body',{required:true, maxLength:500})}
                    />
                </Form.Group>
                {errors.body && <p style={{color:'red'}}><small>Description is required</small></p>}
                {errors.body?.type==="maxLength"&&<p style={{color:'red'}}><small>Description should be less than 500 characters </small></p>}
                <br></br>
                <Form.Group>
                    <Button variant="primary" onClick={handleSubmit(createPost)}>
                        Save
                    </Button>
                </Form.Group>
            </form>
        </div>
    )
}

export default CreatePostPage