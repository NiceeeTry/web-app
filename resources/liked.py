from flask_restful import Resource
from http import HTTPStatus

from models.posts import Post
from models.likes_dislikes import Likes, Dislikes
from models.user import User

from flask_jwt_extended import get_jwt_identity, jwt_required



class Favorites(Resource):
    
    @jwt_required()
    def get(self):
        
        user_id = get_jwt_identity()
        user = User.get_by_id(user_id)
        
        if not user:
            return {'message':'Access is not allowed'}, HTTPStatus.FORBIDDEN
        posts=[]
        
        if user_id:        
            posts = Post.get_liked(user_id=user_id)
        data =[]
        
        if len(posts)>0:
            for post in posts:
                post.likes = Likes.get_likes_count(post.id)
                post.dislikes = Dislikes.get_dislikes_count(post.id)
                post.save()
                data.append(post.data())
                
        return {'data':data, }, HTTPStatus.OK