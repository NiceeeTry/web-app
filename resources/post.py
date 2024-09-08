from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.posts import Post
from models.likes_dislikes import Likes, Dislikes

from flask_jwt_extended import get_jwt_identity, jwt_required


from models.user import User



class PostListResource(Resource):
    
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.get_by_id(user_id)
        if not user:
            return {'message':'Access is not allowed'}, HTTPStatus.FORBIDDEN
        posts=[]
        if user_id:        
            posts = Post.get_posts_in_groups(user_id)
        data =[]
        if len(posts)>0:
            for post in posts:
                post.likes = Likes.get_likes_count(post.id)
                post.dislikes = Dislikes.get_dislikes_count(post.id)
                post.save()
                data.append(post.data())
        return {'data':data, }, HTTPStatus.OK


    @jwt_required()
    def post(self):
        
        json_data = request.get_json()
        current_user = get_jwt_identity()
        user = User.get_by_id(current_user)
        if not user:
            return {'message':'Access is not allowed'}, HTTPStatus.FORBIDDEN
        post = Post(title = json_data['title'],
                    body = json_data['body'],
                    user_id = current_user)
        post.save()
        return post.data(), HTTPStatus.CREATED
    
    
class PostResource(Resource):
    
    @jwt_required()
    def get(self, post_id):
        post = Post.get_by_id(post_id=post_id)
        
        if post is None:
            return {'message':'Post not found'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()

        if post.user_id !=current_user:
            return {'message':'Access is not allowed'}, HTTPStatus.FORBIDDEN
        
        return post.data(), HTTPStatus.OK


    @jwt_required()
    def put(self, post_id):
        json_data = request.get_json()
        post = Post.get_by_id(post_id=post_id)
        
        if post is None:
            return {'message': 'Post not found'},HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()
        
        if current_user!= post.user_id:
            return {'message':'Access is not allowed'}, HTTPStatus.FORBIDDEN
        
        post.title = json_data['title']
        post.body = json_data['body']
        
        if 'likes' in json_data:
            post.likes=json_data['likes']
            
        if 'dislikes' in json_data:
            post.dislikes=json_data['dislikes']
        post.save()
        
        return post.data(), HTTPStatus.OK


    @jwt_required()
    def delete(self, post_id):
        
        post = Post.get_by_id(post_id=post_id)
        
        if post is None:
            return {'message':'Post not found'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()
        
        if current_user !=post.user_id:
            return {'message':'Access is not allowed'}, HTTPStatus.FORBIDDEN
        
        post.delete()
        
        return {"status":"deleted"},HTTPStatus.NO_CONTENT
        
