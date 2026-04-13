from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, RadioField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional, ValidationError
from db import Services

class ContactForm(FlaskForm):
    head = SelectField("Service", choices=[], validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    company = StringField("Company / Organization", validators=[Optional(), Length(max=120)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone Number", validators=[Optional(), Length(max=20)])
    preferred_contact = RadioField(
        "Preferred Contact Method",
        choices=[("email", "Email"), ("phone", "Phone"), ("whatsapp", "WhatsApp")],
        validators=[Optional()],
    )
    request_priority = SelectField(
        "Request Priority",
        choices=[
            ("", "Select priority"),
            ("standard", "Standard"),
            ("urgent", "Urgent"),
            ("planning", "Planning ahead"),
        ],
        validators=[Optional()],
    )
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Send")

    def validate_head(self, field):
        if field.data == "select":
            raise ValidationError("Please choose the service area related to your inquiry.")
