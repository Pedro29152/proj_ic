from biblioteca.cls.proj.proj_bd import (busca_projeto_curso, busca_projeto_descricao, \
    busca_projeto_orientador, busca_projeto_titulo, grava_projeto)

def upload_arquivo(req, nomeGer):
    titulo = req.form['titulo']
    nomeOrientador = req.form['nomeOrientador']
    descricao = req.form['descricao']
    notaProj = req.form['notaProj']
    dataAvaliacao = req.form['dataAvaliacao']
    curso = req.form['curso']
    file = req.files['file']

    codCurso =  curso_bd.get_codCurso(curso)

    rand = hex(randint(0x100000,0xffffff))
    data = datetime.datetime.now()
    data = data.date()

    filename = secure_filename(file.filename)
    nfilename = filename.rsplit('.',2)[0]

    if len(curso) >= 10:
        curso = curso_bd.get_abbr_curso(curso)

    tituloarq = titulo
    if len(titulo) > 41:
        aux = titulo.split()
        tituloarq = ""
        for div in aux:
            tituloarq += div[0]


    filename = filename.replace(
        nfilename, 
        curso.upper().replace(' ', '-') + '-' +
        tituloarq.upper().replace(' ', '-') + '-' + 
        str(data) + "-" + str(rand).upper()
    )
    
    codGer = gerenciador_bd.get_codGer_usr(nomeGer)
    
    proj_bd.grava_projeto(
        titulo, nomeOrientador, descricao,
        filename, notaProj, dataAvaliacao, 
        codGer, codCurso
    )

    file.save(
        os.path.join(
            app.config['UPLOAD_FOLDER'], 
            filename
        )
    )
    return redirect(url_for('upload_file', filename=filename))


def busca_curso(req = None):
    try:
        curso = req.form['query']
    except:
        curso = ''

    try:
        ordem = int(req.form['ordem'])
    except:
        ordem = 0

    cres = True
    try:
        if(req.form['crescente'] == '0'):
            cres = False
    except:
        cres = True

    return busca_projeto_curso(curso, ordem, cres)

def busca_descricao(req = None):
    
    try:
        desc = req.form['query']
    except:
        desc = ''

    try:
        ordem = int(req.form['ordem'])
    except:
        ordem = 0

    cres = True
    try:
        if(req.form['crescente'] == '0'):
            cres = False
    except:
        cres = True

    return busca_projeto_descricao(desc, ordem, cres)
    

def busca_titulo(req = None):

    try:
        titulo = req.form['query']
    except:
        titulo = ''

    try:
        ordem = int(req.form['ordem'])
    except:
        ordem = 0

    cres = True
    try:
        if(req.form['crescente'] == '0'):
            cres = False
    except:
        cres = True

    return busca_projeto_titulo(titulo, ordem, cres)
    
def busca_orientador(req = None):

    try:
        orientador = req.form['query']
    except:
        orientador = ''

    try:
        ordem = int(req.form['ordem'])
    except:
        ordem = 0

    cres = True
    try:
        if(req.form['crescente'] == '0'):
            cres = False
    except:
        cres = True

    return busca_projeto_orientador(orientador, ordem, cres)
    