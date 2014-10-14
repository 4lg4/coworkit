#!/usr/bin/perl

$nacess = '27';
require "../../cfg/init.pl";
$COD = &get('COD');
$MODO = &get('MODO');
$SHOW = &get('SHOW');
$TABLE = "tipo_grupo_item";
$CHAVE = "codigo";



if($COD eq "" && $MODO ne "incluir")
	{
	print $query->header({charset=>utf8});
	print "Requisição inválida";
	exit;
	}

print $query->header({charset=>utf8});
# debug();
# exit;

$SQL = "select column_name, data_type, character_maximum_length, is_nullable, column_default from information_schema.columns where table_name = '$TABLE' $SQL order by ordinal_position";
$sth = &select($SQL);
$rv = $sth->rows();
if($rv > 0)
	{
	$cols = $sth->fetchall_arrayref();
	}


if($MODO ne "incluir")
	{
	$SQL = "select * from $TABLE where $CHAVE = '$COD' order by $CHAVE limit 1";
	$sth = &select($SQL);
	$rv = $sth->rows();
	if($rv > 0)
		{
		$value = $sth->fetchrow_hashref;
		}
	}


print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html id="html">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <link rel="stylesheet" href="/css/CSS_syscall/form.css" rel="stylesheet" type="text/css">
  <link rel="stylesheet" href="/css/CSS_syscall/comum/jquery.css" type="text/css">

  <script type="text/javascript" src="/comum/DPAC_syscall/display.js"></script>
  <script type="text/javascript" src="/comum/DPAC_syscall/iPAC.js"></script>
  <script type="text/javascript" src="/comum/DPAC_syscall/jquery/jquery-1.4.2.js"></script>
  <script type="text/javascript" src="/comum/DPAC_syscall/jquery/ui/jquery.ui.widget.js"></script>

  <script language='JavaScript'>
	function screenRefresh()
		{
		var cores = ["#dfdfdf", "#ffffff"];
		grids = getElementsByClass('navigateable');
		for(var gd=0;gd<grids.length;gd++)
			{
			linhas = grids[gd].getElementsByTagName('TR');
			for(var ln=1;ln<linhas.length;ln++)
				{
				cor_fundo = cores[ln % 2];
				linhas[ln].style.background = cor_fundo;
				}
			}
		}
	function editar()
		{
		document.forms[0].MODO.value = 'editar';
		document.forms[0].submit();
		}
	function ver()
		{
		parent.block(false);
		if(document.forms[0].COD.value == "")
			{
			top.regrid('$SHOW');
			}
		else
			{
			document.forms[0].MODO.value = 'ver';
			document.forms[0].submit();
			}
		}
	function imprimir()
		{
		alert('não implementado!');
		}
	function incluir()
		{
		document.forms[0].MODO.value = 'incluir';
		document.forms[0].submit();
		}
	function excluir()
		{
		if(blk_items == "S")
			{
			top.confirma('Esse atributo já foi utilizado...<br><br>Confirma a exclusão?', '"top.main.excluir_reconfirm()"', '');
			}
		else
			{
			top.confirma('Você tem certeza que deseja excluir esse registro?<br>Essa ação é IRREVERSÍVEL!', 'main.excluir_confirm()', '');
			}
		}
	function excluir_reconfirm()
		{
		action = "top.confirma('Você tem certeza disso?<br><br>Haverá perda de dados irreversível!!!', 'top.main.excluir_force()', '');";
		setTimeout(action, 250);
		}
	function excluir_force()
		{
		document.forms[0].FORCE.value = 'S';
		excluir_confirm();
		}
	function excluir_confirm()
		{
		parent.block(false);
		document.forms[0].action = "del_submit.cgi";
		document.forms[0].submit();
		}
	function voltar()
		{
		top.regrid('$SHOW');
		}
	function cancelar()
		{
		top.confirma('Você tem certeza que deseja cancelar?<br>Todos os dados modificados serão perdidos!', 'top.main.ver()', '');
		}
	function salvar()
		{
HTML

foreach $row(@{$cols})
	{
	if(uc(@$row[3]) ne "YES" and @$row[4] !~ /^nextval/ )
		{
		print "		if(isNULL(document.forms[0].@$row[0].value) == true)\n";
		print "			{\n";
		print "			erro('Você não informou o ".ucfirst(@$row[0])."!', '@$row[0]');\n";
		print "			return false;\n";
		print "			}\n";
HTML
		}
	}

print<<HTML;
		parent.block(false);
		document.forms[0].action = "edit_submit.cgi";
		document.forms[0].submit();
		}
	function erro(x,y)
		{
		if(y.indexOf('[') > 0)
			{
			el = y.substring(0,y.indexOf('['));
			pos = y.substring(y.indexOf('[')+1, y.indexOf(']'));
			document.getElementsByName(el)[pos].style.borderColor = 'red';
			top.alerta(x,"main.document.getElementsByName(\\""+el+"\\")["+pos+"].focus()");
			}
		else
			{
			document.getElementsByName(y)[0].style.borderColor = 'red';
			top.alerta(x,"main.document.forms[0]."+y+".focus()");
			}
		}
	function limpa(y)
		{
		if(y)
			{
			document.getElementsByName(y)[0].style.borderColor = '';
			}
		}
	function START()
		{
HTML
if($MODO eq "editar" || $MODO eq "incluir")
	{
print<<HTML;
		parent.block(true);
		linhas = document.body.getElementsByTagName('INPUT');
		for(var ln=0;ln<linhas.length;ln++)
			{
			linhas[ln].setAttribute('onchange', 'limpa(this.name)');
			}
		top.ac_show(['icon_save', 'icon_cancel']);
		document.forms[0].elements[1].focus();
HTML
	}
else
	{
print<<HTML;
		linhas = document.body.getElementsByTagName('SELECT');
		for(var ln=0;ln<linhas.length;ln++)
			{
			//linhas[ln].disabled=true;
			linhas[ln].setAttribute('onchange', 'document.forms[0].reset()');
			linhas[ln].style.backgroundColor='#cdcdcd';
			}
		linhas = document.body.getElementsByTagName('INPUT');
		for(var ln=0;ln<linhas.length;ln++)
			{
			if(linhas[ln].type.toLowerCase() != 'hidden')
				{
				//linhas[ln].disabled=true;
				linhas[ln].setAttribute('onchange', 'document.forms[0].reset()');
				if(linhas[ln].type.toLowerCase() != 'radio')
					{
					linhas[ln].style.backgroundColor='#cdcdcd';
					}
				}
			}
		linhas = document.body.getElementsByTagName('TEXTAREA');
		for(var ln=0;ln<linhas.length;ln++)
			{
			//linhas[ln].disabled=true;
			linhas[ln].setAttribute('onchange', 'document.forms[0].reset()');
			linhas[ln].style.backgroundColor='#cdcdcd';
			}
HTML
	$menu_act = "top.ac_show(['icon_back','icon_edit'";
	if($nacess_tipo eq "a")
		{
		$SQL2 = "select * from grupo_item where tipo = '$COD'";
		$sth2 = &select($SQL2);
		$rv2 = $sth2->rows();
		if($rv2 > 0)
			{
print<<HTML;
		blk_items = "S";
		\$('#message').html('Esse atributo está sendo usado nos dados de TI');
HTML
			}
		else
			{
			$SQL3 = "select * from comp_item where tipo = '$COD'";
			$sth3 = &select($SQL3);
			$rv3 = $sth3->rows();
			if($rv3 > 0)
				{
print<<HTML;
		blk_items = "S";
		\$('#message').html('Esse atributo está sendo usado pelos campos adicionais dos computadores');
HTML
				}
			else
				{
				$SQL4 = "select * from user_item where tipo = '$COD'";
				$sth4 = &select($SQL4);
				$rv4 = $sth4->rows();
				if($rv4 > 0)
					{
print<<HTML;
		blk_items = "S";
		\$('#message').html('Esse atributo está sendo usado pelos campos adicionais dos usuários');
HTML
					}
				else
					{
print<<HTML;
		blk_items = "N";
HTML
					if($LOGUSUARIO ne "admin")
					      {
					      $menu_act .= ",'icon_delete'";
					      }
					}
				}
			}
		}
	if($LOGUSUARIO eq "admin")
		{
		$menu_act .= ",'icon_delete'";
		}
	$menu_act .= "]);";
	print $menu_act;
	}
print<<HTML;
		top.unLoading();
		}

  </script>
</head>
<body onLoad="START()" style="overflow-x: hidden; overflow-y: auto;">

<form name='CAD' method='post' action='edit.cgi' onSubmit='return false;'>


<div style='width: 95%; margin: 2%; margin-right: 3%;'>
	<div class='fake_aba' style='width: 40%; margin-left: 0px; padding: 5px;'>Edição da tabela Atributos</div>
		<div class="navigateable_box" style="min-height: 20px; overflow-y: auto; background-color: white; padding: 10px;">

			<dl class=form style="width: 80%; margin-top: 0px;">
				<div>
HTML
foreach $row(@{$cols})
	{
	if(@$row[4] =~ /^nextval/ )
		{
		print "					  <dt>".&traduz(@$row[0])."</dt>\n";
		print "					  <dd><input type='text' name='@$row[0]' value='$value->{@$row[0]}'";
		if(@$row[2] eq "")
			{
			if(@$row[1] =~ /^timestamp/)
				{
				print " style='width: 170px' ";
				}
			else
				{
				print " style='width: 50px' ";
				}
			}
		elsif(@$row[2] < 10)
			{
			print " style='width: ".(@$row[2]*20)."px' ";
			}
		elsif(@$row[2] ne "")
			{
			print " style='width: ".(@$row[2]*3)."px' ";
			}
		print " disabled></dd>\n";
		}
	else
		{
		print "					  <dt>".&traduz(@$row[0])."</dt>\n";
		if(@$row[1] =~ /^boolean/)
			{
		    print "					<dd><span style='margin-right: 20px'><input type='radio' name='@$row[0]' value='true'";
			if($value->{@$row[0]} eq "1")
				{
				print " checked";
				}
			print "> Sim</span> <input type='radio' name='@$row[0]' value='false'";
			if($value->{@$row[0]} ne "1")
				{
				print " checked";
				}
			print "> Não</dd>";
			}
		else
			{
			if(@$row[2] > 250)
				{
				print "					<dd><textarea name='@$row[0]' ";
				}
			else
				{
				print "					  <dd><input type='text' name='@$row[0]' value='$value->{@$row[0]}'";
				}
			if(@$row[2] eq "")
				{
				if(@$row[1] =~ /^timestamp/)
					{
					print " style='width: 170px' ";
					}
				else
					{
					print " style='width: 50px' ";
					}
				}
			elsif(@$row[2] < 10)
				{
				print " style='width: ".(@$row[2]*12)."px' ";
				}
			elsif((@$row[2]*3) > 1000)
				{
				print " style='width: 100%'";
				}
			elsif(@$row[2] ne "")
				{
				print " style='width: ".(@$row[2]*3)."px' ";
				}
			if(@$row[2] > 250)
				{
				print ">$value->{@$row[0]}</textarea></dd>\n";
				}
			else
				{
				print "></dd>\n";
				}
			}
		}
	}
print<<HTML;
				</div>
			<br clear=all></dl>
			<div id='message' style='text-align: left; font-family: Tahoma, sans-serif; font-size: 13px; font-weight: bold; color: #31517a; margin-left: 4px;'></div><br>
		</div>
	</div>
</div>



<input type='hidden' name='COD' value='$COD'>
<input type='hidden' name='ID' value='$ID'>
<input type='hidden' name='MODO' value='$MODO'>
<input type='hidden' name='SHOW' value='$SHOW'>
<input type='hidden' name='FORCE' value='N'>
</form>

HTML
