#!/usr/bin/perl

$nacess = "204";
require "../cfg/init.pl";
#$COD = &get('COD');
# $COD  = $USER->{'empresa'};
$empresa   = &get('empresa');
# $endereco  = &get('endereco');
# $MODO = &get('MODO');

# pega endereco da empresa
if($empresa) {
    $DB = DBE("
        select 
            codigo
        from 
            empresa_endereco as ee
        where 
            empresa = $empresa
    ");

    if($DB > 0) {
        while($e = $DB->fetchrow_hashref) {
            $endereco = $e->{codigo};
        }
    }
}


print $query->header({charset=>utf8});


print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html id="html">
<head>
  
<script>

/**
 *   Dados TI
 *       obj 
 */
function DadosTI(){
    var d = this;
    
    /* initialize */
    this.initialize = function(){
        
	\$("#dadosti_pages").DTouchPages({
            pageDisable : true,
            pageCenter  : \$("#dadosti_pages_center"),
            pageRight   : \$("#dadosti_pages_right"),
            postFunctionLeft : function() { 
                \$("#menu_actions").addClass("menu_actions_guaca");
                \$("#main_container").addClass("main_container_guaca");
                eos.menu.action.hide(["icon_dti_save"]);
                eos.menu.action.show(["icon_dti_export"]);
            },
			postFunctionCenter : function() { 
                \$("#menu_actions").removeClass("menu_actions_guaca");
                \$("#main_container").removeClass("main_container_guaca");
                eos.menu.action.hide(["icon_dti_save"]);
                eos.menu.action.show(["icon_dti_export"]);
           
                if(!\$("#itens").DTouchRadio("value")){
                    \$("#dadosti_pages").DTouchPages("disable","right"); // desabilita slide right
                }
            },
			postFunctionRight : function() {
                eos.menu.action.show(["icon_dti_save"]);
                eos.menu.action.hide(["icon_dti_edit"]);
                eos.menu.action.hide(["icon_dti_export"]);
            },
			onCreate : function() {
    
                \$("#agrupamentos_container").DTouchBoxes({
                    title : "Agrupamentos"
                });
    
                \$("#grupos_container").DTouchBoxes({
                    title : "Grupos"
                });
            
            
                \$("#form_item_container").DTouchBoxes({
                    title : "Editar Item"
                });
            
            
                var ttitle  = "<div class='DTouchRadio_list_title'>";
                    ttitle += "     <div style='width:47%'>Cliente</div> ";
                    ttitle += "	    <div style='width:30%'>Endereço</div> ";
                    ttitle += "	    <div style='width:10%'>Cidade</div> ";
                    ttitle += "	    <div style='width:10%'>UF</div> ";
                    ttitle += "</div>";
                \$("#enderecos_container").DTouchBoxes({ title: ttitle });
                \$("#agrupamentos").DTouchRadio({
                    orientation : "vertical",
                    // visibleItems : 5,
                    cacheFromFile : {
                        key  : "dadosti_agrupamentos",
                        file : "agrupos_cache.cgi"
                    },
                        click       : function(x){
                        d.search.reset();

                        d.grupo.list(x.value);
                    },
                    uncheck : function(){
                        d.search.reset();
                        d.grupo.list();
                    }
                });
            
                // grupos
                \$("#grupos").DTouchRadio({
                    orientation : "vertical",
                    // visibleItems : 5,
                    cacheFromFile : {
                        key  : "dadosti_grupos",
                        file : "grupos_cache.cgi"
                    },
                 click       : function(x){
                    
                        // limpa campo de pesquisa
                        d.search.reset();
                        
                        // d.empresa.list(x.value);
HTML
if($empresa eq "")
	{
print<<HTML;
			d.itens.list();
HTML
	}
else
	{
print<<HTML;
			if(\$("#enderecos").DTouchRadio("value"))
				{
				d.itens.list();
				}
HTML
	}
print<<HTML;

                    },
                    uncheck : function(){
                        d.search.reset();
                        d.itens.list();
                    }
                });
            
            
            
            
                /* enderecos
                var title  = '<div class=\"DTouchRadio_list_title\">';
                    title += '	<div style=\"width:47%\">Nome</div> ';
                    title += '	<div style=\"width:30%\">Endereço</div> ';
                    title += '	<div style=\"width:10%\">Cidade</div> ';
                    title += '	<div style=\"width:10%\">Uf</div> ';
                    title += '</div>';
                 */
                \$("#enderecos").DTouchRadio({
                    orientation : "vertical",
                    // title   : title,
                    // uncheck : false,
                    // visibleItems : 5,
                    cacheFromFile : {
                        key  : "dadosti_enderecos",
                        file : "empresas_cache.cgi"
                    },
                    click       : function(x){
                        // limpa campo de pesquisa
                        d.search.reset();
                  
                        \$("#"+x.radios_id).find("input[type=radio]").each(function(){
                            if(\$(this).val() === x.value) {                                
                                \$("#EMPRESA").val(\$(this).parent().find("input[name=empresa]").val());
                                \$("#ENDERECO").val(x.value);
                                d.itens.list(x.value,\$(this).parent().find("input[name=endereco]").val());
                            }
                        });
                        eos.menu.action.show(["icon_dti_export"]);
                    },
                    uncheck : function(){
                        d.search.reset();
HTML
if('$empresa' ne '')
	{
	print "                        \$(\"#itens\").DTouchRadio(\"reset\",\"content\");\n";
	}
else
	{                        
	print "                        d.itens.list();\n";
	}
print<<HTML;
			eos.menu.action.hideAll();
                    }
                });
            
                // seta focus campo principal
                \$("#search").focus();
                
                
                if(\$("#endereco").val()) {
                    \$("#enderecos").DTouchRadio("value",\$("#endereco").val());
                }
            
            }
        });
        
        this.menu();
        
        
        
        this.itens.initialize();
        this.search.initialize();
    };
    
    /* search */
    this.search = {
        reset : function(){
            \$("#search").DSearch("reset");
        }
    };
    
    /* agrupamentos */
    this.agrupamento = {
        
        list : function(e) {
            if(!e) {
                e = 0;
            }
        	
            \$("#agrupamentos").DTouchRadio("reset","content");
                
            \$.DActionAjax({
        		action       : "agrupos.cgi",
        		// req          : req,
			loader       : \$("#agrupamentos_container"),
        		postFunction : function(x) {
				var a = JSON.parse(x);
				a.agrupos.forEach(function(a){
				    d.agrupamento.add(a);
			});
		
		}
            });
        },
        
        add : function(a) {
            
            \$("#agrupamentos").DTouchRadio("addItem",{
                val    : a.value,
                descrp : a.descrp
            });
        }
    };
    
    
    /* grupos */
    this.grupo = {
        
        list : function(agrupo, end) {
            
            \$("#grupos").DTouchRadio("reset","content");
        
    	    var req = "&COD=1"+"&agrupo="+agrupo+"&endereco="+end;
            
            \$.DActionAjax({
    			action : "grupos.cgi",
    			req    : req,
			loader : \$("#grupos_container"),
    			postFunction: function(x) {
				var a = JSON.parse(x);
				a.grupos.forEach(function(a){
					d.grupo.add(a);
				});
    			}
    		});
        },
        
        add : function(g) {
            
            \$("#grupos").DTouchRadio("addItem",{
                val    : g.value,
                descrp : g.descrp
            });            
        }
    };
    
    
    /** 
     *  itens 
     */
    this.itens = {
        item : {
            codigo : ""
        },
        initialize : function(){
            \$("#itens").DTouchRadio({
                title       : "<div></div>",
                uncheck     : false,
                orientation : "vertical",
                click       : function(x){
                    d.search.reset();
                    
                    \$("#dadosti_pages").DTouchPages("disable","right"); // desabilita slide right
                    
                    d.itens.edit(x.value);
                    
                    if(\$("#enderecos").DTouchRadio("value"))
			  {
			  eos.menu.action.show(["icon_dti_new"]);
			  eos.menu.action.show(["icon_dti_export"]);
		    }
		},
                uncheck : function(){
                    eos.menu.action.hide(["icon_dti_del"]);
                    eos.menu.action.hide(["icon_dti_edit"]);
                    eos.menu.action.hide(["icon_dti_access"]);
                }
            });
        },
        
        list : function(empresa, endereco) {
            var o = {
                empresa  : \$("input[name=enderecos_radios]:checked").parent().find("input[name=empresa]").val(),
                endereco : \$("#enderecos").DTouchRadio("value"),
                grupo    : \$("#grupos").DTouchRadio("value"),
                agrupo   : \$("#agrupos").DTouchRadio("value")
            }
            
            if(!o.grupo) {
                \$("#itens").DTouchRadio("reset","content");
                eos.menu.action.hideAll();
                return false;
            }
            
            // variaveis para envio
    		var req = "&agrupo="+o.agrupo+"&grupo="+o.grupo+"&endereco="+o.endereco+"&empresa="+o.empresa;
                     
            \$.DActionAjax({
    			action : "itens.cgi",
    			req    : req,
			loader : \$("#itens_container"),
    			postFunction: function(x) {     // console.log(x);
 	
                    
			// limpa OBJ
			\$("#itens").DTouchRadio("reset","content");
			var its = JSON.parse(x);
			its.itens.forEach(function(i){ // console.log(i);
			    d.itens.add(i);
			});
			
			\$("#itens .DTouchRadio_title").html(its.title);
			
			// ajusta rolagem do radio 
			\$("#itens_container").css("margin-top","50px");
			\$("#itens_container .DTouchRadio_title").css("margin-top","-40px");
		    
			if(\$("#enderecos").DTouchRadio("value"))
			     {
			     eos.menu.action.show(["icon_dti_new"]);
			     eos.menu.action.show(["icon_dti_export"]);
			}
			
			\$("#itens_container .DTouchRadio_list_title").width(\$("#itens_container .DTouchRadio_list_line").width());
			}
    		});
            
            // se estive em edicao nao mexe nos botoes
            if(\$("#dadosti_pages").DTouchPages("page") !== "right") { 
            }
        },
        
        add : function(i) {
            
            \$("#itens").DTouchRadio("addItem",{
                val    : i.value,
                descrp : i.descrp
            });            
        },
        
        // editar item
        edit : function(i) { 
            eos.menu.action.hide(["icon_dti_access"]);
            eos.menu.action.show(["icon_dti_edit","icon_dti_del"]);
            
            \$("input[name=itens_radios]").each(function(){
                
                if(\$(this).val() === i) {
                 
                    // ajusta dados para acesso
                    d.itens.item = {
                        codigo   : i,
                        tipo     : \$(this).parent().find("input[name=tipo]").val(),
                        externo  : \$(this).parent().find("input[name=externo]").val(),
                        acesso   : \$(this).parent().find("input[name=acesso]").val(),
                        porta    : \$(this).parent().find("input[name=porta]").val(),
                        login    : \$(this).parent().find("input[name=login]").val(),
                        password : \$(this).parent().find("input[name=password]").val()
                    }
                    
                    // mostra botao de acesso
                    if(d.itens.item.tipo === "rdp" || d.itens.item.tipo === "ssh" || d.itens.item.tipo === "http" || d.itens.item.tipo === "https" || d.itens.item.tipo === "ftp" || d.itens.item.acesso) {
                        eos.menu.action.show(["icon_dti_access"]);
                    }
                    
                }
            });
        },
        
        // acesso
        access : function() {
            var it = d.itens.item;
            
            // acesso guacamole
            if(it.tipo === "rdp" || it.tipo === "ssh") { 
                
                // popula formulario
                document.querySelector("form[name=guacamole] input[name=ID]").value       = document.querySelector("form[name=AUX] input[name=ID]").value;
                document.querySelector("form[name=guacamole] input[name=protocol]").value = it.tipo;
                document.querySelector("form[name=guacamole] input[name=host]").value     = it.externo;
                document.querySelector("form[name=guacamole] input[name=port]").value     = it.porta;
                document.querySelector("form[name=guacamole] input[name=username]").value = it.login;
                document.querySelector("form[name=guacamole] input[name=password]").value = it.password;
                
                // abrir em nova janela                
                var gua = document.getElementsByName("guacamole")[0];
                    gua.action = "/sys/menu/start.cgi";
                    gua.target = "_blank";
                    gua.submit();
                
                \$("#dadosti_pages").DTouchPages("page","left");
                
            } else if(it.acesso) { // acesso http direto
                // form
                var form = document.createElement("form");
                    form.id     = "dti_acesso";
                    form.name   = "dti_acesso";
                    form.method = "POST";
                    form.target = "_blank";
                    form.action = it.externo;
                
                // campos
                var f = new FormData(form);
                    f.append('login', it.login);
                    f.append('password', it.password);
                   
                // envia e remove dados 
                \$('body').append(form); 
                form.submit();
                delete form;
                
            // acesso http generico
            } else if(it.tipo === "http" || it.tipo === "https" || it.tipo === "ftp") { 
                var form = document.createElement("form");
                    form.id     = "dti_acesso_http";
                    form.name   = "dti_acesso_http";
                    form.method = "POST";
                    form.target = "_blank";
                    form.action = it.externo;
                    
                // envia e remove dados 
                \$('body').append(form); 
                form.submit();
                delete form;
            }
        },
    };
    
    
    /** 
     *  form preview
     */
    this.form = {
        
        /* salvar */
        save : function() {
            d.form.update();
        },
    
        /* editar */
        edit : function(x){
        
        },
    
        /* novo */
        new : function(){ 
            d.itens.item.codigo = "";
            d.form.preview(true);
        },
    
        /* reset */
        reset : function(){
        },
    
        /* enable */
        enable : function(){
        },
    
        /* disable */
        disable : function(){
        },
        
        preview : function(new_item) {
            if(!new_item){
                new_item = "";
            }
            
            // se for novo item seleciona primeira linha e depois limpa para funcionamento do modulo
            if(!d.itens.item.codigo) {
                if(!\$("#grupos").DTouchRadio("value") || (!\$("#enderecos").DTouchRadio("value") && !\$("#itens").DTouchRadio("value"))) {
                    \$.DDialog({ 
                        type    : "alert",
                        message : "Você deve selecionar ao menos um grupo e uma empresa ou item para novo cadastro !" 
                    });
                    
                    return false
                }
                
                new_item = true;
                d.itens.item.codigo = \$("#itens").DTouchRadio("value"); // pega linha para template
            }
            
            \$("#dadosti_pages").DTouchPages("enable","right"); // habilita slide right
            \$("#dadosti_pages").DTouchPages("page","right"); // roda pagina para direita
            
            var o = {
                empresa  : \$("input[name=enderecos_radios]:checked").parent().find("input[name=empresa]").val(),
                endereco : \$("#enderecos").DTouchRadio("value"),
                grupo    : \$("#grupos").DTouchRadio("value"),
                agrupo   : \$("#agrupos").DTouchRadio("value")
            }
            
            // se nao selecionado empresa
            if(!\$("#enderecos").DTouchRadio("value")) {
                o.empresa  = \$("input[name=itens_radios]:checked").parent().find("input[name=empresa]").val();
                o.endereco = \$("input[name=itens_radios]:checked").parent().find("input[name=endereco]").val();
            }
            
            // se for novo item
            if(new_item) {
                d.itens.item.codigo = "";
            }
            
            var req = "&agrupo="+o.agrupo+"&grupo="+o.grupo+"&endereco="+o.endereco+"&empresa="+o.empresa+"&linha="+d.itens.item.codigo+"&empresa_nome="+\$("input[name=enderecos_radios]:checked").parent().find(".DTouchRadio_list_line div:first-child div").text()+"&grupo_nome="+\$("input[name=grupos_radios]:checked").next().text()+"&insert="+new_item;
                        
            \$.DActionAjax({
    			action : "item_detail.cgi",
    			req    : req,
			loader : \$("#dadosti_pages_right"),
    			postFunction: function(x) { // console.log(x); return;
                    
                    \$("#form_item").html(x);
                                        
                    // ajusta campos
                    \$("#form_item input[type=text]").each(function(){
                        eos.template.field.text(\$(this));
                    });
                    
                    
                    // remove duplicados se for o caso
                    \$('#form_item [id]').each(function (i) {    
                        var ids = \$('[id="' + this.id + '"]');    
                        if (ids.length > 1) {
                            \$('[id="' + this.id + '"]:gt(0)').remove();
                        }
                    });
                    
                    
                    // se for novo item limpa campos
                    if(new_item) {
                         \$("#form_item input[type=text]").val("");
                         \$("#itens").DTouchRadio("reset"); // limpa radio 
                    }
    			}
    		});
        },
        
        // atualiza item
        update : function() {
            \$("#dadosti_pages").DTouchPages("page","right");
            
            var o = {
                empresa  : \$("input[name=enderecos_radios]:checked").parent().find("input[name=empresa]").val(),
                endereco : \$("#enderecos").DTouchRadio("value"),
                grupo    : \$("#grupos").DTouchRadio("value"),
                agrupo   : \$("#agrupos").DTouchRadio("value")
            }
            
            // se nao selecionado empresa
            if(!\$("#enderecos").DTouchRadio("value")) {
                o.empresa  = \$("input[name=itens_radios]:checked").parent().find("input[name=empresa]").val();
                o.endereco = \$("input[name=itens_radios]:checked").parent().find("input[name=endereco]").val();
            }
                
            var req = "&agrupo="+o.agrupo+"&grupo="+o.grupo+"&endereco="+o.endereco+"&empresa="+o.empresa+"&linha="+d.itens.item.codigo;
                        
            \$.DActionAjax({
    		    action : "edit_submit.cgi",
    		    req    : req,
		    loader : \$("#dadosti_pages_right"),
    			postFunction: function(x) {
                    
			try {
			    var r = JSON.parse(x); 
			    if(r.status === "error"){
				\$.DDialog({
				    type    : "error",
				    message : r.message
				});
			    }
                        
			    // atualiza listagem
			    d.itens.list();
	      
			    } catch(e) {
				return;
			    }
                    
    			}
    		}); 
        },
        
        // deleta item
        del : function() {
            
            // se nao item selecionado
            if(!d.itens.item.codigo){
                \$.DDialog({
                    type    : "error",
                    message : "Um item deve ser selecionado" 
                });
                return false;
            }
            
            
            \$("#dadosti_pages").DTouchPages("page","center");
            
            var o = {
                empresa  : \$("input[name=enderecos_radios]:checked").parent().find("input[name=empresa]").val(),
                endereco : \$("#enderecos").DTouchRadio("value"),
                grupo    : \$("#grupos").DTouchRadio("value"),
                agrupo   : \$("#agrupos").DTouchRadio("value")
            }
            
            // se nao selecionado empresa
            if(!\$("#enderecos").DTouchRadio("value")) {
                o.empresa  = \$("input[name=itens_radios]:checked").parent().find("input[name=empresa]").val();
                o.endereco = \$("input[name=itens_radios]:checked").parent().find("input[name=endereco]").val();
            }
                
            var req = "&agrupo="+o.agrupo+"&grupo="+o.grupo+"&endereco="+o.endereco+"&empresa="+o.empresa+"&linha="+d.itens.item.codigo;
            
            // Limpa formulário antes de excluir
            \$("#form_item").html('');
            
            \$.DActionAjax({
    			action : "edit_submit.cgi",
    			req    : req,
			loader : \$("#dadosti_pages_right"),
    			postFunction: function(x) {
                    
			try {
			    var r = JSON.parse(x);
			    if(r.status === "error"){
				\$.DDialog({
				    type    : "error",
				    message : r.message
				});
			    }
			    
			    // atualiza listagem
			    d.itens.list();
			    
			    } catch(e) {
				return;
			    }
                    
    			}
    		}); 
        }
    };
    
    
    /* enderecos */
    this.empresa = {
        
        list : function(grupo) {
            
    		var req = "&COD=11"+"&grupo="+grupo;
            
    		$ajax_init 
		\$.DActionAjax({
    			action : "enderecos.cgi",
    			req    : req,
			loader : \$("#enderecos_container"),
    			postFunction: function(x) {
    			}
    		});
        },
        
        add : function(g) {
            
            \$("#grupos").DTouchRadio("addItem",{
                val    : g.value,
                descrp : g.descrp
            });            
        },
        
        export : function() {

            var o = {
                empresa  : \$("input[name=enderecos_radios]:checked").parent().find("input[name=empresa]").val(),
                endereco : \$("#enderecos").DTouchRadio("value"),
            }
            
	    if(!\$("#enderecos").DTouchRadio("value")) {
		\$.DDialog({ 
		    type    : "alert",
		    message : "Você deve selecionar uma empresa!" 
		});
		
		return false
	    }            

            // variaveis para envio
	    var req = "&endereco="+o.endereco+"&empresa="+o.empresa;
	    
	    \$.DActionAjax({
    		action : "/sys/dadosti/dados_ti.xls",
    		req    : req
    	    });
	},
    };
    
    
    /* search global */
    this.search = {
        initialize : function(){
            \$("#search_container").DTouchBoxes();
            \$("#search").DSearch({
                linha:'Dsearch',
                campo: \$("#search"),
                exclude: "DTouchRadio_nosearch",
                all : true
            });
            eos.template.field.search(\$("#search"));
            
            \$("#search").keydown(function(e){
        		if(e.keyCode == 13){
        			e.preventDefault();
                }
            });
            
            document.getElementById("corpo").scrollTop = 0;
        },
        reset : function(){
            \$("#search").DSearch("reset");
            
            // coloca foco no item selecionado
            // grupos
            if(\$("#grupos").DTouchRadio("value")) {
                \$("#grupos").DTouchRadio("slide");
            }
            
            //  enderecos
            if(\$("#enderecos").DTouchRadio("value")) {
                \$("#enderecos").DTouchRadio("slide");
            }
            
            
            \$("#search").focus();
        }
    };



    /* menu */
    this.menu = function(){

        eos.menu.action.new({ // novo
            id       : "icon_dti_new",
            title    : "novo",
            subtitle : "dti",
            click    : function(){
                d.form.new();
            }
        });    
    
        eos.menu.action.new({ // salvar
            id       : "icon_dti_save",
            title    : "salvar",
            subtitle : "dti",
            click    : function(){
                d.form.save();
            }
        });
    
        eos.menu.action.new({ // edit
            id       : "icon_dti_edit",
            title    : "editar",
            subtitle : "dti",
            click    : function(){
                d.form.preview();
            }
        });
        
        eos.menu.action.new({ // del
            id       : "icon_dti_del",
            title    : "delete",
            subtitle : "dti",
            click    : function(){
                // testa se delete or not
                \$.DDialog({
                    type    : "confirm",
                    message : "Deseja realmente remover o item selecionado <br> essa ação é irreversivel !",
                    btnNo   : function(){
                        return false;
                    },
                    btnYes  : function(){
                        d.form.del();
                    }
                });
            }
        });

        eos.menu.action.new({ // exportação
            id       : "icon_dti_export",
            title    : "exportar",
            subtitle : "dti",
            click    : function(){
                 d.empresa.export();
            }
        });
    
        eos.menu.action.new({ // acess
            id       : "icon_dti_access",
            title    : "acesso",
            subtitle : "dti",
            click    : function(){
                d.itens.access();
            }
        });
        
        // esconde icones
    eos.menu.action.hideAll();
    };


}




/**
 *   Document Ready
 */
\$(document).ready(function() { 

    \$("#itens_container").height(\$(window).height()-360);
    dadoti = new DadosTI();
    dadoti.initialize();
    
    if('$empresa' != '')
	   {
    	grid = \$("form:first");
    	grid.find('#enderecos .DTouchRadio').hide();	
    	\$("#enderecos").DTouchRadio('val','$endereco');
    	

        \$('#enderecos .DTouchRadio').each(
            function()
                {
                if(\$(this).html().indexOf('name="empresa" value="$empresa"') != -1) 
                    {
                    \$(this).show();
                    }
                });


	   }
    else
	   {
	   \$('#enderecos div.DTouchRadio').addClass('Dsearch');
	   }
    \$('#grupos div.DTouchRadio').addClass('Dsearch');
    \$("#search").focus();
	
});
</script>
</head>
<body style="overflow-x: hidden; overflow-y: scroll;">

<form>

    <div id="dadosti_pages">
        
        <div id="dadosti_pages_center">
            
            <div id="search_container">
                <input type="text" name="search" id="search" placeholder="Pesquisar... ">
            </div>
            
            <div class="center_container">
                <!-- 
                <div id="agrupamentos_container">
                    <div id="agrupamentos"></div>
                </div>
                -->
                <div id="enderecos_container">
                    <div id="enderecos"></div>
                </div>
                
                <div id="grupos_container">
                    <div id="grupos"></div>
                </div>
                
            </div>
            
            
            <div id="itens_container">
                <div id="itens" style="margin-right:0px"></div>
            </div>
            
            
        </div>
        
        
        <div id="dadosti_pages_right">
            <div id="form_item_container">
                <div id="form_item"></div>
            </div>
        </div>
        
        
        <div id="dadosti_pages_left">
            <iframe name="guacamole_cli" id="guacamole_cli" scrolling="auto" frameborder="0" framespacing="0" allowtransparency="true" src="about:blank"></iframe>
        </div>
        
    </div>

    <input type='hidden' name='endereco' id='endereco' value='$endereco'>
    <input type='hidden' name='empresa' id='empresa' value='$empresa'>
</form>

<form name='dfirewall' method='post' target='main'>
	  <input type='hidden' name='usernamefld'>
	  <input type='hidden' name='passwordfld'>
	  <input type='hidden' name='login' value='Login'>
</form>

</body></html>
HTML
