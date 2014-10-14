#!/usr/bin/perl

$nacess = '66';
require "../cfg/init.pl";

print $query->header({charset=>utf8});

$ID = &get("ID");

print<<HTML;

<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />

	<title>$nome_emp  - $nome_sys</title>
	<link rel="shortcut icon" href="/favicon.ico">
	
	<script src="/comum/DPAC_mobile.js"></script>

<style>
.ui-slider
	{ 
	width: 12em !important; 
	}
</style>

<script>
\$(document).ready(function() 
	{	
	// inicia pagina com ultimas empresas acessadas
	empresas();
	// \$("#coletor_view_pg").hide(); // esconde pagina de visualizacao
	
	// executa uma pesquisa 
	\$(".ui-input-text").keydown(function(event) 
		{
		if(event.which == 13)
			{
			\$("#SEARCH").val(\$(this).val());
			empresas();
			}
		});
	
	// inicializa listviews	
	\$('ul').listview();
	
	// ajustes no input textarea
	\$('#obs').textinput();
	});
	
/* empresas, requests ------------------------------------ */
function empresas()
	{
	// request string
	req=\$("#mobile_frm").serialize();
	//alert(req);
	
	// executa
	$ajax_init \$.ajax(
		{
		type: "POST",
		url: "coletor_submit_mobile.cgi",
		dataType: "html",
		data: req,
		success: function(data)
			{
			\$("body").append(data);
			}
		});
	}
	
/* empresas, View selecao -------------------------------- */
function empresaView(cod)
	{
	// \$('#emp_apelido').text('aaa '+\$("emp_"+cod).text());
	\$("#EMP_COD").val(cod);
	empresas();
	window.location = "#coletor_view_pg";
	}
	
/* empresas, Limpa selecao ------------------------------ */
function empresaClean()
	{
	\$("#EMP_COD").val("");
	\$("#SEARCH").val("");
	empresas();
	window.location = "#empresas_pg";
	}

/* coletor, View selecao -------------------------------- */
function coletorView(cod)
	{
	// \$('#emp_apelido').text('aaa '+\$("emp_"+cod).text());
	\$("#COLETOR").val(cod);
	empresas();
	window.location = "#coletor_view_pg";
	}
</script>
</head>
<body>

<form name="mobile_frm" id="mobile_frm">
	<input type="hidden" name="ID" id="ID" value="$ID">
	<input type="hidden" name="MOBILE" id="MOBILE" value="MOBILE">
	<input type="hidden" name="SEARCH" id="SEARCH" value="$SEARCH">
	<input type="hidden" name="COLETOR" id="COLETOR">
	<input type="hidden" name="EMP_COD" id="EMP_COD">
</form>

<!-- ***********************************************************************************************************************
 	 Lista de Coletores do usuario 	 
***********************************************************************************************************************  -->
<div data-role="page" id="coletores_pg">
<!--  Header  *********************************************************************************************************  -->
    <div data-theme="b" data-role="header" id="coletores_pg_header">
        <h3>TimeSheet</h3>
		<div data-role="controlgroup" data-type="horizontal" class="ui-btn-left">
			<a data-role="button" data-transition="fade" data-icon="home" onClick="call('menu/start_mobile.cgi')">D</a>
			<a data-role="button" data-transition="fade"  href="#empresas_pg">Novo</a>
		</div>
		<a data-role="button" data-transition="fade" data-theme="c"  data-icon="grid" data-iconpos="right" class="ui-btn-right" onClick="call('logon/logout.cgi')">
            Sair
        </a>
    </div>

<!--  lista de empresas ************************************************************************************************  -->
	<div data-role="content" style="padding: 15px" id="pages">
		<ul id="list_coletor_mobile" data-role="listview" data-filter="true" data-filter-placeholder="aperte enter para pesquisar" data-filter-theme="d" data-theme="d" data-divider-theme="d" ></ul>
    </div>
</div>


<!-- ***********************************************************************************************************************
 	 Lista de Empresas 	 
***********************************************************************************************************************  -->
<div data-role="page" id="empresas_pg">
<!--  Header  *********************************************************************************************************  -->
    <div data-theme="b" data-role="header" id="empresas_pg_header">
        <h3>TimeSheet</h3>
		<div data-role="controlgroup" data-type="horizontal" class="ui-btn-left">
			<a data-role="button" data-transition="fade" data-icon="home" onClick="call('menu/start_mobile.cgi')">D</a>
			<a data-role="button" data-transition="fade"  href="#coletores_pg">Lista</a>
		</div>
		<a data-role="button" data-transition="fade" data-theme="c"  data-icon="grid" data-iconpos="right" class="ui-btn-right" onClick="call('logon/logout.cgi')">
            Sair
        </a>
    </div>

<!--  lista de empresas ***********************************************************************************************  -->
	<div data-role="content" style="padding: 15px" id="pages">
		<ul id="list_mobile" data-role="listview" data-filter="true" data-filter-placeholder="aperte enter para pesquisar" data-filter-theme="d" data-theme="d" data-divider-theme="d"></ul>
    </div>
</div>


<!-- ***********************************************************************************************************************
 	 Coletor View
***********************************************************************************************************************  -->
<div data-role="page" id="coletor_view_pg">
<!--  Header  *********************************************************************************************************  -->
    <div data-theme="b" data-role="header" id="coletor_view_pg_header">
        <h3><span id="emp_apelido"></span></h3>
		<a data-role="button" data-transition="fade" data-theme="" data-icon="back" data-iconpos="left" class="ui-btn-left" href="#coletores_pg">TimeSheet</a>
		<a data-role="button" data-transition="fade" data-theme="c"  data-icon="grid" data-iconpos="right" class="ui-btn-right" onClick="call('logon/logout.cgi')">
            Sair
        </a>
    </div>

<!--  dados da empresa ************************************************************************************************  -->
	<div data-role="content" style="padding: 15px">
		<div data-role="fieldcontain">
			
			<div style="float:right;">
			<select name="servidor" id="servidor" data-role="slider">
				<option value="0">Hora Servidor</option>
				<option value="1">Hora Servidor</option>
			</select>
			</div>
			
			<div style="width:100%;">
				<div style="width:60%; float:left; margin-right:5%;">
					<label for="data_exec">Data</label>
					<input placeholder="Data Execução" type='date' name='data_exec' id='data_exec' value=''/>
				</div>
				<div style="width:33%; float:left;">
					<label for="tempo_exec">Duração</label>
					<input placeholder="Tempo Execução" type='time'  name='tempo_exec' id='tempo_exec' value='' />
				</div>
			</div>
			
			<!-- <label for="solicitante">Solicitante</label> -->
			<input placeholder="Solicitante" type='text' name='solicitante' id='solicitante' value='' />
			
			<label for="descrp">Descrição</label>
			<textarea name="descrp" id="descrp"></textarea>
			
			<a data-role="button" data-theme='b'>Salvar</a>
		</div>
	</div>
	
</div>
</body>
</html>		

HTML
exit;