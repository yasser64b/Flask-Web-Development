from flask import render_template,url_for,flash, redirect,request,Blueprint
from flask_login import current_user,login_required
from myproject import db
from myproject.models import BlogPost, Truss
from myproject.truss_posts.forms import BlogPostForm

truss_posts = Blueprint('truss_posts',__name__)

@truss_posts.route('/truss_create',methods=['GET','POST'])
@login_required
def create_post():
    form = BlogPostForm()
    if form.validate_on_submit():

        blog_post = BlogPost(title=form.title.data,
                             text=form.text.data,
                             user_id=current_user.id,
                             )
                        
        bp = BlogPost.query.all()
        if len(bp)>0:
            blog_post_id=int(bp[-1].id +1)
        else: 
            blog_post_id=1

        print(blog_post_id)
        truss_type=form.truss_type.data 
        unit= form.unit.data
        E=form.E.data
        A=form.A.data

    
        numSpans = form.numSpans.data
        span_width = form.span_width.data
        truss_height = form.truss_height.data


        support1_dof= form.support1_dof.data
        support1_node=form.support1_node.data

        support2_dof=form.support2_dof.data
        support2_node=form.support2_node.data
        
        
        pointLoad1x=form.pointLoad1x.data
        pointLoad1y=form.pointLoad1y.data
        pointLoadNode1=form.pointLoadNode1.data
            
        pointLoad2x=form.pointLoad2x.data
        pointLoad2y=form.pointLoad2y.data
        pointLoadNode2=form.pointLoadNode2.data

        pointLoad3x=form.pointLoad3x.data
        pointLoad3y=form.pointLoad3y.data
        pointLoadNode3=form.pointLoadNode3.data
        

        # Add new Truss to database
        new_truss = Truss( truss_type, unit, E, A, numSpans,span_width ,truss_height ,
                            support1_dof, support1_node, support2_dof, support2_node,
                            pointLoad1x, pointLoad1y,pointLoadNode1, 
                            pointLoad2x, pointLoad2y,pointLoadNode2, 
                            pointLoad3x, pointLoad3y,pointLoadNode3, 
                            blog_post_id)

        db.session.add(blog_post)
        db.session.add(new_truss)
        db.session.commit()
        
        flash("Analyze Done! Blog Post Created.")
        return redirect(url_for('core.index'))

    return render_template('create_truss_post.html', form=form,)


# int: makes sure that the blog_post_id gets passed as in integer
# instead of a string so we can look it up later.
@truss_posts.route('/<int:blog_post_id> truss')
def blog_post(blog_post_id):
    # grab the requested blog post by id number or return 404
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    truss = Truss.query.all()
    
    for c in truss:
        if  c.blog_post_id == blog_post.id:
            truss_id = c.id
            break
    trusses= Truss.query.get_or_404(truss_id)

    return render_template('blog_truss_post.html',title=blog_post.title,
                            date=blog_post.date,post=blog_post , trusses=trusses 
    )

@truss_posts.route("/<int:blog_post_id>/truss_update", methods=['GET', 'POST'])
@login_required
def update(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    rus = Truss.query.all()
    for b in rus:
        if  b.blog_post_id == blog_post.id:
         truss_id = b.id
         break
    truss= Truss.query.get_or_404(truss_id)
    if blog_post.author != current_user:
        # Forbidden, No Access
        abort(403)

    form = BlogPostForm()
    if form.validate_on_submit():
        blog_post.title = form.title.data
        blog_post.text = form.text.data
        
        # beam.name = "Beam Updated"
        # beam.Node1 = 0
        # beam.Node2 = form.Node2.data
        # beam.unit = form.unit.data
        # beam.support1_dof = form.support1_dof.data
        # beam.support1_loc = 0
        # beam.support2_dof = form.support2_dof.data
        # beam.support2_loc = form.Node2.data
        # beam.I = form.I.data
        # beam.E = form.E.data
        # beam.pointLoad = form.pointLoad.data
        # beam.pointLoadLoc = form.pointLoadLoc.data
        # beam.momentLoad = form.momentLoad.data
        # beam.momentLoadLoc = form.momentLoadLoc.data
        # beam.distLoadBeg = form.distLoadBeg.data
        # beam.distLoadBegLoc = form.distLoadBegLoc.data
        # beam.distLoadEnd = form.distLoadEnd.data
        # beam.distLoadEndLoc = form.distLoadEndLoc.data
        
        db.session.commit()
        flash('Post Updated')
        return redirect(url_for('truss_posts.blog_post', blog_post_id=blog_post.id, truss_id=truss.id ))
    # Pass back the old blog post information so they can start again with
    # the old text and title.
    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text

        # form.name = "Beam Updated"
        # form.Node1 = 0
        # form.Node2 = beam.Node2
        # form.unit = beam.unit
        # form.support1_dof = beam.support1_dof
        # form.support1_loc = 0
        # form.support2_dof = beam.support2_dof
        # form.support2_loc = beam.Node2
        # form.I = beam.I
        # form.E = beam.E
        # form.pointLoad = beam.pointLoad
        # form.pointLoadLoc = beam.pointLoadLoc
        # form.momentLoad = beam.momentLoad
        # form.momentLoadLoc = beam.momentLoadLoc
        # form.distLoadBeg = beam.distLoadBeg
        # form.distLoadBegLoc = beam.distLoadBegLoc
        # form.distLoadEnd = beam.distLoadEnd
        # form.distLoadEndLoc = beam.distLoadEndLoc
        
    return render_template('create_truss_post.html', title='Update',
                           form=form)


@truss_posts.route("/<int:blog_post_id>/deleteTruss", methods=['POST'])
@login_required
def delete_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    truss = Truss.query.all()
    for b in truss:
        if  b.blog_post_id == blog_post.id:
            truss_id = b.id
            break
    truss= Truss.query.get_or_404(truss_id)

    if blog_post.author != current_user:
        abort(403)
    db.session.delete(blog_post)
    db.session.delete(truss)
    db.session.commit()
    flash('Post has been deleted')
    return redirect(url_for('core.index'))
