from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Email,Length,EqualTo
from flask_wtf.file import FileField, FileRequired, FileAllowed

class ContactForm(FlaskForm):
    email=StringField("Your Email:", validators=[Email(),DataRequired()])
    message=TextAreaField("Message:", validators=[DataRequired(),Length(min=10)])
    submit=SubmitField("Send Message")