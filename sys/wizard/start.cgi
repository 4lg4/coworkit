#!/usr/bin/perl

# $nacess = "direct";
$nacess = "";
require "../cfg/init.pl";
$usuario = &get('usuario'); 
$chave = &get('chave');


$usuario = 90;
$chave = 'lnk@951';
$nacess_emp = "s";
$nacess_ti = "s";
$nacess_ts = "s";

print $query->header({charset=>utf8});

print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html id="html">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">

<script type="text/javascript" src="/comum/DPAC_syscall/DPAC.js"></script>
<!-- 
    <script language="JavaScript" src="/comum/DPAC_syscall/dhtml-suite/js/separateFiles/dhtmlSuite-common.js"></script>
-->

<link rel="stylesheet" href="/css/CSS_syscall/comum/jquery.lightbox-0.5.css" type="text/css" media="screen" />
<script type="text/javascript" src="/comum/DPAC_syscall/jquery/jquery.lightbox-0.5.js"></script>
HTML

# Pega a empresa do parceiro
$sth = $dbh->prepare("select * from usuario where usuario = $usuario ");
$sth->execute;
if($dbh->err ne "")
	{
	&erroDBH();
	}
if($rv = $sth->rows > 0)
	{
	$row = $sth->fetchrow_hashref;
	$empresa = $row->{empresa};
	}
$sth->finish;


# verifica direitos de acesso 
# $nacess_emp = "";
# $nacess_ti = "";
# $nacess_ts = "";
# $pass_ti = 1;

# $sth = $dbh->prepare("select * from usuario_direitos where usuario_direitos.usuario = '$usuario' and (usuario_direitos.menu = '201' or usuario_direitos.menu = '204' or usuario_direitos.menu = '66') ");
# $sth->execute;
# if($dbh->err ne "")
#       {
#       &erroDBH();
#       }
# $rv = $sth->rows;
# if($rv > 0)
# 	{
# 	while($row = $sth->fetchrow_hashref)
# 		{
# 		if($row->{'menu'} eq "201")
# 			{
# 			# Menu de cadastro de empresas
# 			$nacess_emp = $row->{'tipo'};
# 			}
# 		elsif($row->{'menu'} eq "204")
# 			{
# 			# Menu de dados de TI
# 			$nacess_ti = $row->{'tipo'};
# 			}
# 		elsif($row->{'menu'} eq "66")
# 			{
# 			# Menu de Timesheet
# 			$nacess_ts = $row->{'tipo'};
# 			}
# 		}
# 	}
# $sth->finish;


# Verifica se já tem dados de TI preenchidos
#if($nacess_ti ne "")
#	{
#	$sth = $dbh->prepare("select * from parceiro_grupo where parceiro_grupo.parceiro = '$empresa' ");
#	$sth->execute;
#	if($dbh->err ne "")
#		{
#		&erroDBH();
#		}
#	$pass_ti = $sth->rows;
#	}
# $sth->finish;


print<<HTML;
<script language="Javascript">
    top.unLoading();

	// DHTMLSuite.include("modalMessage");
</script>

<!-- <script language="JavaScript" src="/comum/DPAC_syscall/ui.js"></script> -->

<script type="text/javascript">

// quando o documento esta pronto ---------
\$(document).ready(function() 
	{
	\$("#STEP").val("start");
	\$('#icon_step_back').hide();
	
	\$('.light').lightBox();

	});


function erro(x,y)
	{
	if(y.indexOf('[') > 0)
		{
		el = y.substring(0,y.indexOf('['));
		pos = y.substring(y.indexOf('[')+1, y.indexOf(']'));
		document.getElementsByName(el)[pos].style.borderColor = 'red';
		alerta(x,"document.getElementsByName(\\""+el+"\\")["+pos+"].focus()");
		}
	else
		{
		document.getElementsByName(y)[0].style.borderColor = 'red';
		alerta(x,"document.forms[0]."+y+".focus()");
		}
	}
function limpa(y)
	{
	if(y)
		{
		document.getElementsByName(y)[0].style.borderColor = '';
		}
	}

/*  Salva configuração do Wizard  */
function stepExec()
	{
	req = \$("#CAD").serialize();
	
	// Executa wizard submits
	\$.ajax(
		{
		type: "POST",
		url: "edit_submit.cgi",
		dataType: "html",
		data: req,
		success: function(data)
			{
			\$("#salvar_result").html(data);
			},
		error: errojx
		});
	}
	
/*  Botao voltar  */
function stepBack()
	{
	if(\$("#STEP").val() == "trocasenha")
		back = "start";	
	else if(\$("#STEP").val() == "dadosti")
		back = "homescreen";	
	else if(\$("#STEP").val() == "homescreen")
		back = "trocasenha";
		
	// se existirem mais passos
	//	else if(\$("#STEP").val() == "trocasenha")
	//	 back = "dadosti";	

	// stepExec("trocasenha");
	\$("#"+\$("#STEP").val()).hide("slow", function()
		{
		\$("#"+back).show("slow");
		\$("#STEP").val(back);
		
		if(back == "start")
			\$('#icon_step_back').hide();
		});
	}
	
/*  Botao avancar  */
function stepForward()
	{
	// alert(\$("#STEP").val());
	// parent.block(false);
	
	// alert(\$("div.wizard_box:visible").attr("id"));
	
	if(\$("#STEP").val() == "start")
		stepStart();
	else if(\$("#STEP").val() == "trocasenha")
		stepTrocasenha();
	else if(\$("#STEP").val() == "homescreen")
	 	stepHomeScreen();
	else if(\$("#STEP").val() == "dadosti")
	 	stepDadosTI();
	else if(\$("#STEP").val() == "salvar")
	 	stepExec();
	}

/* Tela Inicial, inicia Wizard */
function stepStart()
	{	
	\$("#start").hide("slow", function()
		{
		\$("#trocasenha").show("slow");
		\$("#STEP").val("trocasenha");
		\$('#icon_step_back').show();
		});
		
	// if(\$('input:radio[name=modulo]:checked').val() == 1)
	}

/* troca senha, testa consistencia */
function stepTrocasenha()
	{
	if(\$("#senha_nova").val() == "")
		{
		erro('Você não informou a "nova senha"!', 'senha_nova');
		return false;
		}
	if(\$("#senha_nova_prova").val() == "")
		{
		erro('Você não informou "repetir nova senha"!', 'senha_nova_prova');
		return false;
		}
	if(\$("#senha_nova").val() != \$("#senha_nova_prova").val())
		{
		erro('Novas Senhas não conferem!', 'senha_nova');
		return false;
		}
	if(\$("#senha_nova").val() == '$chave')
		{
		erro('A senha nova não pode ser igual a chave!', 'senha_nova');
		return false;
		}
		
	// stepExec("trocasenha");
	\$("#trocasenha").hide("slow", function()
		{
		\$("#homescreen").show("slow");
		\$("#STEP").val("homescreen");
		\$('#icon_step_back').show();
		});
	}

/* Tela Inicial, testa consistencia */
function stepHomeScreen()
	{	
	// stepExec("homescreen");
	\$("#homescreen").hide("slow", function()
		{
HTML
if($pass_ti > 0)
		{
print<<HTML;
		\$("#salvar").show("slow");
		\$('#icon_step_back').hide();
		\$('#icon_step_fwd').hide();
		\$("#STEP").val("salvar");
		stepExec();
HTML
		}
else
		{
print<<HTML;
		\$("#dadosti").show("slow");
		\$("#STEP").val("dadosti");
		\$('#icon_step_back').show();
HTML
		}
print<<HTML;
		});
		
	// if(\$('input:radio[name=modulo]:checked').val() == 1)
	}
	
/* dados de ti, testa consistencia */
function stepDadosTI()
	{
	// colocar aqui os testes para dados de ti se for o caso
	// stepExec("dadosti");
	\$("#dadosti").hide("slow", function()
		{
		\$("#salvar").show("slow");
		\$('#icon_step_back').hide();
		\$('#icon_step_fwd').hide();
		\$("#STEP").val("salvar");
		stepExec();
		});
	}

function unLoading()
	{
	return true;
	}
	
</script>
<style>
html, body 
	{
	width:100%;
	height:100%;
	margin:0px;
	padding:0px;
	}
.syscall
	{
	font-weight:bolder;
	color:#17378a;
	}
.wizard_message 
	{
	font-weight:bold;
	color:#333;
	font-size:1.2em;
	}
.menu_btn
	{
	width: 46px;
	height: 46px;
	cursor: pointer;
	border-radius: 3px 3px 3px 3px;
	font-family: Arial;
	color: rgb(255, 255, 255);
	margin-top: 3px;
	background: none repeat scroll 0% 0% rgb(30, 49, 105);
	text-shadow: 1px 1px 0px rgb(77, 34, 39);
	}
.menu_btn_container
	{
	display: table-cell;
	vertical-align: bottom;
	width: 46px;
	height: 46px;
	}
.menu_btn_title_sub
	{
	font-size: 10px;
	border-bottom: 1px solid rgb(255, 255, 255);
	width: 40px;
	}
</style>
</head>

<body style="background-image:url(http://www.done.com.br/syscall/wizard/img/bg-page.jpg); margin: 0px; overflow-y: hidden;">

<form name='CAD' id='CAD' method='post'>
<input type='hidden' name='STEP' id='STEP'>
<input type='hidden' name='usuario' id='usuario' value='$usuario'>
<input type='hidden' name='chave' id='chave' value='$chave'>

<center>

<div id="top" style="background:#1784bc; width:100%; height:5px; top:0px; left:0px;"></div>
<div id="logo" style="position: absolute; width:100%; top:0px; left:0px; padding-top:10px; padding-bottom:10px; background-image:url(http://www.done.com.br/syscall/wizard/img/bg.png)">
	<img src="http://www.done.com.br/syscall/wizard/img/logo.png">
</div>
<div id="welcome" style="position: absolute; top: 110px; left: 0px; background-image:url(http://www.done.com.br/syscall/wizard/img/bg-welcome.jpg); width:100%; height:67px;">
	<img src="http://www.done.com.br/syscall/wizard/img/welcome.jpg">
</div>

<!-- usar essa parte nao mexer no resto -->
<div id="main" style="width:100%; position: absolute; top: 0px; bottom: 82px; overflow-y: auto;">
	<table style="width:50%; height:30%;" align="center">
		<tr>
			<td>
			<div id="start" class=".wizard_box" style="padding:20px; width: 600px; margin-top: 20px; margin-left: 60px;">
				<div class='fake_aba'>Assistente de configuração inicial</div>
				<div class="navigateable_box" style="padding-bottom:10px">
					<div id="trocasenha_message" class="wizard_message" style="margin:10px;">
HTML
if($usuario eq "")
	{
	print "<h2>Acesso Negado!</h2>
					</div><br><br>
				</div>
			</div>";
	}
elsif($chave eq "")
	{
	print "<h2>Você não informou a chave de acesso!</h2>
					</div><br><br>
				</div>
			</div>";
	}
elsif($nacess_emp eq "" && $nacess_ti eq "" && $nacess_ts eq "")
	{
	print "<h2>Você não tem direito suficientes de acesso ao sistema!</h2>
					</div><br><br>
				</div>
			</div>";
	}
else
	{
	$sth = $dbh->prepare("select usuario.usuario, usuario.nome, usuario.senha, password('$chave') as chave from usuario where usuario.usuario = '$usuario' ");
	$sth->execute;
	if($dbh->err ne "")
		{
		&erroDBH();
		}
	if($rv = $sth->rows > 0)
		{
		$row = $sth->fetchrow_hashref;
		if($row->{senha} ne $row->{chave})
			{
			print "<h2>O sistema já foi configurado. Você não pode reutilizar esse assistente</h2>					</div><br><br>
				</div>
			</div>";
			}
		else
			{
print<<HTML;
						<h2>
						$row->{nome},<br><br></h2>

						Esse assistente irá guia-lo no processo inicial de configuração do nosso sistema.<br><br><br>

						Clique no botão abaixo para iniciar...
					</div><br><br>
				</div>
			</div>


			<div id="trocasenha" class=".wizard_box" style=" width: 600px; padding:20px; display:none; margin-top: 20px; margin-left: 60px;">
				<div class='fake_aba'>Criação de senha</div>
					
				<div class="navigateable_box" style="padding-bottom:10px">
					<div id="trocasenha_message" class="wizard_message" style="margin:10px;">Definir uma senha pra sua nova conta e o nome de exibição no <span class="syscall">Syscall</span></div>
					
					<dl class=form style="margin:10px; position: relative;">
						<div>
							<dt><nobr>Login/Usuário</nobr></dt>
							<dd><span style='margin-left: 10px; text-weight: bold'>$row->{usuario}</span></dd>
						</div>
						<div>
							<dt>Nome</dt>
							<dd><input type='text' name='nome_user' id='nome_user' value="$row->{nome}" maxlength=100></dd>
						</div>
						<div>
							<dt>Nova Senha</dt>
							<dd><input type='password' name='senha_nova' id='senha_nova' maxlength=20></dd>
						</div>
						<div>
							<dt>Repetir Senha</dt>
							<dd><input type='password' name='senha_nova_prova' id='senha_nova_prova' maxlength=20></dd>
						</div>
					</dl>		
					
				</div>
			</div>	


			<div id="homescreen" class=".wizard_box" style="width: 1024px; padding:20px; display:none; margin-top: 20px; margin-left: -100px;">
				<div class='fake_aba'>Tela Inicial</div>
				<div class="navigateable_box" style="padding-bottom:10px"> nothing()
HTML
	if($nacess_emp ne "")
		{
print<<HTML;
					<div id="homescreen_message" class="wizard_message" style="margin:10px;">Selecione um dos módulos abaixo para ser sua Tela Inicial no <span class="syscall">Syscall</span></div>
						<div style="float:left; width:32%; margin-left:1%; text-align:center;">
							<b><input type="radio" name="modulo" id="modulo" value="201" checked="true"> Cadastro de empresas</b> <br>
							<a href="/img/wizard/empresas.jpg" class="light" title="Cadastro de empresas"><img src="/img/wizard/empresas_p.jpg" style="margin:4px;"></a> <br>
							&nbsp;&nbsp;Lista de todas as empresas, com <br> highlight das empresas mais acessadas.
						</div>
HTML
		}
	if($nacess_ti ne "")
		{
print<<HTML;
						<div style="float:left; width:32%; margin-left:1%; margin-right:1%; text-align:center;">
							<b><input type="radio" name="modulo" id="modulo" value="204"> Dados de TI</b> <br>
							<a href="/img/wizard/dadosti.jpg" class="light" title="Dados de TI"><img src="/img/wizard/dadosti_p.jpg" style="margin:4px;"></a> <br>
							&nbsp;&nbsp;Listagem de todas os agrupamentos <br> e dados das empresas em um só lugar.
						</div>
HTML
		}
	if($nacess_ts ne "")
		{
print<<HTML;
						<div style="float:left; width:32%; text-align:center;">
							<b><input type="radio" name="modulo" id="modulo" value="66"> Time Sheet (Coletor de Horas)</b> <br>
							<a href="/img/wizard/coletor.jpg" class="light" title="Time Sheet (Coletor de Horas)"><img src="/img/wizard/coletor_p.jpg" style="margin:4px;"></a> <br>
							&nbsp;&nbsp;Lançamento de Horas para controle <br> de faturamento.
						</div>
HTML
		}
print<<HTML;
					</div>
				</div>
			</div>


			<div id="dadosti" class=".wizard_box" style="padding:20px; display:none; margin-top: 20px;">
				<div class='fake_aba'>Dados de TI</div>
				<div class="navigateable_box" style="padding-bottom:10px; margin-bottom: 100px;">
					<div id="dadosti_message" class="wizard_message" style="margin:10px;">Selecionar os grupos dos dados de TI no <span class="syscall">Syscall</span></div>
					<div>
HTML
	if($pass_ti == 0)
		{
print<<HTML;
HTML
		$SQL = "select distinct grupo.codigo, grupo.descrp from grupo where exportar is true ";

		$SQL = $SQL."order by grupo.descrp";
        
        $SQL_a = $SQL;
        
		$sth3 = &select($SQL);
		$rv3 = $sth3->rows();
		if($rv3 < 1)
			{
			print "Nenhum grupo cadastrado!";
			}
		else
			{
			print "<table width=100% cellpadding=5 cellspacing=0 border=0 align='center'><tbody>";
			$c=0;
			while($row3 = $sth3->fetchrow_hashref)
				{
				if($c==0)
					{
					print "<tr>";
					}
				print "<td>";
				print "<input type='checkbox' name='grupo' value='".$row3->{'codigo'}."' checked> ";
				print $row3->{'descrp'};
				print "</td>";
				if($c==0)
					{
					$c++;
					}
				else
					{
					print "</tr>";
					$c=0;
					}
				}
			print "</table>";
			}
		}
print<<HTML;
					</div>
				</div>
			</div>


			<div id="salvar" class=".wizard_box" style="padding:20px; width: 600px; display: none; margin-top: 20px; margin-left: 60px;">
				<div class='fake_aba'>Gravando suas configurações</div>
				<div class="navigateable_box" style="padding-bottom:10px">
					<div id="salvar_result" class="wizard_message" style="margin:10px;">

					</div><br><br>
				</div>
			</div>

			</td>
		</tr>
	</table>
</div><br clear=both>
<div id="controls" style="min-width: 1024px; width:100%; height:25px; bottom:81px; position:absolute; padding-top:7px;">
	<input type='button' id='icon_step_back' value='<< Anterior' style='float: left; width: 90px; height: 20px; border: 2px outset ButtonFace; margin-left: 20px; background-color: white;' onClick='stepBack()'><input type='button' id='icon_step_fwd' value='Próximo >>' style='float: right; width: 90px; height: 20px; border: 2px outset ButtonFace; margin-right: 20px; background-color: white;' onClick='stepForward()'>
</div>
<div id="bottom" style="background:#1784bc; min-width: 1024px; width:100%; height:81px; bottom: 0px; left:0px; position:absolute;">
	<div id="bottom_top" style="background:#1784bc; width:100%; height:5px; top:0px; left:0px;"></div>
	<div id="navegadores" style="background:#ffffff; width:100%; height:71px; text-align:right;">
		<img src="http://www.done.com.br/syscall/wizard/img/navegadores.jpg">
	</div>
</div>

</center>

</form>

</body></html>
HTML
			}
		}
	else
		{
		print "<h2>Acesso negado!</h2>
					</div><br><br>
			</div>
		</div>";
		}
	}
