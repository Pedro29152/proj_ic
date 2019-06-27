var idContadorAutor = 0
var idContadorPalavra = 0

function adicionaPalavaChave(){
    if(idContadorPalavra > 9)
        return

    idContadorPalavra++
    let idPalavra = `palavra_chave_${ idContadorPalavra }`
    let idDiv = `palavra_chave_div_${ idContadorPalavra }`

    let tituloPalavra = document.createElement('label')
    tituloPalavra.innerHTML = `Palavra-chave extra ${ idContadorPalavra }:`

    let div = document.createElement('div')
    div.id = idDiv
    
    let legend = document.createElement('legend')
    legend.innerHTML = `<h3>Palavra-chave ${ idContadorPalavra + 1 }</h3>`

    let fieldset = document.createElement('fieldset')
    fieldset.append(legend)
    
    let inputPalavra = document.createElement('input')
    inputPalavra.type = 'text'
    inputPalavra.placeholder = 'Digite a palavra-chave'
    inputPalavra.id = idPalavra
    inputPalavra.required = true
    inputPalavra.name = idPalavra

    let btnRemove = document.createElement('input')
    btnRemove.id = 'btnRemovePala'
    btnRemove.type = 'button'
    btnRemove.value = 'Remover'
    btnRemove.onclick = function(){
        document.getElementById(`palavra_chave_div_${ idContadorPalavra }`).remove()
        idContadorPalavra--
    }

    let container = document.getElementById('imendaHTMLpalavra')
    fieldset.append(tituloPalavra, inputPalavra)
    fieldset.innerHTML += '<br>'
    fieldset.append(btnRemove)
    div.append(fieldset)
    container.append(div)
}

function adicionaAutor(){
    if(idContadorAutor > 3)
        return

    idContadorAutor++
    let idNome = `autor_${ idContadorAutor }`
    let idRa = `ra_autor_${ idContadorAutor }`
    let idDiv = `autor_div_${ idContadorAutor }`

    let tituloNome = document.createElement('label')
    tituloNome.innerHTML = `Autor extra ${ idContadorAutor }:`

    let tituloRa = document.createElement('label')
    tituloRa.innerHTML = `Ra extra ${ idContadorAutor }:`

    let div = document.createElement('div')
    div.id = idDiv
    
    let fieldset = document.createElement('fieldset')
    let legend = document.createElement('legend')
    legend.innerHTML = `<h3>Autor ${ idContadorAutor + 1 }</h3>`
    fieldset.append(legend)
    
    let inputNome = document.createElement('input')
    inputNome.type = 'text'
    inputNome.placeholder = 'Digite o nome do autor'
    inputNome.id = idNome
    inputNome.required = true
    inputNome.name = idNome

    let inputRa = document.createElement('input')
    inputRa.type = 'text'
    inputRa.placeholder = 'Digite o RA'
    inputRa.id = idRa
    inputRa.required = true
    inputRa.name = idRa
    inputRa.maxLength = 13

    let btnRemove = document.createElement('input')
    btnRemove.id = 'btnRemoveAut'
    btnRemove.type = 'button'
    btnRemove.value = 'Remover'
    btnRemove.onclick = function(){
        document.getElementById(`autor_div_${ idContadorAutor }`).remove()
        idContadorAutor--
    }

    let container = document.getElementById('imendaHTMLautor')
    fieldset.append(tituloNome, inputNome)
    fieldset.innerHTML += '<br>'
    fieldset.append(tituloRa, inputRa)
    fieldset.innerHTML += '<br>'
    fieldset.append(btnRemove)
    div.append(fieldset)
    container.append(div)
}

function remove(id){
    document.getElementById(id).remove()
}