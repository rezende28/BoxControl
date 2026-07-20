// Confirma antes de excluir uma caixa

function confirmarExclusao(){

    return confirm(
        "Tem certeza que deseja excluir esta caixa?"
    );

}



// Selecionar todas as caixas prontas

function selecionarTodas(){

    let caixas = document.querySelectorAll(
        'input[name="caixas"]'
    );


    caixas.forEach(function(caixa){

        caixa.checked = true;

    });

}