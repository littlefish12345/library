recaptcha_site_key = '这里填recaptcha给网页用的密钥'

start_page_html = '''<!DOCTYPE HTML>
<html>
<head>
<title>主页</title>
<link rel="shortcut icon" href="/static/icon.jpg">
</head>
<body>
<input type='submit' value='云储存' onclick='javascript:window.location = "/file";' />
<p>此web为开源项目，严禁商用，地址为<a href=https://github.com/littlefish12345/library>https://github.com/littlefish12345/library</a></p>
</body>
</html>
'''

clout_storage_login_html = '''<!DOCTYPE HTML>
<html>
<head>
<title>云储存</title>
<link rel="shortcut icon" href="/static/icon.jpg">
<script src="https://www.recaptcha.net/recaptcha/api.js?render=reCAPTCHA_site_key" async defer></script>
<script>
function robotVerified(a, b){
console.log('Verified: not robot');
document.cookie = "recaptcha="+a;
//setTimeout(function(){document.getElementById("btn").click()}, 1000);
}
</script>
</head>
<body>
<h3>请输入账号和密码</h3>
<form action="?" method='post'>
<input type='text' name='account' placeholder='账号' />
<input type='password' name='password' placeholder='密码' />
<input type='submit' id='btn' value='确定' />
<br></br>
<div class="g-recaptcha" data-callback="robotVerified" data-sitekey="'''+your_site_key+'''"></div>
</form>
<p>访客账号为guest，密码为空</p>
<input type='button' name='submit' onclick='javascript:window.location.href="/";' value='返回' />
</body>
</html>
'''

cloud_storage_login_successful = '''<!DOCTYPE HTML>
<html>
<head>
<title>云储存</title>
<link rel="shortcut icon" href="/static/icon.jpg">
</head>
<body>
<h3>登录成功，正在跳转...</h3>
<script>
setTimeout(function(){window.location.href="/file/allfiles";}, 1200);
</script>
</body>
</html>
'''

cloud_storage_login_error = '''<!DOCTYPE HTML>
<html>
<head>
<title>云储存</title>
<link rel="shortcut icon" href="/static/icon.jpg">
</head>
<body>
<h3>账号或密码错误</h3>
<input type='button' name='submit' onclick='javascript:window.location.href="/file";' value='返回' />
</body>
</html>
'''

cloud_storage_recaptcha_error = '''<!DOCTYPE HTML>
<html>
<head>
<title>云储存</title>
<link rel="shortcut icon" href="/static/icon.jpg">
</head>
<body>
<h3>你没有通过reCAPTCHA测试</h3>
<input type='button' name='submit' onclick='javascript:window.location.href="/file";' value='返回' />
</body>
</html>
'''

cloud_storage_no_password_or_account = '''<!DOCTYPE HTML>
<html>
<head>
<title>云储存</title>
<link rel="shortcut icon" href="/static/icon.jpg">
</head>
<body>
<h3>没有账号或密码</h3>
<input type='button' name='submit' onclick='javascript:window.location.href="/file";' value='返回' />
</body>
</html>
'''

cloud_storage_no_key = '''<!DOCTYPE HTML>
<html>
<head>
<title>云储存</title>
<link rel="shortcut icon" href="/static/icon.jpg">
</head>
<body>
<h3>你还没有登陆，快去登陆吧</h3>
<input type='button' name='submit' onclick='javascript:window.location.href="/file";' value='登录界面' />
</body>
</html>
'''

cloud_storage_documents_list_start = '''<!DOCTYPE HTML>
<html>
<head>
<title>云储存</title>
<link rel="shortcut icon" href="/static/icon.jpg">
</head>
'''

cloud_storage_documents_list_end = '''
</body>
</html>
'''

logout_html = '''<!DOCTYPE HTML>
<html>
<head>
<title>退出登录成功</title>
<link rel="shortcut icon" href="/static/icon.jpg">
</head>
<body>
<h3>退出登录成功</h3>
<input type='button' name='submit' onclick='javascript:window.location.href="/file";' value='登录界面'>
</body>
</html>
'''

delete_file_start = '''<!DOCTYPE HTML>
<html>
<head>
<title>云储存</title>
<link rel="shortcut icon" href="/static/icon.jpg">
</head>
<body>
<h3>删除成功</h3>
<input type='button' name='submit' onclick='javascript:window.location.href="/file/'''

delete_file_end = '''";' value='返回'>
</body>
</html>
'''

upload_html_start = '''<!DOCTYPE HTML>
<html>
<head>
<title>云储存</title>
<link rel="shortcut icon" href="/static/icon.jpg">
</head>
<body>
<h3>请选择一个文件上传</h3>
<form method='POST' enctype='multipart/form-data'>
<input type='file' name='file'>
<input type='submit' value='上传'>
</form>
<input type='button' name='submit' onclick='javascript:window.location.href="/file/'''

upload_html_end = '''";' value='返回' />
</body>
</html>
'''

access_deline = '''<!DOCTYPE HTML>
<html>
<head>
<title>云储存</title>
<link rel="shortcut icon" href="/static/icon.jpg">
</head>
<body>
<h3>访问被拒绝</h3>
</body>
</html>
'''

upload_no_file_start = '''<!DOCTYPE HTML>
<html>
<head>
<title>云储存</title>
<link rel="shortcut icon" href="/static/icon.jpg">
</head>
<body>
<h3>你没有选择文件上传</h3>
<input type='button' name='submit' onclick='javascript:window.location.href="/file/'''

upload_no_file_end = '''/upload";' value='返回' />
</body>
</html>
'''

upload_finish_start = '''<!DOCTYPE HTML>
<html>
<head>
<title>云储存</title>
<link rel="shortcut icon" href="/static/icon.jpg">
</head>
<body>
<h3>上传成功</h3>
<input type='button' name='submit' onclick='javascript:window.location.href="/file/'''

upload_finish_end = '''";' value='返回' />
</body>
</html>
'''

upload_no_space_start = '''<!DOCTYPE HTML>
<html>
<head>
<title>云储存</title>
<link rel="shortcut icon" href="/static/icon.jpg">
</head>
<body>
<h3>你的文件大小范围超出了硬盘大小</h3>
<input type='button' name='submit' onclick='javascript:window.location.href="/file/'''

upload_no_space_end = '''";' value='返回' />
</body>
</html>
'''

new_dir_start = '''<!DOCTYPE HTML>
<html>
<head>
<title>云储存</title>
<link rel="shortcut icon" href="/static/icon.jpg">
</head>
<body>
<h3>请输入新文件夹名称</h3>
<form method='POST' enctype='multipart/form-data'>
<input type='text' name='dir_name'>
<input type='submit' value='确定'>
<input type='button' name='submit' onclick='javascript:window.location.href="/file/'''

new_dir_end = '''";' value='返回' />
</body>
</html>

'''

new_dir_success_start = '''<!DOCTYPE HTML>
<html>
<head>
<title>云储存</title>
<link rel="shortcut icon" href="/static/icon.jpg">
</head>
<body>
<h3>创建成功</h3>
<input type='button' name='submit' onclick='javascript:window.location.href="/file/'''

new_dir_success_end = '''";' value='返回' />
</body>
</html>

'''

new_dir_no_start = '''<!DOCTYPE HTML>
<html>
<head>
<title>云储存</title>
<link rel="shortcut icon" href="/static/icon.jpg">
</head>
<body>
<h3>你没有输入文件夹名</h3>
<input type='button' name='submit' onclick='javascript:window.location.href="/file/'''

new_dir_no_end = '''";' value='返回' />
</body>
</html>

'''

view_start_html = '''<!DOCTYPE HTML>
<html>
<head>
<title>云储存</title>
<link rel="shortcut icon" href="/static/icon.jpg">
</head>
<body>
'''

view_end_html ='''
</body>
</html>'''
