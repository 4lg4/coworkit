#!/usr/bin/perl

$nacess = "201";
require "../cfg/init.pl";
$TABLE = &get('TABLE');
$FILTRO = &get('FILTRO');
$FROM = &get('FROM');

# se nao for chamada do menu
if($FROM ne "menu")
	{	&session(1);	}

# se houver filtro
if($FILTRO ne "")
	{ $FILTRO = "where ".$FILTRO; }

# $DB = &DBE("select * from $TABLE");
$DB = &DBE("select * from empresas_lista_distinct order by emp_nome asc");
while($tbl = $DB->fetchrow_hashref)
	{
	$line .= "<tr>";
	$line .= "		<td style='display:none;'>$tbl->{emp_codigo}</td>";
	$line .= "		<td style='display:none;'>$tbl->{emp_codigo}</td>";
	$line .= "		<td style='display:none;'>Empresas</td>";
	$line .= "		<td>$tbl->{emp_nome}</td>";
	$line .= "		<td>$tbl->{emp_apelido}</td>";
	$line .= "		<td>$tbl->{end_fone}</td>";
	$line .= "		<td>$tbl->{end_mail}</td>";
	$line .= "</tr>";
	}

$line1 = "";
# top 10 empresas
$DB = &DBE("select *, last_view.dt as lastdt from empresas_lista_distinct left join last_view on (empresas_lista_distinct.emp_codigo = last_view.codigo and last_view.tabela = 'empresa' and last_view.usuario = $USER->{id}) LIMIT 10");
while($tbl = $DB->fetchrow_hashref)
	{
	$line1 .= "<tr>";
	$line1 .= "		<td style='display:none;'>$tbl->{emp_codigo}</td>";
	$line1 .= "		<td style='display:none;'>0</td>";
	$line1 .= "		<td style='display:none;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; TOP 10</td>";
	$line1 .= "		<td>$tbl->{emp_nome}</td>";
	$line1 .= "		<td>$tbl->{emp_apelido}</td>";
	$line1 .= "		<td>$tbl->{end_fone}</td>";
	$line1 .= "		<td>$tbl->{end_mail}</td>";
	$line1 .= "</tr>";
	}

# ajuste do grid	
$TBINI .= "<table class='menu_tb dgrid' id='g1' style='min-width:100%;'>";
$TBINI .= "	<thead>";
$TBINI .= "	<tr>";
$TBINI .= "		<th style='display:none;'>Cod</th>";
$TBINI .= "		<th style='display:none;'>group_order</th>";
$TBINI .= "		<th style='display:none;'>group_descrp</th>";
$TBINI .= "		<th>Nome</th>";
$TBINI .= "		<th>Apelido</th>";
$TBINI .= "		<th>Telefone</th>";
$TBINI .= "		<th>E-mail</th>";
$TBINI .= "	</tr>";
$TBINI .= "	</thead>";
$TBINI .= "	<tbody>";
$TBEND .= "	</tbody>";
$TBEND .= "</table>";

# monta as grids
# $R .= $TBINI.$line1.$line.$TBEND;
$R .= $TBINI.$line1.$line.$TBEND;

print $query->header({charset=>utf8});

print<<HTML;

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html id="html">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">

<script type="text/javascript" src="/comum/DPAC.js"></script>
<script>
// on click do grid
function DGridClick(x)
	{
	if(x)
		{
		\$("#COD").value = x;
		}
	else
		{
		\$("#COD").value = "";
		}
		
	\$("#MODO").value = 'ver';
	
	// menua.btnShow(['icon_gridview','#icon_ti','#icon_user','#icon_ti','#icon_cron']);
	menua.btnShow(['icon_gridview','icon_ti','icon_user','icon_ti','icon_cron']);
	}
	
// on DBL click do grid
function DGridDblClick(x)
	{
	abrir()
	}
	
// Filter Update, campo de pesquisa no grid
function gridFilterUpdate(val)
	{
	\$(".dataTables_filter").find("input").val(val).trigger('keyup');
	}

// acesso direto a edicao do cliente
function abrir()
	{
	top.gridFilter(1); // esconde pesquisa do grid
	
	top.Loading();
	\$("#CAD").attr("action", "$dir{empresas}edit.cgi");
	\$("#CAD").submit();
	}

// acesso direto aos dados de ti
function ti()
	{
	top.gridFilter(1); // esconde pesquisa do grid
	
	top.Loading();
	\$("#CAD").attr("action", "$dir{dados_ti}dados_ti.cgi");
	\$("#CAD").submit();
	}

// acesso direto aos dados de usuarios
function users()
	{
	top.gridFilter(1); // esconde pesquisa do grid
	
	top.Loading();
	\$("#CAD").attr("action", "$dir{dados_user}dados_users.cgi");
	\$("#CAD").submit();
	}

// acesso direto ao modulo cron
function cron()
	{
	top.gridFilter(1); // esconde pesquisa do grid
	
	top.Loading();
	\$("#CAD").attr("action", "$dir{cron}dados_cron.cgi");
	\$("#CAD").submit();
	}
	
/* [INI] Document Ready ------------------------------------------------------------------------------------------------------------- */
\$(document).ready(function() 
	{
		
	/*	
	// inicia grid
	var dgrid = new grid('g1','no');
	dgrid.group();
	// dgrid.setTipo('.');
	//dgrid.setQtd('100');
	// dgrid.setFooter('rt<"dataTables_bottom"lpi>');
	dgrid.setFooter('rt<"dataTables_bottom"fi>');
	// dgrid.setHeight("-70");
	dgrid.show();
	*/
	\$("#g1").DGrid();		
	// mostra formulario de consulta do grid
	top.gridFilter();	
	
	// esconde campo de pesquisa do dgrid
	\$(".dataTables_filter").find("input").closest("label").hide();
	
	// menu
	menua = new top.menu();
	menua.btnShow('icon_insert');

	// loader remove
	top.unLoading();
	});
/* [END] Document Ready ------------------------------------------------------------------------------------------------------------- */
</script>
<body style="overflow:hidden;">

<div style="margin-top:10px; height:92%">$R</div>

<form id="CAD" name='AUX' method='POST'>
	<input type='hidden' name='ID' value='$ID'>
	<input type='hidden' name='SHOW' value='$SHOW'>
	<input type='hidden' name='INI' value='0'>
	<input type='hidden' name='PESQLETRA'>
	<input type='hidden' name='ORDER'>
	<input type='hidden' name='MODO'>
	<input type='hidden' name='COD' id='COD'>
</form>

</body>
</html>
HTML

