from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.posts import Post
from models.likes_dislikes import Likes, Dislikes
from models.user import User

from flask_jwt_extended import get_jwt_identity, jwt_required


from models.groups import Groups

class UpdateLikes(Resource):
    @jwt_required()
    def put(self, post_id):
        
        json_data = request.get_json()
        current_user = get_jwt_identity()
        user = User.get_by_id(current_user)
        
        if not user:
            return {'message':'Access is not allowed'}, HTTPStatus.FORBIDDEN
        
        if 'like' in json_data:
            
            if not Likes.is_liked(user_id=current_user, post_id=post_id):
                Likes.like_post(user_id=current_user, post_id=post_id)
            else:
                Likes.remove_like(user_id=current_user, post_id=post_id)
            
            if Dislikes.is_disliked(user_id=current_user, post_id=post_id):
                Dislikes.remove_dislike(user_id=current_user, post_id=post_id)
                
        elif 'dislike' in json_data:
            
            if not Dislikes.is_disliked(user_id=current_user, post_id=post_id):
                Dislikes.dislike_post(user_id=current_user, post_id=post_id)
            else:
                Dislikes.remove_dislike(user_id=current_user, post_id=post_id)
            
            if Likes.is_liked(user_id=current_user, post_id=post_id):
                Likes.remove_like(user_id=current_user, post_id=post_id)
            
        post = Post.get_by_id(post_id=post_id)
        post.likes = Likes.get_likes_count(post.id)
        post.dislikes = Dislikes.get_dislikes_count(post_id)
        post.save()
        return post.data(), HTTPStatus.OK
    