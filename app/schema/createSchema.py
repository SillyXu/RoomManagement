from . import db
from marshmallow_sqlalchemy import ModelSchema
from webargs.flaskparser import use_args, use_kwargs
from .models import Role, User, Personnel, SpareParts, Room, Checkins

# 角色模型的 schema
class RoleSchema(ModelSchema):
    class Meta:
        model = Role
        sqla_session = db.session

# 用户模型的 schema
class UserSchema(ModelSchema):
    class Meta:
        model = User
        sqla_session = db.session

# 人员模型的 schema
class PersonnelSchema(ModelSchema):
    class Meta:
        model = Personnel
        sqla_session = db.session

# 备品信息模型的 schema
class SparePartsSchema(ModelSchema):
    class Meta:
        model = SpareParts
        sqla_session = db.session

# 房间模型的 schema
class RoomSchema(ModelSchema):
    class Meta:
        model = Room
        sqla_session = db.session

# 入住信息模型的 schema
class CheckinsSchema(ModelSchema):
    class Meta:
        model = Checkins
        sqla_session = db.session