import React, {useState} from 'react'
import {Button, Card, Modal} from 'react-bootstrap'
// import Likes from './likes'




const Post=({title,body, onClick, onDelete,likes, dislikes, id, tokenToCall})=>{

    const updatePost=(data)=>{
        console.log(data)
        
        const requestOptions={
            method:'PUT',
            headers:{
                'content-type':'application/json',
                'Authorization':`Bearer ${JSON.parse(tokenToCall)}`
            },
            body:JSON.stringify(data)
        }

        fetch(`/likes/${id}`,requestOptions)
        .then(res=>res.json())
        .then(data=>{console.log(data)
            // const reload = window.location.reload()
            // reload()
        })
        .catch(err=>console.log(err))
    }

    function Likes(){
        const [like,setLike] = useState(likes)
        const[dislike,setDislike] = useState(dislikes)
        const[likeActive, setLikeActive] = useState(false)
        const[dislikeActive, setDislikeActive] = useState(false)
    
        function likef(){
            if(likeActive){
                setLikeActive(false)
                setLike(like-1)
            }else{
                setLikeActive(true)
                setLike(like+1)
                if (dislikeActive){
                    setDislikeActive(false)
                    setLike(like+1)
                    setDislike(dislike-1)
                }
            }

            updatePost({
                        "like":like
                    })
        }
    
        function dislikef(){
            if(dislikeActive){
                setDislikeActive(false)
                setDislike(dislike-1)
            }else{
                setDislikeActive(true)
                setDislike(dislike+1)
                if(likeActive){
                    setLikeActive(false)
                    setDislike(dislike+1)
                    setLike(like-1)
                }
            }

            updatePost({
                "dislike":dislike
            })
        }
    
        return (
            <div className="App">
                <div></div>
                <button onClick={likef}>Like {like}</button>
                <button onClick={dislikef}>Disike {dislike}</button>
            </div>
        );
    }





    return(
        <Card className='post'>
            <Card.Body>
                <Card.Title>{title}</Card.Title>
                <p>{body}</p>
                <Button variant='primary' onClick={onClick}>Update</Button>
                {' '}
                <Button variant='danger' onClick={onDelete}>Delete</Button>
                <br></br>
                <Likes/>
            </Card.Body>
        </Card>
    )
}


export default Post;