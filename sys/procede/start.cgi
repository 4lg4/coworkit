#!/usr/bin/perl

#
# start.cgi
#
# Lista de todos os procedimentos 
#

$nacess = "207";
require "../cfg/init.pl";

$ID = &get('ID');
$EMPRESA = &get('empresa');
$MODO = &get('MODO');

print $query->header({charset=>utf8});


print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html id="html">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">

	
<script language='JavaScript'>

	DLoad("procedimentos"); // carrega dependencias especificas

		
	function Form(){
		this.initialize = function(){
			eos.menu.action.new({ // inclusão
				id       : "icon_procede_new",
				title    : "Novo",
				click    : function(){
					  procede.edit('');
				}
			});			
			eos.menu.action.new({ // edição
				id       : "icon_procede_edit",
				title    : "Editar",
				click    : function(){
					  procede.edit(\$('#codigo').val());
				}
			});
			eos.menu.action.new({ // exclusão
				id       : "icon_procede_delete",
				title    : "Excluir",
				click    : function(){
					  eos.DAction.delete();
				}
			});
			eos.menu.action.new({ // exportar PDF
				id       : "icon_procede_pdf",
				title    : "PDF",
				subtitle : "exportar",
				click    : function(){
					  procede.pdf(\$('#codigo').val());
				}
			});
			eos.menu.action.new({ // cancelar
				id	: "icon_procede_save",
				title: "salvar",
				click	: function(){
					form.save();
				}
			});
			eos.menu.action.new({ // cancelar
				id	: "icon_procede_cancel",
				title: "cancelar",
				click	: function(){
					form.cancel();
				}
			});
		};
		//eos.menu.action.disappear();

		this.save = function(){
			if(! \$("#titulo").val()) {
				\$.DDialog({message:"Você não preencheu o título do procedimento!", focusBack:\$("#titulo")});
				return false;
			}
			if(! \$("#procedimento").val()) {
				\$.DDialog({message:"Você não preencheu a descrição do procedimento!", focusBack:\$("#procedimento-wysiwyg-iframe")});
				return false;
			}
			
			\$("input[name=tags_list_radios]").each(function(){ 
				var field = document.createElement("input"); 
				field.type = "hidden"; 
				field.name = "tags_list"; 
				field.value = \$(this).val();
				\$("#tags_container").append(field);
			})


			\$.DActionAjax({
				action        : "edit_submit.cgi",
				loader        : \$("#defaults_container"),
				target        : "#resultado",
				serializeForm : true
				});
		};
		
		this.cancel = function(){
			eos.menu.action.hide('icon_save');
			eos.menu.action.hide('icon_procede_cancel');
			if(\$('#codigo').val()) {
				eos.menu.action.show('icon_procede_new');
				eos.menu.action.show('icon_procede_edit');
				eos.menu.action.show('icon_procede_delete');
				procede.view(\$('#codigo').val());
			} else {
				\$('#DTouchPages_default').DTouchPages('page','right');
				}
		};
	}
	
	function Procede(){
		this.view = function(c){

			\$('#defaults_container').html("<iframe onLoad='document.getElementById(\\\"wysiwyg\\\").style.height=(wysiwyg.document.body.scrollHeight)+\\\"px\\\"' name='wysiwyg' id='wysiwyg' style='border: 0; width: 100%; height: 100%'></iframe>");
			document.forms[0].action = '/sys/procede/view.cgi';
			document.forms[0].target = 'wysiwyg';
			document.forms[0].submit();
			eos.menu.action.hide('icon_save');
			eos.menu.action.hide('icon_procede_cancel');			
			eos.menu.action.show('icon_procede_new');
			eos.menu.action.show('icon_procede_edit');
			eos.menu.action.show('icon_procede_delete');
			eos.menu.action.show('icon_procede_pdf');
			};

		this.edit = function(c){
		
			\$.DActionAjax({
				action        : "/sys/procede/edit.cgi",
				req           : "codigo="+c+"\&empresa=$EMPRESA",
				loader        : \$("#defaults_container"),
				target        : "#defaults_container",
				serializeForm : false,
				postFunction  : function(){
					eos.menu.action.show('icon_procede_save');
					if(\$('#codigo').val()) {
						eos.menu.action.show('icon_procede_cancel');
						}
					eos.menu.action.hide('icon_procede_new');
					eos.menu.action.hide('icon_procede_edit');
					eos.menu.action.hide('icon_procede_delete');
					eos.menu.action.hide('icon_procede_pdf');
					}
				});
			};			
			
		this.pdf = function(c){
			document.forms[0].action = '/sys/procede/procedimento.pdf';
			document.forms[0].target = '_blank';
			document.forms[0].submit();
			};
			
		this.pdf2 = function(c){

			\$.DActionAjax({
				type          : "download",
				action        : "procedimento.pdf",
				req           : "codigo="+c,
				target        : "_blank",
				serializeForm : false,
				postFunction  : function(){
				      /*
				      *   executa acoes apos finalizacao do carregamento do arquivo ajax,
				      *   mesmo com erro essa funcao eh startada 
				      */
				      }
				});
			};
			
		this.list = function(c){
			// executa lista de procedimentos
			\$.DActionAjax({
				req: "empresa=$EMPRESA",
				action: "start_list.cgi",
				loader: \$("defaults_list_container"),
				serializeForm: false,
				});
			};
			
		}

	// cria pagina touch padrao
	\$("#DTouchPages_default").DTouchPages(
		{
		// editable:true,
		// pageChange: "$PAGE",
		pageChange: "center",
		// pageLeft: false, // \$("#DTouchPages_default_left"),
		pageRight: \$("#DTouchPages_default_right"),
		postFunctionRight : function() {
			eos.menu.action.appear();
			},
		pageCenter: \$("#DTouchPages_default_center"),
		postFunctionCenter : function() {
			eos.menu.action.disappear();
			}
		});
	
	
	\$(document).ready(function(){
	
		// DBox upload
		\$("#bloco_upload").DTouchBoxes({title:"Arquivos Anexos"});
	
		procede = new Procede(); // inicia objeto default
		form = new Form();
		form.initialize();
		
		eos.menu.action.disappear();
		procede.edit('');
		
		procede.list();
		});
</script>
</head>
<body>
<form name='CAD' id='CAD' class="default_form">
	
	<!-- Paginas Touch -->
	<div id="DTouchPages_default">
		
		<div id="DTouchPages_default_center">
			<div id="defaults_list_container"></div>		
		</div>
		
		<div id="DTouchPages_default_right">
			<div id="defaults_container"></div>
		</div>
		
	</div>

	<!-- retorno do codigo -->
	<div id="resultado" class="DDebug"></div>

	<!-- variaveis de ambiente -->
	<input type='hidden' name='codigo' id="codigo" />
	<input type='hidden' name='empresa' id="empresa" value='$EMPRESA' />
</form>


</body>
</html>
HTML
	
exit;
	
