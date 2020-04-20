from flask import Flask, request, redirect
import os

app = Flask(__name__, static_folder="statics")
members=[
    {"id": "sookbun", "pw": "111111"},
    {"id": "duru", "pw": "222222"}
]
    
@app.route("/new", methods = ['GET', 'POST'])
def new():
    template = get_template('new.html')
    if request.method == 'GET':
        return template.format('')
    elif request.method == 'POST':
        #만약 회원이 있으면, "이미 가입되어 있습니다 ."라고 알려주자.
        for mem in members:
            if request.form['id'] == mem['id']:
                return template.format("<p>이미 가입되어 있습니다.</p>") 
            
        members.append({"id": request.form['id'], "pw": request.form['pw']})
        os.makedirs(f"content/{request.form['id']}")
    return redirect("/login")

def get_template(filename):
    with open('views/'+filename, 'r', encoding="utf-8") as f:
        template = f.read()
    return template

def get_menu(name=None):
    menu_tmp = "<li><a href='/"+name+ "/login/{0}'>{0}</a></li>"
    menu = [i for i in os.listdir('content/'+name) if i[0] != '.']
    
    return "\n".join([menu_tmp.format(j) for j in menu])

@app.route('/<name>/login', methods = ['GET', 'POST'])
def index(name):
    template = get_template('template.html')
    content = ''
    button = f'''
    <button type="button" onclick="location.href='/search' ">검색</button><br>
    <button type="button" onclick="location.href='/{name}/create' ">추가</button><br>
    <button type="button" onclick="location.href='/login' ">로그아웃</button>'''
    return template.format(name,name,content,get_menu(name),button)

@app.route('/<name>/login/<title>', methods = ['GET', 'POST'])
def html(name,title):
    template = get_template('template.html')
    button = f'''
    <button type="button" onclick="location.href='/{name}/delete/{title}' ">삭제</button>
    <button type="button" onclick="location.href='/{name}/update/{title}' ">수정</button>'''
    
    with open(f'content/{name}/{title}','r',encoding='utf-8') as f:
        content = f.read()
    return template.format(name,title,content,get_menu(name),button)


@app.route('/favicon.icon')
def favicon():
    return abort(404)

@app.route("/search", methods=['GET', 'POST']) 
def search():
    template = get_template('search.html')
    if request.method == 'GET':
        return template + 'GET'
    elif request.method == 'POST':
        return redirect("/result"+"?keyword=" + request.form['keyword']) 
    
@app.route("/result", methods=['GET', 'POST'])
def result():
    template = get_template('result.html')
    tmp_id = []
    keyword = request.args.get('keyword','')
    list_id = [n['id'] for n in members]
    list_cont = [{"id":i, "title": os.listdir(f'content/{i}')} for i in list_id]
    for i in list_cont:
        if keyword in i['title']:
            tmp_id.append(i['id'])
    return template.format(keyword, ', '.join(tmp_id))

            
@app.route("/<name>/create", methods=['GET', 'POST'])
def create(name):
    template = get_template('create.html')
    menu = get_menu(name)
    if request.method == 'GET':
        return template.format(name,'', menu) + 'GET'
    elif request.method == 'POST':
        with open(f'content/{name}/{request.form["title"]}', 'w') as f:
            f.write(request.form["desc"])
        return redirect(f'/{name}/login')

@app.route("/<name>/delete/<title>")
def delete(name, title):
    os.remove(f'content/{name}/{title}')
    return redirect(f'/{name}/login')

@app.route("/<name>/update/<title>", methods=['GET', 'POST'])
def update(name, title):
    menu = get_menu(name)
    with open('views/update.html', 'r', encoding='utf-8') as f:
        update = f.read()
        
    if request.method == 'GET':
        with open(f"content/{name}/{title}", 'r', encoding = 'utf-8') as file:
            content = file.read()
        return update.format(name, menu, title, content)
    else:
        with open(f"content/{name}/{title}", 'w', encoding = 'utf-8') as f:
            f.write(request.form['desc'])
        
        if request.form['title']:
            os.rename(f"content/{name}/{title}",f"content/{name}/{request.form['title']}")
            
        return redirect(f"/{name}/login")
                        




@app.route("/login", methods = ['GET', 'POST'])
def login():
    template = get_template('login.html')
    if request.method == 'GET':
        return template.format("<p>로그인을 해주세요</p>")
    elif request.method == 'POST':
        #만약 회원이 아니면, "회원이 아닙니다."라고 알려주자.
        m = [e for e in members if e['id'] == request.form['id']]
        if len(m) == 0:
            return template.format("<p>회원이 아닙니다.</p>")
        
        if request.form['pw'] !=  m[0]['pw']:
            return template.format("<p>패스워드를 확인해주세요.</p>")
        
        #로그인 성공시 메인으로
        return redirect("/"+m[0]['id'] + "/login" "?id=" + m[0]['id']) 
    return template