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
	$SQL = "select *, to_char(dtag, '000000') as dtag_format from empresa_comp where empresa_comp.codigo = '$QUAL' limit 1 ";
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
			$COMP = $row->{'codigo'};
			$COMP_OBS = $row->{'obs'};
			if($MODO eq "ver")
				{
				$out .= "<dt>DTAG</dt>";
				$out .= "<dd style='border: solid 1px #cccccc;  padding: 2px; margin: 2px;'>$row->{'dtag_format'} &nbsp;</dd>";
				$out .= "<dt>Endereço</dt>";
				$out .= "<dd style='border: solid 1px #cccccc;  padding: 2px; margin: 2px;'>$row->{'endereco'} &nbsp;</dd>";
				$out .= "<dt>Nome</dt>";
				$out .= "<dd style='border: solid 1px #cccccc;  padding: 2px; margin: 2px;'>$row->{'nome'} &nbsp;</dd>";
				}
			else
				{
				$out .= "<dt>DTAG<input type='hidden' name='comp_codigo' value='".$row->{'codigo'}."'></dt>";
				$out .= "<dd><input type='text' name='comp_dtag' id='c0' value='".$row->{'dtag_format'}."' style='width: 20%' onChange='parent.block(true); show(\"pc_icon_save\"); show(\"pc_icon_cancel\"); hide(\"pc_icon_insert\"); hide(\"pc_icon_delete\"); this.value=String(\"000000\"+this.value).slice(-6);'></dd>";
				$out .= "<dt>Nome</dt>";
				$out .= "<dd><input type='text' name='comp_nome' id='c1' value='".$row->{'nome'}."' onKeyUp='checkChange(\"pc\", this.value, \"".$row->{'nome'}."\")'></dd>";
				&endereco;
				$out .= "<dt>Descrição</dt>";
				$out .= "<dd><textarea name='comp_descrp' onKeyUp='checkChange(\"pc\", this.value, \"".$row->{'descrp'}."\")'>$row->{'descrp'}</textarea></dd>";
				}
			}
		}

	$SQL = "select distinct tipo_grupo_item.codigo, tipo_grupo_item.descrp, seq, tipo_grupo_item.supervisor as hidden from comp_item join tipo_grupo_item on comp_item.tipo = tipo_grupo_item.codigo ";
	if($nacess_tipo ne "s")
		{
		$SQL .= " and tipo_grupo_item.supervisor is false ";
		}
	$SQL .= " where comp_item.parceiro = '$LOGEMPRESA' ";
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
			$out .= "$nomecol[$e]<input type='hidden' name='COMP_ITEM' value='$codcol[$e]'></dt>";
			$SQL = "select * from empresa_comp_adicional where comp_item = '$codcol[$e]' and empresa_comp_adicional.computador = '$COMP' limit 1 ";
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
					$out .= "<dd><input type='text' name='COMP_ITEM_VALOR' value='' onKeyUp='checkChange(\"pc\", this.value, \"\")'";
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
						$out .= "<dd><input type='text' name='COMP_ITEM_VALOR' value='".$row2->{'valor'}."' onKeyUp='checkChange(\"pc\", this.value, \"".$row2->{'valor'}."\")'";
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
		if($MODO eq "ver")
			{
			$out .= "<dt>Auditoria</dt>";
			$out .= "<dd style='border: solid 1px #cccccc;  padding: 2px; margin: 2px; height: 200px;'>$COMP_OBS &nbsp;</dd>";
			}
		else
			{
			$out .= "<dt>Auditoria</dt>";
			$out .= "<dd><textarea name='comp_obs' style='height: 200px;' onKeyUp='checkChange(\"pc\", this.value, \"".$COMP_OBS."\")'>".$COMP_OBS."</textarea></dd>";
			}
		$out .= "</dl>";
		}
	$out =~ s/<ICONEX>/<img src='$dir{'img_syscall'}incluir.png' border=0 alt='incluir' style='margin-top: 10px; cursor: pointer;' id='pc_icon_insert' onClick='add_pc()'><img src='$dir{'img_syscall'}cancelar.png' border=0 alt='cancelar' style='display: none; margin-top: 10px; cursor: pointer;' id='pc_icon_cancel' onClick='document.forms[0].reset(); hide(\"pc_icon_save\"); hide(\"pc_icon_cancel\"); parent.block(false);'><img src='$dir{'img_syscall'}excluir.png' border=0 alt='excluir' style='margin-top: 10px; cursor: pointer;' id='pc_icon_delete' onClick='excluir_pc("$QUAL")'><img src='$dir{'img_syscall'}salvar.png' border=0 alt='salvar' style='display: none; margin-top: 10px; cursor: pointer;' id='pc_icon_save' onClick='hide("pc_icon_save"); salvar_pc("$QUAL")'>/gm;
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

	$out .= "<dt>DTAG</dt>";
	$out .= "<dd><input type='text' id='c0' name='comp_dtag' value='' style='width: 20%' onChange='parent.block(true); show(\"pc_icon_save\"); hide(\"pc_icon_insert\"); hide(\"pc_icon_delete\"); this.value=String(\"000000\"+this.value).slice(-6);'></dd>";
	$out .= "<dt>Nome</dt>";
	$out .= "<dd><input type='text' id='c1' name='comp_nome' value='' onKeyUp='checkChange(\"pc\", this.value, \"\")'></dd>";
	&endereco;
	$out .= "<dt>Descrição</dt>";
	$out .= "<dd><textarea name='comp_descrp' onKeyUp='checkChange(\"pc\", this.value, \"\")'></textarea></dd>";


	$SQL = "select distinct tipo_grupo_item.codigo, tipo_grupo_item.descrp, seq from comp_item join tipo_grupo_item on comp_item.tipo = tipo_grupo_item.codigo ";

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
		$out .= "<dt>$nomecol[$e]<input type='hidden' name='COMP_ITEM' value='$codcol[$e]'></dt>";
		$out .= "<dd><input type='text' id='c".($e+3)."' name='COMP_ITEM_VALOR' value='' onKeyUp='checkChange(\"pc\", this.value, \"\")'></dd>";
		}

	$out .= "<dt>Auditoria</dt>";
	$out .= "<dd><textarea name='comp_obs' style='height: 200px;' onKeyUp='checkChange(\"pc\", this.value, \"".$COMP_OBS."\")'>".$COMP_OBS."</textarea></dd>";
	$out .= "</dl>";

	$out =~ s/<ICONEX>/<img src='$dir{'img_syscall'}cancelar.png' border=0 alt='cancelar' style='margin-top: 10px; cursor: pointer;' id='pc_icon_cancel' onClick='document.forms[0].reset(); hide(\"pc_icon_save\"); hide(\"pc_icon_cancel\"); hide(\"bbottom\"); parent.block(false);'><img src='$dir{'img_syscall'}salvar.png' border=0 alt='salvar' style='margin-top: 10px; cursor: pointer;' id='pc_icon_save' onClick='hide("pc_icon_save"); salvar_pc("$QUAL")'>/gm;
	}


sub endereco
	{
	$out .= "<dt>Endereço</dt>";

	$n = 0;
	$end_cod[$n] = "";
	$end_tipo[$n] = "Principal";
	$end_endereco[$n] = "";
	$end_complemento[$n] = "";
	$end_bairro[$n] = "";
	$end_cep[$n] = "";
	$end_cidade[$n] = "";
	$end_uf[$n] = "";

	$SQL = "select *, empresa_endereco.codigo as end_cod, empresa_endereco.endereco as rua, tipo_endereco.descrp as tipo_end from empresa_endereco join tipo_endereco on empresa_endereco.tipo = tipo_endereco.codigo where empresa_endereco.empresa = '$COD' order by tipo_endereco.codigo, end_cod ";
	$sth4 = &select($SQL);
	$rv4 = $sth4->rows();
	if($rv4 > 0)
		{
		while($row4 = $sth4->fetchrow_hashref)
			{
			$end_cod[$n] = $row4->{'end_cod'};
			$end_tipo[$n] = $row4->{'tipo_end'};
			$end_endereco[$n] = $row4->{'rua'};
			$end_complemento[$n] = $row4->{'complemento'};
			$end_bairro[$n] = $row4->{'bairro'};
			$end_cep[$n] = $row4->{'cep'};
			$end_cidade[$n] = $row4->{'cidade'};
			$end_uf[$n] = $row4->{'uf'};
			$n++;
			}
		}

	$out .= "<dd><select name='comp_endereco' style='width: 50%' onChange='parent.block(true); show(\"pc_icon_save\"); hide(\"pc_icon_insert\"); hide(\"pc_icon_delete\");'>";

	for($f=0; $f<@end_endereco; $f++)
		{
		$out .= "<option value='$end_cod[$f]'";
		if($end_cod[$f] eq $row->{'endereco'})
			{
			$out .= "selected";
			}
		$out .= ">".$end_endereco[$f]." - ".$end_cidade[$f]." / ".$end_uf[$f];
		$out .= "</option>";
		}
	$out .= "</select></dd>";
	}

