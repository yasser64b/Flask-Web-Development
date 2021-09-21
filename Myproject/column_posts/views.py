from flask import render_template,url_for,flash, redirect,request,Blueprint
from flask_login import current_user,login_required
from myproject import db
from myproject.models import BlogPost , Mycolumn, Support1, Support2
from myproject.column_posts.forms import BlogPostForm

column_posts = Blueprint('column_posts',__name__)

@column_posts.route('/col_create',methods=['GET','POST'])
@login_required
def create_post():
    form = BlogPostForm()
    form.support1_dof.choices=[(row.code1 , row.sup1) for row in Support1.query.all()[0:2]]
    form.support2_dof.choices=[(row.code2 , row.sup2) for row in Support2.query.filter_by(sup1_id=1).all()]

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

        name = 'column'
        Node1=0
        Node2= form.Node2.data
        
        I=form.I.data
        E=form.E.data
        unit=form.unit.data
        
        support1_dof=form.support1_dof.data
        support1_loc=0
        support2_dof=form.support2_dof.data
        support2_loc=form.Node2.data

        pointLoad=form.pointLoad.data
        pointLoadLoc=form.Node2.data
    



        # Add new column to database
        new_col = Mycolumn(name,unit, E, Node1, Node2, I, support1_dof, support1_loc, support2_dof, support2_loc,  pointLoad, pointLoadLoc, blog_post_id)

        db.session.add(blog_post)
        db.session.add(new_col)
        db.session.commit()
        
        flash("Analyze Done! Blog Post Created.")
        return redirect(url_for('core.index'))

    return render_template('create_col_post.html',form=form)


# int: makes sure that the blog_post_id gets passed as in integer
# instead of a string so we can look it up later.
@column_posts.route('/<int:blog_post_id> col')
def blog_post(blog_post_id):
    # grab the requested blog post by id number or return 404
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    col = Mycolumn.query.all()
    
    for c in col:
        if  c.blog_post_id == blog_post.id:
            col_id = c.id
            break
    columns= Mycolumn.query.get_or_404(col_id)

    return render_template('blog_col_post.html',title=blog_post.title,
                            date=blog_post.date,post=blog_post , columns=columns 
    )

@column_posts.route("/<int:blog_post_id>/col_update", methods=['GET', 'POST'])
@login_required
def update(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    
    col = Mycolumn.query.all()
    for c in col:
        if  c.blog_post_id == blog_post.id:
         col_id = c.id
         break
    column= Mycolumn.query.get_or_404(col_id)
   
    if blog_post.author != current_user:
        # Forbidden, No Access
        abort(403)

    form = BlogPostForm()
    if form.validate_on_submit():
        blog_post.title = form.title.data
        blog_post.text = form.text.data
        
        db.session.commit()
        flash('Post Updated')
        return redirect(url_for('column_posts.blog_post', blog_post_id=blog_post.id, column_id=column.id))
    # Pass back the old blog post information so they can start again with
    # the old text and title.
    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text
        
    return render_template('create_col_post.html', title='Update',
                           form=form)


@column_posts.route("/<int:blog_post_id>/deleteCol", methods=['POST'])
@login_required
def delete_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    col = Mycolumn.query.all()
    for b in col:
        if  b.blog_post_id == blog_post.id:
            col_id = b.id
            break
    columns= Mycolumn.query.get_or_404(col_id)

    if blog_post.author != current_user:
        abort(403)
    db.session.delete(blog_post)
    db.session.delete(columns)
    db.session.commit()
    flash('Post has been deleted')
    return redirect(url_for('core.index'))

@column_posts.route('/support2_dof/<sup1_code>')
# @login_required
def sup2(sup1_code):
    sup1_id=Support1.query.filter_by(code1=sup1_code).first().id
    support2_dofs = Support2.query.filter_by(sup1_id=sup1_id).all()
    sup2Array=[]
    for sup in support2_dofs:
        sup2obj={}
        sup2obj['id']=sup.id
        sup2obj['sup2']=sup.sup2
        sup2obj['code2']=sup.code2
        sup2Array.append(sup2obj)

    return jsonify({'support2_dofs' : sup2Array})