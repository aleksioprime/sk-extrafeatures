from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, SelectMultipleField, widgets, DateField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Optional, Email

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class LoginForm(FlaskForm):
    email = EmailField(label=('Email'), validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField(label=('Войти'))

class CreateUserForm(FlaskForm):
    email = EmailField(label=('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(label=('Пароль'),
                             validators=[DataRequired(),
                                         Length(min=8, message='Password should be at least %(min)d characters long')])
    confirm_password = PasswordField(
        label=('Повторите пароль'),
        validators=[DataRequired(message='*Required'),
                    EqualTo('password', message='Both password fields must be equal!')])
    first_name = StringField(label=('Имя'), validators=[DataRequired(), Length(max=64)])
    last_name = StringField(label=('Фамилия'), validators=[DataRequired(), Length(max=64)])
    submit = SubmitField(label=('Зарегистрировать'))