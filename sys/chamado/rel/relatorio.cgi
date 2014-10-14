#!/usr/bin/perl

$nacess = "49";
require "../../cfg/init.pl";
$ID = &get('ID');

print $query->header({charset=>utf8});

print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html id="html">
<head>
	
<script language='JavaScript'>
/**
 *   relatorio
 *       obj relatorio
 */
function Relatorio(){
    
    this.initialize = function(){
        
    };
    
    /**
     *  Lista de acoes
     */
    this.genList = function() {

        if(!\$("#competencia").fieldDateTime("value") || !\$("#empresa").val()) {
            \$.DDialog({ 
                type    : "alert",
                message : "Competência e Cliente devem ser selecionados !"
            });
            
            return false;
        }
        
    	\$.DActionAjax({
    		action       : "relatorio_acoes.cgi",
    		loader       : \$("#relatorio_tkt_acao_list"),
            postFunction : function(){
                // eos.menu.action.show(["icon_rel_save"]); //,"icon_insert"]);
                eos.menu.action.show("icon_rel_gerar");
            }
    	});    
    };
    
    /**
     *  Lista de relatorios gerados
     */
    this.list = function() {
            
    	\$.DActionAjax({
    		action : "relatorio_list.cgi",
    		loader : \$("#relatorio_list"),
            serializeForm : false
    	});    
    };
    
    /**
     *  Lista de clientes para cobrar
     */
    this.clientesList = function() {
            
    	\$.DActionAjax({
    		action : "relatorio_clientes_list.cgi",
    		loader : \$("#clientes_list"),
            serializeForm : false
    	});    
    };
    
    
    /**
     *  Encerrar Relatorio
     */
    this.encerrar = function() {
        
        \$.DDialog({
           type    : "confirm",
           message : "Encerrar ?",
           btnYes  : function(){
               \$.DActionAjax({
                   action : "relatorio_submit.cgi",
                   req    : "encerrar=1",
                   postFunction : function(){
                       form.edit();
                   }
               });
           }
        });
    }
    
    /**
     *  Reativar Relatorio
     *      all = reativa todos e deleta o relatorio gerado
     *      id  = reativa item
     */
    this.reativar = function(item) {
        if(!item){
            item = {
                item : "",
                val  : "all"
            };
        }        
        
        if(item.val === "all"){
            var msg = "Reativar todos os itens e remover relatório";
        } else {
            var msg = "Reativar somente o item selecionado ";
        }
        
        
        // confirma reativacao
        \$.DDialog({
           type    : "confirm",
           message : msg,
           btnYes  : function(){
               \$.DActionAjax({
                   action : "relatorio_reativar.cgi",
                   req    : "reativar="+item.val,
                   loader : false,
                   postFunction : function(){
                       if(item.val !== "all"){
                           item.item.remove();
                       }
                   }
               });
           }
        });
    }
    
    /**
     *  Totais, atualiza
     */
    this.totais = function(i) {
        
        var p = i.plano;
        var t = i.tipo;
        
        /* calcula total plano */
        // calcula itens executados
        var item_executado_plano = 0;
        \$("input[name=item_executado_"+p+"]").each(function(){
            item_executado_plano += eos.core.time.toSum(\$(this).val());
        });
        
        // calcula itens faturados
        var item_faturado_plano = 0;
        \$("input[name=item_faturado_"+p+"]").each(function(){
            item_faturado_plano += eos.core.time.toSum(\$(this).val());
        });
        
        var te = eos.core.time.toShow(item_executado_plano);
        \$("input[name=totais_executado_"+p+"]")
            .val(te.h+":"+te.m)
            .parent()
            .find("span")
                .text(te.h+":"+te.m+"h");
        
        var tf = eos.core.time.toShow(item_faturado_plano);
        \$("input[name=totais_faturado_"+p+"]")
            .val(tf.h+":"+tf.m)
            .parent()
            .find("span")
                .text(tf.h+":"+tf.m+"h");
        
        
        /* calcula total plano + tipo */
        // calcula itens executados
        var item_executado_plano = 0;
        \$(".item_executado_"+p+"_"+t+"").each(function(){
            item_executado_plano += eos.core.time.toSum(\$(this).val());
        });

        // calcula itens faturados
        var item_faturado_plano = 0;
        \$(".item_faturado_"+p+"_"+t+"").each(function(){
            item_faturado_plano += eos.core.time.toSum(\$(this).val());
        });

        var te = eos.core.time.toShow(item_executado_plano);
        \$("input[name=totais_executado_"+p+"_"+t+"]")
            .val(te.h+":"+te.m)
            .parent()
            .find("span")
                .text(te.h+":"+te.m+"h");

        var tf = eos.core.time.toShow(item_faturado_plano);
        \$("input[name=totais_faturado_"+p+"_"+t+"]")
            .val(tf.h+":"+tf.m)
            .parent()
            .find("span")
                .text(tf.h+":"+tf.m+"h");
                        
                        
        /*
            recalcular totais por planos quando atualizados
        */
        
        // recalcula totais
        var total_executado = 0;
        \$(".totais_executado_"+p).each(function(){
            total_executado += eos.core.time.toSum(\$(this).val());
        });
        te = eos.core.time.toShow(total_executado);
        \$("input[name=totais_executado_"+p+"]")
            .val(te.h+":"+te.m)
            .parent()
            .find("span")
                .text(te.h+":"+te.m+"h");
        
        var total_faturado = 0;
        \$(".totais_faturado_"+p).each(function(){
            total_faturado += eos.core.time.toSum(\$(this).val());
        });
        tf = eos.core.time.toShow(total_faturado);
        \$("input[name=totais_faturado_"+p+"]")
            .val(tf.h+":"+tf.m)
            .parent()
            .find("span")
                .text(tf.h+":"+tf.m+"h");
        
        
        // recalcula totais
        var total_executado = 0;
        \$(".totais_executado").each(function(){
            total_executado += eos.core.time.toSum(\$(this).val());
        });
        te = eos.core.time.toShow(total_executado);
        \$("input[name=totais_executado]").val(te.h+":"+te.m);
        \$("#totais_executado_text").text(te.h+":"+te.m+"h");
        
        var total_faturado = 0;
        \$(".totais_faturado").each(function(){
            total_faturado += eos.core.time.toSum(\$(this).val());
        });
        tf = eos.core.time.toShow(total_faturado);
        \$("input[name=totais_faturado]").val(tf.h+":"+tf.m);
        \$("#totais_faturado_text").text(tf.h+":"+tf.m+"h");
    };
}


/*
*   Form
*       obj formulario
*/
function Form(){
    /** 
     *  initialize 
     */
    this.initialize = function(){
        
		this.page = \$("#relatorio_page").DTouchPages({
            pageChange : "left",
            pageCenter : \$("#relatorio_page_center"),
            pageRight  : \$("#relatorio_page_right"),
            pageLeft   : \$("#relatorio_page_left"),
			postFunctionCenter : function() {
                eos.menu.action.appear();
            },
			postFunctionRight : function() {
                eos.menu.action.disappear();
                relatorio.list();
            },
			postFunctionLeft : function() {
                eos.menu.action.disappear();
                relatorio.clientesList();
            },
			onCreate : function() {    
                relatorio = new Relatorio(); // Relatorio obj
                
                \$("#form_container").DTouchBoxes();
                
                // cria campos
    			\$("#empresa").fieldAutoComplete({ 
    				type : "empresa"
    			});
                
                eos.template.field.text(\$("#descrp"));
                
                \$("#finalizado").fieldCheckbox({
                    label      : "Somente Finalizados ?",
                    labelCheck : "Somente Finalizados !"
                });
                \$("#finalizado").hide();
                
                \$("#encerrar").fieldCheckbox({
                    label      : "Encerrar ?",
                    labelCheck : "Encerrado !"
                });
                
                \$("#competencia").fieldDateTime({
                    type         : "year-month",
                    postFunction : function(x){
                    }
                });
                
                
                
                eos.template.field.hide(\$("#descrp"));
                \$("#obs").hide();
                \$("#encerrar_container").hide();
                
                
                // se for edicao
                if(\$("#COD").val()){
                    form.edit();
                }
            }
        });
        
        this.menu();
    };

    
    /**
     *  Novo
     */
    this.new = function(){
        \$.DDialog({
           type    : "confirm",
           message : "Novo ?",
           btnYes  : function(){
               eos.core.call.module.tkt_rel();
           }
        });
        /*
        // salva 
    	\$.DActionAjax({
    		action: "relatorio_submit.cgi"
    	});
        */
    };
    
    /**
     *  Reset
     *      reinicia formulario
     */
    this.reset = function(){
        \$("#obs").val("");
        \$("#descrp").val("");
        \$("#COD").val("");
        
        eos.menu.action.hideAll();
        eos.menu.action.show("icon_rel_gerar");
    }
    
    /**
     *  Editar
     */
    this.edit = function(x){
        
        if(x){ // ajusta campo cod
            \$("#COD").val(x);
        }
        
        // limpar div container
        \$("#relatorio_tkt_acao_list").empty();
        
        // esconde icone
        eos.menu.action.hide("icon_rel_gerar");
        
        // pagina central 
        \$("#relatorio_page").DTouchPages("page","center");
        
        // executa
    	\$.DActionAjax({
    		action       : "relatorio_acoes_edit.cgi",
    		loader       : \$("#relatorio_tkt_acao_list"),
            postFunction : function(){
                eos.menu.action.show(["icon_rel_pdf","icon_rel_xls"]); // "icon_insert",
            }
    	});  
    };
    
    /**
     *  Salvar
     */
    this.save = function(){
        
        /*
        // ajusta lista de itens para salvar no relatorio
        var itens = [];
        \$("input[name=relatorio_tkt_acao_list_radios]").each(function(){
            var f = document.createElement("input");
                f.type  = "hidden";
                f.name  = "itens";
                f.value = \$(this).val();
                
            itens.push(f);
        })
        \$("#itens").html(itens);
        <div id="itens"></div>
        */
        
        // salva 
    	\$.DActionAjax({
    		action: "relatorio_submit.cgi"
    	});
    };
    
    /**
     *  Imprimir
     */
    this.print = function(x){
        
        // xls
        if(x) {
    	    \$.DActionAjax({
    	        action       : "relatorio.xls"
            });
            
            return true;
        }
        
        // pdf
    	\$.DActionAjax({
    		action       : "relatorio.pdf"
    	}); 
    };
    
    /**
     *  menu 
     */
    this.menu = function(){

        eos.menu.action.new({ // gerar
            id       : "icon_rel_gerar",
            title    : "gerar",
            subtitle : "relatorio",
            click    : function(){
                form.save();
                // relatorio.genList();
                // \$(".check").css("opacity","0");
                // eos.menu.action.hide("icon_rel_gerar");
                // eos.menu.action.show("icon_rel_save");
            }
        });
        
        // salvar
        eos.menu.action.new({ 
            id       : "icon_rel_save",
            title    : "salvar",
            subtitle : "",
            click    : function(){
                form.save();
            }
        });
        eos.menu.action.hide("icon_rel_save");
        
        // imprimir
        eos.menu.action.new({ 
            id       : "icon_rel_xls",
            title    : "excel",
            subtitle : "",
            click    : function(){
                form.save();
                form.print("xls");
            }
        });
        eos.menu.action.hide("icon_rel_xls");
        
        // imprimir
        eos.menu.action.new({ 
            id       : "icon_rel_pdf",
            title    : "pdf",
            subtitle : "",
            click    : function(){
                form.save();
                form.print();
            }
        });
        eos.menu.action.hide("icon_rel_pdf");
        
        // encerrar
        eos.menu.action.new({ 
            id       : "icon_rel_encerrar",
            title    : "encerrar",
            subtitle : "",
            click    : function(){
                relatorio.encerrar();
            }
        });
        eos.menu.action.hide("icon_rel_encerrar");
        
        // reativar
        eos.menu.action.new({ 
            id       : "icon_rel_reativar",
            title    : "cancelar",
            subtitle : "",
            click    : function(){
                relatorio.reativar();
            }
        });
        eos.menu.action.hide("icon_rel_reativar");
        
        // eos.menu.action.hide("icon_rel_gerar");
        // eos.menu.action.show(["icon_rel_gerar_new","icon_rel_gerar"]);
    }
}


/*
*   Document Ready
*/
\$(document).ready(function() { 
    form = new Form();
    form.initialize();
    
    /**
     *  ajustes visuais box com totais 
     */
    // inicia fechado
    \$("#totais_container").hide(); 
    // \$("#totais_container").addClass("totais_container_close").hide(); 
    // \$("#totais_header_icon").addClass("totais_header_icon_up");
    // \$("#totais").hide();
    
    // adiciona funcionalidades no box
    \$("#totais_header_icon").click(function(){
        // fecha container totais
        \$("#totais_container").toggleClass("totais_container_close", function(){
            \$("#totais").toggle();
        });
        // icon up
        \$(this).toggleClass("totais_header_icon_up");
    });
});

</script>
</head>
<body>

    <!-- Formulario -->
    <form>
	
        <!-- DTouchPages -->
        <div id="relatorio_page">
            
            <!-- Page Center -->
            <div id="relatorio_page_center">
                
                <!-- container center top -->
                <div class="relatorio_container_center_top">
                    
                    <!-- filter generator -->
                    <div id="form_container">
                        
                        <div id="line_one" class="DTouchBoxes_line DTouchBoxes_line_input">
                            <!-- competencia -->
                            <div id="competencia_container">
                                <input type="text" id="competencia" name="competencia" placeholder="Competência" />
                            </div>
                        
                            <!-- cliente -->
                            <div id="empresa_container">
                                <input type="text" id="empresa" name="empresa" placeholder="Cliente" />
                            </div>
                        
                            <!-- outras opcoes -->
                            <div id="competencia_opt_container">
                                <input type="checkbox" id="finalizado" name="finalizado" />
                            </div>
                            
                            <!-- observacoes -->
                            <div id="obs_container">
                                <textarea id="obs" name="obs" placeholder="Observações para cliente"></textarea> 
                            </div>
                            
                            <!-- descricao -->
                            <div id="descrp_container">
                                <input type="text" id="descrp" name="descrp" placeholder="Descrição Interna" /> 
                            </div>
                            
                        </div>
                        
                    </div>
                </div>
                
                <!-- container center -->
                <div class="relatorio_container_center">
                    
                    <!-- lista de acoes geradas -->
                    <div id="relatorio_tkt_acao_list"></div>
                    
                    <!-- totais -->
                    <div id="totais_container">
                        <div id="totais_header" class="totais_header"><span id="totais_header_icon"></span> Totais <span id="totais_header_total"></span></div>
                        <div id="totais"></div>
                    </div>
                </div>
                
            </div>
        
        
            <!-- Page Left -->
            <div id="relatorio_page_left">
                
                    <!-- lista clientes para cobranca -->
                    <div id="clientes_list"></div>
                    
            </div>
            
            <!-- Page Right -->
            <div id="relatorio_page_right">
                
                <!-- container lista 
                <div id="relatorio_list_container">
                    -->
                    <!-- lista de relatorios gerados -->
                    <div id="relatorio_list"></div>
                    <!--
                </div>
                -->
                
            </div>
        </div>
        
    	<!-- variaveis de ambiente -->
    	<input type='hidden' name='COD' id="COD" value='$COD'>
    </form>
    
</body>
</html>

HTML

