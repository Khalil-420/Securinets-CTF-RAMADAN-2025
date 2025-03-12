from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Replace with a strong, random key in production
csrf = CSRFProtect(app)

# Mock database (in-memory dictionary for demonstration)
users = {
    "Glitch": generate_password_hash("16-11-1999")

}

# Mock image data (list of 25 image URLs)
images = ["static/images/Alexander Shadow.png", "static/images/Benjamin Cipher.png", "static/images/Catherine Echo.png", "static/images/Dominic Rogue.png", "static/images/Eleanor Nova.png", "static/images/Frederick Ghost.png", "static/images/Gabriella Blaze.png", "static/images/Harrison Vortex.png", "static/images/Isabella Storm.png", "static/images/James Harper.png", "static/images/Laura Kline.png", "static/images/Katherine Hex.png", "static/images/Nathaniel Zero.png", "static/images/Olivia Specter.png", "static/images/David Moore.png", "static/images/Patrick Drake.png", "static/images/William Hayes.png", "static/images/Quentin Striker.png", "static/images/Rebecca Venom.png", "static/images/Sebastian Falcon.png", "static/images/Theodore Dagger.png", "static/images/Victoria Luna.png", "static/images/Rose Harrie.png", "static/images/William Havoc.png", "static / images / Zachary Inferno.png",
    ]


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if username in users and check_password_hash(users[username], password):
            session['user'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html', form=form)


@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))

    return render_template('dashboard.html', username=session['user'], images=images)


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
