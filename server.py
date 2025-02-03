from flask import Flask, request, redirect, url_for, render_template
import flask_login
import bcrypt

app = Flask(__name__)
app.secret_key = 'li4Quae5juwi0wuw'

# Loginmanager erzeugen
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# Zum Hashen von Passwörtern
# password = bcrypt.hashpw('12345'.encode('utf-8'), bcrypt.gensalt())
# print(password)

users = {
    'user@example.org': {'password': b'$2b$12$VrmJ5xpSirPckgp87bDt1eMPcHcCAKLFdMtU8jyO3bvevbA.sVwim'}
}   # pwd: 1234

print(users['user@example.org']['password'])

class User(flask_login.UserMixin):
    pass


# Loginmanager mitteilen, wie ein User geladen werden kann
@login_manager.user_loader
def user_loader(email):
    print("userloader")
    if email not in users:
        return

    user = User()
    user.id = email
    return user


# Loginseite, Passwort wird gehasht und mit dem gespeicherten verglichen
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''

    email = request.form['email']
    # encode password
    if email in users and bcrypt.checkpw(request.form['password'].encode('utf-8'), users[email]['password']):
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect(url_for('protected'))
    
    return 'Bad login'


@app.route('/protected')
@flask_login.login_required # nur eingeloggte User können diese Seite sehen
def protected():
    return 'Logged in as: ' + flask_login.current_user.id

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


app.run(debug=True)
