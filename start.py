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

sys.path.append(os.getcwd()+'/htmls')

from htmls import *

version = '1.5'

host = ''
port = 5000
debug_mode = False
guest_enable = False
reCAPTCHA_mode = 0
reCAPTCHA_v2_HTML_KEY = ''
reCAPTCHA_v2_chat_KEY = ''
reCAPTCHA_v3_HTML_KEY = ''
reCAPTCHA_v3_chat_KEY = ''
reCAPTCHA_v3_score_min = 0.5

def read_config(): #读配置文件
    global host,port,reCAPTCHA_mode,debug_mode,guest_enable,reCAPTCHA_v2_HTML_KEY,reCAPTCHA_v2_chat_KEY,reCAPTCHA_v3_HTML_KEY,reCAPTCHA_v3_chat_KEY,reCAPTCHA_v3_score_min
    try:
        f = open(os.getcwd()+"/config.ini","r",encoding='utf-8')
    except:
        f = open(os.getcwd()+"/config.ini","w",encoding='utf-8')
        f.close()
        return 0
    lines = f.readlines()
    for i in range(0,len(lines)): #处理空行或注释
        #print(lines[i])
        if lines[i][0:2] == "//" or lines[i] == "\n":
            continue
        elif lines[i][0:10] == "server_ip=": #处理服务器ip
            #print("server_ip=")
            if lines[i][len(lines[i])-1] == "\n":
                host = lines[i][10:len(lines[i])-1]
            else:
                host = lines[i][10:len(lines[i])]
            if host == "auto": #自动获取ip
                print("auto get ip...")
                host = socket.gethostbyname(socket.gethostname())
                print("ip get successful\n")
            continue
        elif lines[i][0:11] == "debug_mode=": #处理调试模式
            #print("debug_mode=")
            if lines[i][len(lines[i])-1] == "\n":
                t_or_f = lines[i][11:len(lines[i])-1]
            else:
                t_or_f = lines[i][11:len(lines[i])]
            if t_or_f == 'true':
                debug_mode = True
            continue
        elif lines[i][0:13] == "guest_enable=": #处理是否有访客
            #print("guest_enable=")
            if lines[i][len(lines[i])-1] == "\n":
                t_or_f = lines[i][13:len(lines[i])-1]
            else:
                t_or_f = lines[i][13:len(lines[i])]
            if t_or_f == 'true':
                guest_enable = True
            continue
        elif lines[i][0:5] == "port=": #处理端口
            #print("port=")
            if lines[i][len(lines[i])-1] == "\n":
                control_port = int(lines[i][5:len(lines[i])-1])
            else:
                control_port = int(lines[i][5:len(lines[i])])
            continue
        elif lines[i][0:15] == "reCAPTCHA_mode=": #处理reCAPTCHA模式
            #print("reCAPTCHA_mode=")
            if lines[i][len(lines[i])-1] == "\n":
                reCAPTCHA_mode = int(lines[i][15:len(lines[i])-1])
            else:
                reCAPTCHA_mode = int(lines[i][15:len(lines[i])])
            continue
        elif lines[i][0:22] == "reCAPTCHA_v2_HTML_KEY=": #处理reCAPTCHA v2给HTML代码中的网站密钥
            #print("reCAPTCHA_v2_HTML_KEY=")
            if lines[i][len(lines[i])-1] == "\n":
                reCAPTCHA_v2_HTML_KEY = lines[i][22:len(lines[i])-1]
            else:
                reCAPTCHA_v2_HTML_KEY = lines[i][22:len(lines[i])]
            continue
        elif lines[i][0:22] == "reCAPTCHA_v2_chat_KEY=": #处理reCAPTCHA v2和验证服务器之间的通信密钥
            #print("reCAPTCHA_v2_HTML_KEY=")
            if lines[i][len(lines[i])-1] == "\n":
                reCAPTCHA_v2_chat_KEY = lines[i][22:len(lines[i])-1]
            else:
                reCAPTCHA_v2_chat_KEY = lines[i][22:len(lines[i])]
            continue
        elif lines[i][0:22] == "reCAPTCHA_v3_HTML_KEY=": #处理reCAPTCHA v2给HTML代码中的网站密钥
            #print("reCAPTCHA_v2_HTML_KEY=")
            if lines[i][len(lines[i])-1] == "\n":
                reCAPTCHA_v3_HTML_KEY = lines[i][22:len(lines[i])-1]
            else:
                reCAPTCHA_v3_HTML_KEY = lines[i][22:len(lines[i])]
            continue
        elif lines[i][0:22] == "reCAPTCHA_v3_chat_KEY=": #处理reCAPTCHA v2和验证服务器之间的通信密钥
            #print("reCAPTCHA_v2_HTML_KEY=")
            if lines[i][len(lines[i])-1] == "\n":
                reCAPTCHA_v3_chat_KEY = lines[i][22:len(lines[i])-1]
            else:
                reCAPTCHA_v3_chat_KEY = lines[i][22:len(lines[i])]
            continue
        elif lines[i][0:23] == "reCAPTCHA_v3_score_min=": #处理reCAPTCHA v3的分数最低值
            #print("reCAPTCHA_v3_score_min=")
            if lines[i][len(lines[i])-1] == "\n":
                reCAPTCHA_v3_score_min = float(lines[i][23:len(lines[i])-1])
            else:
                reCAPTCHA_v3_score_min = float(lines[i][23:len(lines[i])])
            continue
    if host == '': #如果没有设置服务器ip，则设置为自动
        print("auto get ip...")
        host = gethostbyname(gethostname())
        print("ip get successful\n")

read_config()

account_json = open('accounts.json','r')
accounts = json.loads(account_json.read())
account_json.close()

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
    
    account = 'account' in flask.request.form and flask.request.form['account']
    password = 'password' in flask.request.form and flask.request.form['password']
    
    if flask.request.method == 'GET':
        user = in_key(flask.request.cookies.get('key'))
        if user:
            return cloud_storage_login_successful

        if reCAPTCHA_mode ==  0:
            if guest_enable:
                return clout_storage_login_guest
            else:
                return clout_storage_login_html
            
        elif reCAPTCHA_mode ==  1:
            if guest_enable:
                return clout_storage_login_v2_guest_start+reCAPTCHA_v2_HTML_KEY+clout_storage_login_v2_guest_end
            else:
                return clout_storage_login_v2_start+reCAPTCHA_v2_HTML_KEY+clout_storage_login_v2_end
            
        elif reCAPTCHA_mode ==  2 or reCAPTCHA_mode == 3:
            if guest_enable:
                return clout_storage_login_v3_guest_start+reCAPTCHA_v3_HTML_KEY+clout_storage_login_v3_guest_middle+reCAPTCHA_v3_HTML_KEY+clout_storage_login_v3_guest_end
            else:
                return clout_storage_login_v3_start+reCAPTCHA_v3_HTML_KEY+clout_storage_login_v3_middle+reCAPTCHA_v3_HTML_KEY+clout_storage_login_v3_end
    
    else:
        recaptcha = flask.request.cookies.get('recaptcha')
        if reCAPTCHA_mode ==  1:
            r = requests.put(url='https://recaptcha.net/recaptcha/api/siteverify', data={'secret':reCAPTCHA_v2_chat_KEY,'response':recaptcha})
            recaptcha_return = json.loads(r.text)
            if recaptcha_return['success'] == False:
                return cloud_storage_recaptcha_error
        elif reCAPTCHA_mode ==  2 or reCAPTCHA_mode ==  3:
            r = requests.put(url='https://recaptcha.net/recaptcha/api/siteverify', data={'secret':reCAPTCHA_v3_chat_KEY,'response':recaptcha})
            recaptcha_return = json.loads(r.text)
            if (not recaptcha_return['success']) or (recaptcha_return['score'] < reCAPTCHA_v3_score_min):
                if reCAPTCHA_mode ==  2:
                    return cloud_storage_recaptcha_error
                else:
                    html_with_cookie = flask.make_response('<script>javascript:window.location.href="/file/recaptcha/retestv2"</script>')
                    html_with_cookie.set_cookie('account',account)
                    html_with_cookie.set_cookie('password',password)
                    return html_with_cookie
        
        if in_account(account,password) == 1:
            key = crate_key(account)
            html_with_cookie = flask.make_response(cloud_storage_login_successful)
            html_with_cookie.set_cookie('key',key)
            return html_with_cookie
        
        elif in_account(account,password) == 2:
            return cloud_storage_no_password_or_account
        
        elif in_account(account,password) == 3:
            if guest_enable:
                html_with_cookie = flask.make_response(cloud_storage_login_successful)
                html_with_cookie.set_cookie('key','guest')
                html_with_cookie.delete_cookie('recaptcha')
                return html_with_cookie
            else:
                key = flask.request.cookies.get('key')
                del_cookie = flask.make_response(cloud_storage_login_error)
                del_cookie.delete_cookie('key')
                return del_cookie

        else:
            return cloud_storage_login_error

@app.route('/file/recaptcha/retestv2',methods=['GET','POST'])
def recaptcha_mode_3_v2():
    if flask.request.method == 'GET':
        return recaptcha_mode_3_v2_html_start+reCAPTCHA_v2_HTML_KEY+recaptcha_mode_3_v2_html_end
    else:
        recaptcha = flask.request.cookies.get('recaptcha')
        r = requests.put(url='https://recaptcha.net/recaptcha/api/siteverify', data={'secret':reCAPTCHA_v2_chat_KEY,'response':recaptcha})
        recaptcha_return = json.loads(r.text)
        if recaptcha_return['success'] == False:
            return cloud_storage_recaptcha_error
        else:
            account = flask.request.cookies.get('account')
            password = flask.request.cookies.get('password')

            if in_account(account,password) == 1:
                key = crate_key(account)
                html_with_cookie = flask.make_response(cloud_storage_login_successful)
                html_with_cookie.set_cookie('key',key)
                html_with_cookie.delete_cookie('account')
                html_with_cookie.delete_cookie('password')
                html_with_cookie.delete_cookie('recaptcha')
                return html_with_cookie
        
            elif in_account(account,password) == 2:
                return cloud_storage_no_password_or_account
        
            elif in_account(account,password) == 3:
                if guest_enable:
                    html_with_cookie = flask.make_response(cloud_storage_login_successful)
                    html_with_cookie.set_cookie('key','guest')
                    html_with_cookie.delete_cookie('account')
                    html_with_cookie.delete_cookie('password')
                    html_with_cookie.delete_cookie('recaptcha')
                    return html_with_cookie
                else:
                    key = flask.request.cookies.get('key')
                    del_cookie = flask.make_response(cloud_storage_login_error)
                    del_cookie.delete_cookie('key')
                    del_cookie.delete_cookie('account')
                    del_cookie.delete_cookie('password')
                    del_cookie.delete_cookie('recaptcha')
                    return del_cookie

            else:
                return cloud_storage_login_error

@app.route('/file/<file_dir>')
def clout_storage_dir(file_dir):
    user = in_key(flask.request.cookies.get('key'))
    if not user or (not guest_enable and user == 1):
        key = flask.request.cookies.get('key')
        del_cookie = flask.make_response(cloud_storage_no_key)
        del_cookie.delete_cookie('key')
        return del_cookie
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
            
            list_dir = os.listdir(filedir)
            list_dir.sort()
            for file_name in list_dir:
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

            list_dir = os.listdir(filedir)
            list_dir.sort()
            for file_name in list_dir:
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
    if not user or (not guest_enable and user == 1):
        key = flask.request.cookies.get('key')
        del_cookie = flask.make_response(cloud_storage_no_key)
        del_cookie.delete_cookie('key')
        return del_cookie
    elif user == 1:
        return access_deline
    
    file_list = filename.split('@')
    del file_list[0]

    for i in range(0,len(file_list)):
        if file_list[i] == '..':
            del file_list[i]
    
    if (file_list[0] != user) ^ (file_list[0] != 'public'):
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
    if not user or (not guest_enable and user == 1):
        key = flask.request.cookies.get('key')
        del_cookie = flask.make_response(cloud_storage_no_key)
        del_cookie.delete_cookie('key')
        return del_cookie
    elif user == 1:
        return access_deline

    file_list = filedir.split('@')
    del file_list[0]

    for i in range(0,len(file_list)):
        if file_list[i] == '..':
            del file_list[i]
    
    if (file_list[0] != user) ^ (file_list[0] != 'public'):
        file_dir = os.getcwd()+'/files/'+'/'.join(file_list)
    else:
        return access_deline
    
    if flask.request.method == 'GET':
        return upload_html_start+filedir+upload_html_end
    
    else:
        
        file = flask.request.files['file']
        file_in = file.read()
        size = len(file_in)/1024/1024/1024
        free_size = get_free_space(os.getcwd()+'/files/public')
            
        if file_list[0] == 'public':
            if size < free_size:
                f = open(file_dir+'/'+file.filename,'wb')
                f.write(file_in)
                f.close()
                return upload_finish_start+filedir+upload_finish_end
                
            else:
                return upload_no_space_start+filedir+upload_no_space_end
        else:
            if size < int(accounts[user][1])-free_size:
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
    if not user or (not guest_enable and user == 1):
        key = flask.request.cookies.get('key')
        del_cookie = flask.make_response(cloud_storage_no_key)
        del_cookie.delete_cookie('key')
        return del_cookie
    elif user == 1:
        return access_deline

    file_list = filedir.split('@')
    del file_list[0]

    for i in range(0,len(file_list)):
        if file_list[i] == '..':
            del file_list[i]

    if (file_list[0] != user) ^ (file_list[0] != 'public'):
        file_dir = os.getcwd()+'/files/'+'/'.join(file_list)
    else:
        return access_deline

    if flask.request.method == 'GET':
        return new_dir_start+filedir+new_dir_end
    
    else:
        file_name = 'dir_name' in flask.request.form and flask.request.form['dir_name']
        if file_name:
            if not os.path.exists(file_name):
                os.mkdir(file_dir+'/'+file_name)
            return new_dir_success_start+filedir+new_dir_success_end
        else:
            return new_dir_no_start+filedir+new_dir_no_end

@app.route('/file/<filedir>/download',methods=['GET','POST'])
def download(filedir):
    user = in_key(flask.request.cookies.get('key'))
    if not user or (not guest_enable and user == 1):
        key = flask.request.cookies.get('key')
        del_cookie = flask.make_response(cloud_storage_no_key)
        del_cookie.delete_cookie('key')
        return del_cookie

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

    filedir = os.getcwd()+'/files/'+'/'.join(file_list)

    response = flask.make_response(flask.send_from_directory(filedir,file_name,as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(file_name.encode().decode('latin-1'))
    return response

@app.route('/file/<filedir>/view')
def view(filedir):
    user = in_key(flask.request.cookies.get('key'))
    if not user or (not guest_enable and user == 1):
        key = flask.request.cookies.get('key')
        del_cookie = flask.make_response(cloud_storage_no_key)
        del_cookie.delete_cookie('key')
        return del_cookie

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
    app.run(debug=debug_mode,host=host,port=port)
