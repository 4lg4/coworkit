#!/usr/bin/perl

$nacess = "660";
require "../../cfg/init.pl";
$ID = &get('ID'); 
$NF = &get('COD'); 
$MODO = &get('MODO');
# conteudo padrao do campo OBS
$OBS = "Empresa dispensada das retenções conforme LC 123/06 Simples Nacional";

print $query->header({charset=>utf8});


# [INI]  Pega todas datas com evento  ------------------------------------------------------------------------------------
	# $SQL = "select titulo, usuario, to_char(data, 'MM/DD/YYYY') as data_agenda from task where usuario = '".$USER->{id}."' and to_char(data, 'YYYY-MM') = '2012-01' order by data asc"; 
	$DB = DBE("select cliente, to_char(data_emissao, 'MM/DD/YYYY') as data_emissao_ from nf order by data_emissao asc");
	# $rv = $DB->rows();
	while($events = $DB->fetchrow_hashref)
		{
		$events_show  .= "{ Title: '".$events->{cliente}."', Date: new Date('".$events->{data_emissao_}."') },";
		$events_show2 .= "'".$events->{data_emissao_}."',";
		}
		$events_show = substr($events_show, 0, -1); # remove ultima ,	
		$events_show2 = substr($events_show2, 0, -1); # remove ultima ,	
# [INI]  Pega todas datas com evento  ------------------------------------------------------------------------------------


$hoje = timestamp("day").'/'.timestamp("month").'/'.timestamp("year"); # gera dia inicial;

print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html id="html">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  
<script type="text/javascript">
DLoad("faturamento");
// quando o documento esta pronto ---------
\$(document).ready(function() 
	{
        eos.menu.action.new({ // salvar
            id       : "icon_fat_save",
            title    : "salvar",
            subtitle : "",
            click    : function(){
            	if(\$("#cliente").val() == "" || \$("#cliente_descrp").val() == "" || \$("#data_emissao").val() == "" || \$("#data_vcto").val() == "" || \$("#nf_num").val() == "")
            		{
            		console.log(\$("#cliente").val() == "" || \$("#cliente_descrp").val() == "" || \$("#data_emissao").val() == "" || \$("#data_vcto").val() == "" || \$("#nf_num").val() == "");
            		alerta("Campos obrigatórios: <br> <p style='text-align:left'>- Cliente, Número Nota Fiscal <br> - Data Emissão, Data Vencimento.</p>");
            		return;
            		}

            	// envia string para salvar
            	nf("ACAO=salvar");
            }
        });
            
        eos.menu.action.new({ // delete
            id       : "icon_fat_delete",
            title    : "excluir",
            subtitle : "",
            click    : function(){
                
                \$.DDialog({
                    type : "confirm",
                    title : "Excluir NF",
                    message : "Deseja realmente excluir ?",
                    btnYes : function(){
                        nf("&ACAO=delete");
                    }
                });
            }
        });
        
        eos.menu.action.new({ // imprimir
            id       : "icon_fat_print",
            title    : "imprimir",
            subtitle : "",
            click    : function(){
            	\$("#CAD").attr({action:'$dir{faturamento}print.pdf', target:'_blank'});
            	\$("#CAD").submit();
            }
        });
        
        eos.menu.action.new({ // novo
            id       : "icon_fat_new",
            title    : "novo",
            subtitle : "",
            click    : function(){
            	resetform();
            }
        });
        
        
        eos.menu.action.hide(["icon_fat_print","icon_fat_delete"]);
        
	// menu = menu(['icon_cancel','icon_delete','icon_save']);
	// menu_faturamento = new menu(['icon_save','icon_insert']);
	// menu_faturamento.btnNew('icon_duplicate','duplicar','main.nfDuplicar()');
	
	// campo do cliente
	\$("#cliente").fieldAutoComplete({ 
		sql_tbl     : "empresa",
		sql_sfield  : "nome",
		sql_rfield  : "nome",
		sql_order   : "nome",
        placeholder : "Cliente"
	});
	
	// campo data
	\$("#data_emissao").fieldDateTime({ type:"date" });
	\$("#data_vcto").fieldDateTime({ type:"date" });

	// campo numero nf
	\$("#nf_num").fieldNumber({
	    placeholder : "N.F. número"
	});
	\$(".form_faturamento_config input").fieldNumber();
	
	// campos money
	\$("#v1").fieldMoney();
	\$("#v2").fieldMoney();
	\$("#v3").fieldMoney();
	\$("#nf_total").fieldMoney();
    
	// eos.template.field.money(\$("#nf_total"));
    eos.template.field.text(\$("#d1"));
    eos.template.field.text(\$("#d2"));
    eos.template.field.text(\$("#d3"));
    
	// inicia tabs
	\$("#nf_tab").tabs(
		{
		show: function( event, ui ) 
			{
			// \$(".grids").DGrid("bDestroy");
			// \$(".grids").DGrid("refresh");
			}
		});
	
	// inicia formulario
	resetform();
	
	// mostra data inicial
	// \$("#data_exec").val("$hoje"); 
	\$("#dia_list").text("$hoje"); 
	\$("#obs").val("$OBS");	
	
	// troca tab por enter
	\$("#nf_num").keydown(function(event) { if(event.which == 13) \$("#data_emissao").focus(); }); // ativa enter as tab too
	\$("#data_emissao").keydown(function(event) { if(event.which == 13) \$("#data_vcto").focus(); }); // ativa enter as tab too
	\$("#data_vcto").keydown(function(event) { if(event.which == 13) \$("#cliente_descrp").focus(); }); // ativa enter as tab too
	\$("#cliente_descrp").keydown(function(event) { if(event.which == 9) event.preventDefault(); if(event.which == 13) \$("#obs").focus(); }); // desativa tab e ativa enter as tab
	
// DATEPICKER ------------------------------------------------------------
	\$.datepicker.setDefaults(\$.datepicker.regional['pt-BR']); // set regional as PT Brasil	
	
	var events = [ $events_show ]; 
	var events2 = [ $events_show2 ]; 

	\$("#agenda").datepicker(
		{
		beforeShowDay: function(date) 
			{
			var result = [true, '', null];			
					
			var matching = \$.grep(events, function(event) {
				return event.Date.valueOf() === date.valueOf();
			});			
			
			if (matching.length) {
				result = [true, 'highlight', null];
			}
			return result;
			},
        onChangeMonthYear: function(year, month, widget) {
            
            if(month < 10) {
                month = "0"+month;
            }
            
                nfShowDay(year+""+month+"01");
        },
        /*
		onSelect: function(dateText) { console.log(dateText);
			var date,
				selectedDate = new Date(dateText),
				i = 0,
				event = null;
			
			while (i < events.length && !event) {
				date = events[i].Date;

				if (selectedDate.valueOf() === date.valueOf()) {
					event = events[i];
				}
				i++;
			}

			if (event) {
				// alerta(event.Title);
               //  console.log(event);
			}
		}
        */
	});

	\$("#agendaa").click(function()
		{
		var day = \$("#agenda").datepicker('getDate').getDate();
		day = day.toString();
		if(day.length == 1)
			day = "0"+day;
			
        var month = \$("#agenda").datepicker('getDate').getMonth() + 1;
		month = month.toString();
		if(month.length == 1)
			month = "0"+month;
        var year = \$("#agenda").datepicker('getDate').getFullYear();
		
	
		if(events2.indexOf(month+"/"+day+"/"+year) > -1)
			{
			// alerta(month+"/"+day+"/"+year+" Com NFes");
			\$("#dia_list").text(day+"/"+month+"/"+year);
			nfShowDay(year+''+month+''+day);
			}
		// else
		//	alerta(month+"/"+day+"/"+year+" Sem NFes");
		});
// DATEPICKER ------------------------------------------------------------
	
	
	// calcula total NF
	\$("#v1, #v2, #v3").blur(function()
		{
		var soma = 0;
		\$(".valor").each(function()
			{
			soma += money(\$(this).val(),1);
			});
	
		\$('#nf_total').val(money(soma));
        \$("#nf_total").setMask()
		});
	
	// carrega lista de nf
	nf();
	
	unLoading(); // remove loader ---	
	});

/* NF ------------------------------------------------------------------------------------------------------------ */
function nf(req)
	{
	// loading
	Loading();
	
	// prepara post
	req += "&"+\$("#CAD").serialize();
	// alert(req); // debug
	
	// executa
	$ajax_init \$.ajax(
		{
		type: "POST",
		url: "$dir{faturamento}nf.cgi",
		dataType: "html",
		data: req,
		success: function(data)
			{
			\$("body").append(data);
			
			// marca nf que esta em edicao
			if(\$("#NF").val() != "")
				{
				// glow('day_'+\$("#NF").val());
				// menu_faturamento.btnShow('icon_delete');
                eos.menu.action.show(["icon_fat_delete"])
				}
				
			unLoading();
			},
		error: errojx
		});
	}

/* NF Edit ------------------------------------------------------------------------------------------------------  */
function nfEdit(cod)
	{
	// menu_faturamento.btnHide("icon_edit");
	\$("#NF").val(cod);
	
    
    eos.menu.action.show(["icon_fat_print"]);
    
    // eos.menu.action.show(["icon_fat_print","icon_fat_delete"])
	// menu_faturamento.btnShow('icon_print');
	// menu_faturamento.btnShow('icon_duplicate');
	
	// envia string para mostrar
	nf("ACAO=show");
	}

/* NF Show Day / Month ------------------------------------------------------------------------------------------  */
function nfShowDay(dat)
	{
	resetform();
	
	// seta variavel do dia
	\$("#SHOWDAY").val(dat);
	
	// envia string para mostrar
	nf("&SHOWDAY="+dat);
	}

/* NF Duplicar ---------------------------------------------------------------------------------------------------  */
function nfDuplicar()
	{
	\$("#data_emissao").val("$hoje");
	\$("#nf_num, #data_vcto").val("");
	\$("#obs").val("$OBS");	
	\$("#v1, #v2, #v3").val("");
	\$("#nf_total").val("");
	\$("#NF").val("");
	
	// menu_faturamento.btnHide('icon_print');
	// menu_faturamento.btnHide('#icon_duplicate');
	}
	
/* NF Edit BTN --------------------------------------------------------------------------------------------------  */
function nfEditBtn(cod)
	{
	// resetform();
	// \$("#NFTMP").val(cod);
	// menu_faturamento.btnShow("icon_edit");
	}

/* NF Edit BTN --------------------------------------------------------------------------------------------------  */
function nfPrintCfg()
	{
	nf("ACAO=cfg");
	}
	
/* Excluir NF ----------------------------------------------------------------------------------------------------  */
    /*
function excluir() {
    DActionDelete();
}
    */
/*
function DActionDelete(valida)
	{
	if(!valida)
		{
		confirma("Deseja realmente excluir ?","DActionDelete(1)");
		return;
		}
		
	nf("&ACAO=delete");
	}
*/
/* Imprimir  ----------------------------------------------------------------------------------------------------  */
    /*
function imprimir()
	{
	\$("#CAD").attr({action:'$dir{faturamento}print.pdf', target:'_blank'});
	\$("#CAD").submit();
	
	/*
	// executa download
	\$.DDownload(
		{
		action:'$dir{faturamento}print.pdf',
		vars:\$("#CAD").serializeArray()
		});
	*
	}
*/
	
/* Editar  ----------------------------------------------------------------------------------------------------  */
function editar()
	{
	// nfEdit(\$("#NFTMP").val());
	}

/* Salvar ------------------------------------------------------------------------------------------------------------  */
    /*
function salvar()
	{	
	if(\$("#cliente").val() == "" || \$("#cliente_descrp").val() == "" || \$("#data_emissao").val() == "" || \$("#data_vcto").val() == "" || \$("#nf_num").val() == "")
		{
		console.log(\$("#cliente").val() == "" || \$("#cliente_descrp").val() == "" || \$("#data_emissao").val() == "" || \$("#data_vcto").val() == "" || \$("#nf_num").val() == "");
		alerta("Campos obrigatórios: <br> <p style='text-align:left'>- Cliente, Número Nota Fiscal <br> - Data Emissão, Data Vencimento.</p>");
		return;
		}

	// envia string para salvar
	nf("ACAO=salvar");
	}
	*/
/* Novo  --------------------------------------------------------------------------------------------------------------  */
function incluir()
	{
	resetform();
	}
	
/* Limpa Formulario ---------------------------------------------------------------------------------------------------  */
function resetform()
	{
        eos.menu.action.hide(["icon_fat_print","icon_fat_delete"]);
	\$("#data_emissao").val("$hoje");
	\$("#nf_num, #data_vcto").val("");
	\$("#cliente, #cliente_descrp").val("");
	\$("#obs").val("$OBS");	
	\$("#d1, #d2, #d3, #v1, #v2, #v3").val("");
	\$("#nf_total").val("");
	\$("#NF").val("");
	}
</script>
</head>
<body>

<form name='CAD' id='CAD' method='post' class='form_faturamento'>
<input type='hidden' name='ID' id='ID' value='$ID'>
<input type='hidden' name='NF' id='NF'>
<input type='hidden' name='NFTMP' id='NFTMP'>
<input type='hidden' name='SHOWDAY' id='SHOWDAY'>
<input type='hidden' name='MODO' id='MODO' value='$MODO'>

<table style="width:99%; margin-top:10px; margin-right:1%;" border=0>
	<tr valign="top">
		<td style="width:17%; padding:0.5%; padding-left:0px;">

	
<!-- Agenda v v ***************************************************************************************** -->	
	<div align="center" valign="center">
		<span id='agenda'><span>
	</div>
	
	</td>



<td id='DVNF' style="width:80%; padding:0.5%; padding-right:0px;">
		
<!-- NF Formulario v v ************************************************************************************** -->			
	<div id="form_faturamento_fields">
		
		<div style="width:45%; float:left;">	
		<table style="width:95%; margin:0.5%;">	
		<tr class="teste_form">
			<td colspan="2">
			    <input type="text" name="nf_num" id="nf_num"> 
			</td>
		</tr>
		<tr class="teste_form">
			<td>
			    <input type="text" name="data_emissao" id="data_emissao" placeholder="Emissão">
			</td>
			<td>
			    <input type="text" name="data_vcto" id="data_vcto" placeholder="Vencimento"> 
			</td>
		</tr>
		<tr class="teste_form">
			<td colspan="2">
				<input type="hidden" name="cliente" id="cliente"> 
			    <input type="text" name="cliente_descrp" id="cliente_descrp">
			</td>
		</tr>		
		<tr>
			<td colspan="2"><textarea name="obs" id="obs" style="height:78px; width: 100%; resize: none;"></textarea> </td>
		</tr>
		</table>
		
		</div>
		<div style="width:53%; float:left; height:190px;">
			
			<div style="margin-top:25px;">
				
			</div>
			
			<div style="margin-top:5px;  height:100px; padding-left:5px;">
				<div style="margin-top:5px;">
					<span style="float:left; width:64%;"><input type="text" name="d1" id="d1" style="width:70%;" placeholder="Descrição"></span>
					<span style="float:right; width:35%;"><input type="text" name="v1" id="v1" placeholder="Valor" class="valor"></span>
				</div> <br clear=both>
				<div style="margin-top:5px;">
					<span style="float:left; width:64%;"><input type="text" name="d2" id="d2" style="width:70%;" placeholder="Descrição"></span>
					<span style="float:right; width:35%;"><input type="text" name="v2" id="v2" placeholder="Valor" class="valor"></span>
				</div> <br clear=both>
				<div style="margin-top:5px;">
					<span style="float:left; width:64%;"><input type="text" name="d3" id="d3" style="width:70%;" placeholder="Descrição"></span>
					<span style="float:right; width:35%;"><input type="text" name="v3" id="v3" placeholder="Valor" class="valor"></span>
				</div> <br clear=both>
			</div>
			<div style="margin-top:5px; text-align:right;  padding-left:5px;">
				<input type="text" name="nf_total" id="nf_total" style="margin-right:13px;" placeholder="Total">
			</div>
		</div>
	</div>	
	
</td>
</tr>
</table>

<!-- Tabs das nf **************************************************************************** -->		
<div style='width: 99%; margin-right: 1%;'>
	<div id="nf_tab" style="clear:both; top:0px;" align="right" >
		<ul style='border-bottom:0px;'>
			<li style='margin-top: 2px'><a href="#tabs-0">Mês</a></li>
			<!-- <li style='margin-top: 2px'><a href="#tabs-1">Dia <b id="dia_list" style="font-size:10px;"></b></a></li>
			<li style='margin-top: 2px'><a href="#tabs-3">Todas</a></li> -->
			<li style='margin-top: 2px'><a href="#tabs-2">Configuração Impressão</a></li>
		</ul>

		<!--  MES *************************************************************************** -->					
		<div id="tabs-0"  style='min-height:200px;'>
			<div id='nf_month' class="navigateable_box rounded_u" style="height:280px; overflow-y: auto;"></div>
		</div>
		
		<!--   DIA **************************************************************************** 
		<div id="tabs-1"  style='min-height:200px;'>
			<div id='nf_day' class="navigateable_box rounded_u" style="height:280px; overflow-y: auto;"></div>
		</div>
		
		  Anterior 
		<div id="tabs-3"  style='min-height:200px;'>
			<div id='nf_all' class="navigateable_box rounded_u" style="height:280px; overflow-y: auto;"></div>
		</div>
		-->
		
		<!--   CONFIG IMPRESSAO **************************************************************************** -->								
		<div id="tabs-2"  style='min-height:200px;'>
			<div class="navigateable_box rounded_u" style="height:280px; overflow-y: auto; text-align:left;">
				<div style="float:left; width:40%;">
				<table cellspacing='1' cellpadding='1' class='navigateable' style='width:100%;'>
					<thead align="center">
						<tr>
							<th>Campo</th><th>Esquerda</th><th>Topo</td>
						</tr>
					</thead>
					<tbody class='noglow form_faturamento_config'>
						<tr>
							<td>Data Emissão</td><td><input type="text" name="cfg_left_data_emissao" id="cfg_left_data_emissao"></td><td><input type="text" name="cfg_top_data_emissao" id="cfg_top_data_emissao"></td>
						</tr>
						<tr>
							<td>Nome</td><td><input type="text" name="cfg_left_nome" id="cfg_left_nome"></td><td><input type="text" name="cfg_top_nome" id="cfg_top_nome"></td>
						</tr>
						<tr>
							<td>Endereço</td><td><input type="text" name="cfg_left_end" id="cfg_left_end"></td><td><input type="text" name="cfg_top_end" id="cfg_top_end"></td>
						</tr>
						<tr>
							<td>Município</td><td><input type="text" name="cfg_left_municipio" id="cfg_left_municipio"></td><td><input type="text" name="cfg_top_municipio" id="cfg_top_municipio"></td>
						</tr>
						<tr>
							<td>UF</td><td><input type="text" name="cfg_left_uf" id="cfg_left_uf"></td><td><input type="text" name="cfg_top_uf" id="cfg_top_uf"></td>
						</tr>
						<tr>
							<td>CEP</td><td><input type="text" name="cfg_left_cep" id="cfg_left_cep"></td><td><input type="text" name="cfg_top_cep" id="cfg_top_cep"></td>
						</tr>
						<tr>
							<td>CNPJ</td><td><input type="text" name="cfg_left_cnpj" id="cfg_left_cnpj"></td><td><input type="text" name="cfg_top_cnpj" id="cfg_top_cnpj"></td>
						</tr>
						<tr>
							<td>IE</td><td><input type="text" name="cfg_left_ie" id="cfg_left_ie"></td><td><input type="text" name="cfg_top_ie" id="cfg_top_ie"></td>
						</tr>
						<tr>
							<td>Linha 1 Descrição</td><td><input type="text" name="cfg_left_d1" id="cfg_left_d1"></td><td><input type="text" name="cfg_top_d1" id="cfg_top_d1"></td>
						</tr>
						<tr>
							<td>Linha 1 Valor</td><td><input type="text" name="cfg_left_v1" id="cfg_left_v1"></td><td><input type="text" name="cfg_top_v1" id="cfg_top_v1"></td>
						</tr>
						<tr>
							<td>Linha 2 Descrição</td><td><input type="text" name="cfg_left_d2" id="cfg_left_d2"></td><td><input type="text" name="cfg_top_d2" id="cfg_top_d2"></td>
						</tr>
						<tr>
							<td>Linha 2 Valor</td><td><input type="text" name="cfg_left_v2" id="cfg_left_v2"></td><td><input type="text" name="cfg_top_v2" id="cfg_top_v2"></td>
						</tr>
						<tr>
							<td>Linha 3 Descrição</td><td><input type="text" name="cfg_left_d3" id="cfg_left_d3"></td><td><input type="text" name="cfg_top_d3" id="cfg_top_d3"></td>
						</tr>
						<tr>
							<td>Linha 3 Valor</td><td><input type="text" name="cfg_left_v3" id="cfg_left_v3"></td><td><input type="text" name="cfg_top_v3" id="cfg_top_v3"></td>
						</tr>
						<tr>
							<td>Total Serviços</td><td><input type="text" name="cfg_left_total" id="cfg_left_total"></td><td><input type="text" name="cfg_top_total" id="cfg_top_total"></td>
						</tr>
						<tr>
							<td>Observações</td><td><input type="text" name="cfg_left_obs" id="cfg_left_obs"></td><td><input type="text" name="cfg_top_obs" id="cfg_top_obs"></td>
						</tr>
						<tr>
							<td>Valor Líquido</td><td><input type="text" name="cfg_left_liquido" id="cfg_left_liquido"></td><td><input type="text" name="cfg_top_liquido" id="cfg_top_liquido"></td>
						</tr>
					</tbody>
				</table>
				</div>
				
				<div style="float:left; width:20%"> <br> <br>
					<button id="print_config" type="button" class="" onClick="nfPrintCfg()">Atualizar Configuração</button>
				</div>
				
			</div>
		</div>
	</div>
<br clear=both>
</div>
</form>



<!-- NFes da solicitacao SEMANA ************************************************************************ 					
			<div id="tabs-1"  style='min-height:200px;'>
				<div id='nf_week' class="navigateable_box rounded_u" style="height:300px; overflow-y: auto; "></div>
			</div> -->
			
<!-- NFes da solicitacao TODAS *************************************************************************** 
			<div id="tabs-3"  style='min-height:200px;'>
				<div id='DVtaskList' class="navigateable_box rounded_u" style="height:300px; overflow-y: auto;"></div>
			</div>
			-->


</body></html>
HTML
