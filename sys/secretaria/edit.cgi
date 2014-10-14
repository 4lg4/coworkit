#!/usr/bin/perl

# numero de acesso do modulo
$nacess = "100";

require "../cfg/init.pl";

$ID = &get('ID'); 
$MODO = &get('MODO');


#  empresa -----------------------------
$DB = &DBE("select er.empresa, e.nome as empresa_descrp from empresa_relacionamento as er left join empresa as e on e.codigo = er.empresa where er.relacionamento = 5 group by er.empresa, e.nome");
$empresas = "<ul id='empresas_ul' class='grupos_connect' style='height:100%;'>";
while($e = $DB->fetchrow_hashref)
	{
	$empresas .= "<li>".ucfirstall($e->{empresa_descrp})."</li>";
	}
$empresas .= "</ul>";

# secretaria -----------------------------
$DB = &DBE("select * from usuario where tipo = 5 or tipo = 1");
while($s = $DB->fetchrow_hashref)
	{
	#%secretarias->{$s->{usuario}} = "<ul id='secretarias_ul'>";
	#%secretarias->{$s->{usuario}} .= "<li>".ucfirstall($s->{nome})."</li>";
	#%secretarias->{$s->{usuario}} .= "</ul>";
	
	$secretarias .= "<div id='secretaria_".$s->{usuario}."' style='border:1px solid red; float:left; width:20%; height:200px;'>"; 
	$secretarias .= "	<div style='border:1px solid red; height:50px;'>";
	$secretarias .= 		ucfirstall($s->{nome}); 
	$secretarias .= "	</div>";
	$secretarias .= "	<div style='border:1px solid red; height:150px;'>";
	$secretarias .= "		<ul class='grupos_connect' style='height:100%;'>";
	
	# pega todos os vinculos por secretaria
	$DB2 = &DBE("select s.*, e.nome as empresa_descrp from secretaria as s left join empresa as e on e.codigo = s.empresa where s.usuario = $s->{usuario}");
	while($s2 = $DB2->fetchrow_hashref)
		{
		$secretarias .= "		<li>".$s2->{empresa_descrp}."</li>";
		}
	
	$secretarias .= "		</ul>";
	$secretarias .= "	</div>";
	$secretarias .= "</div>";
	}

#foreach my $val (sort keys %secretarias)
#	{
#	$secretarias .= "<div id='secretaria_$val' style='border:1px solid red; float:left; width:20%; height:200px;'>"; 
#	$secretarias .= "	<div style='border:1px solid red; height:50px;'>";
#	$secretarias .= 		$secretarias{$val}; 
#	$secretarias .= "	</div>";
#	$secretarias .= "	<div class='grupos_connect' style='border:1px solid red; height:150px;'>";
#	$secretarias .= "	</div>";
#	$secretarias .= "</div>";
#	}
	
	
print $query->header({charset=>utf8});
		
print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html id="html">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">

<script type="text/javascript">

DLoad("secretaria");

/* [INI] -------------------------------------------------------------------------------------------------------------------------------
	ON START 
		quando o documento esta pronto 
------------------------------------------------------------------------------------------------------------------------------------- */
\$(document).ready(function() 
	{
	// cria menu
	menu = new top.menu(['icon_insert']);
	
	// grupos inicia listas
	\$(".grupos_connect").sortable(
		{
		connectWith: ".grupos_connect",
		dropOnEmpty: true
		})
		.disableSelection();
	
	DActionEditarDB();
	
	// remove loader apos carregada pagina
	top.unLoading();
	});
/* [END] ON START ------------------------------------------------------------------------------------------------------------------  */

/* BTN novo */
function DActionAdd()
	{
	// logica
	}

/* BTN salvar */
function salvar()
	{
	// logica
	}

/* BTN cancelar */
function cancelar()
	{
	// logica
	}
</script>
</head>

<body>


<form name='CAD' id='CAD' method='post'>
	<input type='hidden' name='ID' id='ID' value='$ID'>
	<input type='hidden' name='MODO' id='MODO' value='$MODO'>

	<div style='width:80%; height:250px;'>
		$secretarias
	</div>
	
	
	<div style='width:80%; height:150px;'>
		<div style='border:1px solid black; width:100%; height:20px;'>
			Empresas Parceiras
		</div>
		<div style='border:1px solid black; width:100%; height:130px;'>
			$empresas
		</div>
	</div>
	
</form>


</body>
</html>
HTML
