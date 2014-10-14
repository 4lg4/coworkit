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

# empresa filtro
if($EMPRESA ne "") {
    $sqlempresa = " and empresa.codigo = '$EMPRESA' "; 
}


$DB = &DBE("select distinct monitor_grupo.endereco as codigo_end, monitor_grupo.host as codigo_host, empresa_comp.nome as cliente_host, empresa.nome as cliente_nome, empresa_endereco.endereco as cliente_endereco, empresa_endereco.cidade as cliente_cidade, empresa_endereco.uf as cliente_uf from monitor_grupo join empresa_endereco on monitor_grupo.endereco = empresa_endereco.codigo join empresa on empresa_endereco.empresa = empresa.codigo join parceiro_empresa on parceiro_empresa.empresa = empresa.codigo left join empresa_comp on monitor_grupo.host = empresa_comp.codigo where parceiro_empresa.parceiro = '".$USER->{'empresa'}."' $sqlempresa order by empresa_comp.nome, empresa_endereco.endereco ");

if($DB->rows() > 0)
	{
	while($c = $DB->fetchrow_hashref)
		{
		if($c->{cliente_host} eq '')
			  {
			  $host = 'n/a';
			  }
		else
			  {
			  $host = '<font style="font-weight: bold !important">'.$c->{cliente_host}.'</font>';
			  }
		# 930px MIN width of the table
		$array_radio_default .= "{val:'$c->{codigo_end}#$c->{codigo_host}',descrp:";
		$array_radio_default .= "'<input type=hidden name=cod_end value=\"$c->{codigo_end}\"><input type=hidden name=cod_host value=\"$c->{codigo_host}\">";
		$array_radio_default .= "<div class=\"DTouchRadio_list_line\">";
		if($EMPRESA eq "")
			  {
			  $array_radio_default .= " 	<div style=\"width:35%;\">$host</div> ";
			  $array_radio_default .= " 	<div style=\"width:25%\">$c->{cliente_nome}</div>";
			  }
		else
			  {
			  $array_radio_default .= " 	<div style=\"width:60%;\">$host</div> ";
			  }
		$array_radio_default .= " 	<div style=\"width:25%\">$c->{cliente_endereco}";
		if($c->{cliente_cidade} ne "" || $c->{cliente_uf} ne "")
			  {
			  $array_radio_default .= ", $c->{cliente_cidade}/$c->{cliente_uf}";
			  }
		$array_radio_default .= "</div>";
		$array_radio_default .= " </div>";
		$array_radio_default .= " '},";
    
		}
	# $array_radio_default = substr($array_radio_default, 0,-1); # remove ultima virgula
	}
else
	{
	$array_radio_default .= "{ val:0, descrp:'<div style=\"width:100%\">Nenhum registro encontrado !</div>' }";
	}
	

$radio_title  = "<div class=\"DTouchRadio_list_title\">";
if($EMPRESA eq "")
	{
	$radio_title .= "	<div style=\"width:35%\">Nome da máquina</div>";
	$radio_title .= "	<div style=\"width:35%\">Cliente</div>";
	}
else
	{
	$radio_title .= "	<div style=\"width:70%\">Nome da máquina</div>";	
	}
$radio_title .= "	<div style=\"width:30%\">Endereço</div>";
$radio_title .= "</div>";


print<<HTML;
	<script>
		\$("#defaults_list_container").DTouchRadio({ 
			addItem     : [$array_radio_default], 
			orientation : 'vertical',
			title       : '$radio_title',
			search      : true,                
			searchFile  : "start_list",
			click : function(x) {
				if(x.value === "0"){
					\$('#endereco').val('');
					\$('#host').val('');
					return false;
					}
				else
					{
					\$("#defaults_container").html('');
					\$('#endereco').val(\$("input[name=defaults_list_container_radios]:checked").parent().find("input[name=cod_end]").val());
					\$('#host').val(\$("input[name=defaults_list_container_radios]:checked").parent().find("input[name=cod_host]").val());
					
					monitor.view();
					\$('#DTouchPages_default').DTouchPages("page","right");
					}
				}
			});
		
	</script>
HTML
	
exit;
	
