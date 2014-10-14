#!/usr/bin/perl
 
# 
# menu.cgi
# monta menu conforme tipo de acesso do usuario
#

$nacess = '201';
require "../cfg/init.pl";

$MODO = &get("MODO");

print $query->header({charset=>utf8});

print<<HTML;
<script>
	// start menu
	menu_emp = new menu(['icon_empresa_dti','icon_user','icon_cron','icon_procede','icon_contato']);
	
	if("$nacess_tipo" == "a")
		{
		// menu_emp.btnShow(['icon_empresa_dti','icon_user','icon_cron','icon_procede','icon_contato','icon_empresa_novo','icon_empresa_save','icon_delete']);
		
		menu_emp.btnShow(['icon_empresa_novo','icon_empresa_save','icon_delete']);
		
		// menus do endereco
		// menu_emp.btnNew("icon_end_new","novo","endereco.add()","endereço");
		// menu_emp.btnNew("icon_end_del","excluir","endereco.del()","endereço");
		
		// novo contato
		// menu_emp.btnNew("icon_contato_new","novo","contato.add()","contato");
		
		/*
		if("$MODO" == "incluir")
			menu_emp.btnHide("icon_contato_new");
		else
			menu_emp.btnShow("icon_contato_new");
		*/
		}

	if("$nacess_tipo" == "s")
		// menu_emp.btnShow(['icon_empresa_save','icon_back','icon_empresa_dti','icon_user','icon_cron','icon_procede','icon_contato']);
		menu_emp.btnShow(['icon_empresa_save']);
		
	// if("$nacess_tipo" == "a" || "$nacess_tipo" == "s" || "$nacess_tipo" == "v")
	menu_emp.btnShow(['icon_empresa_dti','icon_user','icon_cron','icon_procede','icon_contato','icon_print']);
	// menu_emp = new menu(['icon_back','icon_export','icon_print','icon_empresa_novo']);
	
</script>
HTML
