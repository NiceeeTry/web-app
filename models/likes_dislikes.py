from extensions import db


class Likes(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)
    like = db.Column(db.Boolean, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    
    
    @classmethod
    def get_likes_count(cls,post_id):
        likes_count = cls.query.filter_by(post_id=post_id, like=True).count()
        return likes_count
    
    @classmethod
    def like_post(cls, user_id, post_id):
        like = cls.query.filter_by(user_id=user_id, post_id=post_id).first()
        if like is None:
            like = cls(user_id=user_id, post_id=post_id, like=True)
            like.save()
        elif like.like is False:
            like.like = True
            like.save()
        else:
            Likes.remove_like(user_id=user_id, post_id=post_id)
            
            
    @classmethod
    def is_liked(cls, user_id, post_id):
        liked = cls.query.filter_by(user_id=user_id, post_id=post_id).first()
        if liked is None:
            return False
        return liked.like
            
            
    @classmethod
    def remove_like(cls, user_id, post_id):
        liked = cls.query.filter_by(user_id=user_id, post_id=post_id).first()
        liked.like = False
        liked.save()
      
        
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
        
        
class Dislikes(db.Model):
    __tablename__ = 'dislikes'

    id = db.Column(db.Integer, primary_key=True)
    dislike = db.Column(db.Boolean, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    
    
    @classmethod
    def get_dislikes_count(cls,post_id):
        dislikes_count = cls.query.filter_by(post_id=post_id, dislike=True).count()
        return dislikes_count
    
    @classmethod
    def dislike_post(cls, user_id, post_id):
        dislike = cls.query.filter_by(user_id=user_id, post_id=post_id).first()

        if dislike is None:
            dislike = cls(user_id=user_id, post_id=post_id, dislike=True)
            dislike.save()
        elif dislike.dislike is False:
            dislike.dislike = True
            dislike.save()
        else:
            Dislikes.remove_dislike(user_id=user_id, post_id=post_id)
            
            
    @classmethod
    def is_disliked(cls, user_id, post_id):
        disliked = cls.query.filter_by(user_id=user_id, post_id=post_id).first()
        if disliked is None:
            return False
        return disliked.dislike
            
            
    @classmethod
    def remove_dislike(cls, user_id, post_id):
        disliked = cls.query.filter_by(user_id=user_id, post_id=post_id).first()
        disliked.dislike = False
        disliked.save()
      
        
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()