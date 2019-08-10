import platform
import requests
import ctypes
import string
import random
import socket
import shutil
import flask
import json
import sys
import os
if platform.system() == 'Windows':
    sys.path.append(os.getcwd()+'\\htmls')
else:
    sys.path.append(os.getcwd()+'/htmls')
from htmls import *

version = '1.2'

recaptcha_server_key = '这里填recaptcha给服务器用的密钥'

account_json = open('accounts.json','r')
accounts = json.loads(account_json.read())
account_json.close()

if platform.system() == 'Windows':
    if not os.path.isdir(os.getcwd()+'\\files'):
        os.mkdir(os.getcwd()+'\\files')

    for key in accounts:
        if not os.path.isdir(os.getcwd()+'\\files\\'+key):
            os.mkdir(os.getcwd()+'\\files\\'+key)

    if not os.path.isdir(os.getcwd()+'\\files\\public'):
        os.mkdir(os.getcwd()+'\\files\\public')

else:
    if not os.path.isdir(os.getcwd()+'/files'):
        os.mkdir(os.getcwd()+'/files')

    for key in accounts:
        if not os.path.isdir(os.getcwd()+'/files/'+key):
            os.mkdir(os.getcwd()+'/files/'+key)

    if not os.path.isdir(os.getcwd()+'/files/public'):
        os.mkdir(os.getcwd()+'/files/public')

app = flask.Flask(__name__)
user_logined_key = {}

#=====起始页=====#

@app.route('/')
def start_page():
    return start_page_html

#*#==========#*#



#=====文件系统=====#

def in_account(account,password):
    global accounts
    
    if account == 'guest':
        return 3
    else:
        if not account or not password:
            return 2
        try:
            if accounts[account][0] == password:
                return 1
        except:
            return 0

def get_free_space(folder):
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value/1024/1024/1024 
    else:
        st = os.statvfs(folder)
        return st.f_bavail * st.f_frsize/1024/1024/1024

def crate_key(user):
    global user_logined_key
    key = ''.join(random.sample(string.ascii_letters + string.digits, 32))
    user_logined_key[key] = user
    return key

def in_key(key):
    global user_logined_key
    try:
        return user_logined_key[key]
    except:
        if key == 'guest':
            return 1
        return False

def del_key(key):
    global user_logined_key
    del user_logined_key[key]
    return None

@app.route('/file',methods=['GET','POST'])
def clout_storage_login():
    global user_logined_key
    if flask.request.method == 'GET':
        user = in_key(flask.request.cookies.get('key'))
        if user:
            return cloud_storage_login_successful
        return clout_storage_login_html
    
    else:
        recaptcha = flask.request.cookies.get('recaptcha')
        r = requests.put(url='https://recaptcha.net/recaptcha/api/siteverify', data={'secret':recaptcha_server_key,'response':recaptcha})
        recaptcha_return = json.loads(r.text)
        print(recaptcha_return)
        if recaptcha_return['success'] == False:
            return cloud_storage_recaptcha_error
        
        account = 'account' in flask.request.form and flask.request.form['account']
        password = 'password' in flask.request.form and flask.request.form['password']
        
        if in_account(account,password) == 1:
            key = crate_key(account)
            html_with_cookie = flask.make_response(cloud_storage_login_successful)
            html_with_cookie.set_cookie('key',key)
            return html_with_cookie
        
        elif in_account(account,password) == 2:
            return cloud_storage_no_password_or_account
        
        elif in_account(account,password) == 3:
            html_with_cookie = flask.make_response(cloud_storage_login_successful)
            html_with_cookie.set_cookie('key','guest')
            return html_with_cookie

        else:
            return cloud_storage_login_error

@app.route('/file/<file_dir>')
def clout_storage_dir(file_dir):
    user = in_key(flask.request.cookies.get('key'))
    if not user:
        return cloud_storage_no_key
    elif user != 1:
        file_dir_list = file_dir.split('@')
        del file_dir_list[0]
        
        for i in range(0,len(file_dir_list)):
            if file_dir_list[i] == '..':
                del file_dir_list[i]
                
        if len(file_dir_list) == 0 or file_dir_list[0] == '':
            html_middle = '''<body>
<h3>文件列表(单击文件名下载)</h3>
<input type='button' name='submit' onclick='javascript:window.location.href="/file/operate/logout";' value='退出登录' />
<input type='button' name='submit' disabled="disabled" value='上传文件' />
<input type='button' name='submit' disabled="disabled" value='新建文件夹' />
<input type='button' name='submit' disabled="disabled" value='上一级' />
<p><a href='/file/allfiles@public'>公共 (文件夹)</a></p>
<p><a href='/file/allfiles@'''+user+''''>私人 (文件夹)</a></p>'''
            return cloud_storage_documents_list_start+html_middle+cloud_storage_documents_list_end
        
        else:
            if platform.system() == 'Windows':
                filedir = os.getcwd()+'\\files\\'+'\\'.join(file_dir_list)
            else:
                filedir = os.getcwd()+'/files/'+'/'.join(file_dir_list)

            if len(file_dir_list) == 1:
                last_grade = 'allfiles'
            
            else:
                last_grade = 'allfiles@'+'@'.join(file_dir_list[:-1])
            
            html_middle = '''<body>
<h3>文件列表(单击文件名下载)</h3>
<input type='button' name='submit' onclick='javascript:window.location.href="/file/operate/logout";' value='退出登录' />
<input type='button' name='submit' onclick='javascript:window.location.href="/file/'''+file_dir+'''/upload";' value='上传文件' />
<input type='button' name='submit' onclick='javascript:window.location.href="/file/'''+file_dir+'''/newdir";' value='新建文件夹' />
<input type='button' name='submit' onclick='javascript:window.location.href="/file/'''+last_grade+'''";' value='上一级' />
'''
            if not((file_dir_list[0] != user) ^ (file_dir_list[0] != 'public')):
                return '<script>window.location.href="/file/allfiles"</script>'
            for file_name in os.listdir(filedir):
                if platform.system() == 'Windows':
                    file_all_dir = filedir+'\\'+file_name
                else:
                    file_all_dir = filedir+'/'+file_name
                if os.path.isdir(file_all_dir):
                    html_middle = html_middle+'''<p><a href='/file/'''+file_dir+'@'+file_name+''''>'''+file_name+''' (文件夹)</a> <a href='javascript:if(confirm("确认要删除？")){window.location="/file/'''+file_dir+'@'+file_name+'''/delete";}'>删除</a></p>\n'''
                else:
                    html_middle = html_middle+'''<p><a href='/file/'''+file_dir+'@'+file_name+'''/download'>'''+file_name+'''</a> <a href='/file/'''+file_dir+'@'+file_name+'''/view'>预览</a> <a href='javascript:if(confirm("确认要删除？")){window.location="/file/'''+file_dir+'@'+file_name+'''/delete";}'>删除</a></p>\n'''

            return cloud_storage_documents_list_start+html_middle+cloud_storage_documents_list_end
                

    else:
        file_dir_list = file_dir.split('@')
        del file_dir_list[0]
        
        for i in range(0,len(file_dir_list)):
            if file_dir_list[i] == '..':
                del file_dir_list[i]
                
        if len(file_dir_list) == 0:
            html_middle = '''<body>
<h3>文件列表(单击文件名下载)</h3>
<input type='button' name='submit' onclick='javascript:window.location.href="/file/operate/logout";' value='退出登录' />
<input type='button' name='submit' disabled="disabled"value='上传文件' />
<input type='button' name='submit' disabled="disabled" value='新建文件夹' />
<input type='button' name='submit' disabled="disabled" value='上一级' />
<p><a href='/file/allfiles@public'>公共 (文件夹)</a></p>'''
            return cloud_storage_documents_list_start+html_middle+cloud_storage_documents_list_end
        
        else:
            if platform.system() == 'Windows':
                filedir = os.getcwd()+'\\files\\'+'\\'.join(file_dir_list)
            else:
                filedir = os.getcwd()+'/files/'+'/'.join(file_dir_list)

            if len(file_dir_list) == 1:
                last_grade = 'allfiles'
            
            else:
                print (file_dir_list)
                last_grade = 'allfiles@'+'@'.join(file_dir_list[:-1])
            
            html_middle = '''<body>
<h3>文件列表(单击文件名下载)</h3>
<input type='button' name='submit' onclick='javascript:window.location.href="/file/operate/logout";' value='退出登录' />
<input type='button' name='submit' disabled="disabled"value='上传文件' />
<input type='button' name='submit' disabled="disabled" value='新建文件夹'>
<input type='button' name='submit' onclick='javascript:window.location.href="/file/'''+last_grade+'''";' value='上一级' />
'''
            if file_dir_list[0] != 'public':
                return '<script>window.location.href="/file/allfiles"</script>'
            for file_name in os.listdir(filedir):
                if platform.system() == 'Windows':
                    file_all_dir = filedir+'\\'+file_name
                else:
                    file_all_dir = filedir+'/'+file_name
                if os.path.isdir(file_all_dir):
                    html_middle = html_middle+'''<p><a href='/file/'''+file_dir+'@'+file_name+''''>'''+file_name+''' (文件夹)</a></p>\n'''
                else:
                    html_middle = html_middle+'''<p><a href='/file/'''+file_dir+'@'+file_name+'''/download'>'''+file_name+'''</a> <a href='/file/'''+file_dir+'@'+file_name+'''/view'>预览</a></p>\n'''

            return cloud_storage_documents_list_start+html_middle+cloud_storage_documents_list_end

@app.route('/file/operate/logout')
def logout():
    key = flask.request.cookies.get('key')
    del_cookie = flask.make_response(logout_html)
    del_cookie.delete_cookie('key')
    return del_cookie

@app.route('/file/<filename>/delete')
def delete_file(filename):
    user = in_key(flask.request.cookies.get('key'))
    if not user:
        return cloud_storage_no_key
    elif user == 1:
        return access_deline
    
    file_list = filename.split('@')
    del file_list[0]

    for i in range(0,len(file_list)):
        if file_list[i] == '..':
            del file_list[i]
    
    if (file_list[0] != user) ^ (file_list[0] != 'public'):
        if platform.system() == 'Windows':
            filedir = os.getcwd()+'\\files\\'+'\\'.join(file_list)
        else:
            filedir = os.getcwd()+'/files/'+'/'.join(file_list)
        back = 'allfiles@'+'@'.join(file_list[:-1])
        
        if os.path.isdir(filedir):
            shutil.rmtree(filedir)
            
        else:
            os.remove(filedir)
        return delete_file_start+back+delete_file_end
    
    else:
        return access_deline

@app.route('/file/<filedir>/upload',methods=['GET','POST'])
def upload_file(filedir):
    user = in_key(flask.request.cookies.get('key'))
    if not user:
        return cloud_storage_no_key
    elif user == 1:
        return access_deline

    file_list = filedir.split('@')
    del file_list[0]

    for i in range(0,len(file_list)):
        if file_list[i] == '..':
            del file_list[i]
    
    if (file_list[0] != user) ^ (file_list[0] != 'public'):
        if platform.system() == 'Windows':
            file_dir = os.getcwd()+'\\files\\'+'\\'.join(file_list)
        else:
            file_dir = os.getcwd()+'/files/'+'/'.join(file_list)
    else:
        return access_deline
    
    if flask.request.method == 'GET':
        return upload_html_start+filedir+upload_html_end
    
    else:
        
        file = flask.request.files['file']
        file_in = file.read()
        size = len(file_in)/1024/1024/1024
        if platform.system() == 'Windows':
            free_size = get_free_space(os.getcwd()+'\\files\\public')
        else:
            free_size = get_free_space(os.getcwd()+'/files/public')
            
        if file_list[0] == 'public':
            if size < free_size:
                if platform.system() == 'Windows':
                    f = open(file_dir+'\\'+file.filename,'wb')
                else:
                    f = open(file_dir+'/'+file.filename,'wb')
                f.write(file_in)
                f.close()
                return upload_finish_start+filedir+upload_finish_end
                
            else:
                return upload_no_space_start+filedir+upload_no_space_end
        else:
            if size < int(accounts[user][1])-free_size:
                if platform.system() == 'Windows':
                    f = open(file_dir+'\\'+file.filename,'wb')
                else:
                    f = open(file_dir+'/'+file.filename,'wb')
                f.write(file_in)
                f.close()
                return upload_finish_start+filedir+upload_finish_end
                
            else:
                return upload_no_space_start+filedir+upload_no_space_end
            
        return upload_no_file_start+filedir+upload_no_file_end

@app.route('/file/<filedir>/newdir',methods=['GET','POST'])
def newdir(filedir):
    user = in_key(flask.request.cookies.get('key'))
    if not user:
        return cloud_storage_no_key
    elif user == 1:
        return access_deline

    file_list = filedir.split('@')
    del file_list[0]

    for i in range(0,len(file_list)):
        if file_list[i] == '..':
            del file_list[i]

    if (file_list[0] != user) ^ (file_list[0] != 'public'):
        if platform.system() == 'Windows':
            file_dir = os.getcwd()+'\\files\\'+'\\'.join(file_list)
        else:
            file_dir = os.getcwd()+'/files/'+'/'.join(file_list)
    else:
        return access_deline

    if flask.request.method == 'GET':
        return new_dir_start+filedir+new_dir_end
    
    else:
        file_name = 'dir_name' in flask.request.form and flask.request.form['dir_name']
        if file_name:
            if not os.path.exists(file_name):
                if platform.system() == 'Windows':
                    os.mkdir(file_dir+'\\'+file_name)
                else:
                    os.mkdir(file_dir+'/'+file_name)
            return new_dir_success_start+filedir+new_dir_success_end
        else:
            return new_dir_no_start+filedir+new_dir_no_end

@app.route('/file/<filedir>/download',methods=['GET','POST'])
def download(filedir):
    user = in_key(flask.request.cookies.get('key'))
    if not user:
        return cloud_storage_no_key

    file_list = filedir.split('@')
    del file_list[0]

    for i in range(0,len(file_list)):
        if file_list[i] == '..':
            del file_list[i]

    if user == 1:
        if file_list[0] != 'public':
            return access_deline

    else:
        if not((file_list[0] != user) ^ (file_list[0] != 'public')):
            return access_deline

    file_name = file_list[-1]
    del file_list[-1]

    if platform.system() == 'Windows':
        filedir = os.getcwd()+'\\files\\'+'\\'.join(file_list)
    else:
        filedir = os.getcwd()+'/files/'+'/'.join(file_list)

    response = flask.make_response(flask.send_from_directory(filedir,file_name,as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(file_name.encode().decode('latin-1'))
    return response

@app.route('/file/<filedir>/view')
def view(filedir):
    user = in_key(flask.request.cookies.get('key'))
    if not user:
        return cloud_storage_no_key

    file_list = filedir.split('@')
    del file_list[0]

    for i in range(0,len(file_list)):
        if file_list[i] == '..':
            del file_list[i]

    if user == 1:
        if file_list[0] != 'public':
            return access_deline

    else:
        if not((file_list[0] != user) ^ (file_list[0] != 'public')):
            return access_deline

    if platform.system() == 'Windows':
        file_dir = os.getcwd()+'\\files\\'+'\\'.join(file_list)
    else:
        file_dir = os.getcwd()+'/files/'+'/'.join(file_list)
        
    file_name = file_list[-1]
    back = 'allfiles@'+'@'.join(file_list[:-1])
    back_file = file_name.split('.')[-1].lower()

    middle_html = '<h4>'+file_name+'</h4>\n'

    if back_file in ['mp4','mkv']:
        middle_html = middle_html+'''<video src = "/file/'''+filedir+'''/download" width="854px" height="480px" autoplay="autoplay" preload="auto" controls="controls">
你的浏览器不支持预览视频
</video>'''

    elif back_file in ['flv']:
        middle_html = middle_html+'''<script src="/static/flv.min.js"></script>
<video id="videoElement" width="854px" height="480px" autoplay="autoplay" preload="auto" controls="controls">
你的浏览器不支持预览视频
</video>
<script>
    if (flvjs.isSupported()) {
        var videoElement = document.getElementById('videoElement');
        var flvPlayer = flvjs.createPlayer({
            type: 'flv',
            url: '''+'\'/file/'+filedir+'/download\''+'''
        });
        flvPlayer.attachMediaElement(videoElement);
        flvPlayer.load();
    }
</script>'''

    elif back_file in ['txt','html','css','js','bat','json']:
        f = open(file_dir,'r')
        line = f.readline()
        while line:
            if line == '\n':
                middle_html = middle_html+'<br></br>\n'
            else:
                middle_html = middle_html+'<p>'+line+'</p>\n'
            line = f.readline()
        f.close()

    elif back_file in ['mp3','wav','ogg']:
        middle_html = middle_html+'''<audio src = "/file/'''+filedir+'''/download" autoplay="autoplay" controls="controls">
<object type="application/x-shockwave-flash" style="outline:none;" data="/file/'''+filedir+'''/download"></object>
</audio>'''

    elif back_file in ['jpg','jpeg','png']:
        middle_html = middle_html+'''<img src = "/file/'''+filedir+'''/download">
</img>'''

    else:
        middle_html = middle_html+'''<h5>这种文件暂时还不支持在线预览</h5>'''
        
    middle_html = middle_html+'''<br></br>
<input type='button' name='submit' onclick='javascript:window.location.href="/file/'''+filedir+'''/download";' value='下载' />
<input type='button' name='submit' onclick='javascript:window.location.href="/file/'''+back+'''";' value='返回' />'''
        
    return view_start_html+middle_html+view_end_html


#*#==========#*#

if __name__ == '__main__':
    app.run(debug=True,host=socket.gethostbyname(socket.gethostname()),port=5000)
