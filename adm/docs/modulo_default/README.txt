Criando um módulo novo

1 - adicionar entrada no menu, pegar numero sequencial gerado

2 - adicionar pasta do modulo em 
	/sys/$modulo_novo
	/sys/done/$modulo_novo (quando modulo especifico para DONE)

3 - adicionar arquivos
	(item 2)/start.cgi (inicio do modulo)
	(item 2)/edit.cgi (edicao do formulario)
	(item 2)/list.cgi (listagem do modulo)
	(item 2)/submit.cgi (acoes para salvar / excluir cadastros)
	(item 2)/list.cgi (listagem do modulo)
	(item 2)/print.pdf (impressao pdf)
	(item 2)/print.xls (impressao xls)

	/comum/modulos/arquivos.js (adicionar aqui os arquivos puro JS)
	/comum/modulos/arquivos.css (adicionar aqui os arquivos puro CSS)


4 - adicionar entrada em /sys/DPAC/DPAC.js no objeto EOS.core.call.module, exemplo abaixo
                // pagamentos
                pagamento : function(x){                    
                    eos.core.call.exec({
                        action : '/sys/done/pagamento/start.cgi',
                        dload  : 'pagamento',
                        vars   : { },
                        postFunction : function(){
                        }
                    });
                },

5 - adicionar entrada em /sys/DPAC/DLoad.js, exemplo abaixo
		// pagamentos
		pagamento : {
    			module	: "pagamento",
    			JS      : ["/comum/modulos/pagamento.js"],
    			CSS 	: ["/css/modulos/pagamento.css"],
    			PATH	: ["/sys/done/pagamento"]
		}