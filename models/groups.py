from extensions import db

class Group_members(db.Model):
    __tablename__= 'group_members'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    group_id = db.Column(db.Integer(), db.ForeignKey('groups.id', ondelete='CASCADE'))


class Groups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(255))
    members = db.relationship('User', secondary="group_members", lazy = True, back_populates='group_list')
    
    def __str__(self):
        return self.group_name
    
    @classmethod
    def get_all_groups(cls):
        groups = cls.query.all()
        return groups
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    
