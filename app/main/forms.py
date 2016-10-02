from flask_wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import Required, Length, Email, Regexp , DataRequired
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Entry


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


class EntryForm(Form):
    title = StringField('Title' , validators=[DataRequired()])
    body = TextAreaField('Body')
    status = SelectField(
        'Entry status',
        choices=(
            (Entry.STATUS_PUBLIC, 'Public'),
            (Entry.STATUS_DRAFT, 'Draft')),
        coerce=int)

    def save_entry(self, entry):
        self.populate_obj(entry)

        return entry
