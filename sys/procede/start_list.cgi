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


$DB = &DBE("select procedimentos.*, procedimentos.dt as procede_data, empresa.nome as cliente_nome, empresa_endereco.endereco as cliente_endereco, empresa_endereco.cidade as cliente_cidade, empresa_endereco.uf as cliente_uf from procedimentos left join empresa_endereco on procedimentos.endereco = empresa_endereco.codigo left join empresa on procedimentos.empresa = empresa.codigo where procedimentos.parceiro = '".$USER->{'empresa'}."' $sqlempresa order by procedimentos.codigo ");

if($DB->rows() > 0)
	{
	while($c = $DB->fetchrow_hashref)
		{
		$c->{problema} = &get($c->{problema}, "NEWLINE_SHOW"); # remove problemas de quebra de linha e aspas
    
		# 930px MIN width of the table
		$array_radio_default .= "{val:$c->{codigo},descrp: ";
		$array_radio_default .= "'<div class=\"DTouchRadio_list_line\">";
		$array_radio_default .= " 	<div style=\"width:5%;\">#$c->{codigo}</div> ";
		$array_radio_default .= " 	<div style=\"width:10%\">".(&dateToShow($c->{procede_data}))."</div>";
		if($EMPRESA eq "")
			  {
			  $array_radio_default .= " 	<div style=\"width:35%;\">$c->{titulo}</div> ";
			  $array_radio_default .= " 	<div style=\"width:25%\">$c->{cliente_nome}</div>";
			  }
		else
			  {
			  $array_radio_default .= " 	<div style=\"width:60%;\">$c->{titulo}</div> ";
			  }
		$array_radio_default .= " 	<div style=\"width:25%\">$c->{cliente_endereco}";
		if($c->{cliente_cidade} ne "" || $c->{cliente_uf} ne "")
			  {
			  $array_radio_default .= ", $c->{cliente_cidade}/$c->{cliente_uf}";
			  }
		$array_radio_default .= "</div>";
		
		# Lista de TAGs do procedimento
		$DB2 = DBE("select procedimentos_tags.tag as tag_codigo, procedimentos_tags_tipo.descrp as tag_descrp from procedimentos_tags join procedimentos_tags_tipo on procedimentos_tags.tag = procedimentos_tags_tipo.codigo where procedimentos_tags.procedimento = '$c->{codigo}' order by procedimentos_tags.ordem");
		$array_radio_default .= " 	<div style=\"width:1%; display: none;\">";
		while($t = $DB2->fetchrow_hashref)
			{
			$array_radio_default .= $t->{tag_descrp}." ";
			}
		$array_radio_default .= " </div>";
		$array_radio_default .= " </div>";
    
  
    $array_radio_default .= " '},";
    
		}
	# $array_radio_default = substr($array_radio_default, 0,-1); # remove ultima virgula
} else {
    $array_radio_default .= "{ val:0, descrp:'<div style=\"width:100%\">Nenhum registro encontrado !</div>' }";
}
	

$radio_title  = "<div class=\"DTouchRadio_list_title\">";
$radio_title .= "	<div style=\"width:5%\">Codigo</div>";
$radio_title .= "	<div style=\"width:10%\">Data</div>";
if($EMPRESA eq "")
	{
	$radio_title .= "	<div style=\"width:35%\">Título</div>";
	$radio_title .= "	<div style=\"width:25%\">Cliente</div>";
	}
else
	{
	$radio_title .= "	<div style=\"width:60%\">Título</div>";	
	}
$radio_title .= "	<div style=\"width:25%\">Endereço</div>";
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
					return false;
					}
				\$('#codigo').val(x.value);
				procede.view(x.value);
				\$('#DTouchPages_default').DTouchPages("page","right");
				}
			});
		
	</script>
HTML
	
exit;
	
