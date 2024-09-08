from extensions import db
from models.groups import Groups, Group_members

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200))
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    posts = db.relationship("Post", backref="user", lazy=True)
    group_list = db.relationship('Groups', secondary="group_members", lazy=True, back_populates='members')

    def __str__(self):
        return self.username
    
    def data(self):
        return {
            "id":self.id,
            "username":self.username
        }
    
    def add_to_group(self, group):
        """Adds user to the group"""
        exist_group = Groups.query.filter_by(group_name = group).first()

        if exist_group:
            self.group_list.append(exist_group)
            self.save()
        else:
            raise Exception('There is no such group')
            
            
            
    def remove_from_group(self, group):
        """Removes user to the group"""
        exist_group = Groups.query.filter_by(group_name = group).first()
        
        if exist_group:
            self.group_list.remove(exist_group)
            self.save()
        else:
            raise Exception('There is no such group')


    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def get_all_users(cls):
        users = cls.query.all()
        return users

    def save(self):
        db.session.add(self)
        db.session.commit()
        

