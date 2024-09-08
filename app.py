from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS

from config import Config
from extensions import db, jwt


from resources.user import UserListResource
from resources.token import TokenResource, RevokeResource, black_list
from resources.post import PostListResource, PostResource
from resources.groupsList import GroupsList
from resources.updateLikes import UpdateLikes
from resources.liked import Favorites

# Admin part
from wtforms import StringField
from utils import hash_password

from models.posts import Post
from models.user import User
from models.groups import Groups

from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView

def create_app(config_str='config.DevelopmentConfig'):
    app = Flask(__name__,
                instance_relative_config=True,
                template_folder="templates",
                static_folder="static")
    app.config.from_object(config_str)

    register_extensions(app)
    register_resources(app)
    if config_str=='config.DevelopmentConfig':
        admin_page_creation(app)
        CORS(app)
    return app


def register_extensions(app):
    db.app = app
    db.init_app(app)
    app.app_context().push()
    migrate = Migrate(app, db)
    jwt.init_app(app)
    with app.app_context():
        db.create_all()
    @jwt.token_in_blocklist_loader
    def check_if_token_in_bl(jwt_header, decypted_token):
        jti = decypted_token['jti']
        return jti in black_list


def register_resources(app):
    api = Api(app)

    api.add_resource(UserListResource, '/users')

    api.add_resource(TokenResource, '/token')
    api.add_resource(RevokeResource, '/logout')

    api.add_resource(PostListResource, '/posts')
    api.add_resource(PostResource, '/posts/<int:post_id>')
    
    api.add_resource(GroupsList, '/groups')
    api.add_resource(UpdateLikes, '/likes/<int:post_id>')
    
    api.add_resource(Favorites, '/liked')
    


def admin_page_creation(app):
    from flask_wtf import FlaskForm
    from wtforms import SelectField, DateField
    from wtforms.validators import DataRequired

    class PostForm(FlaskForm):

        @staticmethod
        def get_user_choices():
            with app.app_context():
                users = User.get_all_users()
                return [(str(user.id), user.username) for user in users]
            
        
        title = StringField('Title', validators=[DataRequired()])
        body = StringField('Body', validators=[DataRequired()])
        user_id = SelectField('User', choices=get_user_choices, validators=[DataRequired()])
        created = DateField('Created', validators=[DataRequired()])
        
    
        
    
    class UserAdminView(ModelView):
        
        column_list = ['id', 'username', 'email', 'password', 'group_list','created']
        def on_model_change(self, form, model, is_created):
            model.password = hash_password(model.password)

    class PostAdminView(ModelView):
        column_list = ['id', 'title', 'body', 'user_id', 'created']
        form = PostForm 

    class GroupAdminView(ModelView):
        column_hide_backrefs = False
        column_list = ['id', 'group_name', 'members']
        
    class AdminBoardView(AdminIndexView):
            @expose('/')
            def add_stats(self):
                all_users = User.query.all()
                
                return self.render('admin/admin_view.html', all_users=all_users)

    admin = Admin(app, name='microblog', template_mode='bootstrap3', index_view=AdminBoardView())
    admin.add_view(PostAdminView(Post, db.session))
    admin.add_view(UserAdminView(User, db.session))
    admin.add_view(GroupAdminView(Groups, db.session))

if __name__ == '__main__':
    app = create_app()
    app.run()