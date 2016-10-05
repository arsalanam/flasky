from datetime import datetime
from flask import request, render_template, session, redirect, url_for

from . import main
from .forms import NameForm , EntryForm , EditEntryForm

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

            return render_template('create_entry.html', form=form)

    else:
        form = EntryForm()
        return render_template('create_entry.html', form=form)





@main.route('/edit/<int:id>', methods=['GET', 'POST'] )
def edit(id):
    if request.method == 'POST':
        form = EditEntryForm(request.form)
        if form.validate():
            entry = db.session.query(Entry).get(id)
            if entry:
                entry.title = form.title.data
                entry.body = form.body.data
                entry.status = form.status.data
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




