#!/usr/bin/perl

$nacess = "903";
require "../cfg/init.pl";

$COD = &get('codigo');

print $query->header({charset=>utf8});

# carrega valores do banco de dados
$n=0;

require "./edit_db.pl";

print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html id="html">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
HTML

print "<script language='JavaScript'> 
	\$(document).ready(function(){
		if('$endereco_descrp' != '') {
			\$('#enderecos').html('<br>Endereço(s): ".$endereco_descrp."');
		}";
		
if($COD eq "")
	{
print<<HTML;
		\$('#detalhe_proced').DTouchBoxes({title:'Descrição do Monitoramento'});
		
		// filter cliente
		\$('#cliente_container').DTouchBoxes();
		\$('#cliente').fieldAutoComplete(
			{ 
			type		: 'empresa',
			postFunction	: function(x) {
				if(\$('#cliente').val() != '') {
					\$.DActionAjax({
						action:"empresa_endereco.cgi",
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

		// filter host
		\$('#host_container').DTouchBoxes();
		\$('#host').fieldAutoComplete(
			{ 
			type		: 'empresa_comp',
			placeholder: "Selecione o Cliente"
			});

HTML
	}
else
	{
	}
print<<HTML;
	\$("#show_container").DTouchBoxes({
			title:"Mostrar Monitoramento?"
			});
		});
	\$("#show").DTouchRadio({
			addItem:[{val:'false',descrp:'Sim',img:'/img/chamado/prior_green.png'},{val:'true',descrp:'Não',img:'/img/chamado/prior_red.png'}]
		});
		
	</script>
</head>
<body>
<input type='hidden' name='codigo_save' value='$COD'>
<div style="margin: 0px 20px; height: 100%;">
	<div id="detalhe_proced">
		<div id="enderecos"></div>
		<div id="descricao">
			<textarea id="descrp" name="descrp" placeholder="Descreva aqui" class="DTouchBoxes_line_textarea"></textarea>
		</div>
	</div>
HTML

if($empresa_cod ne "")
	{
	print "<input type='hidden' name='cliente' value='$empresa_cod'>";
	if($COD ne "")
		{
		}
	}
else
	{
	if($COD eq "")
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
		<div class='DTouchBoxes_title DTouchBoxes_title_input'>
			<input type="text" name="host" id="host" placeholder="Nome da máquina"/>
		</div>
	</div>
	
	<!-- Monitorado ou não -->
	<div id="show_container">
		<div id="show" class="DTouchBoxes_line_list"></div>
	</div>
HTML
		}
	else
		{
		}
	}
print<<HTML;

</div>

</body>
</html>
HTML



