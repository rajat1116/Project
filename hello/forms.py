from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed
import pypyodbc


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class CandidateForm(FlaskForm):
    candidatename = StringField('Candidate Name',
                                validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email ID',
                        validators=[DataRequired(), Email()])
    contact = IntegerField('Contact No', validators=[DataRequired()])
    notice_period = StringField('Notice Period', validators=[DataRequired()])
    skills = StringField('Skills', validators=[DataRequired()])
    source = StringField('Source', validators=[DataRequired()])
    cv = FileField('Upload Resume', validators=[DataRequired(), FileAllowed(['png', 'jpg', 'pdf', 'docx'])])
    choices = [('1', 'Data Engineer'), ('2', 'UI/UX dev'), ('3', 'Java Dev')]
    jobId = SelectField('Select Job ID', choices=choices)
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    choices = [('Job Id', 'Job Id'), ('Skill', 'Skill'), ('Stages', 'Stages'), ('Notice Period', 'Notice Period')]
    s = SelectField('Search', choices=choices)
    e = StringField('Search')
    submit = SubmitField('Go')
