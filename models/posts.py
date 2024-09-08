from extensions import db
from datetime import datetime

from models.user import User
from models.groups import Groups, Group_members
from models.likes_dislikes import Likes

class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    body = db.Column(db.String(500))
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created = db.Column(db.DateTime, default=datetime.now)

    def __str__(self):
        return self.title
    
    def data(self):
        return {
            "id":self.id,
            "title":self.title,
            "body":self.body,
            "likes":self.likes,
            "dislikes":self.dislikes
        }
        
    @classmethod
    def get_posts_in_groups(cls, user_id):
        user = User.query.get(user_id)
                    
        posts = (
        Post.query
        .join(User, User.id == Post.user_id)
        .join(Group_members, User.id == Group_members.user_id)
        .join(Groups, Groups.id == Group_members.group_id)
        .filter(Groups.id.in_([group.id for group in user.group_list]))
        .order_by(Post.created.desc())
        .all()
    )

        return posts

    
    @classmethod
    def get_liked(cls, user_id):
        return cls.query.join(Likes, Likes.post_id == cls.id).filter_by(user_id=user_id).filter_by(like=True).all()
        
    
    @classmethod
    def get_by_id(cls, post_id):
        return cls.query.filter_by(id=post_id).first()
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        