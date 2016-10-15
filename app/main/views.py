from datetime import datetime
from flask import request, render_template, session, redirect, url_for , flash ,g

from . import main
from .forms import NameForm , EntryForm , EditEntryForm , LoginForm
from flask_login import login_user, logout_user ,current_user , login_required
from ..models import  Role, User , Entry ,db


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        return redirect(url_for('.index'))
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False),
                           current_time=datetime.utcnow())


@main.route('/blog/' , methods=['GET', 'POST'] )
def blog():
    if g.user.is_authenticated:
        entries= db.session.query(Entry).filter(Entry.author == g.user).order_by(Entry.created_timestamp.desc())
    else:
        entries = db.session.query(Entry).filter(Entry.status == Entry.STATUS_PUBLIC ).order_by(Entry.created_timestamp.desc())

    return render_template('blog.html',entries =entries)



@main.route('/add/', methods=['GET', 'POST'] )
@login_required
def add():
    if request.method == 'POST':
        form = EntryForm(request.form)
        if form.validate():
            entry = form.save_entry(Entry())
            entry.author = g.user
            db.session.add(entry)
            db.session.commit()
            return redirect(url_for('main.blog'))
        else:

            return render_template('create_entry.html', form=form)

    else:
        form = EntryForm()
        return render_template('create_entry.html', form=form)





@main.route('/edit/<int:id>', methods=['GET', 'POST'] )
@login_required
def edit(id):
    if request.method == 'POST':
        form = EditEntryForm(request.form)
        if form.validate():
            entry = db.session.query(Entry).get(id)
            if entry:
                entry.title = form.title.data
                entry.body = form.body.data
                entry.status = form.status.data
                entry.author = g.user
                db.session.commit()
            return redirect(url_for('main.blog'))
        else:
            return render_template('edit_entry.html', form=form)

    else:
        form = EditEntryForm()
        entry = db.session.query(Entry).get(id)
        form.id.data = entry.id
        form.title.data = entry.title
        form.body.data = entry.body
        form.status.data = entry.status
        return render_template('edit_entry.html', form=form)




@main.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form = LoginForm(request.form)
        if form.validate():
            login_user(form.user, remember=form.remember_me.data)
            flash("Successfully logged in as %s." % form.user.email, "success")
            return redirect(request.args.get("next") or url_for("main.index"))
        else:
            flash("User %s not found." % form.email.data, "failure")
            return render_template("login.html", form=form)
    else:
        form = LoginForm()
        return render_template("login.html", form=form)

@main.route("/logout/")
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(request.args.get('next') or url_for('main.index'))
