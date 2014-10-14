#!/usr/bin/perl

$nacess = '204';
require "../../cfg/init.pl";

$ID = &get('ID');
$COD = &get('COD');
$MODO = &get('MODO');
$QUAL = &get('qual');
if($QUAL eq "undefinied")
	{
	$QUAL = "";
	}


if($LOGUSUARIO eq "admin")
	{
	$nacess_tipo = "s";
	}
if($nacess_tipo eq "a" || $nacess_tipo eq "s")
	{
	$MODO = "editar";
	}
else
	{
	$MODO = "ver";
	}


print "Content-type: text/html\n\n";
$out=<<HTML;
<div id='actions' style='float: left; width: 55px; border: solid 1px #aaaaaa; border-top: none 0px; border-bottom: none 0px; background-color: #99aec9;'>
HTML
if($MODO ne "ver")
	{
$out.=<<HTML;
  <center>
      <ICONEX>
  </center>
HTML
	}
else
	{
	$out .= "&nbsp;";
	}
$out.=<<HTML;
</div>

<div style='position: absolute; top: 0px; left: 60px; right: 0px; width: 80%;'>

HTML


if($QUAL ne "")
	{
	$SQL = "select * from empresa_user where empresa_user.codigo = '$QUAL' limit 1 ";
	$sth = &select($SQL);
	$rv = $sth->rows();
	if($rv < 1)
		{
		&insert;
		}
	else
		{
		$out .= "<dl class='form' style='margin-left: 1%; width: 100%;'>";

		while($row = $sth->fetchrow_hashref)
			{
			$USUARIO = $row->{'codigo'};
			$out .= "<dt>Código<input type='hidden' name='user_codigo' value='$row->{'codigo'}'></dt>";
			$out .= "<dd style='border: solid 1px #cccccc; padding: 2px; margin: 2px; width: 10%;'>$row->{'codigo'} &nbsp;</dd>";
			if($MODO eq "ver")
				{
				$out .= "<dt>Nome</dt>";
				$out .= "<dd style='border: solid 1px #cccccc;  padding: 2px; margin: 2px;'>$row->{'nome'} &nbsp;</dd>";
				}
			else
				{
				$out .= "<dt>Nome</dt>";
				$out .= "<dd><input type='text' name='user_nome' id='c1' value='".$row->{'nome'}."' onKeyUp='checkChange(\"user\", this.value, \"".$row->{'nome'}."\")'></dd>";
				}
			}
		}
	$SQL = "select distinct tipo_grupo_item.codigo, tipo_grupo_item.descrp, seq, tipo_grupo_item.supervisor as hidden from user_item join tipo_grupo_item on user_item.tipo = tipo_grupo_item.codigo ";
	if($nacess_tipo ne "s")
		{
		$SQL .= " and tipo_grupo_item.supervisor is false ";
		}
	$SQL .= " where user_item.parceiro = '$LOGEMPRESA' ";
	$SQL .= "order by seq";

	
	$sth3 = &select($SQL);
	$rv3 = $sth3->rows();
	$ncol = 0;
	if($rv3 > 0)
		{
		while($row3 = $sth3->fetchrow_hashref)
			{
			$codcol[$ncol] = $row3->{'codigo'};
			$nomecol[$ncol] = $row3->{'descrp'};
			$hiddecol[$ncol] = $row3->{'hidden'};
			$ncol++;
			}

		for($e=0; $e<$ncol; $e++)
			{
			if($hiddecol[$e])
				{
				$out .= "<dt style='color: #cc5555; font-weight: bold;'>";
				}
			else
				{
				$out .= "<dt>";
				}
			$out .= "$nomecol[$e]<input type='hidden' name='USER_ITEM' value='$codcol[$e]'></dt>";
			$SQL = "select * from empresa_user_adicional where user_item = '$codcol[$e]' and empresa_user_adicional.user = '$USUARIO' limit 1 ";
			$sth2 = &select($SQL);
			$rv2 = $sth2->rows();
			if($rv2 < 1)
				{
				if($MODO eq "ver")
					{
					if($hiddecol[$e])
						{
						$out .= "<dd style='border: solid 1px #cc5555;";
						}
					else
						{
						$out .= "<dd style='border: solid 1px #cccccc;";
						}
					$out .= "padding: 2px; margin: 2px;'>&nbsp;</dd>";
					}
				else
					{
					$out .= "<dd><input type='text' name='USER_ITEM_VALOR' value='' onKeyUp='checkChange(\"user\", this.value, \"\")'";
					if($hiddecol[$e])
						{
						$out .= " style='border: solid 1px #cc5555'></dd>";
						}
					else
						{
						$out .= "></dd>";
						}
					}
				}
			else
				{
				while($row2 = $sth2->fetchrow_hashref)
					{
					if($MODO eq "ver")
						{
						if($hiddecol[$e])
							{
							$out .= "<dd style='border: solid 1px #cc5555;";
							}
						else
							{
							$out .= "<dd style='border: solid 1px #cccccc;";
							}
						$out .= "padding: 2px; margin: 2px;'>$row2->{'valor'} &nbsp;</dd>";
						}
					else
						{
						$out .= "<dd><input type='text' name='USER_ITEM_VALOR' value='".$row2->{'valor'}."' onKeyUp='checkChange(\"user\", this.value, \"".$row2->{'valor'}."\")'";
						if($hiddecol[$e])
							{
							$out .= " style='border: solid 1px #cc5555'></dd>";
							}
						else
							{
							$out .= "></dd>";
							}
						}
					}
				}
			}
		$out .= "</dl>";
		}
	$out =~ s/<ICONEX>/<img src='$dir{'img_syscall'}incluir.png' border=0 alt='incluir' style='margin-top: 10px; cursor: pointer;' id='user_icon_insert' onClick='add_user()'><img src='$dir{'img_syscall'}cancelar.png' border=0 alt='cancelar' style='display: none; margin-top: 10px; cursor: pointer;' id='user_icon_cancel' onClick='document.forms[0].reset(); hide(\"user_icon_save\"); hide(\"pc_icon_cancel\"); parent.block(false);'><img src='$dir{'img_syscall'}excluir.png' border=0 alt='excluir' style='margin-top: 10px; cursor: pointer;' id='user_icon_delete' onClick='excluir_user("$QUAL")'><img src='$dir{'img_syscall'}salvar.png' border=0 alt='salvar' style='display: none; margin-top: 10px; cursor: pointer;' id='user_icon_save' onClick='hide("user_icon_save"); salvar_user("$QUAL")'>/gm;
	}
elsif($COD ne "")
	{
	&insert;
	}


$out.=<<HTML;
</div>
HTML

print $out;

exit;













sub insert
	{
	$out .= "<dl class='form' style='margin-left: 1%; width: 80%;'>";

	$out .= "<dt>Nome</dt>";
	$out .= "<dd><input type='text' id='c1' name='user_nome' value='' onKeyUp='checkChange(\"user\", this.value, \"\")'></dd>";


	$SQL = "select distinct tipo_grupo_item.codigo, tipo_grupo_item.descrp, seq from user_item join tipo_grupo_item on user_item.tipo = tipo_grupo_item.codigo ";
	$SQL .= "order by seq";


	$sth3 = &select($SQL);
	$rv3 = $sth3->rows();
	$ncol = 0;
	if($rv3 > 0)
		{
		while($row3 = $sth3->fetchrow_hashref)
			{
			$codcol[$ncol] = $row3->{'codigo'};
			$nomecol[$ncol] = $row3->{'descrp'};
			$ncol++;
			}
		}

	for($e=0; $e<$ncol; $e++)
		{
		$out .= "<dt>$nomecol[$e]<input type='hidden' name='USER_ITEM' value='$codcol[$e]'></dt>";
		$out .= "<dd><input type='text' id='c".($e+3)."' name='USER_ITEM_VALOR' value='' onKeyUp='checkChange(\"user\", this.value, \"\")'></dd>";
		}
	$out .= "</dl>";

	$out =~ s/<ICONEX>/<img src='$dir{'img_syscall'}cancelar.png' border=0 alt='cancelar' style='margin-top: 10px; cursor: pointer;' id='user_icon_cancel' onClick='document.forms[0].reset(); hide(\"user_icon_save\"); hide(\"pc_icon_cancel\"); hide(\"bbottom\");  parent.block(false);'><img src='$dir{'img_syscall'}salvar.png' border=0 alt='salvar' style='margin-top: 10px; cursor: pointer;' id='user_icon_save' onClick='hide("user_icon_save"); salvar_user("$QUAL")'>/gm;
	}


