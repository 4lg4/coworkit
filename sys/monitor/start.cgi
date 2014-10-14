#!/usr/bin/perl

#
# start.cgi
#
# Lista de todos os monitoramentos 
#

$nacess = "903";
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

	DLoad("monitoramento"); // carrega dependencias especificas
	
	tickFormatter = function (format, val) {
		if(val > 1048575)
			{
			val = val / 1048576;
			return val.toFixed(0)+"GB";
			}
		else if(val > 1023)
			{
			val = val / 1024;
			if(val < 10)
				{
				return val.toFixed(0)+"MB";
				}
			return val.toFixed(0)+"MB";
			}
		else
			{
			return val.toFixed(0)+"kB ";
			}
	}

		
	function Form(){
		this.initialize = function(){
			eos.menu.action.new({ // inclusão
				id       : "icon_monitor_new",
				title    : "Novo",
				click    : function(){
					  monitor.insert();
				}
			});			
			eos.menu.action.new({ // edição
				id       : "icon_monitor_edit",
				title    : "Editar",
				click    : function(){
					  monitor.edit(\$('#codigo').val());
				}
			});
			eos.menu.action.new({ // exclusão
				id       : "icon_monitor_delete",
				title    : "Excluir",
				click    : function(){
					  eos.DAction.delete();
				}
			});
			eos.menu.action.new({ // salvar
				id	: "icon_monitor_save",
				title: "salvar",
				click	: function(){
					form.save();
				}
			});			
			eos.menu.action.new({ // cancelar
				id	: "icon_monitor_cancel",
				title: "cancelar",
				click	: function(){
					form.cancel();
				}
			});
			\$.DActionAjax({
				action        : "/sys/monitor/edit.cgi",
				req           : "empresa=$EMPRESA",
				loader        : \$("#defaults_container"),
				target        : "#defaults_container",
				serializeForm : false
			});
		};

		this.save = function(){
			if(! \$("#descrp").val()) {
				\$.DDialog({message:"Você não preencheu a descrição do monitoramento!", focusBack:\$("#descrp")});
				return false;
			}
			if(! \$("#show").DTouchRadio("value")) {
				\$.DDialog({message:"Você não informou se é para mostrar o monitoramento!", focusBack:\$("#show")});
				return false;
			}
			
			if(! \$("#codigo_save").val()) {
				if(! \$("#cliente").val()) {
					\$.DDialog({message:"Você não selecionou o cliente!", focusBack:\$("#cliente")});
					return false;
				}
				if(!\$("#cliente_endereco").DTouchRadio("value")) {
					\$.DDialog({message:"Você não selecionou o endereço do cliente!", focusBack:\$("#cliente_endereco")});
					return false;
				}
			}

			\$.DActionAjax({
				action        : "/sys/monitor/edit_submit.cgi",
				loader        : \$("#defaults_container"),
				target        : "#resultado",
				serializeForm : true
				});
		};
		
		this.cancel = function(){
			eos.menu.action.hide('icon_monitor_save');
			eos.menu.action.hide('icon_monitor_cancel');
			if(\$('#codigo').val()) {
				eos.menu.action.show('icon_monitor_new');
				eos.menu.action.show('icon_monitor_edit');
				eos.menu.action.hide('icon_monitor_delete');
				monitor.view(\$('#codigo').val());
			} else {
				\$('#endereco').val('');
				\$.DActionAjax({
					action        : "/sys/monitor/edit.cgi",
					req           : "empresa=$EMPRESA",
					loader        : \$("#defaults_container"),
					target        : "#defaults_container",
					serializeForm : false });
				\$('#DTouchPages_default').DTouchPages('page','center');
				}
		};
	}
	
	function Monitor(){
		this.view = function(c){

			\$.DActionAjax({
				action        : "/sys/monitor/view.cgi",
				req           : "endereco="+\$("#endereco").val()+"\&host="+\$("#host").val()+"\&empresa=$EMPRESA",
				loader        : \$("#defaults_container"),
				target        : "#defaults_container",
				serializeForm : false,
				postFunction  : function(data){
					eos.menu.action.hide('icon_monitor_save');
					eos.menu.action.hide('icon_monitor_cancel');
					eos.menu.action.hide('icon_monitor_delete');
					eos.menu.action.show('icon_monitor_new');
					if(\$("#host").val() != "")
					      {
					      eos.menu.action.show('icon_monitor_edit');
					      }
					else
					      {
					      eos.menu.action.hide('icon_monitor_edit');
					      }					
					}
				});
			};
			
		this.detail_hd = function(x,a,b,c, d){
			\$.DActionAjax({
				req		: "endereco="+\$("#endereco").val()+"\&host="+\$("#host").val()+"\&empresa=$EMPRESA"+"&div=graph_"+x+"&monitor="+a+"&descr="+b+"&item="+c+"&intervalo="+d,
				action		: "/sys/monitor/view_hd.cgi",
				loader		: \$('#monitor_'+x),
				serializeForm	: false
				});
			};

		this.detail_cpu = function(x,a,b,c,d){
			\$.DActionAjax({
				req		: "endereco="+\$("#endereco").val()+"\&host="+\$("#host").val()+"\&empresa=$EMPRESA"+"&div=graph_"+x+"&monitor="+a+"&descr="+b+"&item="+c+"&intervalo="+d,
				action		: "/sys/monitor/view_cpu.cgi",
				loader		: \$('#monitor_'+x),
				serializeForm	: false
				});
			};			

		this.insert = function(c){
			\$('#endereco').val('');
			\$.DActionAjax({
				action        : "/sys/monitor/edit.cgi",
				req           : "empresa=$EMPRESA",
				loader        : \$("#defaults_container"),
				target        : "#defaults_container",
				serializeForm : false,
				postFunction  : function(data){
					\$('#DTouchPages_default').DTouchPages('page','right');
					}
				});		
			};
			
		this.edit = function(c){
			\$.DActionAjax({
				action        : "/sys/monitor/edit.cgi",
				req           : "endereco="+\$("#endereco").val()+"\&host="+\$("#host").val()+"\&empresa=$EMPRESA",
				loader        : \$("#defaults_container"),
				target        : "#defaults_container",
				serializeForm : false,
				postFunction  : function(data){
					eos.menu.action.show('icon_monitor_save');
					eos.menu.action.show('icon_monitor_cancel');
					eos.menu.action.hide('icon_monitor_delete');
					eos.menu.action.hide('icon_monitor_new');
					eos.menu.action.hide('icon_monitor_edit');
					}
				});
			};
			
		this.list = function(c){
			// executa lista de monitoramentos
			\$.DActionAjax({
				req: "empresa=$EMPRESA",
				action: "/sys/monitor/start_list.cgi",
				loader: \$("defaults_list_container"),
				serializeForm: false
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
			if(\$('#endereco').val()) {
				eos.menu.action.hide('icon_monitor_save');
				eos.menu.action.hide('icon_monitor_cancel');
				eos.menu.action.hide('icon_monitor_delete');
				eos.menu.action.show('icon_monitor_new');
				eos.menu.action.hide('icon_monitor_edit');
				}
			else
				{
				eos.menu.action.show('icon_monitor_save');
				eos.menu.action.show('icon_monitor_cancel');
				eos.menu.action.hide('icon_monitor_delete');
				eos.menu.action.hide('icon_monitor_new');
				eos.menu.action.hide('icon_monitor_edit');
				}
			},
		pageCenter: \$("#DTouchPages_default_center"),
		postFunctionCenter : function() {
			eos.menu.action.hide('icon_monitor_save');
			eos.menu.action.hide('icon_monitor_cancel');
			eos.menu.action.hide('icon_monitor_delete');
			eos.menu.action.show('icon_monitor_new');
			eos.menu.action.hide('icon_monitor_edit');
			}
		});
	
	
	\$(document).ready(function(){
	
		monitor = new Monitor(); // inicia objeto default
		form = new Form();
		form.initialize();
		monitor.list();
		eos.menu.action.hide('icon_monitor_save');
		eos.menu.action.hide('icon_monitor_cancel');
		eos.menu.action.hide('icon_monitor_delete');
		eos.menu.action.show('icon_monitor_new');
		eos.menu.action.hide('icon_monitor_edit');
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
	<input type='hidden' name='host' id="host" />
	<input type='hidden' name='endereco' id="endereco" />
	<input type='hidden' name='empresa' id="empresa" value='$EMPRESA' />
</form>


</body>
</html>
HTML
	
exit;
	
