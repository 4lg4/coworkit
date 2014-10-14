#!/usr/bin/perl

$nacess = "";
require "../../cfg/init.pl";
$SHOW = &get('SHOW');
$FROM = &get('FROM');


# seta variaveis de controle
$nacess_ti = "";
$nacess_setor = "";
$nacess_user = "";
$nacess_cron = "";
$nacess_procede = "";
$nacess_processo = "";
if($dir{dados_ti} ne "" || $dir{dados_user} ne "" || $dir{cron} ne "" || $dir{setor} ne "" || $dir{procede} ne "" || $dir{processo} ne "")
	{
	# se o usuario for administrador
	# define flag de controle para acesso ao modulo
	if($LOGUSUARIO eq "admin")
		{
		if($dir{dados_ti} ne "")
			{
			$nacess_ti = "s";
			}
		if($dir{dados_user} ne "")
			{
			$nacess_user = "s";
			}
		if($dir{cron} ne "")
			{
			$nacess_cron = "s";
			}
		if($dir{procede} ne "")
			{
			$nacess_procede = "s";
			}

		}
	else
		{
		$sth = $dbh->prepare("select * from usuario_menu where usuario_menu.usuario = '$LOGUSUARIO' and (usuario_menu.menu = '204' or usuario_menu.menu = '205' or usuario_menu.menu = '206' or usuario_menu.menu = '902' or usuario_menu.menu = '701' or usuario_menu.menu = '705') ");
		$sth->execute;
		if($dbh->err ne "")
		      {
		      print $query->header({charset=>utf8});
		      &erroDBH();
		      }
		$rv = $sth->rows;
		if($rv > 0)
			{
			while($row = $sth->fetchrow_hashref)
				{
				if($row->{'menu'} eq "204")
					{
					$nacess_ti = $row->{direito};
					}
					
				if($row->{'menu'} eq "205")
					{
					$nacess_user = $row->{direito};
					}
					
				if($row->{'menu'} eq "206")
					{
					$nacess_procede = $row->{direito};
					}
					
				if($row->{'menu'} eq "902")
					{
					$nacess_cron = $row->{direito};
					}
				}
			}
		}
	}

print $query->header({charset=>utf8});

print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html id="html">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <link rel="stylesheet" type="text/css" href="$dir{'css_syscall'}grid.css" >
  <script src="/comum/DPAC_syscall/autosave.js" type="text/javascript"></script>
  <script src="/comum/DPAC_syscall/jquery/jquery.table_navigation.js" type="text/javascript"></script>

  <script language='JavaScript'>

  
  
  	\$("#AUX input[name=VOLTAR]").val("0");
	function scrolify(tblAsJQueryObject, height)
		{
		var oTbl = tblAsJQueryObject;
		if(oTbl.height() > height)
			{
			// for very large tables you can remove the four lines below
			// and wrap the table with <div> in the mark-up and assign
			// height and overflow property
			var oTblDiv = \$("<div/>");
			oTblDiv.css('width', oTbl.width());
			oTblDiv.css('height', height);
			oTblDiv.css('overflow-y','scroll'); 
			oTblDiv.css('position','absolute');
			oTblDiv.css('top','13px');
			oTbl.wrap(oTblDiv);

			// save original width
			oTbl.attr("data-item-original-width", oTbl.width());
			oTbl.find('thead tr th').each(function(){
				\$(this).attr("data-item-original-width",\$(this).width());
				}); 
			//oTbl.find('tbody tr:eq(0) td').each(function(){
			//	\$(this).attr("data-item-original-width",\$(this).width());
			//	});                 


			// clone the original table
			var newTbl = oTbl.clone();

			// remove table header from original table
			//oTbl.find('thead tr').remove();                 
			oTbl.find('thead tr th').html('');                 
			// remove table body from new table
			newTbl.find('tbody tr').remove();   

			oTbl.parent().parent().prepend(newTbl);
			var newTblDiv = \$("<div/>");
			newTblDiv.css('overflow-y','auto');               
			newTblDiv.css('position','absolute');
			newTblDiv.css('top','0px');
			newTblDiv.css('z-index','100');
			newTbl.wrap(newTblDiv);

			// replace ORIGINAL COLUMN width                
			newTbl.attr('width', newTbl.attr('data-item-original-width'));
			newTbl.find('thead tr th').each(function(){
				\$(this).attr('style', 'width:'+\$(this).attr("data-item-original-width")+'px');
				});     
			oTbl.attr('width', oTbl.attr('data-item-original-width'));      
			oTbl.find('thead tr th').each(function(){
				\$(this).attr('style', 'width:'+\$(this).attr("data-item-original-width")+'px');
				});
			}
		}
	
	// gera menus
	// var menu_grid = new menu(['icon_insert']);
	
	var tam = document.getElementById('html').scrollHeight-170;
	var tamH = top.\$('#menu').width();


	function startGrid()
		{
		$ajax_init \$.ajax({
				type: "POST",
				url: "/sys/done/grid/tablecols.cgi",
				dataType: "json",
				data: \$("#grid_form").serialize(),
				success: startCols,
				error: erro
				});
		}


	function ListCols()
		{
		$ajax_init \$.ajax({
				type: "POST",
				url: "/sys/done/grid/tablecols.cgi",
				dataType: "json",
				data: \$("#grid_form").serialize(),
				success: showCols,
				error: erro
				});
		}

	function RunGrid()
		{
		LoadingObj('container');
		cookieForms('save', 'grid_$SHOW $ID');
		$ajax_init \$.ajax({
				type: "POST",
				url: "/sys/done/grid/grid.cgi",
				dataType: "html",
				data: \$("#grid_form").serialize(),
				success: showGrid,
				error: erro
				});
		}

	function showGrid(c)
		{
		\$('#container').html(c);
		orig = c;
		screenRefresh();
		scrolify(\$('#grid'), tam+20);
		unLoadingObj('container');
		}

	function startCols(c)
		{
		var options = '<option value="">Todos</option>';
		for (var i = 0; i < c.length; i++)
			{
			options += '<option value="' + c[i].optionValue + '">' + c[i].optionDisplay + '</option>';
		}
		\$("select#cols").html(options);
		cookieForms('open', 'grid_$SHOW $ID');
		\$("#grid_form input[name=ID]").val('$ID');
		RunGrid();
		}

	function showCols(c)
		{
		var options = '<option value="">Todos</option>';
		for (var i = 0; i < c.length; i++)
			{
			options += '<option value="' + c[i].optionValue + '">' + c[i].optionDisplay + '</option>';
			}
		\$("select#cols").html(options);
		}

	function erro(XMLHttpRequest, textStatus, errorThrown)
		{
		unLoading();
		alerta("ERRO!<br><br>"+XMLHttpRequest+" "+textStatus+" "+errorThrown);
		}

	function windowResize()
		{
		if(orig)
			{
			showGrid(orig);
			}
		}

	// function START()
	//	{		
		// inicia grid
		// startGrid();
        
        /*    
        console.log("novo");
        top.eos.menu.action.show(['icon_grid_new']);
        
		// testa tipo de acesso e atualiza o menu actions
		if('$nacess_tipo' == "a")
			{
			top.eos.menu.action.show(['icon_grid_new']);
			}
		else
			{
            top.eos.menu.action.hideAll();
			// menu_grid.btnHideAll();
			}
            
            // menu_grid.btnShow(['icon_insert']);
		}
		*/
	\$(document).ready(function() 
		{
		// START();
        startGrid();
        
        top.eos.menu.action.hideAll();
        top.eos.menu.action.new({ // new
            id       : "icon_grid_new",
            title    : "novo",
            subtitle : "",
            click    : function(){
                DActionAdd();
            }
        });
        
        top.eos.menu.action.new({ // edit
            id       : "icon_grid_edit",
            title    : "editar",
            subtitle : "",
            click    : function(){
                go(\$("#AUX input[name=COD]").val());
            }
        });
        top.eos.menu.action.hide(["icon_grid_edit"]);
        
        
		\$("#PESQ").keypress(function(e)
			{
			if(e.keyCode == 13)
				{
				pesq();
				}
			});
		
		});
  </script>
</head>
<body id="grid_body">
<form name='grid_$SHOW $ID' id='grid_form' onSubmit='pesq(); return false;' method='POST'>

<div id='grid_pesq'>
	<table border=0 cellpadding=4 cellspacing=0>
		<tr>
			<td><nobr>Texto <input type='text' id='PESQ' name='PESQ'></nobr></td>
			<td><nobr>Campo <select name='CAMPO' id="cols" style='width:100px;'><option value=''>Todos</option></select></nobr></td>
HTML
	$colspan = 3; # seta quantidade de td nas letras
	if($SHOW eq "usuario")
		{
		$CODEMP = &get("EMPRESA");
		if($EMPRESA eq "")
			{
			# Cria vetor da tabela tipo_relacionamento (empresas) ----------------
			$n = 0;
			$SQL = "select distinct empresa.codigo, empresa.nome, empresa.apelido from empresa join usuario on empresa.codigo = usuario.empresa";
			$sth9 = &select("select * from pg_tables where tablename='parceiro_empresa'");
			$rv9 = $sth9->rows();
			if($rv9 > 0)
				{
				$SQL .= " join parceiro_empresa on empresa.codigo = parceiro_empresa.empresa and parceiro_empresa.parceiro = '$LOGEMPRESA' ";
				}
			$SQL .= " order by codigo";

			$sth = &select($SQL);
			$rv = $sth->rows();
			if($rv < 2)
				{
				print "<input type='hidden' name='EMPRESA' value='$CODEMP'>";
				}
			else
				{
				$colspan++; # aumenta a quantidade de td nas letras
				print("<td><nobr>Empresa <select name='EMPRESA' onChange='pesq()' style='width:250px;'><option value=''>Todas</option>");
				while($row = $sth->fetchrow_hashref)
					{
					print "<option value='$row->{codigo}'";
					if($GRUPO eq $row->{codigo})
						{
						print " selected";
						}
					print ">$row->{'nome'}</option>";
					}
				print("</select></nobr></td>");
				}
			}
		else
			{
			print "<input type='hidden' name='EMPRESA' value='$CODEMP'>";
			}
		}
	if($SHOW eq "empresas" || $SHOW eq "contatos")
		{ # onChange='pesq_grupo()'
		$GRUPO = &get("GRUPO");
		if($GRUPO eq "")
			{
			$colspan++; # aumenta a quantidade de td nas letras
			print("<td><nobr>Grupo <select name='GRUPO' onChange='pesq()' style='width:100px;'><option value=''>Todos</option>");

			# Cria vetor da tabela tipo_relacionamento (grupos) ----------------
			$n = 0;
			$SQL = "select * from tipo_relacionamento";
			$sth9 = &select("select * from pg_tables where tablename='parceiro_tipo_relacionamento'");
			$rv9 = $sth9->rows();
			if($rv9 > 0)
				{
				$SQL .= " join parceiro_tipo_relacionamento on tipo_relacionamento.codigo = parceiro_tipo_relacionamento.tipo_relacionamento and parceiro_tipo_relacionamento.parceiro = '$LOGEMPRESA' ";
				}
			$SQL .= " order by codigo";

			$sth = &select($SQL);
			$rv = $sth->rows();
			if($rv < 1)
				{
				$tipo_relacionamento_list_cod[$n] = "";
				$tipo_relacionamento_list[$n] = "Nenhum grupo cadastrado";
				}
			else
				{
				while($row = $sth->fetchrow_hashref)
					{
					print "<option value='$row->{codigo}'";
					if($GRUPO eq $row->{codigo})
						{
						print " selected";
						}
					print ">$row->{'descrp'}</option>";
					}
				}
			print("</select></nobr></td>");
			}
		else
			{
			print "<input type='hidden' name='GRUPO' value='$GRUPO'>";
			}
		}
print<<HTML;
			<td width=50><nobr><a href='javascript:pesq()'><img src='$dir{'img_syscall'}btn_pesq.png' border=0 alt='aplicar'></a><a href='javascript:clear()'> <img src='$dir{'img_syscall'}btn_limpar.png' border=0 alt='limpar'></a></nobr></td>
		</tr>
		<tr>
			<td align=right colspan=$colspan><a href='javascript:clear()'>&lowast;</a>
HTML
@alfa = ("#", "A" ... "Z");
for($f=0; $f<@alfa; $f++)
	{
	print "<a href='javascript:pesq(\"".$alfa[$f]."\")' style='margin-right: 1px'>".$alfa[$f]."</a>";
	}
print<<HTML;
			 </td>
		</tr>
	</table>
</div>

<br clear=both>

<div id="container"></div>


	<input type='hidden' name='ID' value='$ID'>
	<input type='hidden' name='SHOW' value='$SHOW'>
	<input type='hidden' name='INI' value='0'>
	<input type='hidden' name='PESQLETRA'>
	<input type='hidden' name='ORDER'>
	<input type='hidden' name='VOLTAR'>


<script language='JavaScript'>
function screenRefresh()
	{
	try
		{
		jQuery.tableNavigation({
			on_activate: function(row)
				{
				view(jQuery(row).attr("id"));
				return true;
				},
			on_select: function(row)
				{
				set_view(jQuery(row).attr("id"));
				return true;
				}
			});
		}
	catch(err)
		{
		// ignora erro
		}
	if(document.getElementById('html').scrollHeight-170 >= tam)
		{
            /*
		if(navigator.userAgent.indexOf("Firefox/3") != -1)
			{
			document.getElementById('grid').getElementsByTagName('TBODY')[0].style.height = tam +"px";
			}
		else
			{
			document.getElementById('grid_scroll').style.height = tam+35 +"px";
			}
            */
		}
        /*
	var cores = ["$cor1", "$cor2"];
	var linhas = document.getElementById('container').getElementsByTagName('TR');
	for(var ln=1;ln<linhas.length;ln++)
		{
		linhas[ln].className='';
		cor_fundo = cores[ln % 2];
		linhas[ln].style.background = cor_fundo;
		}
        */
	}

/* [INI] ---------------------------------------------------------------------------------------------------------------------
	Empresa, Modulo
 	Menu Especifico Cadastro de empresa	
----------------------------------------------------------------------------------------------------------------------------*/
// modulo dados de ti
function ti()
	{
	\$("#AUX input[name=MODO]").val("ver");
	\$("#AUX input[name=VOLTAR]").val("1");
	
	top.call("$dir{'dados_ti'}dados_ti.cgi");
	}
	
// modulo cron
function cron()
	{
	\$("#AUX input[name=MODO]").val("ver");
	\$("#AUX input[name=VOLTAR]").val("1");
	
	top.call("$dir{'cron'}dados_cron.cgi");
	return true;
	}
	
// modulo procedimentos
function procede()
	{
	// Pega variáveis
	var variaveis =
		{
		empresa : \$("#AUX input[name=COD]").val()
		};
	
	top.call("/procede/start.cgi",variaveis);
	return true;
	}
	
// usuarios, abre modulo
function users()
	{
	\$("#AUX input[name=MODO]").val("ver");
	\$("#AUX input[name=VOLTAR]").val("1");
	
	top.call("$dir{'dados_user'}dados_users.cgi");
	}

// computadores, abre modulo
function pcs()
	{
	\$("#AUX input[name=MODO]").val("ver");
	\$("#AUX input[name=VOLTAR]").val("1");
	
	top.call("$dir{'dados_user'}dados_pc.cgi");
	}
	
//	icone Imprimir Actions quando clicado ---
function imprimir()
	{
	\$("#grid_form")
		.append("<input type='hidden' name='ID' value='"+\$("#AUX input[name=ID]").val()+"'>")
		.append("<input type='hidden' name='COD' value='"+\$("#AUX input[name=COD]").val()+"'>");
	//	.attr(
	//		{
	//		target: "_blank",
	//		action: "$dir{empresa}rel_empresas.pdf"
	//		})
	//	.submit();
	
	// console.log("$dir{empresa}rel_empresas.pdf");
		
	document.forms[0].target = "_blank";
	document.forms[0].action = "$dir{empresa}rel_empresas.pdf";
	document.forms[0].submit();
	}
/* [END] Empresa, Modulo -------------------------------------------------------------------------------------------------- */
	
// adicionar novo cadastro
function DActionAdd()
	{ 
	\$("#AUX input[name=MODO]").val('incluir');
	\$("#AUX input[name=COD]").val('');
	
	//Modulos com div
	var variaveis =
		{
		COD : '',
		MODO : 'incluir'
		};
	
	// Cadastro de empresas novo abre no modelo DIV
	if("$SHOW" == "empresas") { 
        
        if(top.eos.core.limit.empresa.verify()){ // dentro do limite
            top.call("empresa/edit.cgi",variaveis);
        } else {
            top.\$.DDialog({
                type    : "error",
                message : "Limite de empresas excedido ! <br><br> Become a premium !" 
            });
        }
        
		return true;
	}
	else if("$SHOW" == "usuario_tipo")
		{
		top.call("cad/usuario_tipo/edit.cgi",variaveis);
		return true;
		}
	else if("$SHOW" == "usuario")
		{
		top.call("cad/usuarios/edit.cgi",variaveis);
		return true;
		}
	
	go();
	}

// edita linha selecionada
function edit(x)
	{
	go(x);
	}

/**
 *  Abrir
 *      Abre cadastro
 */
function abrir()
	{
	// Pega variáveis
	var variaveis =
		{
		COD : \$("#AUX input[name=COD]").val(),
		MODO : 'editar',
		SHOW: '$SHOW'
		};
	
	// Cadastro de empresas novo abre no modelo DIV
	if("$SHOW" == "empresas")
		{
		call("empresa/edit.cgi",variaveis);
		return true;
		}
	// Cadastro de usuario_tipo novo abre no modelo DIV
	else if("$SHOW" == "usuario_tipo")
		{
		call("cad/usuario_tipo/edit.cgi",variaveis);
		return true;
		}
	// Cadastro de usuarios na DIV
	else if("$SHOW" == "usuario")
		{
		call("cad/usuarios/edit.cgi",variaveis);
		return true;
		}
	// Cadastro de dados de ti
	else if("$SHOW" == "tipo_grupo_item" || "$SHOW" == "grupo" || "$SHOW" == "agrupo" )
		{
		call("$dir{$SHOW}edit.cgi");
		return true;
		}
	else
		{
		call("cad/default/edit.cgi",variaveis);
		return true;
		}
	}
	
function set_view(x)
	{
	if(x)
		{
		\$("#AUX input[name=COD]").val(x);
		}
	else
		{
		\$("#AUX input[name=COD]").val("");
		}
	}
	
// Clique unico no grid
function pre_view(cod)
	{
	// mostra icones especificos do cadastro de empresas
	if("$SHOW" == "empresas")
		{
		if("$nacess_ti" != "")
			{
			// menu_grid.btnShow('icon_ti');
			}
		if("$nacess_user" != "")
			{
			// menu_grid.btnShow('icon_user');
			// menu_grid.btnShow('icon_pc');
			}
		if("$nacess_cron" != "")
			{
			// menu_grid.btnShow('icon_cron');
			}
		if("$nacess_procede" != "")
			{
			// menu_grid.btnShow('icon_procede');
			}
		
		// menu_grid.btnShow('icon_print');
		}
		
	// mostra botao editar
	// menu_grid.btnShow('icon_gridview');    
    top.eos.menu.action.show(["icon_grid_edit"]);

	if(cod)
		{
		\$("#AUX input[name=COD]").val(cod);
		}
	else
		{
		\$("#AUX input[name=COD]").val("");
		}
	
	\$("#AUX input[name=MODO]").val("editar");
	
	}
	
// Line, Duplo Clique 
function view(cod)
	{
	// desabilitado o clique duplo
	// apresentando problemas com o carregamento do modulo 
	// usar o botao editar ate resolucao final 	
	
	if(cod)
		{
		\$("#AUX input[name=COD]").val(cod);
		}
	else
		{
		\$("#AUX input[name=COD]").val("");
		}
	
	\$("#AUX input[name=MODO]").val("editar");
	
	pre_view(cod);
	return;
	
	//abrir();
	
	}
function orderby(x)
	{
	\$("#grid_form input[name=INI]").val(0);
	if(\$("#grid_form input[name=ORDER]").val()==x)
		{
		\$("#grid_form input[name=ORDER]").val(x+" desc");
		}
	else if(\$("#grid_form input[name=ORDER]").val()=='')
		{
		if(document.getElementById(x).className == 'asc')
			{
			\$("#grid_form input[name=ORDER]").val(x+" desc");
			}
		else
			{
			\$("#grid_form input[name=ORDER]").val(x);
			}
		}
	else
		{
		\$("#grid_form input[name=ORDER]").val(x);
		}
	RunGrid();
	}
    
/**
 *  Go
 *      executa acao 
 */ 
function go(x)
	{
	Loading();
	if(x)
		{
		\$("#AUX input[name=COD]").val(x);
		}
	else
		{
		\$("#AUX input[name=COD]").val('');
		}
		
	var variaveis =
			{
			COD : x,
			MODO : 'editar'
			};

	// Cadastro de usuario_tipo novo abre no modelo DIV
	if("$SHOW" == "usuario_tipo")
		{
		top.call("cad/usuario_tipo/edit.cgi",variaveis);
		return true;
		}
	else if("$SHOW" == "usuario")
		{
		top.call("cad/usuarios/edit.cgi",variaveis);
		return true;
		}
	else
		{
	
    var urls = "/sys/cad/default";
    if("$SHOW" === "agrupo"){
        urls = "/sys/done/agrupo";
    }
    
	$ajax_init \$.ajax({
			type: "POST",
			url: urls+"/edit.cgi",
			dataType: "html",
			data: \$("#AUX").serialize(),
			success: function(data)
				{
				\$("#main_div").html(data);
				\$("#resultado").html(data);
				unLoading();
				},
			error: errojx
			});
		}
	}
function goto(x)
	{
	if(x > 0)
		{
		\$("#grid_form input[name=INI]").val(x);
		}
	else
		{
		\$("#grid_form input[name=INI]").val('0');
		}
	RunGrid();
	}
function clear()
	{
	document.forms['grid_form'].reset();
	pesq();
	RunGrid();
	}
function pesq(x)
	{
	\$("#AUX input[name=COD]").val('');
	\$("#AUX input[name=MODO]").val('');
	
	\$("#grid_form input[name=INI]").val('0');
	if(x)
		{
		\$("#grid_form input[name=PESQLETRA]").val(x);
		}
	else
		{
		\$("#grid_form input[name=PESQLETRA]").val('');
		}
	RunGrid();
	}
</script>

<div id="img">
</div>

</form>

<div id="foot"></div>

</body></html>
HTML
