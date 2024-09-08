
from flask_restful import Resource
from models.groups import Groups


class GroupsList(Resource):
    def get(self):
        groups = Groups.get_all_groups()
        data =[group.group_name for group in groups]
        return {'groups':data}