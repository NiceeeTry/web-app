import 'bootstrap/dist/css/bootstrap.min.css';
import React from 'react'
import ReactDOM from 'react-dom'
import NavBar from './components/Navbar';
import './styles/main.css'

import {
    BrowserRouter as Router,
    Routes,
    Route
} from 'react-router-dom'
import HomePage from './components/Home';
import SignUpPage from './components/SignUp';
import LoginPage from './components/Login';
import CreatePostPage from './components/CreatePost';
import Likes from './components/likes';

const App = () => {
    return (
        <Router>
        <div className=''>
            <NavBar/>
            <Routes>
                <Route path='/create_post' element={<CreatePostPage/>}></Route>
                <Route path='/login' element={<LoginPage/>}></Route>
                <Route path='/signup' element={<SignUpPage/>}></Route>
                <Route path='/' element={<HomePage/>}></Route>
                <Route path='/liked' element={<Likes/>}></Route>
            </Routes>
        </div>
        </Router>
    )
}

ReactDOM.render( <App/> , document.getElementById('root'));