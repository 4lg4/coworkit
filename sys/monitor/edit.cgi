#!/usr/bin/perl

$nacess = "903";
require "../cfg/init.pl";

$empresa = &get('empresa');
$host = &get('host');

if($host ne "")
	{
	$DB = DBE("select monitor_grupo.* from monitor_grupo where monitor_grupo.host = '$host' ");

	if($DB->rows() == 1)
		{ 
		while($v = $DB->fetchrow_hashref)
			{
			$codigo = $v->{codigo};
			$descrp = $v->{descrp};
			if($v->{hidden})
				{
				$show = "true";
				}
			else
				{
				$show = "false";
				}
			}
		}
	
	
	}


print $query->header({charset=>utf8});

print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html id="html">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">

<script language='JavaScript'>
HTML
if($codigo eq "")
	{
print<<HTML;
	function sel_host(a) {
		if(\$("#cliente").val() == "")
			{
			alerta("Selecionar o Cliente");
			return false;
			}
		\$.DActionAjax({
			action:"/sys/monitor/empresa_comp.cgi",
			req: "empresa="+\$("#cliente").val()+"&endereco="+\$("#cliente_endereco").DTouchRadio("value"),
			loader: \$("#host_container"),
			serializeForm: false,
			postFunction: function(){
				if(\$("#COD").val())
					{
					\$("#host").DTouchRadio("disable");
					}
				}
			});
		}
HTML
	}
print<<HTML;
	\$(document).ready(function(){
		\$('#detalhe_proced').DTouchBoxes({title:'Descrição do Monitoramento'});
HTML
if($codigo eq "")
	{
print<<HTML;
		// filter cliente
		\$('#cliente_container').DTouchBoxes();
		\$('#cliente').fieldAutoComplete(
			{ 
			type		: 'empresa',
			postFunction	: function(x) {
				if(\$('#cliente').val() != '') {
					\$.DActionAjax({
						action:"/sys/monitor/empresa_endereco.cgi",
						req: "empresa="+\$("#cliente").val(),
						loader: \$("#cliente_container"),
						serializeForm: false,
						postFunction: function(){
							if(\$("#COD").val()){
								\$("#cliente_endereco").DTouchRadio("disable");
								}
							}
						});
					}
				},
			onReset		: function() {
				\$("#cliente_endereco").DTouchRadio("reset","hard");
				},
			placeholder: "Selecione o Cliente"
			});

		\$("#host_container").DTouchBoxes({
			title:"Computador"
			});
		\$("#host_container").hide();
HTML
	}
print<<HTML;
		\$("#show_container").DTouchBoxes({
			title:"Mostrar Monitoramento?"
			});
		
		\$("#show").DTouchRadio({
			addItem:[{val:'false',descrp:'Sim',img:'/img/chamado/prior_green.png'},{val:'true',descrp:'Não',img:'/img/chamado/prior_red.png'}]
		});
HTML
	if($descrp ne "")
		{
		print "\$('#descrp').val('$descrp');";
		}
	if($show ne "")
		{
		print "\$('#show').DTouchRadio('val','$show');";
		}
print<<HTML;
	});	
	</script>
</head>
<body>
<input type='hidden' id='codigo_save' name='codigo_save' value='$codigo'>
<div style="margin: 0px 20px; height: 100%;">
	<div id="detalhe_proced">
		<div id="descricao">
			<textarea id="descrp" name="descrp" placeholder="Descreva aqui" class="DTouchBoxes_line_textarea"></textarea>
		</div>
	</div>

	<!-- Monitorado ou não -->
	<div id="show_container">
		<div id="show" class="DTouchBoxes_line_list"></div>
	</div>
HTML
if($descrp eq "")
	{
print<<HTML;
	<!-- cliente / endereco -->
	<div id="cliente_container">
		<div class='DTouchBoxes_title DTouchBoxes_title_input'>
			<input type="text" name="cliente" id="cliente" placeholder="Cliente"/>
		</div>
		<div id="cliente_endereco" class="DTouchBoxes_line_list"></div>
	</div>
	<!-- Nome do servidor -->
	<div id="host_container">
		<div id="host" class="DTouchBoxes_line_list"></div>
	</div>
HTML
	}
print<<HTML;
</div>

</body>
</html>
HTML



