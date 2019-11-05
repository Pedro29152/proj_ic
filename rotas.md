<h1>TELAS</h1>
<hr>
<h2>/index</h2> - <h3>tela inicial</h3>

<h2>/projetos/buscar</h2> - <h3>tela de busca</h3>

<h1>CURSOS</h1>
<hr>

<h2>/cursos/count [GET]</h2> - <h3>quantidade de cursos cadastrados </h3>

<h2>/cursos/buscar [GET]</h2> - <h3>listagem de cursos cadastrados</h3>

<h2>/cursos/cadastrar [POST]</h2> - cadastro de cursos
 ->parametros(passados pelo corpo do formulario):
   -->nomeCurso, abreviacao

<h1>USUARIOS</h1>
<hr>

<h2>/usuarios/count [GET]</h2> - <h3>quantidade de usuarios cadastrados</h3>

<h2>/usuarios/logout [POST, GET]</h2> - <h3>logout do usuario logado</h3>

<h2>/usuarios/login [POST]</h2> - <h3>login de usuarios</h3>
 ->parametros(passados pelo corpo do formulario):
   --username, password, [next_page]

<h2>/usuarios/cadastrar [POST]</h2> - <h3>cadastro de novos usuarios</h3>
 ->parametros(passados pelo corpo do formulario):
   --username, tipoUsuario, gerenciador, password, r_password

<h2>/usuarios/buscar [GET]</h2> - listagem de usuarios cadastrados</h3>
 ->parametros(passados por parametro de requisicao):
   --[nomeUsuario]

<h1>PROJETOS</h1>
<hr>

<h2>/projetos/count [GET]</h2> - <h3>quantidade de projetos cadastrados</h3>

<h2>/projetos/cadastrar [POST] - <h3>cadastro de projetos</h3>
 ->parametros(passados pelo corpo do formulario):
   --titulo, nomeOrientador, raOrientador, descricao, 
	dataAvaliacao, curso, file{arquivo}, 
	autor, ra_autor, [autor_'1-3'], [ra_autor_'1-3'],
	palavra_chave, [palavra_chave_'1-2']

<h2>/projetos/buscar/<tipo> [GET]</h2> - <h3>listagem de projetos por tipo</h3>
 ->tipo: tipo de pesquisa, passado pela url
	(podendo ser: titulo, curso, descricao, orientador, autor e palavrasChave)
 ->parametros(passados por parametro de requisicao):
   -->[query], [ordem], [crescente]
	-->query: valor de pesquisa
	-->ordem: 0 - 6 define se sera ordenado de acordo com, nada, likes, deslikes, 
		numVisitas, numDownloads, dataAvaliacao e dataEnvio, respectivamente
	-->crescente: se igual a "0" sera ordenado por ordem decrescente, caso contrario,
		sera ordenado de maneira crescente

<h2>/projetos/buscar/ranking [GET]</h2> - <h3>listagem do ranking de projetos </h3>
 ->parametros(passados por parametro de requisicao):
   -->[query], [tipo], [ordem]
	-->query: valor de pesquisa
	-->tipo: likes, deslikes, numVisitas, numDownloads e notaProjeto
	-->ordem: '' ou 'desc'

<h2>/projetos/download_file/<filename></h2> [GET] - <h3>download do arquivo do projeto</h3>
 - filename: nome do arquivo a ser baixado, passado pela url

<h1>GERENCIADORES</h1>
<hr>

<h2>/gerenciadores/count [GET]</h2> - <h3>quantidade de gerenciadores cadastrados</h3>

<h2>/gerenciadores/buscar [GET]</h2> - <h3>lsitagem de gerenciadores cadastrados</h3>
 ->parametros(passados por parametro de requisicao):
   -->[nomeGerenciador]

<h2>/gerenciadores/cadastrar [POST]</h2> - <h3>cadastro de gerenciadores</h3>
 ->parametros(passados pelo corpo do formulario):
   --cpfGerenciador, instituicao, nomeGerenciador e emailGerenciador