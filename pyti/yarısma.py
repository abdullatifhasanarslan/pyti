from bottle import get, post, request,default_app,run,template, route, redirect,debug

class soru:
    def __init__(self,metin,şık1,şık2,şık3,şık4):
        self.metin = metin
        self.şık1 = şık1
        self.şık2 = şık2
        self.şık3 = şık3
        self.şık4 = şık4

class şık:
    def __init__(self,metin,doğruluk=False):
        self.metin = metin
        self.doğruluk = doğruluk
    def kontrol(self):
        return str(self.doğruluk)

yarısanlar = []
yarısanlar_sonuç = []
sorular = [soru("aaaa",
                şık("w",True),
                şık("e"),
                şık("e"),
                şık("e")),
           soru("aaaa",
                şık("w",True),
                şık("e"),
                şık("e"),
                şık("e"))]

def htmlify(title="FSM", script="", style="", header="", body="", ending=""):

    page = """<!DOCTYPE html>
              <html>
                  <head>
                      <style>
                      """ + style + """
                      </style>
    
                      <script>
                      """ + script + """
                      </script>
                      
                      <title>""" + title + """</title>
                      <meta charset="utf-8" />
                  </head>
                  <body>
                      """ + header + body + ending + """
                  </body>
              </html>"""
    return page



@route('/')
def anasayfa():
    return htmlify(body="""<form action="/a" method="post">
  İsim:<br>
  <input type="text" name="isim">
  <input type="submit" value="Başla">
  </form>    """)

@get('/hata')
def anasayfa():
    return htmlify(body="""<form action="/a" method="post">
  İsim: (Başka bir isim seçiniz)<br>
  <input type="text" name="isim">
  <input type="submit" value="Başla">
</form>    """)

@route('/a',method="POST")
def anasayfa2():
    isim = request.forms.get('isim')
    for i in yarısanlar:
        if i == isim:
            redirect("/hata")
            break
    else:
        yarısanlar.append(isim)
        yarısanlar_sonuç.append([])
        redirect('/'+isim+'/1')


##    return htmlify(body="<p>"+sor+"</p>"+"""<form action="/"+name+"/2">
##      <input type="radio" name="cevap" value="a" checked>""" +"w"+"""<br>
##      <input type="radio" name="cevap" value="b">""" + "d" +"""<br>
##      <input type="radio" name="cevap" value="c">""" + "f" +"""
##      <input type="submit" value="2.soru">
##    </form> """)

def ask(sıra):
    sıras = str(sıra)
    @route('/<name>/'+sıras)
    def soru(name):
         return htmlify(body="<p>"+sorular[sıra-1].metin+"</p>"+'<form action="/' + name + '/' + str(sıra+1) + '''a" method="post">
          <input type="radio" name="cevap" value='''+ sorular[sıra-1].şık1.kontrol() + " checked>" + sorular[sıra-1].şık1.metin + '''<br>
          <input type="radio" name="cevap" value='''+ sorular[sıra-1].şık2.kontrol() + ">" + sorular[sıra-1].şık2.metin + '''<br>
          <input type="radio" name="cevap" value='''+ sorular[sıra-1].şık3.kontrol() + ">" + sorular[sıra-1].şık3.metin + '''<br>
          <input type="radio" name="cevap" value='''+ sorular[sıra-1].şık4.kontrol() + ">" + sorular[sıra-1].şık4.metin + '''<br><br>
          <input type="submit" value='->''' + str(sıra+1) +'''.soru'>
        </form> ''')
    @route('/<name>/'+sıras+'a',method="POST")
    def değer(name):
        cevap = request.forms.get('cevap')
        for i in range(len(yarısanlar)):
            if yarısanlar[i] == name:
                yarısanlar_sonuç[i].append(cevap)
                print(yarısanlar_sonuç)
                redirect('/' + name + '/' + sıras)
for i in range(1,3):
    ask(i)

##
##
##@route('/<name>/1')
##def soru_1(name):
##     return htmlify(body="<p>"+sorular[0].metin+"</p>"+'<form action="/' + name + '''/1a" method="post">
##      <input type="radio" name="cevap" value='''+ sorular[0].şık1.kontrol() + " checked>" + sorular[0].şık1.metin + '''<br>
##      <input type="radio" name="cevap" value='''+ sorular[0].şık2.kontrol() + ">" + sorular[0].şık2.metin + '''<br>
##      <input type="radio" name="cevap" value='''+ sorular[0].şık3.kontrol() + ">" + sorular[0].şık3.metin + '''<br>
##      <input type="radio" name="cevap" value='''+ sorular[0].şık4.kontrol() + ">" + sorular[0].şık4.metin + '''<br><br>
##      <input type="submit" value='->2.soru'>
##    </form> ''')
##@route('/<name>/1a',method="POST")
##def değer_1(name):
##    cevap = request.forms.get('cevap')
##    for i in range(len(yarısanlar)):
##        if yarısanlar[i] == name:
##            yarısanlar_sonuç[i].append(cevap)
##            print(yarısanlar_sonuç)
##            redirect('/' + name + '/2')
##    
##@route('/<name>/2')
##def soru_2(name):
##     return htmlify(body="<p>"+sorular[1].metin+"</p>"+'<form action="/' + name + '''/2a" method="post">
##      <input type="radio" name="cevap" value='''+ sorular[1].şık1.kontrol() + " checked>" + sorular[1].şık1.metin + '''<br>
##      <input type="radio" name="cevap" value='''+ sorular[1].şık2.kontrol() + ">" + sorular[1].şık2.metin + '''<br>
##      <input type="radio" name="cevap" value='''+ sorular[1].şık3.kontrol() + ">" + sorular[1].şık3.metin + '''<br>
##      <input type="radio" name="cevap" value='''+ sorular[1].şık4.kontrol() + ">" + sorular[1].şık4.metin + '''<br><br>
##      <input type="submit" value='->3.soru'>
##    </form> ''')
##@route('/<name>/2a',method="POST")
##def değer_2(name):
##    cevap = request.forms.get('cevap')
##    for i in range(len(yarısanlar)):
##        if yarısanlar[i] == name:
##            yarısanlar_sonuç[i].append(cevap)
##            print(yarısanlar_sonuç)
##            redirect('/' + name + '/3')
##
##


##@route('/')
##@route('/hello/<name>')
##def greet(name='Stranger'):
##    return template('Hello {{name}}, how are you?', name=name)    "





application = default_app()
if __name__ == "__main__":
    run(debug=True)


##from bottle import run,get, post, request # or route
##
##@get('/login') # or @route('/login')
##def login():
##    return '''
##        <form action="/login" method="post">
##            Username: <input name="username" type="text" />
##            Password: <input name="password" type="password" />
##            <input value="Login" type="submit" />
##        </form>
##    '''
##def check_login(a,b):
##    return True
##
##@post('/login') # or @route('/login', method='POST')
##def do_login():
##    username = request.forms.get('username')
##    password = request.forms.get('password')
##    if check_login(username, password):
##        return "<p>Your login information was correct.</p>"
##    else:
##        return "<p>Login failed.</p>"
##if __name__ == '__main__':
##    run()
