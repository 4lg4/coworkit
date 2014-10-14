#!/usr/bin/perl

$nacess = '902';
require "../../cfg/init.pl";

$ID = &get('ID');
$COD = &get('COD');
$MODO = &get('MODO');
$QUAL = &get('cron');
$ENDERECO = &get('cod_endereco');


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
	if($QUAL ne "")
		{
$out.=<<HTML;
  <center>
      <ICONEX>
      <img src='$dir{'img_syscall'}salvar.png' border=0 alt='salvar' style='margin-top: 10px; cursor: pointer; display: none;' id='cron_icon_save_$ENDERECO' onClick='hide("cron_icon_save_$ENDERECO"); salvar_cron("$QUAL", "$ENDERECO")'>
  </center>
HTML
		}
	else
		{
$out.=<<HTML;
  <center>
      <ICONEX>
      <img src='$dir{'img_syscall'}salvar.png' border=0 alt='salvar' style='margin-top: 10px; cursor: pointer;' id='cron_icon_save_$ENDERECO' onClick='salvar_cron("$QUAL", "$ENDERECO")'>
  </center>
HTML
		}
	}
else
	{
	$out .= "&nbsp;";
	}
$out.=<<HTML;
</div>

<div style='float: left; width: 90%;'>

HTML


if($QUAL ne "")
	{
	$SQL = "select *, cron.codigo as cron_codigo, cron.descrp as cron_descrp, to_char(cron.dtcad, 'DD/MM/YYYY às HH24:MI:SSh') as dtcad_formatada, tipo_cron.descrp as tipo_descr, cron.tipo as tipo_codigo from cron left join tipo_cron on cron.tipo = tipo_cron.codigo where cron.codigo = '$QUAL' ";
	$sth = &select($SQL);
	$rv = $sth->rows();
	if($rv < 1)
		{
		&insert;
		}
	else
		{
		$out .= "<dl class='form' style='margin-left: 1%; width: 80%;'>";

		while($row = $sth->fetchrow_hashref)
			{
			$CRON = $row->{'codigo'};
			$CHAVE = $row->{'chave'};
			if($MODO eq "ver")
				{
				$out .= "<dt>Monitorado</dt>";
				$out .= "<dd><input type='radio' name='cron_hidden' value='0'";
				if(!$row->{'hidden'})
					{
					$out .= " checked ";
					}
				$out .= " onClick='this.value=this.defaultChecked'> Sim &nbsp;&nbsp;&nbsp;<input type='radio' name='cron_hidden' value='1'";
				if(!$row->{'hidden'})
					{
					$out .= " checked ";
					}
				$out .= " onClick='this.value=this.defaultChecked'> Não &nbsp;</dd>";
				$out .= "<dt>Tipo</dt>";
				$out .= "<dd style='border: solid 1px #cccccc;  padding: 2px; margin: 2px;'>$row->{'tipo_descr'} &nbsp;</dd>";
				$out .= "<dt>Código</dt>";
				$out .= "<dd style='border: solid 1px #cccccc;  padding: 2px; margin: 2px; width: 10%;'>$row->{'cron_codigo'} &nbsp;</dd>";
				$out .= "<dt>Chave</dt>";
				$out .= "<dd style='border: solid 1px #cccccc;  padding: 2px; margin: 2px; width: 15%;'>$row->{'chave'} &nbsp;</dd>";
				$out .= "<dt>Tempo mínimo execução</dt>";
				$out .= "<dd style='border: solid 1px #cccccc;  padding: 2px; margin: 2px; width: 15%;'>$row->{'tmin'} &nbsp; (hh:mm:ss)</dd>";
				$out .= "<dt>Tempo máximo execução</dt>";
				$out .= "<dd style='border: solid 1px #cccccc;  padding: 2px; margin: 2px; width: 15%;'>$row->{'tmax'} &nbsp; (hh:mm:ss)</dd>";
				$out .= "<dt>Descrição</dt>";
				$out .= "<dd style='border: solid 1px #cccccc;  padding: 2px; margin: 2px; height: 50px;'>$row->{'cron_descrp'} &nbsp;</dd>";
				}
			else
				{
				$out .= "<dt>Monitorado</dt>";
				$out .= "<dd><input type='radio' name='cron_hidden' value='0'";
				if(!$row->{'hidden'})
					{
					$out .= " checked ";
					}
				$out .= " onClick=' show(\"cron_icon_cancel_$ENDERECO\"); show(\"cron_icon_save_$ENDERECO\"); hide(\"cron_icon_insert_$ENDERECO\"); hide(\"cron_icon_delete_$ENDERECO\");'> Sim &nbsp;&nbsp;&nbsp;<input type='radio' name='cron_hidden' value='1'";
				if($row->{'hidden'})
					{
					$out .= " checked ";
					}
				$out .= " onClick=' show(\"cron_icon_cancel_$ENDERECO\"); show(\"cron_icon_save_$ENDERECO\"); hide(\"cron_icon_insert_$ENDERECO\"); hide(\"cron_icon_delete_$ENDERECO\");'> Não &nbsp;</dd>";

				$out .= "<dt>Tipo</dt>";
				$out .= "<dd>";

				$out .= "<select name='cron_tipo' onChange=' show(\"cron_icon_cancel_$ENDERECO\"); show(\"cron_icon_save_$ENDERECO\"); hide(\"cron_icon_insert_$ENDERECO\"); hide(\"cron_icon_delete_$ENDERECO\");'>";
				$sth2 = &select("select * from tipo_cron order by descrp");
				$rv2 = $sth2->rows();
				if($rv2 > 0)
					{
					while($row2 = $sth2->fetchrow_hashref)
						{
						$out .= "<option value='".$row2->{'codigo'}."'";
						if($row->{'tipo_codigo'} eq $row2->{'codigo'})
							{
							$out .= "selected";
							}
						$out .= ">".$row2->{'descrp'}."</option>";
						}
					}
				$out .= "</select></dd>";

				$out .= "<dt>Código</dt>";
				$out .= "<dd><input type='text' name='cron_codigo' value='".$row->{'cron_codigo'}."' style='width: 10%' readonly></dd>";
				$out .= "<dt>Chave</dt>";
				$out .= "<dd><input type='text' name='cron_chave' value='".$row->{'chave'}."' style='width: 15%' readonly></dd>";
				$out .= "<dt>Tempo mínimo execução</dt>";
				$out .= "<dd><input type='text' name='cron_tmin' value='".$row->{'tmin'}."' style='width: 10%' onKeyUp='checkChange(\"$ENDERECO\", this.value, \"".$row->{'tmin'}."\")' onChange='limpa(this.name)'> (hh:mm:ss)</dd>";
				$out .= "<dt>Tempo máximo execução</dt>";
				$out .= "<dd><input type='text' name='cron_tmax' value='".$row->{'tmax'}."' style='width: 10%' onKeyUp='checkChange(\"$ENDERECO\", this.value, \"".$row->{'tmax'}."\")' onChange='limpa(this.name)'> (hh:mm:ss)</dd>";
				$out .= "<dt>Descrição</dt>";
				$out .= "<dd><textarea name='cron_descrp' onKeyUp='checkChange(\"$ENDERECO\", this.value, \"".$row->{'cron_descrp'}."\")' style='height: 70px' onChange='limpa(this.name)'>$row->{'cron_descrp'}</textarea></dd>";
				}
			}
		$out .= "</dl>";
		$out .= "<br clear=both><br><div style='width: 100%; margin-left: 15px;'><font class='info'>Endereço para enviar mensagens de monitoramento:</font> <nobr><font class='infobold' style='text-decoration: underline'>http://".$ENV{'SERVER_NAME'}."/sys/cron/add.cgi?codigo=".$QUAL."&chave=".$CHAVE."&valor=&lt;sua mensagem&gt;</font></nobr></div>";

		$out =~ s/<ICONEX>/<img src='$dir{'img_syscall'}incluir.png' border=0 alt='incluir' style='margin-top: 10px; cursor: pointer;' id='cron_icon_insert_$ENDERECO' onClick='add_cron(\"$ENDERECO\")'><img src='$dir{'img_syscall'}cancelar.png' border=0 alt='cancelar' style='margin-top: 10px; cursor: pointer; display: none;' id='cron_icon_cancel_$ENDERECO' onClick='document.forms[0].reset(); hide(\"cron_icon_save_$ENDERECO\"); hide(\"cron_icon_cancel_$ENDERECO\"); show(\"cron_icon_insert_$ENDERECO\"); show(\"cron_icon_delete_$ENDERECO\");'><img src='$dir{'img_syscall'}excluir.png' border=0 alt='excluir' style='margin-top: 10px; cursor: pointer;' id='cron_icon_delete_$ENDERECO' onClick='excluir_cron(\"$QUAL\", \"$ENDERECO\")'>/gm;
		}
	}
elsif($ENDERECO ne "")
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

	$out .= "<dt>Tipo</dt>";
	$out .= "<dd>";

	$out .= "<select name='cron_tipo' onChange=' show(\"cron_icon_save\"); hide(\"cron_icon_insert\"); hide(\"cron_icon_delete\");'>";
	$sth2 = &select("select * from tipo_cron order by descrp");
	$rv2 = $sth2->rows();
	if($rv2 > 0)
		{
		while($row2 = $sth2->fetchrow_hashref)
			{
			$out .= "<option value='".$row2->{'codigo'}."'>";
			$out .= $row2->{'descrp'}."</option>";
			}
		}
	$out .= "</select></dd>";

	$out .= "<dt>Tempo mínimo execução</dt>";
	$out .= "<dd><input type='text' name='cron_tmin' value='00:01:00' style='width: 10%' onChange='limpa(this.name)'> (hh:mm:ss)</dd>";
	$out .= "<dt>Tempo máximo execução</dt>";
	$out .= "<dd><input type='text' name='cron_tmax' value='06:00:00' style='width: 10%' onChange='limpa(this.name)'> (hh:mm:ss)</dd>";
	$out .= "<dt>Descrição</dt>";
	$out .= "<dd><textarea name='cron_descrp' style='height: 70px' onChange='limpa(this.name)'></textarea></dd>";
	$out .= "</dl>";

	$out =~ s/<ICONEX>/<img src='$dir{'img_syscall'}cancelar.png' border=0 alt='cancelar' style='margin-top: 10px; cursor: pointer;' id='cron_icon_cancel_$ENDERECO' onClick='document.forms[0].reset(); hide(\"cron_icon_save_$ENDERECO\"); hide(\"cron_icon_cancel_$ENDERECO\"); show(\"cron_icon_insert\_$ENDERECO"); show(\"cron_icon_delete_$ENDERECO\"); \$(\"#detailcron_$ENDERECO\").html(\"\"); hide(\"cx2_$ENDERECO\"); '>/gm;
	}



