#!/usr/bin/perl

$nacess = "10";
require "../cfg/init.pl";

$ID = &get('ID');
# $EXTRA = &get('EXTRA');
# $TECNICO = &get('TECNICO');

$COD = &get('COD');
# if($COD eq "")
#	{
#	$TECNICO = $USER->{usuario};
#	}

# variavel para controle de troca de pagina direto do menu
$PAGE = &get('PAGE');
if($PAGE eq "") {
	$PAGE = "center";
}

# $DTLISTINI = timestamp("year")."-".timestamp("month")."-01";
# $DTLISTINISHOW = "01/".timestamp("month")."/".timestamp("year");

print $query->header({charset=>utf8});

# 
# <!DOCTYPE html PUBLIC "-//WAPFORUM//DTD XHTML Mobile 1.0//EN" "http://www.wapforum.org/DTD/xhtml-mobile10.dtd">
# <meta name="viewport" content="initial-scale=1, user-scalable=no" />
# <meta name="viewport" content="width=device-width">
# <meta name="viewport" content="user-scalable=yes, initial-scale=1.0, maximum-scale=2.0, width=device-width" />
# <!-- 
# <meta name="viewport" content="width=device-width, initial-scale=1" />
# <script type="application/javascript" src="/comum/fastclick/lib/fastclick.js"></script>  
# <meta name="viewport" content="initial-scale = 1.0,maximum-scale = 1.0" />
# -->
#
# // include("/comum/jquery/jquery.mobile-1.3.0.js");
# // DDebug();
# // include("/comum/jquery/jquery.mobile-1.3.0.js");

print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html id="html">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	
<script language='JavaScript'>

    // Armazena pesquisas
    odate_ini = '';
    odate_end = '';
    oemp_cod = '';
    oemp_desc = '';
    osearch = '';

    // DLoad("chamado"); // carrega dependencias especificas

    /*
    *   Template, acoes
    */  
    var t  = "<div class='eos_template_chamado_acoes acao_item_container'>";
        t += "     <div class='acao_item_data'></div>";
        t += "    <div class='acao_item_descrp_container'>";
        t += "        <div>";
        t += "            Execução";
        t += "        </div>";
        t += "        <div class='acao_item_descrp'></div>";
        t += "        <div class='acao_item_anexos'></div>";
        t += "    </div>";
        t += "    <div class='acao_item_usuario'></div>";
        t += "</div>";
    eos.template.chamado.acoes = t; // adiciona template ao core
    
    /* 
    *   Empresa
    *       objeto empresa 
    */
    function Empresa()
    	{
    	/* 
        *   enderecos empresa
        */
    	this.endereco = function(end){
    		if(\$("#cliente").val() == "") {
    			alerta("Selecionar o Cliente");
    			return false;
    		}

    		\$.DActionAjax({
    			action:"empresa_endereco.cgi",
    			req: "empresa="+\$("#cliente").val()+"&end="+end,
    			loader: \$("#cliente_container"),
    			serializeForm: false,
                postFunction: function(){
                    if(\$("#COD").val()){
                        \$("#cliente_endereco").DTouchRadio("disable");
                    }
                }
    		});
    	};
		
    	// area	
    	this.area = function(a){
    		if(\$("#cliente").val() == ""){
    			alerta("Selecionar o Cliente");
    			return false;
    		}
		
    		\$.DActionAjax({
    			action:"area.cgi",
    			req: "empresa="+\$("#cliente").val()+"&area="+a,
    			loader: \$("#area_container"),
    			serializeForm: false,
                postFunction: function(){
                    if(\$("#COD").val()){
                        \$("#area").DTouchRadio("disable");
                    }
                }
    		});
    	}
		
    	// planos
    	this.planos = function(a,p) { 
            
            if(!p){
                p = "";
            }
            
    		if(\$("#cliente").val() == ""){
    			\$.DDialog("Selecionar o Cliente");
    			return false;
    		}
		
    		// mostra planos
    		// \$("#plano_container").DTouchBoxes("show");
		
    		// carrega planos
    		\$.DActionAjax({
    			action:"planos.cgi",
    			req: "empresa="+\$("#cliente").val()+"&area="+a+"&plano="+p,
    			loader: \$("#plano_container"),
    			serializeForm: false,
                postFunction: function(){
                    if(\$("#plano").DTouchRadio("value")){
                        \$("#plano").DTouchRadio("disable");
                    }
                }
    		});
    	}
    };
	
    
    
    
    
    
    /** 
     *   Chamado
     *       Objeto
     */
    function Chamado() {
    	// reativar chamado
    	this.reativar = function(){
		
    	};
        
        
        /**
         *  Imprimir
         */
        this.print = function(){
            // executa
        	\$.DActionAjax({
        		action       : "os.pdf"
        	}); 
        };
        
        
    	/**
         *   emails, do ticket
         */
    	this.emails = function(){
            \$("#emails_container").DTouchBoxes("show");
            
            \$.DActionAjax({ 
                action:"emails.cgi",
                req: "&COD="+\$("#COD").val(),
                serializeForm: false,
                loader : \$("#emails_container")
            });
        };
        
    	/**
         *   emails, do cadastro cliente area
         */
        this.emails_update = function(email){
            if(!email) {
                email = "";
                loader = \$("#emails_container");
            } else {
                loader = false;
            }
            
            \$("#emails_container").DTouchBoxes("show");
            
    		\$.DActionAjax({
    			action:"emails_update.cgi",
    			req: "email="+email+"&empresa="+\$("#cliente").val()+"&area="+\$("#area").DTouchRadio("value"),
    			loader: loader,
    			serializeForm: false,
                postFunction: function(){
                    // console.log(x);
                }
    		});
        }
        
        
    	/**
         *   finalizar chamado
         */
    	this.finalizar = function(){
            \$.DDialog({
                type    : "confirm",
                message : "Deseja finalizar o ticket atual ?",
                btnYes  : function(){
                    \$.DActionAjax({ 
                        action:"finalizar.cgi",
                        req: "&COD="+\$("#COD").val()
                    });
                },
                btnNo   : function(){
                	return true;
                }
            });
        };
        
    	/**
         *   cancelar chamado
         */
    	this.cancelar = function(){
            
            \$.DDialog({
                type    : "confirm",
                title   : "Deseja cancelar o ticket atual ?",
                message : "<textarea name='cancelar' placeholder='Motivo Cancelamento ?'\></textarea>",
                btnYes  : function(){
                
                    var req  = "cancelar="+\$(this).parent().find("textarea[name=cancelar]").val();
                        req += "&COD="+\$("#COD").val();
                        
                    \$.DActionAjax({ 
                        action:"finalizar.cgi",
                        req: req
                    });
                },
            });
        };
        
        
    	/**
         *   reabrir chamado
         */
    	this.reopen = function(){
            
            \$.DDialog({
                type    : "confirm",
                message : "Deseja reabrir o ticket atual ?",
                btnYes  : function(){
                    
                    \$("#RECOD").val(\$("#COD").val()); // ajusta pai
                    \$("#COD").val("");
                    form.save();
                    
                    /*
                    \$.DActionAjax({ 
                        action:"reopen.cgi"
                        // req: "&COD="+\$("#COD").val()
                    });
                    */
                }
            });
        };
        
            
    	/**
         *   acoes - lancamentos
         */
    	this.acoes = {
            /* lista acoes */
            type : "",
            
            /* carrega acoes */
            load : function(){
                // remove acoes
                \$("#chamado_acoes").empty();
                
                form.menu.initialize() // regera menus 
                eos.menu.action.hideAll(); // esconde menus
                
                // alteracao liberada ?
                if(!\$("#data_previsao").val() || !\$("#tempo_previsao").val() || !\$("#plano").DTouchRadio("value")) { 
                    eos.menu.action.show(["icon_tkt_save"]);
                }
                
                
                \$.DActionAjax({ 
                    action:"edit_acoes.cgi",
                    req: "&COD="+\$("#COD").val()
                });
            },
            
            
            /* lista acoes */
            list : function(ca){
                // template 
                var template = \$('.eos_template_chamado_acoes').clone().removeClass('eos_template_chamado_acoes').show();
                
                var acoes_obj = this; // ajuste para uso do objeto dentro do while

                
                // adiciona item 
            	ca.forEach(function(i){    
                    acoes_obj.new(i);
                });
                
                // ajusta menu
                // eos.menu.action.hideAll(); // esconde menus
                
                \$("#tkt_status").addClass("tkt_status_show"); // mostra status tkt
                
                if(ca.length === 0) { // no actions
                    
                    eos.menu.action.show(["icon_tkt_action_encaminhar","icon_tkt_action_executar","icon_tkt_new","icon_tkt_imprimir","icon_tkt_cancelar"]);
                    \$("#tkt_status span").text("aberto"); // status tkt
                    
                } else { // at least one action
                    eos.menu.action.show(["icon_tkt_action_encaminhar","icon_tkt_action_executar","icon_tkt_action_finalizar","icon_tkt_new","icon_tkt_imprimir","icon_tkt_cancelar"]);
                    
                    // ajusta menu 
                    if(\$("#finalizado").val()){ 
                        eos.menu.action.hideAll(); // esconde menus
                        eos.menu.action.show(["icon_tkt_new","icon_tkt_imprimir","icon_tkt_reabrir"]);
                        \$("#tkt_status span").text("finalizado"); // status tkt
                        
                    } else if(\$("#cancelado").val()){ 
                        \$("#tkt_status span").text("cancelado"); // status tkt
                        
                    } else { 
                        \$("#tkt_status span").text("atendimento"); // status tkt
                    }
                }
                
                
                // ajusta boxes acoes, primeira acao
                /*
                var box = \$("#chamado_acoes div:first-child")
                cont = box.find(".acao_item_descrp_container");
                cont.find(".acao_item_descrp").hide();
                cont.find(".acao_item_executor_descrp").css("width","100%");                
                // box.find(".acao_item_usuario").hide();
                */
            },
            
            
            /**
             *   new
             *       adiciona nova acao
             */
            new : function(i){
                
                // encaminhar: se for novo encaminhar ou edicao responsavel = executor
                var encaminhar = false;
                var cliente = false;
                chamado.acoes.type = "executar"; // ajusta tipo acao
                
                if(i === "encaminhar"){
                    i = "";
                    encaminhar = "encaminhar";
                    chamado.acoes.type = "encaminhar"; // ajusta tipo acao
                } else if(i === "cliente"){
                    i = "";
                    encaminhar = "cliente";
                    cliente = true;
                    chamado.acoes.type = "cliente"; // ajusta tipo acao
                } else if(i) {
                    if(i.tempo){
                        encaminhar = "executar-editar";
                    } else {
                        encaminhar = "encaminhar-editar";
                    }
                }
                
                // cria novo
                var t = \$('.eos_template_chamado_acoes').clone().removeClass('eos_template_chamado_acoes').show().appendTo('#chamado_acoes');
                
                var acoes = [];
                
                // codigo holder
                acoes["codigo"] = t.find(".acao_codigo")
                    .prop({
                        name : "acao_codigo"
                    });
                
                // protocolo
                acoes["protocolo"] = t.find(".acao_item_protocolo");
                acoes["data"] = t.find(".acao_item_data");
                
                // data do item
                acoes["data_execucao"] = t.find(".acao_item_data_execucao input")
                    .prop({
                        id          : "acao_data_execucao_new",
                        name        : "acao_data_execucao",
                        type        : "text",
                        placeholder : "Data",
                    })
                    .fieldDateTime({type:"date-time"}); 
                    
                // tempo do item
                acoes["tempo"] = t.find(".acao_item_tempo input")
                    .prop({
                        name        : "acao_tempo",
                        type        : "text",
                        placeholder : "Execução",
                    })
                    .fieldDateTime({type:"time"});

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
                    
                /*
                * V2 alpha 1
                * desabilitado pois existe campo interno e cada lancamento será computado
                *
                // interno
                acoes["interno"] = t.find(".acao_item_cfg_interno input")
                    .prop({
                        name  : "acao_interno",
                        id    : "interno_"+eos.tools.idGen(),
                        type  : "checkbox"
                    })
                    .fieldCheckbox({
                        label : "interno"
                    });
                */
                   
                // usuario do item
                acoes["usuario"] = t.find(".acao_item_usuario");
                
                // descrp do item
                acoes["descrp"] = t.find(".acao_item_descrp textarea")
                    .prop({
                        name        : "acao_descrp",
                        placeholder : "Comunicação interna"
                    });
                
                // executor do item
                acoes["executor"] = t.find(".acao_item_executor input")
                    .prop({
                        name        : "acao_executor",
                        id          : "executor_"+eos.tools.idGen(),
                        placeholder : "Encaminhar para..."
                    })
                    .fieldAutoComplete({type: "usuario"});
                    
                // descrp do item
                acoes["executor_descrp"] = t.find(".acao_item_executor_descrp textarea")
                    .prop({
                        name        : "acao_executor_descrp",
                        placeholder : "Comunicação Pública"
                    });
                        
                // tipo atendimento item
                acoes["tipo"] = t.find(".acao_item_tipo select");
                acoes["tipo"]
                    .prop({
                        name        : "acao_tipo",
                        id          : "tipo_"+eos.tools.idGen()
                    })
                    .fieldSelect(
                        { 
                        table       : "tkt_acao_tipo",
                        placeholder : "Tipo de Atendimento"
                        });
                
                // botao encaminhar
                acoes["executor_encaminhar"] = t.find(".acao_item_encaminhar")
                    .prop({id : "executor_encaminhar_"+eos.tools.idGen()})
                    .hide();
                acoes["executor_encaminhar"].find("span").html("encaminhar ?");
                
                // botao executar
                acoes["executor_executar"] = t.find(".acao_item_executar")
                    .prop({id : "executor_executar_"+eos.tools.idGen()})
                    .hide();
                acoes["executor_executar"].find("span").html("executar ?");
                
                
                // seta valores
                if(i){
                    acoes["codigo"].val(i.codigo); // ajusta codigo do item
                    
                    acoes["tipo"].fieldSelect("value", i.tipo.tipo);
                    acoes["tipo"]
                        .parent()
                            .append("<span class='input_show'>"+i.tipo.descrp+"</span>")
                            .find("div")
                                .hide();
                    
                    acoes["protocolo"].html("#"+\$("#COD").val()+"."+i.codigo);
                    acoes["data"].html(i.data);
                        
                    
                    /*
                    acoes["data_execucao"].hide().val(i.data_execucao);
                    acoes["data_execucao"]
                        .parent()
                            .append("<span class='input_show'>"+i.data_execucao+"</span>");
                    */
                    // acoes["data_execucao"].fieldDateTime("value",i.data_execucao);
                    acoes["data_execucao"].parents(".acao_item_data_execucao").html(i.data_execucao);
                                
                    acoes["tempo"].fieldDateTime("value",i.tempo);
                    acoes["tempo"]
                        .parent()
                            .append("<span class='input_show'>"+i.tempo+"</span>")
                            .find("input")
                                .hide();
                    /*
                    acoes["tempo"]
                        .parent()
                            .append("<span class='input_show'>"+i.tempo+"</span>");
                    */
                    acoes["descrp"]
                        .hide()
                        .parent()
                            .append("<span class='descrp_show'>"+i.usuario.descrp+"</span>");
                    
                    acoes["usuario"].html(i.usuario.nome);
                    
                    acoes["executor_descrp"]
                        .hide()
                        .parent()
                            .append("<span class='descrp_show'>"+i.executor.descrp+"</span>");
                    
                    acoes["executor"]
                        .fieldAutoComplete("value", {
                            id  : i.executor.executor,
                            val : i.executor.nome
                        });
                    acoes["executor"]
                        .parent()
                        .find(".EOS_template_field_field")
                            .append("<span class='input_show'>"+i.executor.nome+"</span>")
                            .find("input")
                                .hide();
                    
                    if(i.sigiloso){
                        acoes["sigiloso_"] = t.find(".acao_item_cfg_sigiloso .fieldCheckbox");
                        acoes["sigiloso_"].fieldCheckbox("check");
                        // acoes["sigiloso"] = t.find(".acao_item_cfg_sigiloso input");
                        
                        // verificar motivo que ao marcar nao executa postfunction oncheck                        
                        acoes["executor_descrp"].parents(".acao_item_executor_descrp").hide();
                        acoes["descrp"].parents(".acao_item_descrp").addClass("acao_item_descrp_full"); // full internal box class
                    }
                    /*
                    * V2 alpha 1, dasabilitado pois existe campo interno
                    if(i.interno){
                        acoes["interno"].fieldCheckbox("check");
                    }
                    */
                    /*
                    // desabilita troca de executor se ja setado
                    if(i.executor.executor){
                        acoes["executor"].fieldAutoComplete("disable");
                    }
                    */
                    /* 
                    * V2 alpha 1
                    *   capacidade de editar seus lancamentos, 
                    *
                    * V2 rc
                    *   desabilitado pois nao ha necessidade
                    *   caso voltar atras na decisao esta e a linha para isso
                    *
                    *   -/-/- usuario logado for diferente do usuario da acao e nao for supervisor deixa readonly
                    *   if("$USER->{usuario}" !== i.executor.executor && "$USER->{tacess}" !== "s"){
                    */
                    
                    acoes["sigiloso_"] = t.find(".acao_item_cfg_sigiloso .fieldCheckbox");
                    acoes["sigiloso_"].fieldCheckbox("disable");
                    
                    // acoes["interno"].fieldCheckbox("disable"); // V2 alpha 1
                    acoes["tipo"].fieldSelect("disable");
                    // acoes["data_execucao"].fieldDateTime("disable");
                    acoes["tempo"].fieldDateTime("disable");
                    acoes["usuario"].fieldAutoComplete("disable");
                    acoes["descrp"].prop("readonly",true);
                    acoes["executor"].fieldAutoComplete("disable");
                    acoes["executor_descrp"].prop("readonly",true); 
                     
                    // }
                    
                } else { // novo
                    
                    acoes["codigo"].addClass("acao_codigo_new");
                    acoes["usuario"].html("$USER->{nome}");
                    // this.formExecEnc(encaminhar,acoes);
                    
                    // adiciona ids para melhor controle ao salvar
                    acoes["executor_descrp"].prop("id","acao_descrp_publico_new");
                    acoes["descrp"].prop("id","acao_descrp_interno_new");
                    // acoes["data_execucao"].prop("id","acao_data_execucao_new");
                    acoes["executor"].prop("id","acao_executor_new");
                    acoes["tipo"].prop("id","acao_tipo_new");
                    acoes["tempo"].prop("id","acao_tempo_new");
                    acoes["sigiloso_"] = t.find(".acao_item_cfg_sigiloso .fieldCheckbox");
                    acoes["sigiloso_"].addClass("acao_sigiloso_new");
                    
                }
                
                // ajusta formulario
                this.formExecEnc(encaminhar,acoes);
                
                /* adiciona anexos
                i.anexos.forEach(function(a){
                    t.find(".acao_item_anexos").append(a.descrp+"<hr>");
                });
                */
                
                // acoes["usuario"].fieldAutoComplete("val",{id  : i.executor.executor, val : i.executor.nome});
                
                // t.DTouchBoxes();
                t.DTouchBoxes({ 
                    minimize : true
                });
            }, 
            /*
            *   formExecEnc
            *       ajusta formulario de acoes 
            */
            formExecEnc : function(opt,acoes){
                /*
                *   Executar ou Encaminhar                   
                *    false        true
                */
                acoes["executor_encaminhar"]
                    .click(function(){
                        \$(this).hide(); 
                                            
                        acoes["tempo"].parents(".acao_item_tempo").hide();
                        acoes["tipo"].parents(".acao_item_tipo").hide();
                        // acoes["data_execucao"].parents(".acao_item_data_execucao").hide();
                        acoes["executor"].parents(".acao_item_executor").show();
                        acoes["executor_executar"].show();
                        
                        chamado.acoes.type = "encaminhar"; // ajusta tipo acao
                    });
                
                acoes["executor_executar"]
                    .click(function(){
                        \$(this).hide(); 
                                                
                        acoes["executor"].parents(".acao_item_executor").hide();
                        
                        acoes["tipo"].parents(".acao_item_tipo").show();
                        acoes["tempo"].parents(".acao_item_tempo").show();
                        // acoes["data_execucao"].parents(".acao_item_data_execucao").show();
                        acoes["executor_encaminhar"].show();
                        
                        chamado.acoes.type = "executar"; // ajusta tipo acao
                    });
            
                /*
                *   ajustes visuais
                */
                if(opt === "encaminhar" || opt === "encaminhar-editar"){ // encaminhar
                
                    acoes["tipo"].parents(".acao_item_tipo").hide();
                    acoes["tempo"].parents(".acao_item_tempo").hide();
                    // acoes["data_execucao"].parents(".acao_item_data_execucao").hide();
                    acoes["executor"].parents(".acao_item_executor").show();
                    acoes["executor_executar"].show();                    
                    
                    if(opt === "encaminhar"){ // novo
                        acoes["executor_executar"].show();
                    } else { // editar
                        acoes["executor_executar"].hide();                        
                        acoes["executor"].parents(".acao_item_executor").addClass("acao_item_executar_editar");
                        acoes["tipo"].parents(".acao_item_tipo").addClass("acao_item_tipo_editar");
                    }
                
                } else { // executar
                
                    acoes["executor"].parents(".acao_item_executor").hide();
                    acoes["tempo"].parents(".acao_item_tempo").show();
                    acoes["executor_encaminhar"].show();
                    // acoes["data_execucao"].parents(".acao_item_data_execucao").show();
                

                    if(opt === "executar-editar") { // editar 
                        acoes["executor_encaminhar"].hide();
                        acoes["tipo"].parents(".acao_item_tipo").addClass("acao_item_encaminhar_editar");
                        
                    } else { // novo
                        acoes["executor_encaminhar"].show();
                    }
                }
            }
    	};
			
    	/* 
        *   lista chamados 		
        */
    	this.list = function(){

		// Monta requisição com os campos de pesquisa preenchidos
		reqx = "";
		if(osearch)
			{
			reqx += "&search="+osearch;
			}		
		if(oemp_cod)
			{
			reqx += "&filter_empresa="+oemp_cod;
			}
		if(oemp_desc)
			{
			reqx += "&filter_empresa_descrp="+oemp_desc;
			}
		if(odate_ini)
			{
			reqx += "&filter_date_ini="+odate_ini;
			}
		if(odate_end)
			{
			reqx += "&filter_date_end="+odate_end;
			}
			
			
		
    		// executa arquivo
    		\$.DActionAjax({
    			action: "edit_list.cgi",
    			// req: "COD="+\$("#COD").val(),
    			req: reqx,
    			loader: "chamados_list_container",
    			serializeForm: false
    		});	
    	};
		
    	// edita chamado
    	this.edit = function(c){
            
            var obj = this;
            
            // se vier codigo
            if(c){
                \$("#COD").val(c);
            }
            
            // Guarda valor do campo busca
	        osearch = \$("#chamados_list_container_search_field").val();
            
            // busca dados form
    		\$.DActionAjax({
    			action: "edit_db_frm.cgi",
    			req: "&COD="+\$("#COD").val(),
                postFunction : function() {
                    
                    // se ja finalizado remove botoes
                    // if(\$("#finalizado").val()) {
                        eos.menu.action.hideAll();
                        // }
                    
            		// carrega acoes
            		obj.acoes.load();
                }
    		});            
    	};
		
    	// prioridade
    	this.prioridade = function(p){
    		\$('#prioridade_container').DTouchBoxes("show");
		
    		if(p){
    			\$("#prioridade").DTouchRadio("val",p)
                \$("#prioridade").DTouchRadio("disable");
            }
    	};
        
        // novo ticket
        this.new = function(){
            if(\$(".acao_codigo_new").length > 0){
                \$.DDialog({
                    type    : "confirm",
                    message : "Existem Alterações não salvas no formulário <br> deseja salvar as alterações ?",
                    btnYes  : function(){
                    	form.save();
                    },
                    btnNo   : function(){
                    	\$("#DTouchPages_chamado").DTouchPages("page","center");
                    	form.reset();
                    }
                });
            } else if(\$("#COD").val()) {
                form.reset();
            }
        };
    }


// form, objeto
function Form(){
	var isChanged = false;
	
	// inicializa formulario
	this.initialize = function() {
		// esconde boxes ao iniciar formulario
		\$("#protocolo_container").hide();

		// ajusta responsavel para usuario logado
		\$("#responsavel").text("$USER->{nome}");
		
		// testa modificacoes no formulario
		// this.isChange(false);
		
		// cria pagina touch padrao
		\$("#DTouchPages_chamado").DTouchPages({
			// editable:true,
			// pageChange: "$PAGE",
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
				// eos.menu.action.show('icon_tkt_new'); // ajusta icones
				eos.menu.action.disappear(); // some menu action
				chamado.list();  
            },
			onCreate : function() {
                
				// gera boxes
				\$("#area_container").DTouchBoxes({         // area
					title:"Área"
				});
				\$("#plano_container").DTouchBoxes({        // planos
					title:"Planos"
				});
				\$("#cliente_container").DTouchBoxes();     // cliente
				\$("#acoes_first_container").DTouchBoxes(); // chamado 
				\$("#emails_container").DTouchBoxes();      // emails
				\$("#prioridade_container").DTouchBoxes({   // prioridade
					title:"Prioridade"
				});
                
				// esconde boxes
                \$("#emails_container").DTouchBoxes("hide");
				\$("#area_container").DTouchBoxes("hide");
				\$("#plano_container").DTouchBoxes("hide");
                
				// cliente, inicializa campo
				\$("#cliente").fieldAutoComplete({ 
					sql_tbl:"empresa",
					sql_sfield:"nome",
					sql_rfield:"nome",
					sql_order:"nome",
					postFunction:function(x)
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
                \$('#cliente_descrp_container').hide(); // esconde campo cliente
                
				// data_previsao
				\$("#data_previsao").fieldDateTime({ 
					type:"date-time"
				});
	
				// chamado tempo_previsao previsto
				\$("#tempo_previsao").fieldDateTime({ 
					type: "time",
					postFunction: function() {
						\$("#tempo_previsao_faturado").val(\$(this).val());
					}
				});	
                
                \$('#data_previsao_container').hide(); // esconde data previsao 
				
                
				// recorrente
				\$("#recorrente_dia").fieldNumber({ 
					range     : { min : 1, max : 30 },
                    maxlength : 2
				});
                
				\$("#recorrente_data_final").fieldDateTime({ 
					type:"date"
				});
                
                
                // V2 alpha 1	
                // executor
                // \$("#executor_container").DTouchBoxes();
                // \$("#executor").fieldAutoComplete({type:"usuario"});
                
				// carrega formulario com dados vindo do banco de dados
				// DActionEditDB(); // unloader dentro desta funcao	
                \$.DActionAjax({
                    action : "edit_db.cgi"
                });
                
                
			},
			// pageLeft: false, // \$("#DTouchPages_chamado_left"),
			pageRight: \$("#DTouchPages_chamado_right"),
			pageCenter: \$("#DTouchPages_chamado_center")
		});
				
		/* lista de emails
		\$("#emails_list").DTouchRadio({ 
            orientation : "vertical",
			editable    : true,
            unique      : true
		});
        */
        
        // campo para insercao do email 
		\$("#email").fieldEmail({
			postFunction: function(x){ 
                // adiciona item no radio
				\$("#emails_list").DTouchRadio("additem",{val:x,descrp:x});
                
                \$("#email").fieldEmail("reset");
                
                eos.menu.action.show(["icon_tkt_save"]); // mostra icone ao adicionar email se sumido little POG

                // se for edicao
                // if(\$("#COD").val()) {
            	chamado.emails_update(x);
                // }
			}
		});
        
        // botao de add no campo do email
        \$("#email_add_btn").click(function(){
            \$("#email").fieldEmail("trigger");
        });
        
            
            
        // inicializa campos input TEXT
        \$("#CAD input[type=text]:not(.DFields)").each(function(){
            eos.template.field.text(\$(this));
        });
                    
    	\$("#prioridade").DTouchRadio({ 
    		table : "tkt_prioridade"
    	});
            
    	// se for edicao direto de outro modulo
    	if("$COD" != "") { 
            \$('#COD').val("$COD");
    		chamado.edit();
    	}
        
        this.menu.initialize(); // inicia menu
	};
	
	/*
    *   formulario modificado, teste
    */ 
    /*
	this.isChange = function(x)
		{
		if(x)
			{
			if(x === true)
				chamado_menu.btnShow(['icon_tkt_save','icon_cancel']); // ajusta icones
				
			return isChanged = x;
			}
		else
			return isChanged
		}
    */
		
	/*
    *   reseta formulario
    */
	this.reset = function() {
        /**
         *    Recarega o modulo para zerar o formulario....
         *       ajustar para limpar campos e nao precisar recarregar o modulo
         *       testar performance
         */    
        eos.core.call.module.tkt(); // carrega modulo tkt
        return true;
        
		// limpa acoes
		\$("#chamado_acoes").html("");
		
		// reinicia campos
		\$("#cliente").fieldAutoComplete("reset");
		\$("#cliente_endereco").DTouchRadio("reset","hard");
		\$("#area").DTouchRadio("reset","hard");
        \$("#plano").DTouchRadio("reset","hard");
        \$("#prioridade").DTouchRadio("reset");

		// limpa campos
		\$("#CAD #COD, #solicitante, #data_previsao, #tempo_previsao, #descrp").val("");
		
		// esconde boxes
		\$("#area_container").DTouchBoxes("hide");
        \$("#plano_container").DTouchBoxes("hide");
        // \$("#prioridade_container").DTouchBoxes("hide");
		
        // limpa descritivos
        \$("#protocolo").text("");
        \$("#data_inclusao").text("");
			
		// menus
		// eos.menu.action.show(['icon_tkt_save','icon_tkt_new']);
	};
	
    	
	/**
     *   salva formulario
     */
	this.save = function(){
        var msg = ""; // mensagem de erro
        
        /** 
         *   testa campos obrigatorios baseado no tipo de lancamento
         */        
        if(\$(".acao_codigo_new").length == 1) { // nova acao ?            
            // casos
            switch(chamado.acoes.type){
                case "encaminhar" : 
                
                    if(!\$("#acao_executor_new").val()){ // campo encaminhar test
                        msg += "<li> Usuário para encaminhar </li>";
                    }
                
                    if(!\$("#acao_descrp_interno_new") && \$(".acao_sigiloso_new").fieldCheckbox("isChecked")){ // campo comunicacao interna
                        msg += "<li> Comunicação interna </li>";
                    }
                
                    if(!\$("#acao_descrp_publico_new").val() && !\$(".acao_sigiloso_new").fieldCheckbox("isChecked")){ // campo comunicacao externa
                        msg += "<li> Comunicação externa </li>";
                    }
                
                    // if(\$("#acao_executor_new").val() === "$USER->{usuario}"){ // usuario encaminhante mesmo logado NO !
                    //    msg += "<li> Não pode encaminhar para você mesmo ! </li>";
                    // }
                
                    if(msg){ // se algum erro
                        \$.DDialog({ 
                            // message : "Campos obrigatórios da Ação devem ser preenchidos: <ul>"+msg+"</ul>",
                            message : "<ul>"+msg+"</ul>",
                            title   : "Ações "
                        });
                    return false;
                    } else { // corrige campos ocultos para salvar corretamente
                        // acao.find(".acao_item_tipo select").fieldSelect("value","");

                    }
                break;
            
                // acao executar
                case "executar" : 
                                                
                    if(!\$("#acao_descrp_interno_new") && \$(".acao_sigiloso_new").fieldCheckbox("isChecked")){ // campo comunicacao interna
                        msg += "<li> Comunicação interna </li>";
                    }
                
                    if(!\$("#acao_descrp_publico_new").val() && !\$(".acao_sigiloso_new").fieldCheckbox("isChecked")){ // campo comunicacao externa
                        msg += "<li> Comunicação externa </li>";
                    }
                
                    if(!\$("#acao_tipo_new").fieldSelect("value")){ // campo tipo
                        msg += "<li> Tipo de atendimento vazio ! </li>";
                    }
                    
                    /*
                    if(!\$("#acao_data_execucao_new").fieldDateTime("value")){ // campo data execucao
                        msg += "<li> Comunicação externa </li>";
                    }
                    */
                    /*
                    if(!\$("#acao_tempo_new").fieldDateTime("value") || \$("#acao_tempo_new").fieldDateTime("value") === "00:00"){ // campo tempo
                        msg += "<li> Tempo deve ser maior que 00:00 ! </li>";
                    }
                    */
                    if(msg){ // se algum erro
                        \$.DDialog({ 
                            // message : "Campos obrigatórios da Ação devem ser preenchidos: <ul>"+msg+"</ul>",
                            message : "<ul>"+msg+"</ul>",
                            title   : "Ações "
                        });
                    return false;
                    } else { // corrige campos ocultos para salvar corretamente    
                        \$("#acao_executor_new").val("$USER->{usuario}"); // define usuario logado mesmo encaminhar para controle interno tabela
                    }
                break;
            
                case "cliente" : 
                    var acao = \$("input[name=acao_codigo]").parents(".DTouchRadio");
                break;
            }
        }
        
		// testa campos obrigatorios
		if(!\$("#cliente_endereco").DTouchRadio("value")) {
            msg += "<li> Endereço do cliente </li>";
		}
        if(!\$("#area").DTouchRadio("value")) {
            msg += "<li> Área </li>";
        } 
        if(!\$("#prioridade").DTouchRadio("value")) {
            msg += "<li> Prioridade </li>";
        } 
        if(!\$("#solicitante").val()) {
            msg += "<li> Solicitante </li>";
        } 
        if(!\$("#descrp").val()) { 
            msg += "<li> Descrição do Problema </li>";
        }
        if(!\$("#cliente").val()) {
            msg += "<li> Cliente </li>";
        }
        if(!\$("#plano").DTouchRadio("value") && "$USER->{tipo}" !== "99") {
            msg += "<li> Plano </li>";
        }

		
        if(msg){ // se algum erro
            \$.DDialog({ 
                // message : "Campos obrigatórios da Ação devem ser preenchidos: <ul>"+msg+"</ul>",
                message : "<ul>"+msg+"</ul>",
                title   : "Formulário básico "
            });
			return false;
        }

		// endereco selecionado
		var req  = "&empresa_endereco="+\$("#cliente_endereco").DTouchRadio("value");
        /*
            * V2 alpha 1 
            req += "&area="+\$("#area").DTouchRadio("value");
            req += "&prioridade="+\$("#prioridade").DTouchRadio("value");
            req += "&solicitante="+\$("#solicitante").DTouchRadio("value");
            req += "&descrp="+\$("#descrp").DTouchRadio("value");
            req += "&cliente="+\$("#cliente").DTouchRadio("value");
         */  
        
        if(\$("#acao_descrp_publico_new").val()) {
            var dp = \$("#acao_descrp_publico_new").val();
            dp = dp.replace(/\;/g,'\, ');
        }
        if(\$("#acao_descrp_interno_new").val()){
            var di = \$("#acao_descrp_interno_new").val();
            di = di.replace(/\;/g,'\, ');
        }
        
            req += "&acao_new="+\$(".acao_codigo_new").length;
            req += "&acao_descrp_publico_new="+dp;
            req += "&acao_descrp_interno_new="+di;
            req += "&acao_executor_new="+\$("#acao_executor_new").val();
            req += "&acao_tipo_new="+\$("#acao_tipo_new").val();
            req += "&acao_data_execucao_new="+\$("#acao_data_execucao_new").fieldDateTime("value");
            req += "&acao_tempo_new="+\$("#acao_tempo_new").val();
            req += "&acao_sigiloso_new="+\$(".acao_sigiloso_new").fieldCheckbox("isChecked");
            
            // emails
            \$("input[name=emails_list_radios]").each(function(){
                \$(this).prop({
                    type : "hidden"
                });
            });
            
         
            
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
            
            // new icon
            eos.menu.action.new({ // novo
                id       : "icon_tkt_new",
                title    : "novo",
                subtitle : "ticket",
                group    : "icon_tkt",
                click    : function(){
                    form.reset(); 
                }
            });
            
            // save icon
            eos.menu.action.new({ // salvar
                id       : "icon_tkt_save",
                title    : "salvar",
                subtitle : "ticket",
                group    : "icon_tkt",
                click    : function(){
                    form.save(); 
                }
            });
            
            /**
             *   icone finalizacao
             */
            eos.menu.action.new({ 
                id       : "icon_tkt_action_finalizar",
                title    : "finalizar",
                subtitle : "ticket",
                group    : "icon_tkt_end",
                click    : function(){
                    chamado.finalizar(); // finalizar
                }
            });
            
            // cancelar
            eos.menu.action.new({ 
                id       : "icon_tkt_cancelar",
                title    : "cancelar",
                subtitle : "ticket",
                group    : "icon_tkt_end",
                click    : function(){
                    chamado.cancelar();
                }
            });
            
            
            
            /**
             *   icones edicao
             */
            
            // encaminhar
            eos.menu.action.new({ 
                id       : "icon_tkt_action_encaminhar",
                title    : "encaminhar",
                subtitle : "ação",
                group    : "icon_tkt_action",
                click    : function(){
                    chamado.acoes.new('encaminhar'); // novo box acao
                    \$("#icon_tkt_action_executar, #icon_tkt_action_encaminhar").remove(); // remove icones
                    // form.isChange(true); // tranca formulario
                    
                    eos.menu.action.hide("icon_tkt_action_finalizar");
                    eos.menu.action.show(["icon_tkt_save","icon_tkt_new","icon_tkt_imprimir"]);
                    
                    // posiciona visualizacao da acao
                    \$("#DTouchPages_chamado_center").scrollTop(\$("#DTouchPages_chamado_center").height()+200);
                    \$("#acao_descrp_interno_new").focus();
                }
            });
            
            // executar
            eos.menu.action.new({ 
                id       : "icon_tkt_action_executar",
                title    : "executar",
                subtitle : "ação",
                group    : "icon_tkt_action",
                click    : function(){
                    chamado.acoes.new(); // novo box acao
                    \$("#icon_tkt_action_executar, #icon_tkt_action_encaminhar").remove(); // remove icones
                    // form.isChange(true); // tranca formulario
                    
                    eos.menu.action.hide("icon_tkt_action_finalizar");
                    eos.menu.action.show(["icon_tkt_save","icon_tkt_new","icon_tkt_imprimir"]);
                    
                    // posiciona visualizacao da acao
                    \$("#DTouchPages_chamado_center").scrollTop(\$("#DTouchPages_chamado_center").height()+200);
                    \$("#acao_descrp_interno_new").focus();
                }
            }); 
            
            // print icon
            eos.menu.action.new({ // imprimir
                id       : "icon_tkt_imprimir",
                title    : "imprim",
                subtitle : "o.s.",
                group    : "icon_tkt",
                click    : function(){
                    chamado.print(); 
                }
            });
            
            // reabrir
            eos.menu.action.new({ 
                id       : "icon_tkt_reabrir",
                title    : "reabrir",
                subtitle : "ticket",
                group    : "icon_tkt",
                click    : function(){
                    chamado.reopen(); 
                }
            });
            
            
            // recorrente
            eos.menu.action.new({ 
                id       : "icon_tkt_recorrente",
                title    : "recorrente",
                subtitle : "ticket",
                group    : "icon_tkt",
                click    : function(){
                    // form.reset(); 
                    \$("#tkt_recorrente").toggleClass("tkt_recorrente_show",function(){
                        \$("#acoes_first_container").toggleClass("acoes_first_container_recorrente");
                    });
                }
            });
            
            
            /*
            // edit icon
            eos.menu.action.new({ // editar
                id       : "icon_tkt_edit",
                title    : "editar",
                subtitle : "ticket",
                group    : "icon_tkt",
                click    : function(){
                    chamado.edit(); 
                }
            });
            */
            
            // eos.menu.action.show(['icon_tkt_save',"icon_tkt_imprimir"]);
            
            // esconde icones 
            eos.menu.action.hide(["icon_tkt_action_encaminhar","icon_tkt_action_executar","icon_tkt_action_finalizar", "icon_tkt_imprimir","icon_tkt_cancelar","icon_tkt_reabrir"]);
            
            
            /**
             *  Cliente do Parceiro
             *      usuario tipo 99
             */
            if("$USER->{tipo}" === "99") {
                // remove icones
                eos.menu.action.destroy('icon_tkt_action_encaminhar');
                eos.menu.action.destroy('icon_tkt_cancelar');
                eos.menu.action.destroy('icon_tkt_action_executar');
                eos.menu.action.destroy('icon_tkt_action_finalizar');
                eos.menu.action.destroy('icon_tkt_imprimir');
                
                \$(".acao_item_descrp").addClass("hidden");
                \$(".acao_item_executor_descrp").addClass("cliente_parceiro_descrp");
            }
        },
        // esconde
        hide : function(){
            
        },
        // listagem
        list : function(){
            
        }   
    }
}

// quando o documento esta pronto 
\$(document).ready(function(){
    /* 
    *   gerar caches
    */
    eos.core.getList("tkt_acao_tipo"); // tipo da acao
    eos.core.getList("tkt_prioridade"); // prioridade do ticket
    
    /*
    *   inicializa objetos do modulo
    */
	empresa = new Empresa(); // inicia objeto empresa
	chamado = new Chamado(); // inicia objeto chamado
	// chamado_menu = new menu(['icon_tkt_save','icon_tkt_new']); // inicia objeto menu
    // chamado_menu = new menu(); // inicia objeto menu    
    
	form = new Form(); // inicia objeto formulario
	form.initialize(); // inicializa formulario
	// form.reset(); // reseta formulario
	
	});
</script>

</head>
<body>

<form name='CAD' id='CAD' class="chamado_form">
	
<!-- Paginas Touch -->
<div id="DTouchPages_chamado">
	
	<!-- Pagina Central -->
	<div id="DTouchPages_chamado_center">
		
		<!-- dados basicos -->
		<div id="dados_container">
			
			<!-- cliente / endereco -->
			<div id="cliente_container">
				<div id="cliente_descrp_container" class='DTouchBoxes_title DTouchBoxes_title_input'>
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
                    <div id="email_add_btn"></div>
				</div>
				<div id="emails_list" class="DTouchBoxes_line_list_input_title"></div>
			</div>
            
			<!-- executor 
                usado em V2 alpha 1
			<div id="executor_container">
				<div class='DTouchBoxes_title DTouchBoxes_title_input'>
                    <input type="text" name="executor" id="executor" placeholder="Executor Principal" />
				</div>
			</div>
            -->
		</div>
        
		
		<!-- Acoes -->
		<div id="acoes_container">
			
			<!-- primeira acao -->
			<div id="acoes_first_container" class="DTouchBoxes_nolimit">
			
				<!-- protocolo de abertura -->
				<div class="DTouchBoxes_line DTouchBoxes_line_text">
                    <div id="responsavel_container">
                        <span id="responsavel"></span>
                    </div>
                    <div id="protocolo_protocolo">
					    <span id="protocolo" ></span>
                    </div>
                    <div id="protocolo_data">
					    <span id="data_inclusao" ></span>
                    </div>
				</div>
			
				<!-- data_previsao -->
				<div id="data_previsao_container" class="DTouchBoxes_line DTouchBoxes_line_input">
					<div id="data_previsao_container_datetime">
						<input type="text" name="data_previsao" id="data_previsao" placeholder="Previsão de atendimento" />
					</div>
					<div id="data_previsao_container_time">
						<input type="text" name="tempo_previsao" id="tempo_previsao" placeholder="Previsão"/>
					</div>
				</div>
			
				<!-- solicitante / solicitacao -->
				<div id="solicitante_solicitacao_container" class="DTouchBoxes_line">
					<div id="solicitante_solicitacao_container_solicitante" class="DTouchBoxes_line_input">
						<input type="text" name="solicitante" id="solicitante" placeholder="Solicitante"/>
					</div>
					<div id="solicitante_solicitacao_container_solicitacao" class="DTouchBoxes_line_textarea">
						<textarea id="descrp" name="descrp" placeholder="Solicitação"></textarea>
					</div>
					<div id="cancelado_container" class="DTouchBoxes_line_input">
						<span id="cancelado" class="descrp_show"></span>
					</div>
				</div>			
			</div>
            
            <div id="tkt_status"><span>criado</span></div>
            
            <div id="tkt_recorrente" class="DTouchBoxes DTouchBoxes_nolimit">
                <div id="tkt_recorrente_line_a" class="DTouchBoxes_line">
                    <div id="tkt_recorrente_line_a_a">repetir a cada (dias)</div> 
                    <div id="tkt_recorrente_line_a_b"><input type="text" id="recorrente_dia" name="recorrente_dia"></div>
                    <div id="tkt_recorrente_line_a_c"></div>
                </div>
                <div id="tkt_recorrente_line_b" class="DTouchBoxes_line">
                    <div id="tkt_recorrente_line_b_a">até a data</div>
                    <div id="tkt_recorrente_line_b_b"><input type="text" id="recorrente_data_final" name="recorrente_data_final"></div>
                    <div id="tkt_recorrente_line_b_c">(<input type="checkbox" id="recorrente_eterno" name="recorrente_eterno"> eterno)</div>
                </div>
            </div>
		
			<div id="chamado_acoes"></div>
		</div>
	</div>









	<!-- Pagina Direita
	<div id="DTouchPages_chamado_right">
	</div>
	     Pagina Esquerda 
	<div id="DTouchPages_chamado_left">
    -->
        
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
        
        <div style="display:none;">
			<div id="filter_status_container">
				| <a class="filter_groups">Abertos</a> 
				| <a class="filter_groups">Vencidos</a> 
				| <a class="filter_groups">Fechados</a> 
				| <a class="filter_groups">Excluidos</a> |
                
				<!-- Se for supervisor, campo de pesquisa por tecnico -->
				<div id="filter_tec_container">
					Técnico:
					<input type="text" name="filter_tec" id="filter_tec" placeholder="Técnico"/>
				</div>
			
				<!-- Limpador de filtros -->
				<div id="icon_clear" alt="Limpar pesquisa">	</div>
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
    <input type='hidden' name='RECOD' id="RECOD" />
    <input type='hidden' name='finalizado' id="finalizado" />
    <input type='hidden' name='responsavel' id="responsavel_codigo" />
</form>

<!--
/*
*   Template, acoes
*/  

****** template v2 alpha 1

<div class='eos_template_chamado_acoes acao_item_container DTouchBoxes_nolimit' style='display:none;'>
    <input type='hidden' name='acao_codigo' />
    
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
        <div class='acao_item_executor'>
            <input/>
        </div>
        <div class='acao_item_tipo'>
            <select></select>
        </div>
    </div>
    <div class='acao_item_data_container DTouchBoxes_line DTouchBoxes_line_input'>
        <div class='acao_item_data_execucao'>
            <input/>
        </div>
        <div class='acao_item_tempo'>
            <input/>
        </div>
        <div class='acao_item_cfg'>
            <div class='acao_item_cfg_interno'>
                <input/>
            </div>
            <div class='acao_item_cfg_sigiloso'>
                <input/>
            </div>
        </div>
    </div>
</div>


****** template v2-rc
-->
<div class='eos_template_chamado_acoes acao_item_container DTouchBoxes_nolimit' style='display:none;'>
    <input type='hidden' class="acao_codigo" />
    
    <div class='acao_item_protocolo_container DTouchBoxes_line DTouchBoxes_line_input'>
        <div class='acao_item_usuario'></div>
        <div class='acao_item_protocolo' style="display:none;"></div>
        <div class='acao_item_data_execucao'>
            <input/>
        </div>
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
    <!--
    <div class='DTouchBoxes_line DTouchBoxes_line_input acao_last_line'>
        <div>Mais</div>
    </div>
    -->
</div>



</body></html>
HTML
