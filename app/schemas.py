from flask_marshmallow import Marshmallow

ma = Marshmallow()

class UserSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'name', 'email',  'password', 'otp')
        
class ScamSchema(ma.Schema):
    class Meta:
        fields = ('scam_id', 'url', 'count')
        
class HistorySchema(ma.Schema):
    class Meta:
        fields = ('history_id', 'user_id', 'url','status','datetime')


user_schema = UserSchema()
scam_schema = ScamSchema()
history_schema = HistorySchema()
