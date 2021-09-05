# -*- coding:utf-8 -*-
import controller.Task as task
import controller.Label_info as label_info
import controller.Label as label
import controller.Editor as editor
import controller.Dataset as dataset
import controller.Project as project
import controller.User as user
from flask import Flask, request, g, render_template, session, redirect, url_for, Response, send_file, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
import hashlib
import time
import os
import json
import sys
sys.path.append('.model')
sys.path.append('.controller')

app = Flask(__name__, template_folder='../front-end',
            static_folder='../front-end', static_url_path='')

# for image file path
UPLOAD_FOLDER = 'image'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOW_EXTENSIONS = ['png', 'jpg', 'jpeg']

app.secret_key = 'easy'
login_manager = LoginManager()
login_manager.login_view = 'signin'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Please login.'
login_manager.init_app(app)

class User(UserMixin):
    pass

users = user.get_all_user()

# if the username is in the records
def query_user(username):
    for user in users:
        if user['username'] == username:
            return user

# get the current user
@login_manager.user_loader
def load_user(username):
    if query_user(username) is not None:
        curr_user = User()
        curr_user.id = username
        return curr_user

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'
    
# query the org_id by name
def query_orgid(userid):
    for user in users:
        if user['username'] == userid:
            return user["org_id"]

# adapt MD5 to encrypt the password
def toMd5(data):
    return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()


# The prefix of Api
apiPrefix = '/api/v1/'
# The prefix of image url
i_url = 'http://192.168.0.202:5000/api/v1/image/'

#################### Flask user login management #########################

# @app.route(apiPrefix)
# def index():
#     login_url=url_for('signin')
#     return redirect(login_url)

@app.route(apiPrefix + 'login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_data(as_text=True)
        user = json.loads(data)
        username = user["name"]
        password = toMd5(user["password"])
        user = query_user(username)
        # validate the password
        if user is not None and password == user['password']:
            curr_user = User()
            curr_user.id = username
            # use login_user in Flask-Login
            login_user(curr_user, remember=True)
            re = {
                'code': 0,
                'message': 'Login sucessfully',
            }
            return json.dumps(re)
    # GET
    re = {
        'code': -1,
        'message': 'Username or password is incorrect',
    }
    return json.dumps(re)


@app.route(apiPrefix + 'logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    re = {
        'code': 0,
        'message': 'Logged out successfully!',
    }
    return json.dumps(re)

#################### User Api #########################
@app.route(apiPrefix + 'sign_up', methods=['GET', 'POST'])
def sign_up():
    try:
        data = request.get_data(as_text=True)
        # duplicate name check
        u = json.loads(data)
        name = u["name"]
        if query_user(name) is not None:
            re = {
            'code': -1,
            'message': 'Duplicate User Name.',
            }
        else:
            newUser = user.signup(data)
            users.append(newUser)
            re = {
                'code': 0,
                'message': 'Signup sucessfully, please login.',
            }
        return json.dumps(re)
    except Exception as e:
        if str(e)=="UNIQUE constraint failed: t_user.name":
            re = {
            'code': -1,
            'message': 'Duplicate User Name.',
            }

        elif str(e)=="UNIQUE constraint failed: t_orgnization.name":
            re = {
            'code': -1,
            'message': 'Duplicate Orgnization Name.',
            }

        elif str(e)=="Cannot find org code":
            re = {
            'code': -1,
            'message': 'The org code is not exsit.',
            }
        else:
            re = {
                'code': -1,
                'message': 'Signup failed.',
            }
        return json.dumps(re)

# unused
@app.route(apiPrefix + 'log_in', methods=['GET', 'POST'])
def log_in():
    data = request.get_data(as_text=True)
    re = user.login(data)
    return re

@app.route(apiPrefix + 'get_user_list', methods=['GET', 'POST'])
def get_user_list():
    # get org_id based on the user name (current_user.id)
    org_id = query_orgid(current_user.id)
    data = request.get_data(as_text=True)
    re = user.get_user_list(None, org_id)
    return re

@app.route(apiPrefix + 'search_user', methods=['GET', 'POST'])
def search_user():
    # get org_id based on the user name (current_user.id)
    org_id = query_orgid(current_user.id)
    data = request.get_data(as_text=True)
    re = user.get_user_list(data, org_id)
    return re

@app.route(apiPrefix + 'delete_user', methods=['GET', 'POST'])
def delete_user():
    data = request.get_data(as_text=True)
    re = user.delete_user(data)
    deleteuser = json.loads(data)
    name = deleteuser["name"]
    for i in range(0,len(users)):
        u = users[i]
        if u["username"] == name:
            users.pop(i)

    return re

@app.route(apiPrefix + 'reset_password', methods=['GET', 'POST'])
def reset_password():
    data = request.get_data(as_text=True)
    re = user.change_password(data)   
    if re["code"] == 0:
        # change the password in cache
        for u in users:
            if u["username"] == re["name"]:
                u["password"] = re["password"]
                break
    
    return json.dumps(re)

@app.route(apiPrefix + 'get_current_user', methods=['GET', 'POST'])
@login_required
def get_current_user():
    re = user.get_cur_user(current_user.id)
    return re

#################### Project Api #########################

@app.route(apiPrefix + 'get_project_list', methods=['GET', 'POST'])
@login_required
def get_project_list():
    # get org_id based on the user name (current_user.id)
    org_id = query_orgid(current_user.id)
    data = request.get_data(as_text=True)
    re = project.get_project_list(None, org_id)
    return re


@app.route(apiPrefix + 'search_project', methods=['GET', 'POST'])
@login_required
def search_project():
    # get org_id based on the user name (current_user.id)
    org_id = query_orgid(current_user.id)
    data = request.get_data(as_text=True)
    re = project.get_project_list(data, org_id)
    return re


@app.route(apiPrefix + 'add_project', methods=['GET', 'POST'])
def add_project():
    # get org_id based on the user name (current_user.id)
    org_id = query_orgid(current_user.id)
    data = request.get_data(as_text=True)
    re = project.add_project(data, org_id, current_user.id)
    return re


@app.route(apiPrefix + 'delete_project', methods=['GET', 'POST'])
def delete_project():
    data = request.get_data(as_text=True)
    re = project.delete_project(data)
    return re


@app.route(apiPrefix + 'get_project_setting', methods=['GET', 'POST'])
def get_project_setting():
    org_id = query_orgid(current_user.id)
    data = request.get_data(as_text=True)
    re = project.get_setting(data, org_id, current_user.id)
    return re

@app.route(apiPrefix + 'get_project_details', methods=['GET', 'POST'])
def get_project_details():
    data = request.get_data(as_text=True)
    re = project.get_details(data, current_user.id)
    return re

@app.route(apiPrefix + 'get_project_details_search', methods=['GET', 'POST'])
def get_project_details_search():
    data = request.get_data(as_text=True)
    re = project.get_details_search(data, current_user.id)
    return re

@app.route(apiPrefix + 'attach_dataset', methods=['GET', 'POST'])
def attach_dataset():
    data = request.get_data(as_text=True)
    re = project.attach_or_dettach_dataset(data, current_user.id)
    return re

@app.route(apiPrefix + 'change_role_permission', methods=['GET', 'POST'])
def change_role_permission():
    data = request.get_data(as_text=True)
    re = project.change_user_authority(data, current_user.id)
    return re

#################### Dataset Api #########################

@app.route(apiPrefix + 'get_dataset_list', methods=['GET', 'POST'])
@login_required
def get_dataset_list():
    # get org_id based on the user name (current_user.id)
    org_id = query_orgid(current_user.id)
    data = request.get_data(as_text=True)
    re = dataset.get_dataset_list(None, org_id)
    return re


@app.route(apiPrefix + 'search_dataset', methods=['GET', 'POST'])
@login_required
def search_dataset():
    # get org_id based on the user name (current_user.id)
    org_id = query_orgid(current_user.id)
    data = request.get_data(as_text=True)
    re = dataset.get_dataset_list(data, org_id)
    return re


@app.route(apiPrefix + 'add_dataset', methods=['GET', 'POST'])
def add_dataset():
    # get org_id based on the user name (current_user.id)
    org_id = query_orgid(current_user.id)
    data = request.get_data(as_text=True)
    re = dataset.add_dataset(data, org_id, current_user.id)
    return re


@app.route(apiPrefix + 'delete_dataset', methods=['GET', 'POST'])
def delete_dataset():
    data = request.get_data(as_text=True)
    re = dataset.delete_dataset(data)
    return re

@app.route(apiPrefix + 'delete_image_in_dataset', methods=['GET', 'POST'])
def delete_image_in_dataset():
    data = request.get_data(as_text=True)
    re = dataset.delete_image(data)
    return re


@app.route(apiPrefix + 'active_dataset', methods=['GET', 'POST'])
def active_dataset():
    data = request.get_data(as_text=True)
    re = dataset.active_dataset(data)
    return re


@app.route(apiPrefix + 'upload_images', methods=['GET', 'POST'])
def upload_images():
    dataset_id = request.form['id']
    upload_file = request.files["file"]
    # upload the images into server
    if upload_file and allowed_file(upload_file.filename):
        alias = str(time.time()) + secure_filename(upload_file.filename)
        upload_file.save(os.path.join(
            app.root_path, app.config['UPLOAD_FOLDER'], alias))

        # insert the url into databse
        re = dataset.insert_image(i_url + alias, upload_file.filename, alias, dataset_id, current_user.id)
        json_image = json.dumps(re)
        return json_image
    else:
        re = {
            'ok': 'false',
            'message': 'failed',
            'data': ''
        }
        return json.dumps(re)


@app.route(apiPrefix + 'get_images_in_dataset', methods=['GET', 'POST'])
def get_images_in_dataset():
    # get org_id based on the user name (current_user.id)
    data = request.get_data(as_text=True)
    re = dataset.get_image_list(data)
    return re

#################### Editor Api #########################

@app.route(apiPrefix + 'add_editor', methods=['GET', 'POST'])
def add_editor():
    try:
        org_id = query_orgid(current_user.id)
        data = request.get_data(as_text=True)
        re = editor.create_editor(data, org_id, current_user.id)
        return re
    except Exception as e:
        print(e)


@app.route(apiPrefix + 'get_editor_list', methods=['GET', 'POST'])
def get_editor_list():
    org_id = query_orgid(current_user.id)
    re = editor.editor_list(org_id)
    return re

# insert objects and classifications to editor_id''
@app.route(apiPrefix + 'editor_setting_edit', methods=['GET', 'POST'])
def editor_setting_edit():
    try:
        data = request.get_data(as_text=True)
        re = editor.add_combination(data)
        return re
    except Exception as e:
        print(e)

# get objects and classifications in editor_id ''
@app.route(apiPrefix + 'get_editor_setting', methods=['GET', 'POST'])
def get_editor_setting():
    try:
        data = request.get_data(as_text=True)
        t = json.loads(data)
        re = editor.load_list(t['id'])
        return re
    except Exception as e:
        print(e)


@app.route(apiPrefix + 'choose_editor', methods=['GET', 'POST'])
def choose_editor():
    try:
        data = request.get_data(as_text=True)
        re = editor.choose_editor(data)
        return re
    except Exception as e:
        print(e)


@app.route(apiPrefix + 'get_editor_copy_setting', methods=['GET', 'POST'])
def get_editor_copy_setting():
    try:
        data = request.get_data(as_text=True)
        t = json.loads(data)
        re = editor.load_list_copy(t['id'])
        return re
    except Exception as e:
        print(e)


@app.route(apiPrefix + 'editor_copy_setting_edit', methods=['GET', 'POST'])
def editor_copy_setting_edit():
    try:
        data = request.get_data(as_text=True)
        re = editor.add_combination_copy(data)
        return re
    except Exception as e:
        print(e)


@app.route(apiPrefix + 'get_project_editor_copy_setting', methods=['GET', 'POST'])
def get_project_editor_copy_setting():
    try:
        data = request.get_data(as_text=True)
        t = json.loads(data)
        re = editor.load_list_copy_by_project_id(t['id'])
        return re
    except Exception as e:
        print(e)

# get objects and classifications in editor_copy_id''


@app.route(apiPrefix + 'editor_setting_delete', methods=['GET', 'POST'])
def editor_setting_delete():
    try:
        data = request.get_data(as_text=True)
        re = editor.delete_editor(data)
        return re
    except Exception as e:
        print(e)

#################### labelling Api #########################
# handle choose image
@app.route(apiPrefix + 'choose_image', methods=['POST'])
def choose_image():
    try:
        data = request.get_data(as_text=True)
        re = label_info.choose_image(data, current_user.id)
        return json.dumps(re)
    except Exception as e:
        print(e)

# handle choose view image
@app.route(apiPrefix + 'view_image', methods=['POST'])
def view_image():
    try:
        data = request.get_data(as_text=True)
        re = label_info.choose_view_image(data)
        return json.dumps(re)
    except Exception as e:
        print(e)

# handle submit label
@app.route(apiPrefix + 'submit_label', methods=['POST'])
def submit_label():
    try:
        data = request.get_data(as_text=True)
        re = label_info.submit_image(data, current_user.id)
        return json.dumps(re)
    except Exception as e:
        print(e)

# handle skip label
@app.route(apiPrefix + 'skip_label', methods=['POST'])
def skip_label():
    try:
        data = request.get_data(as_text=True)
        re = label_info.skip_image(data, current_user.id)
        return json.dumps(re)
    except Exception as e:
        print(e)

# handle back
@app.route(apiPrefix + 'back_label', methods=['POST'])
def back_label():
    try:
        data = request.get_data(as_text=True)
        re = label_info.back_image(data)
        return json.dumps(re)
    except Exception as e:
        print(e)

# handle next label
@app.route(apiPrefix + 'next_label', methods=['POST'])
def next_label():
    try:
        data = request.get_data(as_text=True)
        re = label_info.next_label_image(data)
        return json.dumps(re)
    except Exception as e:
        print(e)
#################### reviewing Api #########################

# handle choose image
@app.route(apiPrefix + 'choose_review_image', methods=['POST'])
def choose_review_image():
    try:
        data = request.get_data(as_text=True)
        re = label_info.choose_review_image(data)
        return json.dumps(re)
    except Exception as e:
        print(e)

# handle choose reviewed image
@app.route(apiPrefix + 'view_review_image', methods=['POST'])
def view_review_image():
    try:
        data = request.get_data(as_text=True)
        re = label_info.choose_review_view_image(data)
        return json.dumps(re)
    except Exception as e:
        print(e)

# handle submit reviewing result
@app.route(apiPrefix + 'submit_review', methods=['POST'])
def submit_review():
    try:
        data = request.get_data(as_text=True)
        re = label_info.submit_review(data, current_user.id)
        return json.dumps(re)
    except Exception as e:
        print(e)

@app.route(apiPrefix + 'next_review', methods=['POST'])
def next_review():
    try:
        data = request.get_data(as_text=True)
        re = label_info.next_review_image(data)
        return json.dumps(re)
    except Exception as e:
        print(e)
#################### export Api #########################

# handle export


@app.route(apiPrefix + 'export', methods=['POST'])
def export():
    try:
        data = request.get_data(as_text=True)
        t = json.loads(data)
        re = task.create_export(t['id'])
        return json.dumps(re)
    except Exception as e:
        print(e)

#################### Upload & delete & download Api #########################


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[-1] in ALLOW_EXTENSIONS

# upload file from front end to 'image' folder
@app.route(apiPrefix + 'upload', methods=['POST'])
def upload():
    # dataset_id = request.form['id']
    upload_file = request.files["file"]
    if upload_file and allowed_file(upload_file.filename):
        filename = str(time.time()) + secure_filename(upload_file.filename)
        upload_file.save(os.path.join(
            app.root_path, app.config['UPLOAD_FOLDER'], filename))
        re = {
            'ok': 'true',
            'message': 'success',
            'image_name': filename,
            'url': i_url + filename
        }
        return json.dumps(re)
    else:
        re = {
            'ok': 'false',
            'message': 'failed',
            'data': ''
        }
        return json.dumps(re)

# show image in url: i_url + "<imageName>"
@app.route(apiPrefix + 'image/<imageName>')
def get_frame(imageName):
    if imageName.rsplit('.', 1)[-1] == 'png':
        with open(r'./image/{}'.format(imageName), 'rb') as f:
            image = f.read()
            resp = Response(image, mimetype="image/png")
            return resp
    elif imageName.rsplit('.', 1)[-1] == 'jpg':
        with open(r'./image/{}'.format(imageName), 'rb') as f:
            image = f.read()
            resp = Response(image, mimetype="image/jpg")
            return resp
    elif imageName.rsplit('.', 1)[-1] == 'jpeg':
        with open(r'./image/{}'.format(imageName), 'rb') as f:
            image = f.read()
            resp = Response(image, mimetype="image/jpeg")
            return resp


@app.route(apiPrefix + 'delete_image', methods=["POST"])
def delete_image():
    try:
        data = request.get_data(as_text=True)
        d = json.loads(data)
        alias = d['alias']
        re = label.delete_image_alias(alias)
        return re
    except Exception as e:
        print(e)


@app.route(apiPrefix + 'export/<filename>')
def download_file(filename):
    directory = "./export/"
    return send_from_directory(directory, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
