from datetime import datetime
from flask import request, render_template, session, redirect, url_for

from . import main
from .forms import NameForm , EntryForm

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
    entries = Entry.query.all()

    return render_template('blog.html',entries =entries)



@main.route('/add/', methods=['GET', 'POST'] )
def add():
    if request.method == 'POST':
        form = EntryForm(request.form)
        if form.validate():
            entry = form.save_entry(Entry())
            db.session.add(entry)
            db.session.commit()
            return redirect(url_for('main.blog'))
        else:
            form = EntryForm()
        return render_template('create_entry.html', form=form)

    else:
        form = EntryForm()
        return render_template('create_entry.html', form=form)



