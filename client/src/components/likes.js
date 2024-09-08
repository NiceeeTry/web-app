import React, {useEffect, useState} from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../auth";
import Post from "./Post";
import { Modal, Form, Button } from "react-bootstrap";
import {useForm} from 'react-hook-form'

const LoggedinHome=()=>{
    const [posts, setPosts] = useState([]);
    const [show,setShow]=useState(false)
    const {register,reset, handleSubmit, setValue,formState:{errors}}=useForm()
    const [postId,setPostId]=useState(0);

    const token=localStorage.getItem('REACT_TOKEN_AUTH_KEY');
    const requestOptions={
        headers:{
            'content-type':'application/json',
            'Authorization':`Bearer ${JSON.parse(token)}`
        },

    }



    useEffect(
        ()=>{
            fetch('/liked',requestOptions)
            .then(res=>res.json())
            .then(data=>{
                setPosts(data)
            })
            .catch(err=>console.log(err))
        },[]
    );

    const getAllPosts=()=>{
        fetch('/liked',requestOptions)
            .then(res=>res.json())
            .then(data=>{
                setPosts(data)
            }).catch(err=>console.log(err))
    }

    

        const closeModal=()=>{
            setShow(false)
        }
        const showModal=(id)=>{
            setShow(true)
            setPostId(id)

            posts.data?.map(
                (post)=>{
                    if(post.id==id){
                        setValue('title',post.title)
                        setValue('body',post.body)
                    }
                }
            )
        }


        // let token=localStorage.getItem('REACT_TOKEN_AUTH_KEY')
        const updatePost=(data)=>{
            console.log(data)
            
            const requestOptions={
                method:'PUT',
                headers:{
                    'content-type':'application/json',
                    'Authorization':`Bearer ${JSON.parse(token)}`
                },
                body:JSON.stringify(data)
            }

            fetch(`/posts/${postId}`,requestOptions)
            .then(res=>res.json())
            .then(data=>{console.log(data)
                const reload = window.location.reload()
                reload()
            })
            .catch(err=>console.log(err))
        }

    const deletePost=(id)=>{
        console.log(id)

        const requestOptions={
            method:'DELETE',
            headers:{
                'content-type':'application/json',
                'Authorization':`Bearer ${JSON.parse(token)}`
            }
        }
        fetch(`/posts/${id}`, requestOptions)
        .then(res=>res.status)
        .then(data=>{
            console.log(data)
            getAllPosts()
        })
        .catch(err=>console.log(err))
    }

    return (
        <div className="posts container">
            <Modal
                show={show}
                size="lg"
                onHide={closeModal}
            >
            <Modal.Header closeButton>
                <Modal.Title>
                    Update Post
                </Modal.Title>
            </Modal.Header>
            <Modal.Body>


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
                    <Button variant="primary" onClick={handleSubmit(updatePost)}>
                        Save
                    </Button>
                </Form.Group>
            </form>


            </Modal.Body>
            </Modal>
            <h1>List of Posts</h1>
            {
                posts.data?.map(
                    (post,index)=>(
                        <Post 
                        title={post.title} 
                        key={index}
                        body={post.body}
                        likes={post.likes}
                        dislikes={post.dislikes}
                        id = {post.id}
                        tokenToCall ={token}
                        onClick={()=>{showModal(post.id)}}

                        onDelete={()=>{deletePost(post.id)}}
                        />
                    )
                )
                  
            }
        </div>
    )
}


const LoggedOutHome=()=>{
    return(
        <div className="home container">
        <   h1 className="heading">Finally Here is Project</h1>
            <Link to="/signup" className="btn btn-primary">Get Started</Link>
        </div>
    )
}
const HomePage=()=>{
const [logged]=useAuth()

    return (
        <div>
        {logged?<LoggedinHome/>:<LoggedOutHome/>}
        </div>
    )
}

export default HomePage;