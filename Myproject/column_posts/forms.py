from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, SubmitField, TextAreaField, FieldList, FormField
from wtforms.validators import DataRequired


class BlogPostForm(FlaskForm):
    # no empty titles or text possible
    # we'll grab the date automatically from the Model later


    title = StringField('Title of project', default='Column Analysis')
    text = TextAreaField('Comments', default='This project is ... ')
    
    name= "Column"
    Node1=0
    Node2= FloatField('L:', default=10)

    unit= SelectField(u'Unit system', choices=[ ('US(kips,ft,F)', 'kips,ft,F'),('SI( N  ,m ,C)', 'N,m,C')])
    
    support1_dof= SelectField(u'Bottom Support', choices=[])
    support1_loc= 0

    support2_dof= SelectField(u'Top Support', choices=[])
    support2_loc= Node2

    I=FloatField('Moment of Inertia (I):', default=100)
    
    E=FloatField('Modulus of Elasticity (E):', default=519119.5)

    pointLoad=FloatField('Point Load:', default=100)
    pointLoadLoc=Node2


    submit = SubmitField('Analyze & Post')


