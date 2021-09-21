from myproject import db,login_manager
from structure import *
from analyze import *
from visualize import *
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
# By inheriting the UserMixin we get access to a lot of built-in attributes
# which we will be able to call in our views!
# is_authenticated()
# is_active()
# is_anonymous()
# get_id()


# The user_loader decorator allows flask-login to load the current user
# and grab their id.

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    profile_image = db.Column(db.String(20), nullable=False, default='default_profile.png')
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    # This connects BlogPosts to a User Author.
    posts = db.relationship('BlogPost', backref='author', lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        # https://stackoverflow.com/questions/23432478/flask-generate-password-hash-not-constant-output
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"UserName: {self.username}"

class BlogPost(db.Model):
    # Setup the relationship to the User table
    users = db.relationship(User)

    # Model for the Blog Posts on Website
    id = db.Column(db.Integer, primary_key=True)
    # Notice how we connect the BlogPost to a particular author
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(140), nullable=False)
    text = db.Column(db.Text, nullable=False)

    # beams = db.relationship('Beam', backref='blogpost')

    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id =user_id
        


    def __repr__(self):
        return f"Post Id: {self.id} --- Date: {self.date} --- Title: {self.title}"

################################### Data Base for beam Supports ####################################################

class Support1(db.Model):
    __tablename__='supports1'
    id = db.Column(db.Integer, primary_key= True)
    sup1= db.Column(db.Text)
    code1 = db.Column(db.Text)
    def __init__ (self,sup1, code1):
        self.sup1=sup1
        self.code1=code1


class Support2(db.Model):
    __tablename__='supports2'
    id = db.Column(db.Integer, primary_key= True)
    sup2= db.Column(db.Text)
    code2 = db.Column(db.Text)
    sup1_id=db.Column(db.Integer)
    def __init__ (self,sup2, code2, sup1_id):
        self.sup2=sup2        
        self.code2=code2
        self.sup1_id=sup1_id



###########################################################  BEAM SECTION ################################################# 

class Beam(db.Model):
    __tablename__ = 'beams'


    id = db.Column(db.Integer, primary_key= True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    blog_post_id = db.Column(db.Integer)
    
    name = db.Column(db.Text)
    Node1 = db.Column(db.Float)
    Node2 = db.Column(db.Float)


    support1_dof=db.Column(db.Text)
    support1_loc=db.Column(db.Float)
    support2_dof=db.Column(db.Text)
    support2_loc=db.Column(db.Float)
    
    I = db.Column(db.Float)
    E = db.Column(db.Float)
    unit=db.Column(db.Text)
    
    pointLoad=db.Column(db.Float)
    pointLoadLoc=db.Column(db.Float)
    
    momentLoad=db.Column(db.Float)
    momentLoadLoc=db.Column(db.Float)
    
    distLoadBeg=db.Column(db.Float)
    distLoadBegLoc=db.Column(db.Float)
    distLoadEnd=db.Column(db.Float)
    distLoadEndLoc=db.Column(db.Float)
    
    max_disp=db.Column(db.Float)
    min_disp=db.Column(db.Float)
    disp0L=db.Column(db.Float)
    disp05L=db.Column(db.Float)
    dispL=db.Column(db.Float)
    disp_max_x=db.Column(db.Float)
    disp_min_x=db.Column(db.Float)



    max_moment=db.Column(db.Float)
    min_moment=db.Column(db.Float)
    moment0L=db.Column(db.Float)
    moment05L=db.Column(db.Float)
    momentL=db.Column(db.Float)
    
    max_shear=db.Column(db.Float)
    min_shear=db.Column(db.Float)
    shear0L=db.Column(db.Float)
    shear05L=db.Column(db.Float)
    shearL=db.Column(db.Float)
    
    R1=db.Column(db.Float)
    R2=db.Column(db.Float)

    beam_img = db.Column(db.Text)
    result_img = db.Column(db.Text)

    # a beam can have many loads
    # load=db.relationship('Load', backref='beam', lazy='dynamic')

    def __init__ (self, name, unit, E, Node1, Node2, I,support1_dof, support1_loc, support2_dof, support2_loc , pointLoad, pointLoadLoc,momentLoad,momentLoadLoc, distLoadBeg, distLoadBegLoc,distLoadEnd, distLoadEndLoc, blog_post_id):
        
        self.blog_post_id=blog_post_id
        self.name=name
        self.Node1=Node1
        self.Node2=Node2
        self.I=I
        self.E=E
        self.unit=unit
        self.support1_dof=support1_dof
        self.support1_loc= support1_loc
        self.support2_dof= support2_dof
        self.support2_loc=support2_loc

        self.pointLoad=pointLoad
        self.pointLoadLoc=pointLoadLoc
        self.momentLoad=momentLoad
        self.momentLoadLoc=momentLoadLoc
        self.distLoadBeg=distLoadBeg
        self.distLoadBegLoc=distLoadBegLoc
        self.distLoadEnd=distLoadEnd
        self.distLoadEndLoc= distLoadEndLoc

        
        beam1=beam( Node1, Node2,I)
        beam1.set_support(support_dof=support1_dof,name='1', Loc=support1_loc)
        beam1.set_support(support_dof=support2_dof,name='2', Loc=support2_loc)
        beam1.set_E(E)
        beam1.set_unit(unit)
        if pointLoad !=0:  
            beam1.set_pointLoad('Point load', pointLoadLoc, pointLoad )
        if momentLoad !=0:
            beam1.set_momentLoad('Moment load', momentLoadLoc, momentLoad)
        if (distLoadBeg , distLoadEnd) !=(0,0):
            beam1.set_distributedLoad('Distributed Load', distLoadBegLoc, distLoadEndLoc,distLoadBeg,distLoadEnd)

        analyzeData=beam1.get_analyze()
        x05L=len(analyzeData[-1])//2

        self.max_disp=round(max(analyzeData[4]),5)
        self.min_disp=round(min(analyzeData[4]),5)
        self.disp0L=round(analyzeData[4][0],5)
        self.disp05L=round(analyzeData[4][x05L],5)
        self.dispL=round(analyzeData[4][-1],5)

        self.disp_max_x= analyzeData[-1][np.argmax(analyzeData[4])]
        self.disp_min_x= analyzeData[-1][np.argmin(analyzeData[4])]

        
        self.max_moment=round(max(analyzeData[3]),2)
        self.min_moment=round(min(analyzeData[3]),2)
        self.moment0L=round(analyzeData[3][0],2)
        self.moment05L=round(analyzeData[3][x05L],2)
        self.momentL=round(analyzeData[3][-1],2)
        
        self.max_shear=round(max(analyzeData[2]),2)
        self.min_shear=round(min(analyzeData[2]),2)
        self.shear0L=round(analyzeData[2][0],2)
        self.shear05L=round(analyzeData[2][x05L],2)
        self.shearL=round(analyzeData[2][-1],2)

        self.R1=round(analyzeData[0],2)
        self.R2=round(analyzeData[1],2)


        self.beam_img=beam1.drawBeam()
        self.result_img=beam1.plot_results()

    def __repr__(self):
        # return f"Date: {self.date}"
        return f"Date: {self.date} --- blog_post_id: {self.blog_post_id}"

########################################################  COLUMN SECTION #############################################################
class Mycolumn(db.Model):
    __tablename__ = 'mycolumns'

    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    id = db.Column(db.Integer, primary_key= True)
    # post_id = db.Column(db.Integer, db.ForeignKey('blog_post.id'), nullable=False)
    blog_post_id = db.Column(db.Integer)
    
    
    name = db.Column(db.Text)
    unit=db.Column(db.Text)
    E = db.Column(db.Float)

    Node1 = db.Column(db.Float)
    Node2 = db.Column(db.Float)
    I = db.Column(db.Float)


    support1_dof=db.Column(db.Text)
    support1_loc=db.Column(db.Float)
    support2_dof=db.Column(db.Text)
    support2_loc=db.Column(db.Float)
    
    
    pointLoad=db.Column(db.Float)
    pointLoadLoc=db.Column(db.Float)
        
    
    K_factor=db.Column(db.Float)

    buckling_load1=db.Column(db.Float)
    buckling_load2=db.Column(db.Float)
    buckling_load3=db.Column(db.Float)
    
    result_img = db.Column(db.Text)

    # a beam can have many loads
    # load=db.relationship('Load', backref='beam', lazy='dynamic')

    def __init__ (self, name, unit, E, Node1, Node2, I,support1_dof, support1_loc, support2_dof, support2_loc , pointLoad, pointLoadLoc,blog_post_id):
        
        self.blog_post_id=blog_post_id
        self.name=name
        self.Node1=Node1
        self.Node2=Node2
        self.I=I
        self.E=E
        self.unit=unit
        self.support1_dof= support1_dof
        self.support1_loc= support1_loc
        self.support2_dof= support2_dof
        self.support2_loc= support2_loc

        self.pointLoad=pointLoad
        # self.pointLoad=100
        self.pointLoadLoc=pointLoadLoc
        # self.pointLoadLoc=10
       

        # print('Column here')
        col1=column(Node1,Node2,I)
        col1.set_E(E)
        col1.set_unit(unit)
        col1.set_support(support_dof=support1_dof,name='1', Loc=support1_loc)
        col1.set_support(support_dof=support2_dof,name='2', Loc=support2_loc)
        
        if pointLoad !=0:  
            col1.set_pointLoad('Point load', pointLoadLoc, pointLoad )

        output=col1.plot_results()
        self.K_factor=output[1]
        self.buckling_load1=round(output[2],2)
        self.buckling_load2=round(output[3],2)
        self.buckling_load3=round(output[4],2)
        self.result_img=output[0]
    
    def __repr__(self):
        return f"Date: {self.date}"


#####################################################   TRUSS  SECTION   ##################################################
class Truss(db.Model):
    __tablename__ = 'trusses'

    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    id = db.Column(db.Integer, primary_key= True)
    blog_post_id=db.Column(db.Integer)
    # post_id = db.Column(db.Integer, db.ForeignKey('blog_post.id'), nullable=True)
    truss_type = db.Column(db.Text)
    unit=db.Column(db.Text)
    E = db.Column(db.Float)
    A = db.Column(db.Float)

    numSpans = db.Column(db.Float)
    span_width = db.Column(db.Float)
    truss_height = db.Column(db.Float)


    support1_dof=db.Column(db.Text)
    support1_node=db.Column(db.Integer)
    support2_dof=db.Column(db.Text)
    support2_node=db.Column(db.Integer)
    
    
    pointLoad1x=db.Column(db.Float)
    pointLoad1y=db.Column(db.Float)
    pointLoadNode1=db.Column(db.Integer)
        
    pointLoad2x=db.Column(db.Float)
    pointLoad2y=db.Column(db.Float)
    pointLoadNode2=db.Column(db.Integer)

    pointLoad3x=db.Column(db.Float)
    pointLoad3y=db.Column(db.Float)
    pointLoadNode3=db.Column(db.Integer)

    ###############
    # GSM=db.Column(db.Text)
    # dispmat=db.Column(db.Text)
    # forceresult=db.Column(db.Text)
    # elstraindb.Column(db.Text)
    # elstress=db.Column(db.Text)
    # eforce=db.Column(db.Text)
    result_img = db.Column(db.Text)

    maxDispy=db.Column(db.Float)
    maxDispNodey=db.Column(db.Float)
    minDispy=db.Column(db.Float)
    minDispNodey=db.Column(db.Float)

    maxDispx=db.Column(db.Float)
    maxDispNodex=db.Column(db.Float)
    minDispx=db.Column(db.Float)
    minDispNodex=db.Column(db.Float)

    R1x=db.Column(db.Float)
    R1y=db.Column(db.Float)
    R2x=db.Column(db.Float)
    R2y=db.Column(db.Float)

    maxForce=db.Column(db.Float)
    maxForceElem=db.Column(db.Float)
    minForce=db.Column(db.Float)
    minForceElem=db.Column(db.Float)

    def __init__ (self, truss_type, unit, E, A, numSpans,span_width ,truss_height ,
                support1_dof, support1_node, support2_dof, support2_node,
                pointLoad1x, pointLoad1y,pointLoadNode1, 
                pointLoad2x, pointLoad2y,pointLoadNode2, 
                pointLoad3x, pointLoad3y,pointLoadNode3,
                blog_post_id 
                ):
        
        
        self.blog_post_id=blog_post_id
        self.truss_type=truss_type
        self.unit=unit
        self.E=E
        self.A=A
        self.numSpans=numSpans
        self.span_width=span_width
        self.truss_height=truss_height


        self.support1_dof= support1_dof
        self.support1_node= support1_node

        self.support2_dof= support2_dof
        self.support2_node= support2_node

        self.pointLoad1x=pointLoad1x
        self.pointLoad1y=pointLoad1y
        self.pointLoadNode1=pointLoadNode1
        
        self.pointLoad2x=pointLoad2x
        self.pointLoad2y=pointLoad2y
        self.pointLoadNode2=pointLoadNode2

        self.pointLoad3x=pointLoad3x
        self.pointLoad3y=pointLoad3y
        self.pointLoadNode3=pointLoadNode3
     
        truss1=truss(truss_type, numSpans,span_width, truss_height, A, unit)
        truss1.set_E(E)
        truss1.set_support(support1_dof, support1_node)
        truss1.set_support(support2_dof, support2_node)
        
        
        truss1.set_pointLoad(pointLoadNode1, pointLoad1x, pointLoad1y)
        truss1.set_pointLoad(pointLoadNode2, pointLoad2x, pointLoad2y)
        truss1.set_pointLoad(pointLoadNode3, pointLoad3x, pointLoad3y)

        output=truss1.plot_results()
        
        self.result_img=output[0]

        self.GSM=output[1]
        
        #  Displacement on nodes
        self.dispmat=output[2].flatten()
        self.dispmatx=output[2].flatten()[::2]
        self.dispmaty=output[2].flatten()[1::2]

        self.maxDispy=-1*np.around(max(self.dispmaty),4)
        self.maxDispNodey=np.argmax(self.dispmaty)+1
        self.minDispy=-1*np.around(min(self.dispmaty),4)
        self.minDispNodey=np.argmin(self.dispmaty)+1

        self.maxDispx=np.around(max(self.dispmatx),4)
        self.maxDispNodex=np.argmax(self.dispmatx)+1
        self.minDispx=np.around(min(self.dispmatx),4)
        self.minDispNodex=np.argmin(self.dispmatx)+1
       
        #  forces on nodes
        self.forceresult=output[3].flatten()
        self.forceresultx=output[3].flatten()[::2]
        self.forceresulty=output[3].flatten()[1::2]
        self.R1x=np.around(self.forceresultx[self.support1_node-1],1)
        self.R1y=np.around(-1*self.forceresulty[self.support1_node-1],1)

        self.R2x=np.around(self.forceresultx[self.support2_node-1],1)
        self.R2y=np.around(-1*self.forceresulty[self.support2_node-1],1)
        
        # Element forces after displacement        
        self.eforce=output[6].flatten()
        self.maxForce=-1*np.around(max(self.eforce),2)
        self.maxForceElem=np.argmax(self.eforce)+1
        self.minForce=-1*np.around(min(self.eforce),2)
        self.minForceElem=np.argmin(self.eforce)+1



    def __repr__(self):
        return f"Date: {self.date}"

