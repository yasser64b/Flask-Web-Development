from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, SubmitField, TextAreaField, FieldList, FormField
from wtforms.validators import DataRequired


class CodeForm_sup1(FlaskForm):
    sup1 = StringField('sup1', default='Fixed')
    code1 = StringField('code1', default='111')
    submit = SubmitField('Add sup1')

class CodeForm_sup2(FlaskForm):
    sup2 = StringField('sup2', default='Fixed')
    code2 = StringField('code2', default='111')
    sup1_id = IntegerField('sup1_id', default=1)
    submit = SubmitField('Add sup2')

