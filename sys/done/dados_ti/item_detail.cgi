#!/usr/bin/perl

$nacess = '204';
require "../../cfg/init.pl";

$ID = &get('ID');
$COD = &get('cod_emp');
if($COD eq "")
	{
	$COD = &get('COD');
	}
if($COD eq "undefinied")
	{
	$COD = "";
	}
$MODO = &get('MODO');
$GRUPO = &get('grupo');
if($GRUPO eq "undefinied")
	{
	$GRUPO = "";
	}
$LINHA = &get('linha');
if($LINHA eq "undefinied")
	{
	$LINHA = "";
	}
$LINHA =~ s/^\d+_//;
$ENDERECO = &get('cod_endereco');
if($ENDERECO eq "undefinied")
	{
	$ENDERECO = "";
	}
$BOX = &get('box');
if($BOX eq "")
	{
	$BOX = $ENDERECO;
	}

# se usuario for admin ajusta nacess_tipo para Supervisor
if($LOGUSUARIO eq "admin")
	{
	$nacess_tipo = "s";
	}
if($MODO eq "editar")
	{
	if($nacess_tipo eq "a" || $nacess_tipo eq "s")
		{
		$MODO = "editar";
		}
	else
		{
		$MODO = "ver";
		}
	}
	
$cfg_3 = &get_cfg(3);
	
print "Content-type: text/html\n\n";
$out=<<HTML;
<div id='actions' style='float: left; width: 55px; border: none 0px; background-color: #99aec9; margin-top: 8px;'>
  <center>
      <ICONEX>
  </center>
</div>

<div style='float: left; width: 90%;'>

HTML

if($LINHA ne "")
	{
	$SQL = "select distinct tipo_grupo_item.codigo, tipo_grupo_item.descrp, seq, grupo_empresa.endereco, tipo_grupo_item.supervisor as hidden from grupo_item join tipo_grupo_item on grupo_item.tipo = tipo_grupo_item.codigo join grupo_empresa on grupo_item.grupo = grupo_empresa.grupo ";
	$SQL .= " where grupo_empresa.linha = '$LINHA' and grupo_empresa.grupo = '$GRUPO' ";
	if($COD > 0)
		{
		$SQL .= "and grupo_empresa.empresa = '$COD' and grupo_empresa.endereco = '$ENDERECO' ";
		}
	if($nacess_tipo ne "s")
		{
		$SQL .= " and tipo_grupo_item.supervisor is false ";
		}
	$SQL .= "order by seq";


	$sth3 = &select($SQL);
	$rv3 = $sth3->rows();
	$ncol = 0;
	if($rv3 > 0)
		{
		$out .= "<dl class='form' style='margin-left: 1%; width: 90%;'>";

		while($row3 = $sth3->fetchrow_hashref)
			{
			$ENDERECO = $row3->{'endereco'};
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
			$out .= "$nomecol[$e]<input type='hidden' name='GRUPO_ITEM_$BOX' value='$codcol[$e]'></dt>";
			$SQL = "select distinct * from grupo_empresa where grupo_item = '$codcol[$e]' and linha = '$LINHA' and grupo_empresa.grupo = '$GRUPO' ";
			if($COD > 0)
				{
				$SQL .= "and grupo_empresa.empresa = '$COD' and grupo_empresa.endereco = '$ENDERECO' ";
				}
			$SQL .= "limit 1 ";
			$sth2 = &select($SQL);
			$rv2 = $sth2->rows();
			if($rv2 < 1)
				{
				if($MODO eq "ver")
					{
					if($hiddecol[$e])
						{
						$out .= "<dd style='border-bottom: solid 1px #cc5555;";
						}
					else
						{
						$out .= "<dd style='border-bottom: solid 1px #cccccc;";
						}
					$out .= "padding: 2px; margin: 2px;'>&nbsp;</dd>";
					}
				else
					{
					$out .= "<dd><input type='text' name='GRUPO_ITEM_VALOR_$BOX' value='' onKeyUp='checkChange(\"$BOX\", this.value, \"\")' ";
					if($hiddecol[$e])
						{
						$out .= " style='border-bottom: solid 1px #cc5555'></dd>";
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
						if(lc($nomecol[$e]) eq "endereço externo")
							{
							$go{end} = $row2->{'valor'};
							}
						elsif(lc($nomecol[$e]) eq "usuário")
							{
							$go{user} = $row2->{'valor'};
							}
						elsif(lc($nomecol[$e]) eq "senha")
							{
							$go{pass} = $row2->{'valor'};
							}
						elsif(lc($nomecol[$e]) eq "porta")
							{
							$go{porta} = $row2->{'valor'};
							}
						elsif(lc($nomecol[$e]) eq "sistema operacional")
							{
							$go{tipo} = $row2->{'valor'};
							}
						elsif(lc($nomecol[$e]) eq "tipo" && lc($row2->{'valor'} eq "ssh"))
							{
							$go{tipo} = "ssh";
							}
						elsif(lc($nomecol[$e]) eq "tipo" && (lc($row2->{'valor'}) eq "rdp" || lc($row2->{'valor'}) eq "ts"))
							{
							$go{tipo} = "rdp";
							}
						elsif(lc($nomecol[$e]) eq "porta")
							{
							$go{port} = $row2->{'valor'};
							}
						if($hiddecol[$e])
							{
							$out .= "<dd style='border-bottom: solid 1px #cc5555;";
							}
						else
							{
							$out .= "<dd style='border-bottom: solid 1px #cccccc;";
							}
						$out .= "padding: 2px; margin: 2px;'>";
						if($row2->{'valor'} =~ m/^http/)
							{
							if($cfg_3 ne "")
								{
								# Abre em nova janela
								$out .= "<a href='".$row2->{'valor'}."' target='".$cfg_3."'>".$row2->{'valor'}."</a>";
								}
							else
								{
								# Abre dentro do EOS
								$out .= "<a href='javascript:top.callExt(\"".$row2->{'valor'}."\")'>".$row2->{'valor'}."</a>";
								}
							}
						else
							{
							$out .= $row2->{'valor'};
							}
						$out .= "&nbsp;</dd>";
						}
					else
						{
						$out .= "<dd><input type='text' name='GRUPO_ITEM_VALOR_$BOX' value='".$row2->{'valor'}."' onKeyUp='checkChange(\"$BOX\", this.value, \"".$row2->{'valor'}."\")'";
						if($hiddecol[$e])
							{
							$out .= " style='border-bottom: solid 1px #cc5555'></dd>";
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
		if($MODO eq "editar")
			{
			$out =~ s/<ICONEX>/<img src='$dir{'img_syscall'}cancelar.png' border=0 alt='cancelar' style='margin-top: 4px; cursor: pointer;' id='detail_icon_cancel_$BOX' onClick='document.forms[0].reset(); hide(\"detail_icon_save_$BOX\"); hide(\"cx4_$BOX\"); parent.block(false);'><img src='$dir{'img_syscall'}excluir.png' border=0 alt='excluir' style='margin-top: 4px; cursor: pointer;' id='detail_icon_delete_$BOX' onClick='excluir("$LINHA", "$GRUPO", "$ENDERECO", "$COD")'><img src='$dir{'img_syscall'}salvar.png' border=0 alt='salvar' style='margin-top: 4px; cursor: pointer;' id='detail_icon_save_$BOX' onClick='hide("detail_icon_save_$BOX"); salvar("$LINHA", "$GRUPO", "$ENDERECO", "$COD");'>/gm;
			}
		elsif($nacess_tipo eq "a" || $nacess_tipo eq "s")
			{
			if($go{end} ne "")
				{
				if($go{tipo} =~ m/pfsense 2.0/i)
					{
					if($cfg_3 ne "")
						{
						# Abre em nova janela
						$icon_go = "<img src='$dir{'img_syscall'}acessar.png' border=0 alt='acessar DFirewall' style='margin-top: 4px; cursor: pointer;' onClick='document.dfirewall.target=\"$cfg_3\"; document.dfirewall.action=\"$go{end}\"; document.dfirewall.usernamefld.value=\"$go{user}\"; document.dfirewall.passwordfld.value=\"$go{pass}\"; document.dfirewall.submit();'>";
						}
					else
						{
						$icon_go = "<img src='$dir{'img_syscall'}acessar.png' border=0 alt='acessar DFirewall' style='margin-top: 4px; cursor: pointer;' onClick='top.Loading(); document.dfirewall.action=\"$go{end}\"; document.dfirewall.usernamefld.value=\"$go{user}\"; document.dfirewall.passwordfld.value=\"$go{pass}\"; document.dfirewall.submit(); top.DFullscreen(true); top.unLoading();'>";
						}
					}
				elsif($go{tipo} =~ m/pfsense 2.1/i)
					{
					$icon_go = "<img src='$dir{'img_syscall'}acessar.png' border=0 alt='acessar DFirewall' style='margin-top: 4px; cursor: pointer;' onClick='document.dfirewall.target=\"_blank\"; document.dfirewall.action=\"$go{end}\"; document.dfirewall.usernamefld.value=\"$go{user}\"; document.dfirewall.passwordfld.value=\"$go{pass}\"; document.dfirewall.submit();'>";
					}
				elsif($go{tipo} =~ m/rdp/i)
					{
					$icon_go = "<img src='$dir{'img_syscall'}acessar.png' border=0 alt='Remote Desktop' style='margin-top: 4px; cursor: pointer;' onClick='top.document.guacamole.ID.value=\"$ID\"; top.document.guacamole.host.value=\"$go{end}\"; top.document.guacamole.protocol.value=\"$go{tipo}\"; ";
					if($go{user} ne "")
						{
						$icon_go .= "top.document.guacamole.username.value=\"$go{user}\"; ";
						}
					if($go{pass} ne "")
						{
						$icon_go .= "top.document.guacamole.password.value=\"$go{pass}\"; ";
						}
					if($go{porta} eq "")
						{
						$go{porta} = "3389";
						}
					$icon_go .= "top.document.guacamole.port.value=\"$go{porta}\"; ";
					if($cfg_3 ne "")
						{
						# Abre em nova janela
						$icon_go .= "top.document.guacamole.action=\"/sys/menu/start.cgi\"; top.document.guacamole.target=\"_blank\"; top.document.guacamole.submit();'>";
						}
					else
						{
						$icon_go .= "top.callExt(\"/guacamole/client.xhtml\");'>";
						}
					}
				elsif($go{tipo} =~ m/ssh/i)
					{
					$icon_go = "<img src='$dir{'img_syscall'}acessar.png' border=0 alt='Remote Desktop' style='margin-top: 4px; cursor: pointer;' onClick='top.document.guacamole.ID.value=\"$ID\"; top.document.guacamole.host.value=\"$go{end}\"; top.document.guacamole.protocol.value=\"$go{tipo}\"; ";
					if($go{user} ne "")
						{
						$icon_go .= "top.document.guacamole.username.value=\"$go{user}\"; ";
						}
					if($go{pass} ne "")
						{
						$icon_go .= "top.document.guacamole.password.value=\"$go{pass}\"; ";
						}
					if($go{porta} eq "")
						{
						$go{porta} = "22";
						}
					$icon_go .= "top.document.guacamole.port.value=\"$go{porta}\"; ";
					if($cfg_3 ne "")
						{
						# Abre em nova janela
						$icon_go .= "top.document.guacamole.action=\"/sys/menu/start.cgi\"; top.document.guacamole.target=\"_blank\"; top.document.guacamole.submit();'>";
						}
					else
						{
						$icon_go .= "top.callExt(\"/guacamole/client.xhtml\");'>";
						}
					}
				}
			$out =~ s/<ICONEX>/<img src='$dir{'img_syscall'}incluir.png' border=0 alt='incluir' style='margin-top: 4px; cursor: pointer;' id='detail_icon_insert_$BOX' onClick='add("$ENDERECO", "$COD")'><img src='$dir{'img_syscall'}editar.png' border=0 alt='editar' style='margin-top: 4px; cursor: pointer;' id='detail_icon_editar_$BOX' onClick='get_detail_edit("$LINHA", "$GRUPO", "$ENDERECO", "$COD")'>$icon_go/gm;
			}

		}
	else
		{
		&insert;
		}
	}
elsif($GRUPO ne "" && $ENDERECO ne "")
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
	$SQL = "select distinct tipo_grupo_item.codigo, tipo_grupo_item.descrp, seq, tipo_grupo_item.supervisor as hidden from grupo_item join tipo_grupo_item on grupo_item.tipo = tipo_grupo_item.codigo ";
	$SQL .= " where grupo_item.grupo = '$GRUPO' ";
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
		$out .= "$nomecol[$e]<input type='hidden' name='GRUPO_ITEM_$BOX' value='$codcol[$e]'></dt>";
		$out .= "<dd><input type='text' id='c".$e."' name='GRUPO_ITEM_VALOR_$BOX' value='' onKeyUp='checkChange(\"$BOX\", this.value, \"\")'";
		if($hiddecol[$e])
			{
			$out .= " style='border: solid 1px #cc5555'></dd>";
			}
		else
			{
			$out .= "></dd>";
			}
		}
	$out .= "</dl>";

	$out =~ s/<ICONEX>/<img src='$dir{'img_syscall'}cancelar.png' border=0 alt='cancelar' style='margin-top: 4px; cursor: pointer;' id='detail_icon_cancel_$BOX' onClick='document.forms[0].reset(); hide(\"detail_icon_save_$BOX\"); hide(\"cx4_$BOX\"); parent.block(false);'><img src='$dir{'img_syscall'}salvar.png' border=0 alt='salvar' style='margin-top: 4px; cursor: pointer;' id='detail_icon_save_$BOX' onClick='hide("detail_icon_save_$BOX"); salvar("$LINHA", "$GRUPO", "$ENDERECO", "$COD");'>/gm;
	}


