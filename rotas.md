<h1>TELAS</h1>

<h2>/index</h2>
<h3>tela inicial</h3>

<h2>/projetos/buscar</h2>
<h3>tela de busca</h3>

<h1>CURSOS</h1>

<h2>/cursos/count [GET]</h2>
<h3>quantidade de cursos cadastrados </h3>

<h2>/cursos/buscar [GET]</h2>
<h3>listagem de cursos cadastrados</h3>

<h2>/cursos/cadastrar [POST]</h2>
<h3>cadastro de cursos</h3>
<p>->parametros(passados pelo corpo do formulario):</p>
<p>-->nomeCurso, abreviacao</p>

<h1>USUARIOS</h1>

<h2>/usuarios/count [GET]</h2>
<h3>quantidade de usuarios cadastrados</h3>

<h2>/usuarios/logout [POST, GET]</h2>
<h3>logout do usuario logado</h3>

<h2>/usuarios/login [POST]</h2>
<h3>login de usuarios</h3>
<p>->parametros(passados pelo corpo do formulario):</p>
<p>-->username, password, [next_page]</p>

<h2>/usuarios/cadastrar [POST]</h2>
<h3>cadastro de novos usuarios</h3>
<p>->parametros(passados pelo corpo do formulario):</p>
<p>-->username, tipoUsuario, gerenciador, password, r_password</p>

<h2>/usuarios/buscar [GET]</h2>
<h3>listagem de usuarios cadastrados</h3>
<p>->parametros(passados por parametro de requisicao):</p>
<p>-->[nomeUsuario]</p>

<h1>PROJETOS</h1>

<h2>/projetos/count [GET]</h2>
<h3>quantidade de projetos cadastrados</h3>

<h2>/projetos/cadastrar [POST]</h2>
<h3>cadastro de projetos</h3>
<p>->parametros(passados pelo corpo do formulario):</p>
<p>--titulo, nomeOrientador, raOrientador, descricao, 
	dataAvaliacao, curso, file{arquivo}, 
	autor, ra_autor, [autor_'1-3'], [ra_autor_'1-3'],
	palavra_chave, [palavra_chave_'1-2']
</p>

<h2>/projetos/buscar/<tipo> [GET]</h2>
<h3>listagem de projetos por tipo</h3>
<p>->tipo: tipo de pesquisa, passado pela url
	(podendo ser: titulo, curso, descricao, orientador, autor e palavrasChave)
</p>
<p>->parametros(passados por parametro de requisicao):
</p>
<p>-->[query], [ordem], [crescente]
</p>
<p>-->query: valor de pesquisa
</p>
<p>-->ordem: 0 - 6 define se sera ordenado de acordo com, nada, likes, deslikes, 
	numVisitas, numDownloads, dataAvaliacao e dataEnvio, respectivamente
</p>
<p>-->crescente: se igual a "0" sera ordenado por ordem decrescente, caso contrario,
	sera ordenado de maneira crescente
</p>

<h2>/projetos/buscar/ranking [GET]</h2>
<h3>listagem do ranking de projetos</h3>
<p>->parametros(passados por parametro de requisicao):</p>
<p>-->[query], [tipo], [ordem]</p>
<p>-->query: valor de pesquisa</p>
<p>-->tipo: likes, deslikes, numVisitas, numDownloads e notaProjeto</p>
<p>-->ordem: '' ou 'desc'</p>

<h2>/projetos/download_file/(filename) [GET]</h2>
<h3>download do arquivo do projeto</h3>
<p>- filename: nome do arquivo a ser baixado, passado pela url</p>

<h1>GERENCIADORES</h1>

<h2>/gerenciadores/count [GET]</h2>
<h3>quantidade de gerenciadores cadastrados</h3>

<h2>/gerenciadores/buscar [GET]</h2>
<h3>lsitagem de gerenciadores cadastrados</h3>
<p>->parametros(passados por parametro de requisicao):</p>
<p>-->[nomeGerenciador]</p>

<h2>/gerenciadores/cadastrar [POST]</h2>
<h3>cadastro de gerenciadores</h3>
<p>->parametros(passados pelo corpo do formulario):</p>
<p>--cpfGerenciador, instituicao, nomeGerenciador e emailGerenciador</p>