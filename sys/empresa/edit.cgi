#!/usr/bin/perl

$nacess = "201";
require "../cfg/init.pl";
$COD = &get('COD');
$MODO = &get('MODO');

$EMPNEW = &get('EMPNEW');

$avatar = &get('avatar');

# se parceiro e nao DONE
if(($COD eq $USER->{empresa} && $USER->{empresa_cad} && $USER->{empresa_cad} ne "1") || ($COD eq $USER->{empresa_cad})) {
    $COD = $USER->{empresa_cad};
    
    if(!$avatar){
        $avatar = "show";
    }
}

print $query->header({charset=>utf8});

print<<HTML;

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html id="html">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">

<script type="text/javascript">
	// Carrega as dependencias do módulo
	DLoad('empresa');

/*
//	Modo EDITAR Actions quando clicado ---
	function editar()
		{
		top.Loading();
		document.forms[0].target = "_self";
		document.forms[0].action = "edit.cgi";
		document.forms[0].MODO.value = 'editar';
		document.forms[0].submit();
		}
*/		
//	icone Exportar Actions quando clicado ---
	function exportar() {
		\$.DActionAjax({
			action : "$dir{'relat'}empresas.xls",
		});
	}

//	icone Imprimir Actions quando clicado ---
	function imprimir() {
		\$.DActionAjax({
			action : "rel_empresas.pdf"
		});
    }
		
//	icone Cancelar Actions quando clicado ---
	function DActionDelete() {
                
        \$.DDialog({
            type    : "confirm",
            message : "Você tem certeza que deseja excluir essa empresa? <br> Essa ação é IRREVERSÍVEL!",
            btnYes  : function(){
            	\$.DActionAjax({
            		action        : "edit_submit_delete.cgi",
                });
            }
        });
	}


/* [INI] --------------------------------------------------------------------------------------------------------------------------
	 Editar
---------------------------------------------------------------------------------------------------------------------------------*/
function DActionEdit() { 
	\$.DActionAjax({
		action        : "edit_db_frm.cgi",
		req           : "&COD="+\$("#COD").val(),
        serializeForm : false,
		postFunction  : function(data) {
        }
	});
}	
/* [END] Editar ------------------------------------------------------------------------------------------------------------- */





/* --------------------------------------------------------------------------------------------------------------------------------
	[INI] Document READY 
		Quando Documento já estiver completamente carregado
---------------------------------------------------------------------------------------------------------------------------------*/
\$(document).ready(function() {
	// Loading();
    
	// gera cache
    // eos.core.getList("uf");            // uf brasil
    // eos.core.getList("pais");          // lista de paises
    // eos.core.getList("tipo_endereco"); // tipos de enderecos
    eos.core.getList("tipo_contato");  // tipo de contatos
    
    
    
    // ao sair do nome replica no apelido
    \$("#nome").focusout(function(){
        if(!\$("#apelido").val()){
            \$("#apelido").val(\$("#nome").val());
        }
    });
    
	
	
	// abas groupos
	\$("#grupos_tabs").tabs();
	
	// abas dados pricipais / bancos / documentos
	\$("#top_tabs").tabs({
		show: function( event, ui ) {
			// btn upload
			if(ui.index == 2) {
				eos.menu.action.show("icon_empresa_upload");
            } else {
                eos.menu.action.hide("icon_empresa_upload");
            }
		}
	});
	
	
	// bancos
	\$("#banco_codigo_form").fieldAutoComplete(
		{ 
		sql_tbl:"bancos"
		// postFunction:"bancoAdd()"
		});
		
	// update bancos list
	\$("#banco_icon_update").click(function()
		{
		// junta todos inputs da linha
		var linha = \$("input:radio[name='bancos_list_radios']:checked").next().find('input[type=hidden]');
		
		// navega entre os inputs da linha
		linha.each(function()
			{
			// atualiza input hidden da lista
			\$(this).val(\$("#"+\$(this).prop('name')+"form").val());

			// atualiza descricao
			\$(this).next('span').text(\$("#"+\$(this).prop('name')+"form").val());
			
			// ajuste para campo autocomplete field
			if(\$(this).prop('name') == 'banco_codigo_')
				\$(this).next('span').text(\$("#"+\$(this).prop('name')+"form_descrp").val());
			});	
		});
	
            
	// adiciona bancos list
	\$("#banco_icon_add").click(function(e){
        
		// testa campos
		if(\$("#banco_codigo_form").val() == "" || \$("#banco_agencia_form").val() == "" || \$("#banco_conta_form").val() == "") {
			\$.DDialog({
                message : "Campos Banco, Agência, Conta Corrente devem ser preenchidos !"
            });
			return false;
		}
        
		// gen. the line to add into a list object
		var fields  = "<div><input type='hidden' value='"+\$("#banco_codigo_form").val()+"' name='banco_codigo_'> <span>"+\$("#banco_codigo_form_descrp").val()+"</span></div>";
			fields += "<div><input type='hidden' value='"+\$("#banco_agencia_form").val()+"' name='banco_agencia_'> ag. <span>"+\$("#banco_agencia_form").val()+"</span></div>";
			fields += "<div><input type='hidden' value='"+\$("#banco_conta_form").val()+"' name='banco_conta_'> c/c. <span>"+\$("#banco_conta_form").val()+"</span></div>";
			fields += "<div><input type='hidden' value='"+\$("#banco_obs_form").val()+"' name='banco_obs_'> <span>"+\$("#banco_obs_form").val()+"</span></div>";
		
        // limpa campos apos inclusao
        \$("#banco_codigo_form_descrp, .banco_form").val("");
        
		// add line
		\$("#bancos_list").DTouchRadio("addItem",{
            val    : 'add-'+\$("input[name=banco_codigo_]").length, 
            descrp : fields
        });
	});
		
	// var aaa = {val:'add', descrp:'fields'};
	
	// console.log(DListGet("bancos"));
	// var aaa = undefined;
	// console.log(DListGetVar);
	// console.log("modulo");
	
	// unLoading();
	
	//\$("#select_test").DList(
	//	{ 
	//	table:"bancos",
	//	type:"select"
	//	});
	
	// carrega enderecos
	// DActionAjax("enderecos.cgi"); 
    \$.DActionAjax({
        action : "enderecos.cgi"
    });
	
	// ajusta formulario em modo visualizacao
	// DActionForm('ver');
	
	\$("#empresa_nome").DTouchBoxes({ type:"bar" });
	// \$("#top_tabs_container").DTouchBoxes();


    /* text inputs do formulario principal */
    \$("#empresa_nome input[type=text]").each(function(){
        eos.template.field.text(\$(this));
    });
    \$(".banco_form").each(function(){
        eos.template.field.text(\$(this));
    });
    
    // inicia objs
    contato  = new Contato();
    endereco = new Endereco();
    empresa  = new Empresa();
    empresa.initialize();
    
	// popula formulario
	DActionEditDB();
});



/**
 *  Endereco Obj
 */
function Endereco() {
    var end = this;
    
    /**
     *  Initialize
     */
    this.initialize = function(){
    };
    
    
    /**
     *  Add
     */
    this.add = function(){    
        var add = new Date().getUTCMilliseconds();
	
        \$.DActionAjax({
            action : "enderecos.cgi",
            req    : "add="+add,
            loader : \$("#end_tabs")
        });
    };

    /**
     *  Del
     */
    this.del = function(conf){
        \$.DDialog({
            type    : "confirm",
            message : "Deseja realmente excluir o endereço atual ?",
            btnYes  : function(){
                \$('#end_tabs').tabs("remove", "#"+\$('#end_tabs .ui-tabs-panel[aria-hidden="false"]').prop('id'));
            }
        });
    };
}
    


/**
 *  Contato Obj
 */
function Contato() {
    var cont = this;
    
    /**
     *  Initialize
     */
    this.initialize = function(){
    };
    
    
    /**
     *  Add
     */
    this.add = function(){    
    	\$.DActionAjax({
    		action        : "contatos.cgi",
            req           : "add="+\$("#end_tabs .ui-tabs-active").prop("id")+"&id_add="+\$(".contatos_form").length+1,
            serializeForm : false,
            loader        : \$(".endereco_contatos:visible")
        });
    };

    /**
     *  List
     */
    this.list = function(cod){
    	\$.DActionAjax({
    		action        : "contatos.cgi",
            req           : "end="+cod,
            serializeForm : false,
            loader        : \$(".endereco_contatos:visible")
        });
    };
}


/**
 *  Empresa Obj
 */
function Empresa() {
    var emp = this;
    
    /**
     *  Initialize
     */
    this.initialize = function(){
        
        // menu
        this.menu.initialize();
        
        // avatar
        if("$avatar" === "show"){
            this.avatar.initialize();
            emp.tkt.hide();
        } else if("$avatar" !== ""){
            this.avatar.initialize();
            this.avatar.auto();
            \$("#top_tabs").tabs('option', 'selected', 3);
        } else {
            \$("#avatar_tab").hide();
            
            emp.tkt.initialize();
        }
        
        
        /* edicao */
        if(\$("#COD").val()) {
            // inicia upload
            this.upload.initialize();
            
        } else { // novo
            
            \$("#upload_tab").hide();
            \$("#avatar_tab").hide();
        }
        
        
        
        // ajusta pages
		\$("#empresa_page").DTouchPages({
            pageCenter : \$("#empresa_page_center"),
            pageRight  : \$("#empresa_page_right"),
			postFunctionCenter : function() {
                \$("#search").focus();
                eos.menu.action.hideAll();
                eos.menu.action.show(['icon_empresa_novo']);
                emp.list();
            },
			postFunctionRight : function() {
                eos.menu.action.hideAll();
            	emp.menu.edit();
            },
			onCreate : function() {
			    if(\$("#COD").val() || "$EMPNEW" === "yes"){
                    \$("#empresa_page").DTouchPages("page","right");            
			    }
                
                // pesquisa global
                \$("#search_container").DTouchBoxes();
                \$("#search").DSearch({
                    linha:'DTouchRadio',
                    campo: \$("#search"),
                    exclude: "DTouchRadio_nosearch",
                    all : true
                });
                eos.template.field.search(\$("#search"));
			}
        });
    };
    
    /** 
     *  list, 
     *      lista de usuarios 
     */
    this.list = function() {
        \$.DActionAjax({
            action : "edit_list.cgi",
            loader : \$("#empresa_list")
        });
    };
    
    /** 
     *  Edit, 
     *      modo de edicao
     */
    this.edit = function() {
        this.menu.list();
        
    };
    
    /** 
     *  Menu, 
     *      menus
     */
    this.menu = {
        initialize : function(){
            // menu action v2
            menu_emp = new menu();
            
            // menu action v3
            eos.menu.action.new({ // novo
                id       : "icon_empresa_novo",
                title    : "novo",
                subtitle : "empresa",
                click    : function(){
                    if(eos.core.limit.empresa.verify()){ // dentro do limite
                        call("/sys/empresa/edit.cgi",{ EMPNEW : "yes" });
                    } else {
                        top.\$.DDialog({
                            type    : "error",
                            message : "Limite de empresas excedido ! <br><br> Become a premium !" 
                        });
                    }
                }
            });
            eos.menu.action.new({ // editar
                id       : "icon_empresa_edit",
                title    : "editar",
                subtitle : "empresa",
                click    : function(){
                    call("/sys/empresa/edit.cgi",{ COD : \$("#empresa_list").DTouchRadio("value") });
                }
            });
            eos.menu.action.new({ // salvar
                id       : "icon_empresa_save",
                title    : "salvar",
                subtitle : "empresa",
                click    : function(){
                    empresa.save();
                }
            });
            eos.menu.action.new({ // Dados TI
                id       : "icon_empresa_dti",
                title    : "TI",
                subtitle : "dados",
                click    : function(){
                    var emp;
                    
                    if(\$(".DTouchPages_right_active").length === 1) {
                        emp = \$("#COD").val();
                    } else {
                        emp = \$("#empresa_list").DTouchRadio("value");
                    }
                    
            		\$("#AUX input[name=MODO]").val('ver');
                    \$("#AUX input[name=COD]").val(emp);
                    
                     // if(\$(".empresa_endereco_container_master:first input[name=endereco_codigo]").val()) {
                    //    var end = \$(".empresa_endereco_container_master:first input[name=endereco_codigo]").val();
                    // } else {
                    //      var end = \$("input[name=empresa_list_radios]:checked").parent().find(".DTouchRadio_list_line input[name=list_end]").val();
                        //}

                    // console.log("dados ti ",emp);

                    eos.core.call.module.dadosti({
                        empresa : emp
                    });
                }
            });
            eos.menu.action.new({ // Users
                id       : "icon_empresa_users",
                title    : "usuári.",
                subtitle : "dados",
                click    : function(){
            		\$("#AUX input[name=MODO]").val('ver');
                    \$("#AUX input[name=COD]").val(\$("#empresa_list").DTouchRadio("value"));
            		call("$dir{'dados_user'}dados_users.cgi");
                }
            });
            eos.menu.action.new({ // Computadores
                id       : "icon_empresa_pcs",
                title    : "computad.",
                subtitle : "dados",
                click    : function(){
            		\$("#AUX input[name=MODO]").val('ver');
                    \$("#AUX input[name=COD]").val(\$("#empresa_list").DTouchRadio("value"));
            		call("$dir{'dados_user'}dados_pc.cgi");
                }
            });
            // cria cron se for done
            if("$USER->{empresa}" === "1") { 
                eos.menu.action.new({ // cron
                    id       : "icon_empresa_cron",
                    title    : "cron",
                    subtitle : "",
                    click    : function(){
                		\$("#AUX input[name=MODO]").val('ver');
                        \$("#AUX input[name=COD]").val(\$("#empresa_list").DTouchRadio("value"));
                		call("$dir{'cron'}dados_cron.cgi");
                    }
                });
            }
            eos.menu.action.new({ // procedimento
                id       : "icon_empresa_procedimento",
                title    : "proced.",
                subtitle : "",
                click    : function(){
            		var variaveis = {
            			empresa  : \$("#empresa_list").DTouchRadio("value")
            		};
            		call("procede/start.cgi",variaveis);
                }
            });
            eos.menu.action.new({ // exportar
                id       : "icon_empresa_exportar",
                title    : "export.",
                subtitle : "",
                click    : function(){
                    \$("#CAD input[name=COD]").val(\$("#empresa_list").DTouchRadio("value"));
            		\$.DActionAjax({
            			action : "$dir{'relat'}empresas.xls",
            		});
                }
            });
            eos.menu.action.new({ // imprimir
                id       : "icon_empresa_imprimir",
                title    : "imprim.",
                subtitle : "",
                click    : function(){
                    \$("#CAD input[name=COD]").val(\$("#empresa_list").DTouchRadio("value"));
            		\$.DActionAjax({
            			action : "rel_empresas.pdf"
            		});
                }
            });
            
            // endereco
            eos.menu.action.new({ // novo
                id       : "icon_endereco_add",
                title    : "novo",
                subtitle : "endereco",
                click    : function(){
                    endereco.add()
                }
            });
            eos.menu.action.new({ // del
                id       : "icon_endereco_del",
                title    : "excluir",
                subtitle : "endereco",
                click    : function(){
                    endereco.del();
                }
            });
            
            // contatos
            eos.menu.action.new({ // novo
                id       : "icon_contato_add",
                title    : "novo",
                subtitle : "contato",
                click    : function(){
                    contato.add();
                }
            });
            
            // planos
            eos.menu.action.new({ // novo
                id       : "icon_planos",
                title    : "planos",
                subtitle : "",
                click    : function(){                     
                    eos.core.call.module.planos();
                }
            });
            
            // esconde menus
            eos.menu.action.hideAll();
            
            
            // cria cron se for done
            if("$USER->{empresa}" === "1") { 
                menu_emp.btnShow(['icon_cron']);
            };

        },
        edit : function(){
        	// start menu
        	if("$nacess_tipo" == "a") {
        		menu_emp.btnShow(['icon_empresa_novo','icon_empresa_save','icon_delete','icon_end_new','icon_end_del','icon_contato_new','icon_planos']);
                eos.menu.action.show(["icon_contato_add","icon_endereco_add","icon_endereco_del"]);
        	}
            
        	if("$nacess_tipo" == "s") {
        		menu_emp.btnShow(['icon_empresa_save']);
            }

        	menu_emp.btnShow(['icon_empresa_dti','icon_user','icon_procede','icon_contato','icon_print']);
            
            // cria cron se for done
            if("$USER->{empresa}" === "1") { 
                menu_emp.btnShow(['icon_cron']);
            };
        },
        list : function (){
            eos.menu.action.show([
                'icon_empresa_dti',
                'icon_empresa_users',
                'icon_empresa_pcs',                
                'icon_empresa_cron',
                'icon_empresa_procedimento',
                'icon_empresa_exportar',
                'icon_empresa_imprimir',
                'icon_empresa_edit',
                'icon_empresa_novo',
                'icon_planos'
            ]);
        }        
    };
    
	
    
    /**
     *  Upload
     */
    this.upload = {
        initialize : function(){ 
            \$("#upload_tab").show();
            
            /* botao upload
            eos.menu.action.new({
                id       : "icon_empresa_upload",
                title    : "upload",
                subtitle : "documento",
                click    : function(){
                    \$("#upload_emp").DUpload("upload");
                }
            }); 
            eos.menu.action.hide("icon_empresa_upload");
            */
            
            // inicia lista 
            \$("#upload_list").DTouchRadio({
                orientation : "vertical",
                itemDel     : function(x){
                    eos.core.upload.delete(x);
                },
                click       : function(x){
                    eos.core.upload.download(x.value);
                }
            });
            
            // inicia upload field
            \$("#upload_emp").DUpload({
                link : {
                    tbl    : "empresa",
                    codigo : \$("#COD").val()
                },
                automatic : true,
                postFunction : function(x){ 
                    emp.upload.addNew(x); // adiciona item novo
                    \$("#upload_emp").DUpload("reset"); // limpa campo apos inclusao
                }
            });
        },
        
        /* adiciona novo vindo do campo de upload */
        addNew : function(x){
            var descrp  = "<div class='DTouchRadio_list_line'> "
                descrp += "     <div style='width:20%'>";
                descrp += "         <span>"+ x.type +"</span>";
                descrp += "     </div>";
                descrp += "     <div style='width:66%'>";
                descrp +=           x.descrp;
                descrp += "     </div>";
                descrp += "     <div style='width:10%'>";
                descrp +=           eos.core.math.toMB({value:x.size, decimal:2})+"MB" 
                descrp += "     </div>";
                descrp += "</div>";
            
            \$("#upload_list").DTouchRadio("addItem",{
                val    : x.codigo,
                descrp : descrp
            });
        },
        
        /* adiciona vindo do banco de dados */
        addDb : function(items){
            var up = this;
            
            items.forEach(function(i){
                up.addNew(i);
            });
        }
        
    };
    
    
    /**
     *  Avatar
     */
    this.avatar = {
        auto : function(){
            \$("#imagem").DUpload("focus");
        },
        
        show : function(x){
            if(x) {
                \$("#avatar").prop("src","/sys/cfg/DPAC/view_avatar.cgi?COD="+x+"&ID="+\$("#AUX input[name=ID]").val());
                \$("#CODIMG").val(x);
                
                // troca avatar do menu
                \$("#user_menu_float_avatar_company img").prop("src","/sys/cfg/DPAC/view_avatar.cgi?COD="+x+"&ID="+\$("#AUX input[name=ID]").val());
                
                \$("#avatar_del").show();
            }
        },
        
        del : function(conf){
            
            function delAvatar(){
                eos.core.upload.delete(\$("#CODIMG").val(), function(){
                });
                
                \$("#CODIMG").val("");
                \$("#avatar").prop("src","");    // remove imagem
                \$("#user_menu_float_avatar_company img").prop("src","");   // remove avatar do menu
                \$("#avatar_del").hide();
            }
            
            // sem confirmacao
            if(conf){
                delAvatar();
                return;
            }
             
            \$.DDialog({
                type    : "confirm",
                message : "Deseja remover o avatar ?",
                btnYes  : function(){
                    delAvatar();
                }
            })
        },
        
        initialize : function(){ 
            
            // inicia objeto
            \$("#imagem").DUpload({
                type : "simple",
                link : {
                    tbl    : "empresa_avatar",
                    codigo : \$("#COD").val()
                },
                placeholder : "Imagem Empresa",
                automatic   : true,
                mimetype    : ["image"],
                postFunction : function(x){

                    // deleta imagem antiga
                    if(\$("#CODIMG").val()){
                        empresa.avatar.del(1);
                    } 
                    
                    empresa.avatar.show(x.codigo);
                    \$("#imagem").DUpload("reset");            
                }
            });
            
            
            /* trocar imagem
            \$("#avatar_change").click(function(){
                \$("#imagem").DUpload("reset");
                \$("#imagem").DUpload("focus");
            });
            */
            
            // remove imagem
            \$("#avatar_del").click(function(){
                empresa.avatar.del();
            });
            
        }
        
    };
    
    
    /* [INI] --------------------------------------------------------------------------------------------------------------------------
    	 Salvar
    ---------------------------------------------------------------------------------------------------------------------------------*/
    this.save = function() { 
        
    	// Nome / Apelido 
    	if(\$("#nome").val() == "") //  || \$("#apelido").val() == "")
    		{
    		\$.DDialog({message:"Você deve preencher os campos Nome e Apelido !"});
    		return false;
    		}
	
    	// Tipo empresa (PF / PJ)
    	if(\$("input[name=tipo_emp]").is(':checked') === false)
    		{
    		\$.DDialog({message:"Você deve selecionar o Tipo de Empresa (Fisica / Jurídica) !"});
    		return false;
    		}
    	else 
    		{
    		var nao_salva = "";
    		\$("input[name=doc]").each(function()
    			{
    			if((isDoc(\$(this).val()) != false && isDoc(\$(this).val()) != true) && uc(\$(this).val()) != "ISENTO")
    				nao_salva += \$(this).val()+", ";
    			});
    		if(nao_salva != "")
    			{
    			\$.DDialog({message:"Verfique os documentos digitados ! <br> Devem conter números ou ISENTO <br><br>"+nao_salva});
    			return false;
    			}
    		}
	
    	// endereco, testa se existe 
    	if(\$("input[name=grupos_participantes]").length < 1)
    		{
    		\$.DDialog({message:"Você deve selecionar ao menos um grupo !"});
    		return false;
    		}
		
    	// endereco, testa se existe 
    	if(\$("select[name=endereco_tipo]").length < 1)
    		{
    		\$.DDialog({message:"Você deve criar ao menos um endereço !"});
    		return false;
    		}

    	// endereco principal, testa se existe 
    	var nao_salva = 0;
    	\$("select[name=endereco_tipo] :selected").each(function() { 
            if(\$(this).text().toLowerCase() === "principal") {
    			nao_salva ++;
            }
    	});
    	if(nao_salva != 1) {
    		\$.DDialog({message:"Você deve definir um endereço principal !"});
    		return false;
    	}
	
	
    	// ajusta contatos para salvar
    	var contatos = []; // inicia array
    	var fields = "";
        var contato_dado_check = false;
    	var i = 1;
    	\$(".contatos_container").each(function(){
    		// monta objeto com dados dos contatos
    		var contatos_int = {};
    			contatos_int.id = \$(this).prop("id");
    			contatos_int.descrp = "descrp";
    			contatos_int.tipo = [];
    			contatos_int.valor = [];
		
		
    		var endereco_id = \$(this).parents(".empresa_endereco_container_master").find("input[name=endereco_codigo]").val();
    		var contato_id = \$(this).parents(".contatos_container_dbox").find("[name=contato_cod]").val();
    		var contato_descrp = \$(this).parents(".contatos_container_dbox").find("input[name=contato_descrp]").val();

    		// fields += "<input type='hidden' name='contatos_endereco' value='"+endereco_id+"'>";
    		fields += "<input type='hidden' name='contatos_"+endereco_id+"_id' value='"+contato_id+"'>";
    		fields += "<input type='hidden' name='contatos_"+endereco_id+"_"+contato_id+"_descrp' value='"+contato_descrp+"'>";
			
            // se nao houver nenhum dado no box !
		    if(\$(this).find("[name=field_valor_]").length > 0) {
                
        		// pega conteudo dos campos tipo
        		\$(this).find("[name=field_tipo_]").each(function(){
        			// console.log(\$(this).val());
                        contatos_int.tipo.push(\$(this).val());
                    
        			    fields += "<input type='hidden' name='contatos_"+endereco_id+"_"+contato_id+"_tipo' value='"+\$(this).val()+"'>";
        		});
		
        		// pega conteudo dos campos valor
        		\$(this).find("[name=field_valor_]").each(function(){
        			// console.log(\$(this).val());
                        contatos_int.valor.push(\$(this).val());
                    
        			    fields += "<input type='hidden' name='contatos_"+endereco_id+"_"+contato_id+"_valor' value='"+\$(this).val()+"'>";
        		});
                
        		// adiciona objeto com dados no container principal
        		contatos.push(contatos_int);
                
            } else {
            
                contato_dado_check = true;
            }
            
    		// adiciona objeto com dados no container principal
    		// contatos.push(contatos_int);
            
            
    		// pega contato principal
    		\$(this).parents(".contatos_container_dbox").find(".checkbox_principal").each(function(){
            
                var val = "false";
            
                if(\$(this).is(":checked")) {
                    val = "true";
                }
            
    			// contatos_int.principal.push(val);
		
    			fields += "<input type='hidden' name='contatos_"+endereco_id+"_"+contato_id+"_principal' value='"+val+"'>";
    		});
    	});
        
        // controle do conteudo de cada contato
        if(contato_dado_check) {
    		\$.DDialog({
                type    : "alert",
                message : "Contato sem nenhum dado verifique !"
            });
            
            return false;
        }
        
        
        // enderecos descricao principal, controla se nao vazio
        var para = false;
        
        \$(".empresa_endereco_dados").each(function(){
            if(!\$(this).find("input[name=endereco]").val()){
    		    para = true;
            }
        });
        
        if(para) {
    		\$.DDialog({
                type    : "alert",
                message : "Você deve escrever o endereço ! "
            });
            
            return false;
        }
        
        // contatos principais, controle se algum selecionado
        var para = false;
        
        
        \$(".endereco_contatos").each(function(){
            if(\$(this).find(".contato_title_default_selected").length === 0 && \$(".contatos_container_dbox").length > 0){
    		    para = "- "+\$(this).parent().find("input[name=endereco]").val();
            }
        });
        
        if(para) {
    		\$.DDialog({
                type    : "alert",
                message : "Você deve definir um contato como PRINCIPAL em "+para+" ! <br><br> * clique na estrela ao lado do nome"
            });
            
            return false;
        }
    
    	// adiciona campos para serem serializados
    	\$("#contatos_form_container").html(fields);
	
        
        // Service Desk
        // var tkt_opt = "&tkt_open_status="+\$("input[name=tkt_open]:checked").val();
        if(\$("#tkt_login").val() && \$("#tkt_password").val()) {
            if(!\$("#tkt_login").val() || !\$("#tkt_password").val()) {
        		\$.DDialog({
                    type    : "alert",
                    message : "Você deve definir login (email) e senha para habilitar o Service Desk !"
                });
        		return false;
            }
        }
    
    	// executa
    	\$.DActionAjax({
    		action : "edit_submit.cgi",
    		req    : \$.param(contatos)
    	});
    }
    /* [END] Salvar ------------------------------------------------------------------------------------------------------------- */
 
 
    /**
     *  TKT
     */
    this.tkt = {
        initialize : function(){
            \$("#tkt_login").fieldEmail();
            eos.template.field.password(\$("#tkt_password"));
            // eos.template.field.text(\$("#tkt_password"));
            \$("#tkt_tab").show();
        },
        hide : function(){
            \$("#tkt_tab").hide();
        }
    }
 
    
}

/**
 *  Form Obj
 */
function Form() {
    var f = this;
    
    /**
     *  Initialize
     */
    this.initialize = function(){
    };
}
</script>

</head>
<body>

<form name='CAD' id='CAD' class="empresa_form" method='post'>

    <!-- DTouchPages -->
    <div id="empresa_page">
        
        <!-- Page Center -->
        <div id="empresa_page_center">
                <!-- Pesquisa -->
                <div id="search_container_container">
                    <div id="search_container">
                        <input type="text" name="search" id="search" placeholder="Pesquisar... ">
                    </div>
                </div>
                
                <!-- Lista de empresas -->
                <div id="empresa_list_container">
                    <div id="empresa_list"></div>
                </div>
                
                <!-- limite de usuarios -->
                <div id="empresa_limit"></div>
        </div>
        
        <!-- Page Right -->
        <div id="empresa_page_right">
                    

    <!-- Pagina principal do modulo -->
    <div id="empresa_form_center">
    
        <!-- Nome / Apelido -->
        <div id="empresa_nome">
        	<div class="empresa_nome_descrp">Nome</div>
        	<div class="empresa_nome_field"><input type="text" name="nome" id="nome" maxlength='200' placeholder="Nome"></div>
			
        	<div class="empresa_nome_descrp">Apelido</div> 
        	<div class="empresa_nome_field"><input type="text" name="apelido" id="apelido" maxlength='200' placeholder="Apelido"></div>
        </div>

        <!-- Dados Bancarios / Principais / Arquivos anexos -->
        <div id="top_tabs">
        	<ul>
        		<li><a href="#t-0">Dados Principais</a></li>
        		<!-- <li><a href="#t-1">Mais Dados</a></li> -->
        		<li><a href="#t-2">Dados Bancários</a></li>
        		<li id="upload_tab"><a href="#t-3">Arquivos Anexados</a></li>
                <li id="avatar_tab"><a href="#t-4">Avatar Empresa</a></li>
                <li id="tkt_tab"><a href="#t-5">Service Desk</a></li>
        	</ul>
	
        	<!-- Dados Principais -->
        	<div id="t-0">
		
        		<!-- campos basicos empresa -->
        		<div id="empresa_basic_container">
                    <!-- campos basicos titulo -->
                    <div id="empresa_basic">
        				<div class="empresa_basic_descrp">Tipo</div>
        				<div id="tipo_emp_container"></div>
        				<div id="empresa_basic_ativo">
        						<input type='checkbox' name='ativo' id='ativo' value='true'> <font class='formtxt'>Ativo</font>
        				</div>
                    </div>
                    
			        <!-- campos basicos lista -->
        			<div class="empresa_mais_dados"></div>
        		</div>
	
        		<!-- campo obs -->
        		<div id="empresa_obs">
        			<textarea name='obs' id='obs'>$obs</textarea>
        		</div>	
        	</div>	
	
        	<!-- second tab -->
        	<div id="t-2">
                
                <!-- Dados Bancarios -->
        		<div id="bancos">
                    
                    <!-- Dados Bancarios formulario -->
        			<div id="bancos_title">
        				<div id="banco_codigo_form_container">
        					<input type='text' name="banco_codigo_form" id="banco_codigo_form" placeholder="Banco">
        				</div>
        				<div id='banco_agencia_form_container'>
        					<input type='text' name='banco_agencia_form' id='banco_agencia_form' class="banco_form" maxlength="10" placeholder="Agência">
        				</div>
        				<div id='banco_conta_form_container'>
        					<input type='text' name='banco_conta_form' id='banco_conta_form' class="banco_form" maxlength="20"  placeholder="Conta">
        				</div>
        				<div id='banco_obs_form_container'>
        					<input type='text' name='banco_obs_form' id='banco_obs_form' class="banco_form" maxlength="300"  placeholder="Descrição">
        				</div>
        				<div id="bancos_title_icon">
        					<span class="icon_add" id="banco_icon_add" title="Adicionar nova conta bancária"></span>
        					<span class="icon_update" id="banco_icon_update" title="Atualizar conta bancária"></span>
        				</div>
        			</div>
                    
	                <!-- Dados Bancarios lista -->
        			<div class="lista" id="bancos_list"></div>
        		</div>
        	</div>
	
	
        	<div id="t-3" style="display:none;">
	
        		<!-- Arquivos Anexados -->
                <div id="upload_container">
        		    <div id="upload_form">
        		        <input id="upload_emp" name="upload_emp" />
        		    </div>
                    <div id="upload_list"></div>
                </div>
        	</div>
            
            
            <!-- Imagem da empresa -->
        	<div id="t-4" style="display:none;">
                <div id="imagem_container">
					<input name="imagem" id="imagem" >
				</div>
                <div id="avatar_container">
                    <div id="avatar_change">alterar imagem</div>
                    <div id="avatar_del">remover imagem</div>
                    <img id="avatar">
                </div>
        	</div>
            
            
            <!-- Tkts -->
        	<div id="t-5" style="display:none;">
                <input type="hidden" id="tkt_usuario" name="tkt_usuario">
                <input type="hidden" id="tkt_login_confirm" name="tkt_login_confirm">
                
                <div id="tkt_container">
                    <div class="tkt_line">Configurar Service Desk do cliente</div>
                    <div class="tkt_line">
                        Empresa pode abrir chamados ? 
                        Sim <input type="radio" name="tkt_open" value="false">
                        Não <input type="radio" name="tkt_open" value="true" checked>
    				</div>
                    <div class="tkt_line">
                        <input type="text" id="tkt_login" name="tkt_login" placeholder="Login">
                    </div>
                    <div class="tkt_line">
                        <input type="password" id="tkt_password" name="tkt_password" placeholder="Senha">
                    </div>
                </div>
        	</div>
            
        </div>


        <!-- Grupos Relacionados -->
        <div id="grupos_tabs">
        	<ul>
        		<li><a href="#g-0" title="Arraste o grupo desejado entre listas">Grupos</a></li>
        		<li><a href="#g-1" title="Arraste o técnico desejado entre listas">Técnicos</a></li>
        		<li><a href="#g-2" title="Arraste o plano desejado entre listas">Planos</a></li>
        	</ul>
        	<div id="g-0">

        		<!-- grupos -->
        		<div id="empresa_grupos">
        			<div id="empresa_grupos_part">
        				<div id="empresa_grupos_part_title">
        					<div id='grupo_add_title'>
        						Selecionados
        						<span style="display:none;"><div id="grupo_add_show" class="icon_plus"></div></span>
        					</div>
        					<div id='grupo_add'>
        						<nobr>
        							<div id="grupo_add_img" class="icon_plus"></div>
        							<input type='text' name='grupo_nome' id='grupo_nome' maxlength="100">
        							<div id="grupo_hide_img" class="icon_arrow_right"></div>
        						</nobr>
        					</div>
        				</div>
        				<div id="DVgrupo_showlist"></div>
        			</div>
			
        			<div id="empresa_grupos_exis">
        				<div id="empresa_grupos_exis_title">
        					<div>Disponíveis</div>
        				</div>
        				<div id="DVgrupo_showlist_exis"></div>
        			</div>
        		</div>
		
        	</div>
        	<div id="g-1">
		
        		<!-- tecnicos -->
        		<div id="empresa_tecnicos">
        			<div id="empresa_tecnicos_part">
        				<div id="empresa_tecnicos_part_title">
        					<div>Selecionados</div>
        				</div>
        				<div id="tecnicos_list"></div>
        			</div>
			
        			<div id="empresa_tecnicos_exis">
        				<div id="empresa_tecnicos_exis_title">
        					<div>Disponíveis</div>
        				</div>
        				<div id="tecnicos_list_exis"></div>
        			</div>
        		</div>

		
        	</div>
        	<div id="g-2">
		
        		<!-- planos -->
        		<div id="empresa_planos">
        			<div id="empresa_planos_part">
        				<div id="planos_list"></div>
        			</div>			
        		</div>		
		
        	</div>
        </div>
        
        <!-- enderecos -->
        <div id="end_tabs" style="clear:both; background-color:transparent;" ></div>
		
        <!-- armazena contatos para salvar -->
        <div id="contatos_form_container"></div>
        
    </div> <!-- (end) Pagina principal do modulo -->
	
    	
    <!-- campos formulario principal -->
    <input type='hidden' name='COD' id='COD' value='$COD'>
    <input type='hidden' name='CODIMG' id='CODIMG' >
    <input type='hidden' name='MODO' value='$MODO'>
    
    
    </div> <!-- Page Right -->
    
</form>

<!-- Div de Debug -->
<div id="resultado" class="DDebug"></div>

</body></html>
HTML

