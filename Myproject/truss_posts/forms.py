from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, SubmitField, TextAreaField, FieldList, FormField
from wtforms.validators import DataRequired


class BlogPostForm(FlaskForm):
    # no empty titles or text possible
    # we'll grab the date automatically from the Model later


    title = StringField('Title of project', default='Truss Analysis')
    text = TextAreaField('Comments', default='This truss analysis project ')
    
    truss_type= SelectField(u'Truss Type', choices=[('Pratt Roof', 'Pratt Roof'), ('Howe Roof', 'Howe Roof'), ('Pratt Bridge', 'Pratt Bridge'),
                                                     ('Howe Bridge', 'Howe Bridge'), ('Warren Bridge', 'Warren Bridge')])
    
    unit= SelectField(u'Unit system', choices=[ ('US(kips,ft,F)', 'kips,ft,F'),('SI( N  ,m ,C)', 'N,m,C')])
   
    E=FloatField('Modulus of Elasticity (E):', default=519119.5)
    A=FloatField('Member Cross Section:', default=100)
   
   
    numSpans = SelectField(u'Number of Panels', choices=[(2, 2),(4,4), (6,6), (8,8), (10,10)], coerce=int, default=4)
    span_width = FloatField('Sapn Width:', default=10)
    truss_height = FloatField('Truss Height:', default=10)


    support1_dof= SelectField(u'Support:', choices=[ ('110', 'Pinned'), ('010', 'Roller')])

    support1_node=IntegerField('Node Number:', default=1)

    support2_dof=SelectField(u'Support', choices=[ ('010', 'Roller'), ('110', 'Pinned')])

    support2_node=IntegerField('Node Number:', default=5)
    
    
    pointLoad1x=FloatField(' X dir:', default=0)
    pointLoad1y=FloatField(' Y dir:', default=1)
    pointLoadNode1=IntegerField('Node', default= 3)
        
    pointLoad2x=FloatField('X dir:', default=0)
    pointLoad2y=FloatField('Y dir:', default=0)
    pointLoadNode2=IntegerField('Node', default= 3)

    pointLoad3x=FloatField('X dir:', default=0)
    pointLoad3y=FloatField('Y dir:', default=0)
    pointLoadNode3=IntegerField('Node', default= 4)


    submit = SubmitField('Analyze & Post')


