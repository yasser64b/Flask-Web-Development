from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, SubmitField, TextAreaField, FieldList, FormField
from wtforms.validators import DataRequired


class BlogPostForm(FlaskForm):
    # no empty titles or text possible
    # we'll grab the date automatically from the Model later


    title = StringField('Title of project', default='Beam Analysis')
    text = TextAreaField('Comments', default='My project is ... ')
    
    name= "Beam"
    Node1=0
    Node2= FloatField('L:', default=10)

    unit= SelectField(u'Unit system', choices=[ ('US(kips,ft,F)', 'kips,ft,F'),('SI( N  ,m ,C)', 'N,m,C')])
    
    support1_dof= SelectField(u'Support 1', validators=[DataRequired()])
    # support1_dof= SelectField(u'Support', choices=[ ('110', 'Pinned'), ('010', 'Roller'), ('111', 'Fixed'),('001', 'Rotation Fixed'), ('000', 'Free')])
    support1_loc= 0
    
    support2_dof= SelectField(u'Support 2', validators=[DataRequired()])
    # support2_dof= SelectField(u'Support', choices=[ ('110', 'Pinned'), ('010', 'Roller'),('111', 'Fixed'), ('001', 'Rotation Fixed'), ('000', 'Free')])
    support2_loc= Node2

    I=FloatField('Moment of Inertia (I):', default=0.05)
    
    E=FloatField('Modulus of Elasticity (E):', default=519119.5)

    pointLoad=FloatField('Point Load:', default=100)
    pointLoadLoc=FloatField('Location:', default=5)
    momentLoad=FloatField('Moment Load:', default=0)
    momentLoadLoc=FloatField('Location:',default=0)
    distLoadBeg=FloatField('Load at a', default=10)
    distLoadBegLoc=FloatField('Location (a)', default=1)
    distLoadEnd=FloatField('Load at b', default=20)
    distLoadEndLoc=FloatField('Location (b)', default=4)

    submit = SubmitField('Analyze & Post')


