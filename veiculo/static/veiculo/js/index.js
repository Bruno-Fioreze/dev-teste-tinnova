//utils

const get_elemento_by_termo = (termo) => {
    let xpath = `//span[text()='${termo}']`;
    let elemento = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    return elemento
}

const set_border = (elemento) => {
    elemento.classList.add("border-danger", "remove_azul")
    setTimeout( () => {
        elemento.classList.remove("border-danger", "remove_azul")
    }, 3000)
}


const validate_marca = (elemento) => {
    const value = elemento.value
    if (document.getElementById("autocomplete_marca").querySelectorAll(`option[value='${value}']`).length == 0){
        elemento.focus()
        set_border(elemento)
        return
    }
}

const populate_autocomplete = (marcas) => {
    limpa_conteudo_elemento("autocomplete_marca")
    let datalist = document.getElementById("autocomplete_marca")
    marcas.forEach(function(apelido, key){
        option = document.createElement("option")
        option.setAttribute("data-id", `${apelido["id"]}`)
        option.value = `${apelido["marca"]}`
        datalist.appendChild(option)
    })
}

const limpa_conteudo_elemento = (id_elemento) => {
    id_elemento = document.getElementById(id_elemento) 
    while(id_elemento.firstChild) id_elemento.removeChild(id_elemento.firstChild)
}

const remove_data_grid = (pk) => {
    document.getElementById(`veiculo_${pk}`).remove();
}

const atualiza_grid =(data) => {
    document.getElementById(`veiculo_marca_${data.id}`).innerText = data["marca"]
    document.getElementById(`veiculo_ano_${data.id}`).innerText = data["ano"]
}

const formata_saida_vendido = (vendido) => {
    let saida = ""
    switch (vendido) {
    case '':
        break;
    case 'false':
        saida = 0
        break
    case 'true':
        saida = 1
        break;
    }
    return saida
}

const set_data_atualizar = (data) => {
    document.getElementById("atualiza_veiculo").value = data.veiculo
    document.getElementById("atualiza_marca").value = data.marca
    document.getElementById("atualiza_ano").value = data.ano
    document.getElementById("atualiza_vendido").value = data.vendido
    document.getElementById("atualiza_descricao").value = data.descricao
    document.getElementById("atualiza_pk").value = data.id
}

const validation =  (type="cadastro") => {
    const form = document.getElementById(`form--${type}`)
    let pk = false
    let is_valid = true
    let data = new FormData(form);
    let method = "POST"
    data = Object.fromEntries(data.entries());
    if ( type != "cadastro"  ) {
        pk = document.getElementById("atualiza_pk").value
        method = get_method_update()
        data["vendido"] = formata_saida_vendido(data["vendido"])
    }

    if ( document.getElementById(`${type}_marca`).value == "" || document.getElementById(`${type}_ano`).value == ""  ){
        is_valid = false
    }
    return { data, pk, is_valid, method}
}

const get_method_update = () => {
    let method = "PATCH"
    const inputs = document.getElementById("form--atualiza")
    for (input  of  inputs ){
        if ( input.value == ""){
            method = "PUT"
        }
    }
    return method
}
//is_valid

const create_row = (veiculo) => {
    let listagem = document.getElementsByClassName("sessao--listagem")[0]
    listagem.innerHTML += `
        <div id='veiculo_${veiculo.id}' class='row  border border-rounded pt-1 pb-2'>
            <div id='veiculo_marca_${veiculo.id}' class='col-md-3'>
                ${veiculo.marca}
            </div>
            <div id='veiculo_ano_${veiculo.id}' class='col-md-3'>
                ${veiculo.ano}
            </div>
            <div class='col-md-3'>
                <button class='btn btn-warning text-white' onclick='abrir_modal_atualizar(${veiculo.id})'> Atualizar </button>
            </div>
            <div class='col-md-3'>
                <button class='btn btn-danger' onclick='deletar_veiculo(${veiculo.id})'> Deletar </button>
            </div>
        </div>
    `
}


const create_row_badge = (cls, array) => {
    let listagem = document.getElementsByClassName(cls)[0]
    for ( item of array ){
        let span = document.createElement("span")
        span.innerText = item
        span.classList.add("badge", "bg-success", "p-1", "m-1")
        span.setAttribute("onclick", `get_by_marca_modelo('${item}')`)
        listagem.appendChild(span)
    }
}

const verify_item_array = (array, item) => {
    if ( ! array.includes(item) ){
        array.push( item )
    }
    return array
}

const create_grid = async (data) => {
    let ano = []
    let marca = []
    for( veiculo of data  ){
        ano = await verify_item_array(ano, veiculo.ano)
        marca = await  verify_item_array(marca, veiculo.marca) 
        create_row(veiculo)
    }
    create_row_badge("sessao--filtro--ano", ano)
    create_row_badge("sessao--filtro--marca", marca)
}

const create_grid_search_by_ano_marca =  (data) =>{
    data.map(
        (veiculo) => {
            create_row(veiculo)
        }
    )
}

//requests

function request (url, settings) {
    url = new URL(url)
    return fetch(url, settings)
}

//veículo
const get_all_veiculo = async () => {
    limpa_conteudo_elemento("listagem") 
    limpa_conteudo_elemento("filtro--ano")
    limpa_conteudo_elemento("filtro--marca")
    
    const location = `${window.location.protocol}${window.location.host}`
    const url = `${location}/veiculo/`

    const settings = {
        "method": "GET",
    }
    alerta_carregando()
    
    const response_code = {
        200: success,
        404: not_found,
        422: error_parameters,
        500: error_internal,
        424: error_function_dependency
    }

    try {
        const response = await request(url, settings)
        const dados = await response.json()
        swal.close()
        if(dados.length == 0){
            get_swal_alert(["Atenção !", "Nenhum registro encontrado.", "info"])
            return
        }
        response_code[response.status](dados, create_grid)
    } catch (e){
        console.log(e)
        swal.close()
        get_swal_alert(["Erro !", "Ocorreu um erro inesperado.", "error"])
    }
}

const cadastrar_veiculo = async () => {

    const validator = validation('cadastro')
    
    if ( ! validator.is_valid ){
        get_swal_alert(["Atenção !", "Preencha os campos Marca e Ano.", "info"])
        return
    }
        
    const location = `${window.location.protocol}${window.location.host}`
    const url = `${location}/veiculo/`

    let myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    let raw = JSON.stringify(validator.data);

    let requestOptions = {
        method: validator.method, 
        headers: myHeaders,
        body: raw,
    };

    alerta_carregando()
    
    const response_code = {
        200: success,
        404: not_found,
        422: error_parameters,
        500: error_internal,
        424: error_function_dependency
    }

    try {
        const response = await request(url, requestOptions)
        const dados = await response.json()
        swal.close()
        response_code[response.status](dados, create_row)
        // Eu não consegui fazer no update por falta de tempo.
        if ( get_elemento_by_termo(validator.data.marca) == null){
            create_row(dados)
            let marca = [ dados.marca ]
            create_row_badge("sessao--filtro--marca", marca)
        }
        if ( get_elemento_by_termo(validator.data.ano) == null){
            let ano = [ dados.ano ]
            create_row_badge("sessao--filtro--ano", ano)
        }
    } catch (e){
        console.log(e)
        swal.close()
        get_swal_alert(["Erro !", "Ocorreu um erro inesperado.", "error"])
    }
}

const abrir_modal_atualizar = async  (pk) => {
    let modal_atualizar = new bootstrap.Modal(document.getElementById('md_atualiza_veiculo'), {
        keyboard: false
    })
    
    const location = `${window.location.protocol}${window.location.host}`
    const url = `${location}/veiculo/${pk}/?by_pk=true`

    const settings = {
        "method": "GET",
    }
    alerta_carregando()
    
    const response_code = {
        200: success,
        404: not_found,
        422: error_parameters,
        500: error_internal,
        424: error_function_dependency
    }

    try {
        const response = await request(url, settings)
        const dados = await response.json()
        swal.close()
        dados["atualiza"] = true
        response_code[response.status](dados, set_data_atualizar)
        modal_atualizar.toggle()
    } catch (e){
        console.log(e)
        swal.close()
        get_swal_alert(["Erro !", "Ocorreu um erro inesperado.", "error"])
    }
}


const atualizar_veiculo = async () => {
    const validator = validation('atualiza')

    if ( ! validator.is_valid ){
        get_swal_alert(["Atenção !", "Preencha os campos Marca e Ano.", "info"])
        return
    }

    const location = `${window.location.protocol}${window.location.host}`
    const url = `${location}/veiculo/${validator.pk}/`

    let myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    let raw = JSON.stringify(validator.data);

    let requestOptions = {
        method: validator.method, 
        headers: myHeaders,
        body: raw,
    };

    alerta_carregando()
    
    const response_code = {
        200: success,
        404: not_found,
        422: error_parameters,
        500: error_internal,
        424: error_function_dependency
    }

    try {
        const response = await request(url, requestOptions)
        const dados = await response.json()
        swal.close()
        dados["marca"] = document.getElementById('atualiza_marca').value
        dados["ano"] = document.getElementById('atualiza_ano').value
        dados["id"] = validator.pk
        response_code[response.status](dados, atualiza_grid)
    } catch (e){
        console.log(e)
        swal.close()
        get_swal_alert(["Erro !", "Ocorreu um erro inesperado.", "error"])
    }
}

const deletar_veiculo = async  (pk) => {
    const location = `${window.location.protocol}${window.location.host}`
    const url = `${location}/veiculo/${pk}/`

    const settings = {
        "method": "DELETE",
    }
    alerta_carregando()
    
    const response_code = {
        200: success,
        404: not_found,
        422: error_parameters,
        500: error_internal,
        424: error_function_dependency
    }

    try {
        const response = await request(url, settings)
        const dados = await response.json()
        swal.close()
        response_code[response.status](pk, remove_data_grid)
    } catch (e){
        console.log(e)
        swal.close()
        get_swal_alert(["Erro !", "Ocorreu um erro inesperado.", "error"])
    }
}

const get_by_marca_modelo = async  (termo) => {
    limpa_conteudo_elemento("listagem")
    const location = `${window.location.protocol}${window.location.host}`
    const url = `${location}/veiculo/${termo}/`

    const settings = {
        "method": "GET",
    }
    alerta_carregando()
    
    const response_code = {
        200: success,
        404: not_found,
        422: error_parameters,
        500: error_internal,
        424: error_function_dependency
    }

    try {
        const response = await request(url, settings)
        const dados = await response.json()
        swal.close()
        response_code[response.status](dados, create_grid_search_by_ano_marca)
    } catch (e){
        console.log(e)
        swal.close()
        get_swal_alert(["Erro !", "Ocorreu um erro inesperado.", "error"])
    }
}


//marca
const get_all_marca = async () => {
        
    const location = `${window.location.protocol}${window.location.host}`
    const url = `${location}/marca/`

    const settings = {
        "method": "GET",
    }
    alerta_carregando()
    
    const response_code = {
        200: success,
        404: not_found,
        422: error_parameters,
        500: error_internal,
        424: error_function_dependency
    }

    try {
        const response = await request(url, settings)
        const dados = await response.json()
        swal.close()
        response_code[response.status](dados, populate_autocomplete)
    } catch (e){
        console.log(e)
        swal.close()
        get_swal_alert(["Erro !", "Ocorreu um erro inesperado.", "error"])
    }
}

// alerts response
const get_swal_alert = ([title, text, icon] = par) => {
    Swal.fire({
        title: title,
        text: text,
        icon: icon,
    })
}

const alerta_processando = () => {
    Swal.fire({
        title: 'Processando!',
        icon : "info",
        html: 'extraindo informações..',
            didOpen: () => {
                swal.showLoading()
            }
   })
}

function alerta_carregando(){

    Swal.fire({
        title: 'Carregando!',
        icon : "info",
        html: 'Buscando informações solicitadas..',
            didOpen: () => {
                swal.showLoading()
            }
   })

}

const success = (dados, metodo) => {
    metodo(dados)
}

const not_found = () => {
    get_swal_alert(["Atenção !", "Nada Encontrado.", "warning"])
}

const error_parameters = () => {
    get_swal_alert(["Atenção !", "Parâmetros passados de forma incorreta.", "info"])
}

const error_internal = () => {
    get_swal_alert(["Erro !", "Ocorreu um erro interno no servidor.", "error"])
}

const error_function_dependency = () => {
    get_swal_alert(["Erro !", "O Processamento não foi realizado, pois uma função interna falhou.", "error"])
}

//ações iniciais
const acoes_iniciais = () => {
    get_all_veiculo()
    get_all_marca()
}

window.addEventListener("load", acoes_iniciais)

