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
$ENDERECO = &get('cod_endereco');
$BOX = &get('box');
if($BOX eq "")
	{
	$BOX = $ENDERECO;
	}
$MODO = &get('MODO');
$ACAO = &get('ACAO');
$GRUPO = &get('grupo');
if($GRUPO eq "undefined")
	{
	$GRUPO = "";
	}
$LINHA = &get('linha');
@GRUPO_ITEM = &get_array('GRUPO_ITEM_'.$BOX);
@GRUPO_ITEM_VALOR = &get_array('GRUPO_ITEM_VALOR_'.$BOX);
$PESQ = &get('PESQ');
$ORDER = &get('ORDER_LISTIT');
if($ORDER eq "")
	{
	$ORDER = "linha";
	}

if($LOGUSUARIO eq "admin")
	{
	$nacess_tipo = "s";
	}

print "Content-type: text/html\n\n";
print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
</head>
<body>

HTML

if($GRUPO ne "")
	{
	if($LINHA ne "" && $ACAO eq "delete")
		{
		$rv = $dbh->do("delete from grupo_empresa where empresa = '$COD' and endereco = '$ENDERECO' and linha = '$LINHA' and grupo = '$GRUPO' ");
		if($dbh->err ne "")
			{
			&erroDBH("Falha na inicialização dos itens do grupo!!!");
			$dbh->rollback;
			exit;
			}
		$dbh->commit;
		}
	elsif($LINHA ne "" && $ACAO eq "save")
		{
		$dbh->begin_work;
		$rv = $dbh->do("delete from grupo_empresa where empresa = '$COD' and endereco = '$ENDERECO' and linha = '$LINHA' and grupo = '$GRUPO' ");
		if($dbh->err ne "")
			{
			&erroDBH("Falha na inicialização dos itens do grupo!!!");
			$dbh->rollback;
			exit;
			}
		for($f=0; $f<@GRUPO_ITEM; $f++)
			{
			if($GRUPO_ITEM_VALOR[$f] ne "")
				{
				$rv = $dbh->do("insert into grupo_empresa (empresa, endereco, linha, grupo, grupo_item, valor) values ('$COD', '$ENDERECO', '$LINHA', '$GRUPO', '$GRUPO_ITEM[$f]', '$GRUPO_ITEM_VALOR[$f]') ");
				if($dbh->err ne "")
					{
					&erroDBH("Falha na inclusão dos itens do grupo!!!");
					$dbh->rollback;
					exit;
					}
				}
			}
		$dbh->commit;
		}
	elsif($ACAO eq "save")
		{
		$dbh->begin_work;
		$sth4 = &select("select max(linha) from grupo_empresa where empresa = '$COD' and endereco = '$ENDERECO' and grupo = '$GRUPO' ");
		$rv4 = $sth4->rows();
		if($rv4 < 1)
			{
			$LINHA = "1";
			}
		else
			{
			while($row4 = $sth4->fetch)
				{
				$LINHA = @$row4[0];
				$LINHA++;
				}
			}

		for($f=0; $f<@GRUPO_ITEM; $f++)
			{
			if($GRUPO_ITEM_VALOR[$f] ne "")
				{
				$rv = $dbh->do("insert into grupo_empresa (empresa, endereco, linha, grupo, grupo_item, valor) values ('$COD', '$ENDERECO', '$LINHA', '$GRUPO', '$GRUPO_ITEM[$f]', '$GRUPO_ITEM_VALOR[$f]') ");
				if($dbh->err ne "")
					{
					&erroDBH("Falha na inclusão dos itens do grupo!!!");
					$dbh->rollback;
					exit;
					}
				}
			}
		$dbh->commit;
		$LINHA = "";
		}

	$SQL = "select *, tipo_grupo_item.supervisor as hidden from grupo_item join tipo_grupo_item on grupo_item.tipo = tipo_grupo_item.codigo ";
	$SQL .= " where grupo_item.grupo = '$GRUPO' ";
	if($nacess_tipo ne "s")
		{
		$SQL .= " and tipo_grupo_item.supervisor is false ";
		}
	$SQL .= "order by seq";

    $SQL_a = $SQL;
	$sth3 = &select($SQL);
	$rv3 = $sth3->rows();
	$ncol=0;
	if($rv3 < 1)
		{
		print "Nenhum item cadastrado!";
		}
	else
		{
            
            
        # lista itens
            
		print "<table width=100% cellpadding=4 cellspacing=2 border=0 id='tbitem_$BOX' class='navigateable' align='center'><thead><tr>";
		while($row3 = $sth3->fetchrow_hashref)
			{
			print "<th";
			if($row3->{'hidden'} eq 1)
				{
				print " style='background-color: #cc5555' ";
				}
			if($ORDER eq $row3->{'codigo'})
				{
				print " class='asc'";
				}
			elsif($ORDER eq $row3->{'codigo'}." desc")
				{
				print " class='desc'";
				}
			else
				{
				print " class='thor'";
				}
			print " onClick=\"orderby('$GRUPO', '$ENDERECO', '".$row3->{'codigo'}."')\">".$row3->{'descrp'}."</th>";
			$col[$ncol] = $row3->{'codigo'};
			$ncol++;
			}
		print "</tr></thead><tbody>";

		$SQL = "select grupo_empresa.linha, grupo_empresa.empresa, grupo_empresa.endereco from grupo_empresa ";
		$CORDER = $ORDER;
		$CORDER =~ s/ desc//;
		if($ORDER ne "" && $CORDER ne "linha")
			{
			$SQL .= " left join grupo_empresa as ordertab on grupo_empresa.empresa = ordertab.empresa and grupo_empresa.endereco = ordertab.endereco and grupo_empresa.linha = ordertab.linha and grupo_empresa.grupo = ordertab.grupo and ordertab.grupo_item = '$CORDER'  ";
			}
		$SQL .= "where ";
		if($COD > 0)
			{
			$SQL .= "grupo_empresa.empresa = '$COD' and ";
			}
		if($ENDERECO > 0)
			{
			$SQL .= "grupo_empresa.endereco = '$ENDERECO' and ";
			}
		$SQL .= " grupo_empresa.linha is not null and ";
		$SQL .= "grupo_empresa.grupo = '$GRUPO' ";
		if($PESQ ne "")
			{
			$SQL .= " and grupo_empresa.valor <=> '%$PESQ%' "; 
			}
		if($ORDER =~ /linha/)
			{
			$SQL = $SQL."order by grupo_empresa.".$ORDER;
			}
		elsif($ORDER =~ /desc/)
			{
			$SQL = $SQL."order by ordertab.valor desc nulls last, grupo_empresa.linha desc";
			}
		else
			{
			$SQL = $SQL."order by ordertab.valor nulls first, grupo_empresa.linha";
			}
            
        $SQL_list_a = $SQL;
		$sth = &select($SQL);
		$rv = $sth->rows();
		if($rv > 0)
			{
			$last = "";
			while($row = $sth->fetchrow_hashref)
				{
				if($last ne $row->{'endereco'}.$row->{'linha'})
					{
					$COD = $row->{'empresa'};
					$ENDERECO = $row->{'endereco'};
					print "<tr id='".$row->{'endereco'}."_".$row->{'linha'}."' onClick='if(parent.bloqueado == true) { parent.unblock(); } else { get_detail(\"".$row->{'linha'}."\", \"".$GRUPO."\", \"".$ENDERECO."\", \"".$COD."\"); screenRefresh(\"tbitem_$BOX\",\"".$row->{'endereco'}."_".$row->{'linha'}."\"); }'>";
					for($e=0; $e<$ncol; $e++)
						{
						$SQL = "select * from grupo_empresa where grupo_item = '$col[$e]' and linha = '".$row->{'linha'}."' and grupo_empresa.grupo = '$GRUPO' ";
						if($COD > 0)
							{
							$SQL .= "and grupo_empresa.empresa = '$COD' ";
							}
						 if($ENDERECO > 0)
							{
							$SQL .= "and grupo_empresa.endereco = '$ENDERECO' ";
							}
						$SQL .= "limit 1 ";
                        
                        $SQL_list_b = $SQL;
						$sth2 = &select($SQL);
						$rv2 = $sth2->rows();
						if($rv2 < 1)
							{
							print "<td>&nbsp;</td>";
							}
						else
							{
							while($row2 = $sth2->fetchrow_hashref)
								{
								print "<td>";
								if($row2->{'valor'} =~ m/^http/)
									{
									#print "<a href='javascript:top.callExt(\"".$row2->{'valor'}."\")'>".$row2->{'valor'}."</a>";
									print $row2->{'valor'};
									}
								else
									{
									print $row2->{'valor'};
									}
								print "&nbsp;</td>";
								}
							}
						}
					print "</tr>";
					}
				if($last eq "")
					{
					if($LINHA eq "")
						{
						$LINHA = $row->{'linha'};
						}
					if($ENDERECO eq "")
						{
						$PENDERECO = $row->{'endereco'};
						}
					else
						{
						$PENDERECO = $ENDERECO;
						}
					if($COD eq "")
						{
						$PCOD = $row->{'empresa'};
						}
					else
						{
						$PCOD = $COD;
						}
					$LINHAID = $row->{'endereco'}."_".$LINHA;
					}
				$last = $row->{'endereco'}.$row->{'linha'};
				}
			}

		print "</tbody></table>";
		if($ACAO ne "delete")
			{
			print "<script language='JavaScript'>\n";
			print "get_detail(\"".$LINHA."\", \"".$GRUPO."\", \"".$PENDERECO."\", \"".$PCOD."\"); screenRefresh(\"tbitem_$BOX\",\"".$LINHAID."\");\n";
			print "</script>\n";
			}
		}
	}
print<<HTML;

<script>
</script>

</body></html>
HTML

exit;
