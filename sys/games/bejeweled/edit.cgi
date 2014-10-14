#!/usr/bin/perl

$nacess = "0";
require "../../cfg/init.pl";
$ID = &get('ID');

print $query->header({charset=>utf8});

print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html id="html">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	
<script language='JavaScript'>
	// carrega dependencias especificas
	DLoad("bejeweled");
	
// salva score
function DActionSave()
	{
	\$("#CAD input[name=SCORE]").val(\$("#points").text());
	
	DActionAjax("edit_submit.cgi",\$("#CAD").serialize());
	}


// quando o documento esta pronto 
\$(document).ready(function() 
	{ 
	unLoading();
	
	menu_beweled = new menu();
	menu_beweled.btnNew("icon_snake_reset","finalizar","DActionSave()");

	Bejeweled = Bejeweled || {};
    Bejeweled.init();

	// unLoading();
	});
</script>
<style>
.jqplot-table-legend
	{
	top: 15px !important;
	}
</style>
</head>
<body>

<form name='CAD' id='CAD'>
	
	<div id="bejeweled_container">
	    <div id="grid"></div>
		<div id="points_container"> Score: <span id="points"></span></div>
	</div>

	<div id="resultado" class="DDebug"></div>

	<!-- variaveis de ambiente -->
	<input type='hidden' name='SCORE'>
	<input type='hidden' name='GAME' value='2'>
</form>
</body></html>

HTML


