from templateapp import app
from flask import request, url_for, session, redirect, escape, flash, render_template
from settings import config
import models, forms
from flask_oauth import OAuth
from decorators import anon_required, login_required

oauth = OAuth()
twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key=config['TWITTER_KEY'], 
    consumer_secret=config['TWITTER_SECRET']
)


@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')

@app.route('/twitterlogin')
def twitterlogin():
    if not session.get('twitter_token'):
      return twitter.authorize(callback=url_for('oauth_authorized',
          next=request.args.get('next') or request.referrer or None))
    flash("You already logged in!")
    return render_template("page.html")

@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)
    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    # Save Profile
    user = models.User.get_user_or_none(resp['screen_name'])
    if user:
      correct_key = models.User.verify_user_or_none(resp['screen_name'], resp['oauth_token_secret'])
      if correct_key:
        # Load User 
        session['email'] = resp['screen_name'] 
        flash('Welcome back, %s' % resp['screen_name'])
        return redirect(next_url)
      else:
        flash('There was an error with your Twitter authentication. Try again later.')
        return redirect(url_for('login'))      
    else:
      newuser = models.User(resp['screen_name'], resp['oauth_token_secret']) 
      newuser.add_to_db()
      session['email'] = resp['screen_name'] 
      flash('You were signed in as %s' % resp['screen_name'])
      return redirect(url_for('index'))
      
    

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
@anon_required
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
      user = models.User.verify_user_or_none(request.form['email'], request.form['password'])
      if user:
        session['email'] = request.form['email']
        return redirect(url_for('index'))
      else:
        flash("No account exists with that email and password combination. You can create a new account by going to /register")
        return redirect(url_for('login'))
    return render_template('authenticate.html', form=form, form_name="Login") 


@app.route('/register', methods=['GET', 'POST'])
@anon_required
def register():
  print request.url
  form = forms.RegistrationForm()
  if form.validate_on_submit():
    user_email = request.form['email']
    user_pass1 = request.form['pass1']
    user_pass2 = request.form['pass2']
    if user_pass1 != user_pass2:
      return "Your passwords did not match. Please try again."  
    elif models.User.get_user_or_none(user_email): 
      form.email.errors.append('This email has already been registered.')
    else:
      newuser = models.User(user_email, user_pass1) 
      newuser.add_to_db()
      session['email'] = user_email
      return redirect(url_for('index'))
  return render_template('authenticate.html', form=form, form_name="Register") 
 
@app.route('/logout')
@login_required
def logout():
    session.pop('email', None)
    session.pop('twitter_token', None)
    return redirect(url_for('index'))
