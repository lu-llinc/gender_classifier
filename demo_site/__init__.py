from flask import Flask, jsonify, render_template, request
import os
import sys
import re
from model import Model
from read_config import read_server_config
from flaskext.mysql import MySQL
classifier_path = '../gender_classifier'
sys.path.append(os.path.dirname(os.path.expanduser(classifier_path)))
from gender_classifier import classifier

# Location of all configuration files to use.
# Overwrite using additional command line arguments.
package_directory = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILES = [os.path.join(package_directory, './config.cfg')]

# Read the configuration
config_files = CONFIG_FILES
if __name__ == '__main__':
    if len(sys.argv) > 1:
        config_files = sys.argv[1:]
    print 'Reading from config files:', config_files
config = read_server_config(config_files)
app = Flask(__name__)

# MySQL
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = config['database']['user']
app.config['MYSQL_DATABASE_PASSWORD'] = config['database']['password']
app.config['MYSQL_DATABASE_DB'] = config['database']['default_db']
app.config['MYSQL_DATABASE_HOST'] = config['database']['host']
app.config['MYSQL_DATABASE_PORT'] = config['database']['port']
mysql.init_app(app)
repo = Model(mysql)

# Other
gender_classifier = classifier.Classifier(config['faceplusplus']['apikey'], config['faceplusplus']['apisecret']
                                          , config['twitter']['consumerkey'], config['twitter']['consumersecret']
                                          , config['twitter']['accesstoken'], config['twitter']['accesssecret'])

@app.route('/')
def hello_world():
    return render_template('home.html')


@app.route('/generateerror')
def generate_error():
    1 / 0
    return render_template('home.html')


# API

@app.route('/api/classify', methods=['POST'])
def classify():
    data = request.json
    term = data['term'].strip()
    term_lowered = data['term'].strip().lower()

    repo.execute('SELECT * FROM t_pre_prediction where LOWER(pre_term) = %s', (term_lowered,))
    result = repo.fetchone()
    if result is None:
        # does not exist, create a new one
        gender, term_type = get_gender(term)
        repo.execute('INSERT INTO t_pre_prediction(pre_term, pre_type, pre_prediction) VALUES (%s, %s, %s)', (term, term_type, gender))
        id = repo.insert_id()
        repo.commit()
        return jsonify(prediction=gender, type=term_type, term=term, id=id)
    else:
        # update the current one
        count = result['pre_count']+1
        repo.execute('UPDATE t_pre_prediction SET pre_count = %s, pre_last_accessed = NOW() WHERE pre_id = %s', (count, result['pre_id']))
        repo.commit()
        return jsonify(prediction=result['pre_prediction'], type=result['pre_type'], term=term, id=result['pre_id'])


def get_gender(term):
    if is_url(term):
        term_type = 'url'
        result = gender_classifier.predict_gender_from_image(term)
        gender = result['gender']
    elif is_twitter_user(term):
        term_type = 'twitter_username'
        try:
            result = gender_classifier.predict_gender_of_twitter_user(term)
            gender = result['gender']
        except Exception as exc:
            if exc.message == 'Account could not be retrieved':
                gender = 'Not a Twitter user'
    else:
        term_type = 'first_name'
        result = gender_classifier.predict_gender_by_name(term)
        gender = result['gender']

    return gender.lower(), term_type.lower()


def is_url(term):
    r_url = re.compile(r"^https?:")
    return r_url.match(term)


def is_twitter_user(term):
    if term[0] == '@':
        return True
    return False


@app.route('/api/correction', methods=['POST'])
def feedback():
    data = request.json
    correction = data['correction']
    id = data['id']
    repo.execute('INSERT INTO t_cor_correction(cor_pre_id, cor_correction) VALUES (%s, %s)', (id, correction))
    repo.commit()
    return jsonify(message="Thank you so much!")


#   Error handling


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(**config['server'])
