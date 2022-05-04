from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL


##WTFORM

class SearchForm(FlaskForm):
    id = StringField('Task ID No.',validators=[DataRequired()])
    submit = SubmitField('Submit Search')

class AddForm(FlaskForm):
    title = StringField('Task Title', validators=[DataRequired()])
    date = StringField('Date: MMDDYYYY',validators=[DataRequired()])
    weight = StringField('Priority(0-5)', validators=[DataRequired()])
    completion= StringField('Completion %')
    body = StringField('Comments')
    submit = SubmitField('Add Task')

class EditForm(FlaskForm):
    completion = StringField('Current Completion %')
    body = StringField('Comments')
    submit = SubmitField('Submit')