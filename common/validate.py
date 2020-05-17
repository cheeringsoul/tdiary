from datetime import datetime
from marshmallow import fields, Schema, validates, ValidationError, pre_load, EXCLUDE


class SchemaSplit(Schema):
    class Meta:
        """排除unknown fields"""
        unknown = EXCLUDE

    """去掉所有字段首尾空格"""
    @pre_load
    def process_author(self, data, **kwargs):
        result = {}
        for key, value in data.items():
            result[key] = value.strip()
        return result


class DiarySchema(SchemaSplit):
    weather = fields.Str(required=True)
    date = fields.Str()
    diary_content = fields.Str(required=True, data_key='diary')

    @validates("weather")
    def validate_weather(self, value):
        if len(value) > 5:
            raise ValidationError("length of weather should less than 5 char.")

    @validates("diary_content")
    def validate_weather(self, value):
        if len(value) > 300:
            raise ValidationError("length of weather should less than 5 char.")

    @pre_load
    def convert_date(self, data):
        date = data['date']
        if date != 'N':
            data['date'] = datetime.strptime(date, '%Y-%m-%d')
        return data


def validate_password(value):
    digital = 0
    lower = 0
    upper = 0
    special_char = 0
    special_char_set = """
    '!@#$%^&*()-_=+[{]};:",<.>/?
    """
    if len(value) > 16 or len(value) < 6:
        raise ValidationError('密码长度必须在6到16之前')
    for s in value:
        if s.isdigit():
            digital = 1
        elif s.islower():
            lower = 1
        elif s.isupper():
            upper = 1
        elif s in special_char_set:
            special_char = 1
    if sum([digital, lower, upper, special_char]) < 2:
        raise ValidationError('密码必须包含数字、大写字母、小写字母、特殊字符至少两种')


class RegisterSchema(SchemaSplit):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    password_repeated = fields.Str(required=True)

    @validates('username')
    def validate_username(self, value):
        if len(value) > 8:
            raise ValidationError('length of username should less than 9 char.')

    @validates('password')
    def validate_password(self, value):
        validate_password(value)


class UpdatePasswordSchema(SchemaSplit):
    old_password = fields.Str(required=True)
    new_password = fields.Str(required=True)
    repeated_password = fields.Str(required=True)

    @validates('old_password')
    def validate_password(self, value):
        validate_password(value)

    @validates('new_password')
    def validate_password(self, value):
        validate_password(value)

    @validates('repeated_password')
    def validate_password(self, value):
        validate_password(value)

    @pre_load
    def check_password(self, data, **kwargs):
        if data['new_password'] != data['repeated_password']:
            raise ValidationError('两次密码不一致!')
        return data
