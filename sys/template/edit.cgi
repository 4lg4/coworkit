#!/usr/bin/perl

$nacess = "10";
require "../cfg/init.pl";

# carregamento de variaveis
$ID  = &get('ID');
$COD = &get('COD');

# header padrao do documento
print $query->header({charset=>utf8});

print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	
<script language='JavaScript'>

    /* 
    *   Exemplo Comentario
    *       Este e o exemplo de um comentario complexo
    *       com mais de uma linha e com diversas explicacoes
    */
    // esse eh um exemplo de comentario simples usado na boa pratica ao final da linha
    


    /*
    *   Carregamento de libs essencias para o funcionamento do modulo
    *       verificar em: 
    *           /comum/DPAC/DLoad.js
    *         
    *   EOS core v3 nao usa o carregamento das libs nesse local, mas a configuracao do modulo se mantem
    *       verificar em:
    *           /comum/DPAC/DPAC.js
    *           EOS.app -> core.call.module
    *
    */
    // DLoad("chamado");
    
    
    
    /* 
    *   OBJETOS necessarios para o funcionamento do modulo
    *
    *   o exemplo a seguir e do objeto empresa que manipula dados da empresa
    */
    
    /*
    *   Empresa
    *       objeto empresa 
    */
    function Empresa()
    	{       
    	/* enderecos empresa */
    	this.endereco = function(end){
    		
            /*
            * executa funcoes para o carregamento do endereco especifico da empresa que esta sendo manipulada
            */

            /*
            *   nesse caso uso DAction Ajax para fazer um carregamento no arquivo especicado
            *   envio variaveis especificas para um retorno apropriado do conteudo
            *   nao envio o formulario inteiro pois eh desnecessario usando serializeForm : false
            */
    		\$.DActionAjax({
    			action        : "empresa_endereco.cgi",
    			req           : "empresa="+\$("#cliente").val()+"&end="+end,
    			loader        : \$("#cliente_container"),
    			serializeForm : false,
                postFunction  : function(){
                    /*
                    *   executa acoes apos finalizacao do carregamento do arquivo ajax,
                    *   mesmo com erro essa funcao eh startada 
                    */
                }
    		});
    	};
		
    	/* area	*/
    	this.area = function(a){
            /*
            *   mesma ideia de codigo aplicado a this.endereco
            */
    	}
		
    	/* planos	*/
    	this.planos = function(a){
            /*
            *   mesma ideia de codigo aplicado a this.endereco
            */
    	}
    };
	
    /* 
    *   Chamado
    *       Objeto
    */
    function Chamado(){
    	/* reativar chamado */
    	this.reativar = function(){
            /*
            *   mesma ideia de codigo aplicado a this.endereco
            */
    	};
        
    	/*  emails */
    	this.emails = function(){
            /*
            *   mesma ideia de codigo aplicado a this.endereco
            */
        };
        
    	/* finalizar chamado */
    	this.finalizar = function(){
            /*
            *   mesma ideia de codigo aplicado a this.endereco
            */
            
            /*
            *   Exemplo de uso do DDialog
            *       alerta / erro / confirmacao
            *
            *       nesse caso usei como confirmacao
            *           ao clicar em SIM executa um ajax com o arquivo 
            *           ao clicar em NAO retorna true e nao executa nada
            */
            \$.DDialog({
                type    : "confirm",
                message : "Deseja finalizar o ticket atual ?",
                btnYes  : function(){
                    \$.DActionAjax({ 
                        action:"edit_submit_finalizar.cgi",
                        req: "&COD="+\$("#COD").val()
                    });
                },
                btnNo   : function(){
                	return true;
                }
            });
        };
            
    	/*
        *   acoes - lancamentos
        *
        *       nesse exemplo temos um objeto mais complexo com "grupos" e "subgrupos"
        */
    	this.acoes = {

            /*
            *   carrega acoes
            */
            load : function(){
                /*
                *   mesma ideia de codigo aplicado a this.endereco
                */
            },
            
            /*
            *   lista acoes
            */
            list : function(ca){
                /*
                *   mesma ideia de codigo aplicado a this.endereco
                */
                
                /*
                *   neste caso inicio a manipulacao de templates para deixar todo o processamento do lado do cliente
                *   o funcionamento eh bem simples.
                *       
                *   No final do documento tera a sessao de templates que nada mais sao que <DIVs> com display:none
                *
                */
                
                // template 
                var template = \$('.eos_template_chamado_acoes').clone().removeClass('eos_template_chamado_acoes').show();
                
            },
            
            /*
            *   new
            *       adiciona nova acao
            */
            new : function(i){
                
                /*
                *   mesma ideia de codigo aplicado a this.endereco
                */
                
                
                /*
                *   nesse exemplo eu clono o template e atraves de classes "chaves" manipulo os objetos 
                *   genericos dentro de cada template
                */
                
                // cria novo
                var t = \$('.eos_template_chamado_acoes').clone().removeClass('eos_template_chamado_acoes').show().appendTo('#chamado_acoes');
                
                var acoes = [];
                                                
                // data do item
                acoes["data_execucao"] = t.find(".acao_item_data_execucao input")
                    .prop({
                        name        : "acao_data_execucao",
                        type        : "text",
                        placeholder : "Data execução",
                    })
                    .fieldDateTime({type:"date-time"}); 
                    


                // sigiloso
                acoes["sigiloso"] = t.find(".acao_item_cfg_sigiloso input")
                    .prop({
                        name  : "acao_sigiloso",
                        id    : "sigiloso_"+eos.tools.idGen(),
                        type  : "checkbox"
                    })
                    .fieldCheckbox({
                        label      : "sigiloso ?",
                        labelCheck : "sigiloso !",
                        onCheck    : function(x){ 
                            // se sigiloso esconde box externo
                            x.parents(".DTouchBoxes").find(".acao_item_executor_descrp")
                                .hide()
                                .find("textarea") // clear text content
                                    .val("");
                                    
                            x.parents(".DTouchBoxes").find(".acao_item_descrp").addClass("acao_item_descrp_full"); // full internal box class
                        },
                        onUncheck  : function(x){ 
                            x.parents(".DTouchBoxes").find(".acao_item_executor_descrp").show(); // mostra box desrp externo                                    
                            x.parents(".DTouchBoxes").find(".acao_item_descrp").removeClass("acao_item_descrp_full"); // remove full internal box class
                        }
                    });
                    

                // t.DTouchBoxes();
                t.DTouchBoxes({ 
                    minimize : true
                });
            }
    	};
			
    	/* 
        *   lista chamados 		
        */
    	this.list = function(){
			
    		// executa arquivo
    		\$.DActionAjax({
    			action: "edit_list.cgi",
    			// req: "COD="+\$("#COD").val(),
    			loader: "chamados_list_container",
    			serializeForm: false
    		});	
    	};
		
    	/* edita chamado */
    	this.edit = function(c){
            /*
            *   mesma ideia de codigo aplicado a this.endereco
            */
    	};
    }



/* 
*   Buttons Actions
*       substituir no core V3 usar EOS.app -> eos.menu.action (ver em DPAC.js)
*/
    
/* Cancelar	*/
function DActionCancel(){
    /*
    *   code 
    */
}
	
/* Editar */
function DActionEdit(){
    /*
    *   code 
    */
}

// novo / incluir
function DActionAdd(){
    /*
    *   code 
    */
}
	
// salvar, funcoes
function DActionSave(){
    /*
    *   code 
    */
}


/*
*   Form
*       Objeto formulario baseado no core EOS v3 usar essa metodologia para melhor consistencia e escalabilidade do sistema
*/
function Form(){
	
	/* inicializa formulario */
	this.initialize = function() {
        /*
        *   code 
        */
        
        
        
        /*
        *   Nesse caso uso o DTouchPages para criar paginas deslizantes
        *
        *   *** note que precisamos melhorar o codigo pois uso o comando destroy para remover o botao de pesquisar adicionado
        *       pela pesquisa na pagina da direita
        *
        *   onCreate, essa parte eh essencial para o carregamento correto do formulario pois carrega todos objeto encadeadamente
        *       conforme exemplo usado abaixo
        *
        *   pageRight, pageCenter, pageLeft: usado para definir qual objeto sera a pagina correta
        */
		
		// cria pagina touch padrao
		\$("#DTouchPages_chamado").DTouchPages({
            pageChange: "center",
			postFunctionCenter : function() {
                eos.menu.action.appear(); // mostra menu action
                
                /*
                *
                *   DTouchRadio_search_adv
                *
                *   Remove botao de pesquisa avancada
                *       Ver melhor solucao para remocao do botao de pesquisa avancada do dtouch radio
                *
                */
                eos.menu.action.destroy("icon_DTouchRadio_search_adv");
            },
			postFunctionRight : function() {
                /*
                *   code 
                */
            },
			onCreate : function() {
                
				// gera boxes
				\$("#area_container").DTouchBoxes({         // area
					title:"Área"
				});
				\$("#cliente_container").DTouchBoxes();     // cliente
                
				// esconde boxes
				\$("#area_container").DTouchBoxes("hide");
				\$("#plano_container").DTouchBoxes("hide");
                
                
				// cliente, inicializa campo
				\$("#cliente").fieldAutoComplete({ 
					type         : "empresa",
					postFunction : function(x)
						{
						empresa.endereco();
                        \$("#plano").DTouchRadio("reset","hard"); // zera planos
                        \$("#plano_container").DTouchBoxes("hide"); // esconde planos
						empresa.area();
						chamado.prioridade();
						},
					onReset: function()
						{
						\$("#cliente_endereco").DTouchRadio("reset","hard");
						},
					placeholder: "Selecione o Cliente"
				});
                
				/* 
                *   carrega formulario com dados vindo do banco de dados
                *
                *   manter ainda para funcionamento com core V1 e V2
                */
				DActionEditDB();
			},
			// pageLeft: false, // \$("#DTouchPages_chamado_left"),
			pageRight: \$("#DTouchPages_chamado_right"),
			pageCenter: \$("#DTouchPages_chamado_center")
			});
				
            
        /*  
        *   Campos, foi adicionado ao core v3 a padronizacao dos campos usados no sistema se localizando em 
        *   DPAC.js -> EOS.app  eos.template.field.text(\$(this));
        *  
        *   conforme o exemplo abaixo inicializo todos os campos text que ainda n foram inicializados
        *   ver melhorias e automacoes para esse codigo
        */ 
        \$("#CAD input[type=text]:not(.DFields)").each(function(){
            eos.template.field.text(\$(this));
        });
           
           
        /*
        *   nesse exemplo crio um touch radio apartir da tabela 
        */         
    	\$("#prioridade").DTouchRadio({ 
    		table : "tkt_prioridade"
    	});
        
        /*
        *   aqui uso para controlar se formulario esta entrando em modo de edicao
        */    
    	if("$COD" != "") {
            \$('#COD').val("$COD");
    		chamado.edit();
    	}
        
        this.menu.initialize(); // inicia menu
	};
    
	/*
    *   reseta formulario
    */
	this.reset = function() {
        /*
        *    Recarega o modulo para zerar o formulario....
        */    
        eos.core.call.module.tkt(); // carrega modulo tkt
        return true;  
    };
		
	/*
    *   salva formulario
    */
	this.save = function(){
        
        /* 
        *   testa campos obrigatorios baseado no tipo de lancamento
        *   monta string para enviar ao arquivo e executa ajax
        */      
                  
		// testa campos obrigatorios
		if(!\$("#cliente_endereco").DTouchRadio("value") || !\$("#area").DTouchRadio("value") || !\$("#prioridade").DTouchRadio("value") || !\$("#solicitante").val() || !\$("#descrp").val() || !\$("#cliente").val() ) {
			var msg  = "Campos obrigatórios devem ser preenchidos: <ul>";
				msg += "<li> Endereço do cliente </li>";
				msg += "<li> Prioridade </li>";
				msg += "<li> Solicitante </li>";
			
				if(\$("#plano_container").is(":visible"))
					msg += "<li> Plano </li>";
				
				msg += "<li> Problema </li> </ul>";
			
			\$.DDialog({message:msg});
			return false;
		}

		// endereco selecionado
		var req  = "&empresa_endereco="+\$("#cliente_endereco").DTouchRadio("value");
            req += "&acao_new="+\$(".acao_codigo_new").length;
            req += "&acao_descrp_publico_new="+\$("#acao_descrp_publico_new").val();
            req += "&acao_descrp_interno_new="+\$("#acao_descrp_interno_new").val();
            req += "&acao_executor_new="+\$("#acao_executor_new").val();
            req += "&acao_tipo_new="+\$("#acao_tipo_new").val();
            req += "&acao_tempo_new="+\$("#acao_tempo_new").val();
            req += "&acao_sigiloso_new="+\$(".acao_sigiloso_new").fieldCheckbox("isChecked");
         
            
		\$.DActionAjax({
			action: "edit_submit.cgi",
			req: req
		});
	};
    
    
    /*
    *   Menu
    *       controle do menu do formulario
    */
    this.menu = {
        // inicia
        initialize : function(){
            eos.menu.action.show('icon_save');
            
            /*
            *   icones edicao
            * 
            *   nesse exemplo demonstro como criar botoes on the fly usando o core V3 EOS.app
            *       melhor handle de click e possibilidade de escalar
            */
            eos.menu.action.new({ // encaminhar
                id       : "icon_tkt_action_encaminhar",
                title    : "ação",
                subtitle : "encaminhar",
                group    : "icon_tkt_action",
                click    : function(){
                    chamado.acoes.new('encaminhar'); // novo box acao
                    \$("#icon_tkt_action_executar, #icon_tkt_action_encaminhar").remove(); // remove icones
                    // chamado_formulario.isChange(true); // tranca formulario
                    
                    eos.menu.action.hide("icon_tkt_action_finalizar");
                    eos.menu.action.show(["icon_save","icon_insert"]);
                    
                    // posiciona visualizacao da acao
                    \$("#DTouchPages_chamado_center").scrollTop(\$("#DTouchPages_chamado_center").height()+200);
                    \$("#acao_descrp_interno_new").focus();
                }
            });
            
            /*
            *   icone finalizacao
            */
            eos.menu.action.new({ 
                id       : "icon_tkt_action_finalizar",
                title    : "finalizar",
                subtitle : "",
                group    : "icon_tkt_action",
                click    : function(){
                    chamado.finalizar(); // finalizar
                }
            });
            
            // esconde icones 
            eos.menu.action.hide(["icon_tkt_action_encaminhar","icon_tkt_action_executar","icon_tkt_action_finalizar"]);
        },
    }
}

/* 
*   quando o documento esta pronto 
*
*   colocar aqui somente inicializacoes para melhor carregamento de objetos em tempo correto
*/
\$(document).ready(function(){
    /* 
    *   gerar caches
    *   nesse exemplo demonstro o uso dos caches para tabelas simples que nao sao alteradas
    *   uma vez criado o cache somente sera recriado ao atualizar o eos
    *   melhorar essa ideia.... sugestao: quando validar usuario e senha setar caches que deverao ser limpos
    */
    eos.core.getList("tkt_acao_tipo"); // tipo da acao
    eos.core.getList("tkt_prioridade"); // prioridade do ticket
    
    /*
    *   inicializa objetos do modulo
    */
	empresa = new Empresa(); // inicia objeto empresa
	chamado = new Chamado(); // inicia objeto chamado
    
	chamado_formulario = new Form(); // inicia objeto formulario
	chamado_formulario.initialize(); // inicializa formulario
});
</script>

</head>
<body>

<form name='CAD' id='CAD' class="chamado_form">
	
<!-- Paginas Touch -->
<div id="DTouchPages_chamado">
	
	<!-- Pagina Central -->
	<div id="DTouchPages_chamado_center">
			
			<!-- cliente / endereco -->
			<div id="cliente_container">
				<div class='DTouchBoxes_title DTouchBoxes_title_input'>
                    <input type="text" name="cliente" id="cliente" placeholder="Cliente"/>
				</div>
				<div id="cliente_endereco" class="DTouchBoxes_line_list"></div>
			</div>
			
			<!-- Area -->
			<div id="area_container">
				<div id="area" class="DTouchBoxes_line_list"></div>
			</div>
		
			<!-- Plano utilizado -->
			<div id="plano_container">
				<div id="plano" class="DTouchBoxes_line_list"></div>
			</div>
		
			<!-- prioridade do chamado -->
			<div id="prioridade_container">
				<div id="prioridade" class="DTouchBoxes_line_list"></div>
			</div>
			
			<!-- chamado emails -->
			<div id="emails_container">
				<div class='DTouchBoxes_title DTouchBoxes_title_input'>
                    <input type="text" name="email" id="email" placeholder="Lista de emails" />
				</div>
				<div id="emails_list" class="DTouchBoxes_line_list_input_title"></div>
			</div>            
		</div>
        
		
	</div>




	<!-- Pagina Direita -->
        
    <div id="DTouchPages_chamado_right">
		
		<div class="eos_template_chamado_filter DTouchBoxes" style="display:none;">
            <div class="DTouchBoxes_line DTouchBoxes_line_input">
				<div class="filter_date_ini">
					<input />
                </div>
                <div class="filter_date_end">
					<input /> 
				</div>
            </div>
			<div class="filter_empresa DTouchBoxes_line DTouchBoxes_line_input">
 				<input />
			</div>				
		</div>

		
		<div id="chamados_list_container"></div>
		<div id="list_container"></div>
	</div>
	
</div>

	<!-- retorno do codigo -->
	<div id="resultado" class="DDebug"></div>

	<!-- variaveis de ambiente -->
	<input type='hidden' name='COD' id="COD" />
    <input type='hidden' name='finalizado' id="finalizado" />
    <input type='hidden' name='responsavel' id="responsavel_codigo" />
</form>

<!--
/*
*   Template, acoes
*/  
-->
<div class='eos_template_chamado_acoes acao_item_container DTouchBoxes_nolimit' style='display:none;'>
    <input type='hidden' class="acao_codigo" />
    
    <div class='acao_item_protocolo_container DTouchBoxes_line DTouchBoxes_line_text'>
        <div class='acao_item_usuario'></div>
        <div class='acao_item_protocolo'></div>
        <div class='acao_item_data'></div>
    </div>
    <div class='acao_item_descrp_container DTouchBoxes_line DTouchBoxes_line_textarea'>
        <div class='acao_item_descrp DTouchBoxes_line_textarea'>
            <textarea></textarea>
        </div>
        <div class='acao_item_executor_descrp DTouchBoxes_line_textarea'>
            <textarea></textarea>
        </div>
        <div class='acao_item_anexos'></div>
    </div>
    <div class='DTouchBoxes_line DTouchBoxes_line_input'>
        <div class='acao_item_encaminhar'><span></span></div>
        <div class='acao_item_executar'><span></span></div>
        <div class='acao_item_executor'> 
            <input/>
        </div>
        <div class='acao_item_tipo'>
            <select></select>
        </div>
        <div class='acao_item_tempo'>
            <input/>
        </div>
        <div class='acao_item_cfg'>
            <div class='acao_item_cfg_sigiloso'>
                <input/>
            </div>
        </div>
    </div>
</div>



</body></html>
HTML
