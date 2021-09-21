from flask import render_template,url_for,flash, redirect,request,Blueprint
from myproject import db
from myproject.models import Support1, Support2
from myproject.beam_codes.forms import CodeForm_sup1, CodeForm_sup2

beam_codes = Blueprint('beam_codes',__name__)

@beam_codes.route('/sup1',methods=['GET','POST'])
def create_codeSup1():
    form = CodeForm_sup1()
    if form.validate_on_submit():

        sup1 = form.sup1.data
        code1 = form.code1.data
        

        # Add new beam to database
        new_sup1 = Support1(sup1, code1)

        db.session.add(new_sup1)
        db.session.commit()
        
        flash("Analyze Done! code added.")
        # return redirect(url_for('core.index'))

    return render_template('create_codeSup1.html',form=form )

@beam_codes.route('/sup2',methods=['GET','POST'])
def create_codeSup2():
    form = CodeForm_sup2()
    if form.validate_on_submit():
      
        sup2 = form.sup2.data
        code2 = form.code2.data
        sup1_id=form.sup1_id.data


        # Add new beam to database
        new_sup2 = Support2(sup2, code2, sup1_id)

        db.session.add(new_sup2)

        db.session.commit()
        
        flash("Analyze Done! code added.")
        # return redirect(url_for('core.index'))

    return render_template('create_codeSup2.html',form=form )