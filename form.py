from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, RadioField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional
from db import Services
import email_validator

class ContactForm(FlaskForm):
    head = SelectField("Service", choices=[], validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone Number", validators=[Optional(), Length(max=20)])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Send")