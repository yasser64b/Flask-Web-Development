from flask import render_template,url_for,flash, redirect,request,Blueprint, jsonify
from flask_login import current_user,login_required
from myproject import db
from myproject.models import BlogPost , Beam, Support1, Support2
from myproject.beam_posts.forms import BlogPostForm

beam_posts = Blueprint('beam_posts',__name__)

@beam_posts.route('/create',methods=['GET','POST'])
@login_required
def create_post():
    form = BlogPostForm()
    
    form.support1_dof.choices=[(row.code1 , row.sup1) for row in Support1.query.all()]
    form.support2_dof.choices=[(row.code2 , row.sup2) for row in Support2.query.filter_by(sup1_id=1).all()[:-1]]

    if form.validate_on_submit():

        # flash('sup1: %s, sup2: %s' % (form.support1_dof.data, form.support2_dof.data))

        blog_post = BlogPost(title=form.title.data,
                             text=form.text.data,
                             user_id=current_user.id
                             )


        bp = BlogPost.query.all()
        if len(bp)>0:
            blog_post_id=int(bp[-1].id +1)
        else: 
            blog_post_id=1
            
        name = 'beam'
        Node1=0
        Node2= form.Node2.data
        
        I=form.I.data
        E=form.E.data
        unit=form.unit.data
        
        support1_dof=form.support1_dof.data
        support1_loc=0
        support2_dof=form.support2_dof.data
        support2_loc=Node2

        pointLoad=form.pointLoad.data
        pointLoadLoc=form.pointLoadLoc.data
        momentLoad=form.momentLoad.data
        momentLoadLoc=form.momentLoadLoc.data
        distLoadBeg=form.distLoadBeg.data
        distLoadBegLoc=form.distLoadBegLoc.data
        distLoadEnd=form.distLoadEnd.data
        distLoadEndLoc=form.distLoadEndLoc.data
        



        # Add new beam to database
        new_beam = Beam(name,unit, E, Node1, Node2, I, support1_dof, support1_loc, support2_dof, support2_loc,  pointLoad, pointLoadLoc,momentLoad,momentLoadLoc, distLoadBeg, distLoadBegLoc,distLoadEnd, distLoadEndLoc,blog_post_id)

        db.session.add(blog_post)
        db.session.add(new_beam)

        db.session.commit()
        
        flash("Analyze Done! Blog Post Created.")
        return redirect(url_for('core.index'))

    return render_template('create_post.html',form=form, )


# int: makes sure that the blog_post_id gets passed as in integer
# instead of a string so we can look it up later.
@beam_posts.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    # grab the requested blog post by id number or return 404
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    
    bm = Beam.query.all()
    for b in bm:
        if  b.blog_post_id == blog_post.id:
            beam_id = b.id
    beams= Beam.query.get(beam_id)

    return render_template('blog_post.html',title=blog_post.title,
                            date=blog_post.date,post=blog_post , beams=beams,  
    )

@beam_posts.route("/<int:blog_post_id>/update", methods=['GET', 'POST'])
@login_required
def update(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    bm = Beam.query.all()
    for b in bm:
        if  b.blog_post_id == blog_post.id:
         beam_id = b.id
         break
    beam= Beam.query.get_or_404(beam_id)
    
    if blog_post.author != current_user:
        # Forbidden, No Access
        abort(403)

    form = BlogPostForm()
    if form.validate_on_submit():
        blog_post.title = form.title.data
        blog_post.text = form.text.data
        
        db.session.add(blog_post)

        db.session.commit()
        flash('Post Updated')
        return redirect(url_for('beam_posts.blog_post', blog_post_id=blog_post.id, beam_id=beam.id))
    # Pass back the old blog post information so they can start again with
    # the old text and title.
    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text
        
    return render_template('create_post.html', title='Update',
                           form=form)


@beam_posts.route("/<int:blog_post_id>/delete", methods=['POST'])
@login_required
def delete_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    bm = Beam.query.all()
    for b in bm:
        if  b.blog_post_id == blog_post.id:
         beam_id = b.id
         break
    beams= Beam.query.get_or_404(beam_id)

    if blog_post.author != current_user:
        abort(403)
    db.session.delete(blog_post)
    db.session.delete(beams)
    db.session.commit()
    flash('Post has been deleted')
    return redirect(url_for('core.index'))


@beam_posts.route('/support2_dof/<sup1_code>')
# @login_required
def sup2(sup1_code):
    sup1_id=Support1.query.filter_by(code1=sup1_code).first().id
    if sup1_id==1:
        support2_dofs = Support2.query.filter_by(sup1_id=sup1_id).all()[:-1]
    else:
        support2_dofs = Support2.query.filter_by(sup1_id=sup1_id).all()
    sup2Array=[]
    for sup in support2_dofs:
        sup2obj={}
        sup2obj['id']=sup.id
        sup2obj['sup2']=sup.sup2
        sup2obj['code2']=sup.code2
        sup2Array.append(sup2obj)

    return jsonify({'support2_dofs' : sup2Array})