#!/usr/bin/perl

$nacess = '204';
require "../../cfg/init.pl";

$ID = &get('ID');
$COD = &get('cod_empresa');
$MODO = &get('MODO');
$ACAO = &get('ACAO');
$QUAL = &get('qual');
$COMP = &get('comp');
if($COMP eq "")
	{
	$COMP = &get('comp_codigo');
	}
$DTAG = &get('comp_dtag');
$NOME = &get('comp_nome');
$EMPRESA = &get('cod_empresa');
$ENDERECO = &get('comp_endereco');
$DESCRP = &get('comp_descrp');
$OBS = &get('comp_obs');
@COMP_ITEM = &get_array('COMP_ITEM');
@COMP_ITEM_VALOR = &get_array('COMP_ITEM_VALOR');
$PESQ = &get('PESQ_PC');
$ORDER = &get('ORDER_LISTPC');
if($ORDER eq "")
	{
	$ORDER = "dtag";
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
print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
</head>
<body>
HTML


if($QUAL ne "" && $ACAO eq "delete")
	{
	$rv = $dbh->do("delete from empresa_comp_adicional where computador = '$COMP' ");
	if($dbh->err ne "")
		{
		&erroDBH("Falha na inicialização dos itens do grupo!!!");
		$dbh->rollback;
		exit;
		}
	$rv = $dbh->do("delete from empresa_comp where codigo = '$COMP' ");
	if($dbh->err ne "")
		{
		&erroDBH("Falha na inicialização dos itens do grupo!!!");
		$dbh->rollback;
		exit;
		}
	}
elsif($QUAL ne "" && $ACAO eq "save")
	{
	$dbh->begin_work;
	$rv = $dbh->do("delete from empresa_comp_adicional where computador = '$QUAL' ");
	if($dbh->err ne "")
		{
		&erroDBH("Falha na inicialização dos itens do grupo!!!");
		$dbh->rollback;
		exit;
		}
	$SQL1 = "update empresa_comp set codigo='$COMP', nome='$NOME', empresa='$EMPRESA', descrp='$DESCRP', obs='$OBS'";
	if($ENDERECO ne "")
		{
		$SQL1 .= ", endereco='$ENDERECO'"; 
		}
	if($DTAG eq "")
		{
		$SQL1 .= ", dtag=NULL";
		}
	else
		{
		#  $DTAG =~ /^[0]+$/
		$SQL1 .= ", dtag='$DTAG'"; 
		}
	$SQL1 .= " where codigo='$QUAL'";
	$rv = $dbh->do($SQL1);
	if($dbh->err ne "")
		{
		&erroDBH("Falha na inclusão dos itens do grupo!!!");
		$dbh->rollback;
		exit;
		}
	for($f=0; $f<@COMP_ITEM; $f++)
		{
		if($COMP_ITEM_VALOR[$f] ne "")
			{
			$rv = $dbh->do("insert into empresa_comp_adicional (computador, comp_item, valor) values ('$COMP', '$COMP_ITEM[$f]', '$COMP_ITEM_VALOR[$f]') ");
			if($dbh->err ne "")
				{
				&erroDBH("Falha na inclusão dos itens adicionais do grupo!!!");
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


	$SQL1 = "select codigo from empresa_comp where nome = '$NOME' and empresa='$EMPRESA' and descrp = '$DESCRP' and obs = '$OBS'";
	if($ENDERECO ne "")
		{
		$SQL1 .= " and endereco='$ENDERECO'";
		}
	if($DTAG eq "" or $DTAG =~ /^[0]+$/)
		{
		$SQL1 .= " and dtag is null";
		}
	else
		{
		$SQL1 .= " and dtag='$DTAG'";
		}
	$sth = $dbh->prepare($SQL1);
	$sth->execute;
	if($dbh->err ne "")
		{
		&erroDBH("Falha ao identificar o código do computador!!!");
		$dbh->rollback;
		&erroDBR;
		}
	else
		{
		$rv = $sth->rows;
		if($rv > 0)
			{
			$row = $sth->fetch;
			$COMP = @$row[0];
			}
		else
			{
			$sth->finish;
			$SQL1 = "insert into empresa_comp (nome, empresa, descrp, obs";
			$SQL2 = ") values ('$NOME', '$EMPRESA', '$DESCRP', '$OBS'";

			if($ENDERECO ne "")
				{
				$SQL1 .= ", endereco";
				$SQL2 .= ", '$ENDERECO'"; 
				}
			if($DTAG eq "" or $DTAG =~ /^[0]+$/)
				{
				$SQL1 .= ", dtag";
				$SQL2 .= ", NULL";
				}
			else
				{
				$SQL1 .= ", dtag";
				$SQL2 .= ", '$DTAG'"; 
				}
			$SQL2 .= ")";

			$rv = $dbh->do($SQL1.$SQL2);
			if($dbh->err ne "")
				{
				&erroDBH("$SQL1 $SQL2 Falha na inclusão dos itens do grupo!!!");
				$dbh->rollback;
				exit;
				}

			$sth = $dbh->prepare("select currval('empresa_comp_codigo_seq') ");
			$sth->execute;
			if($dbh->err ne "")
				{
				&erroDBH("Falha ao identificar o código do computador!!!");
				$dbh->rollback;
				&erroDBR;
				}
			else
				{
				$rv = $sth->rows;
				if($rv == 1)
					{
					$row = $sth->fetch;
					$COMP = @$row[0];
					}
				else
					{
					&erroDBH("Falha ao identificar o código do computador!!!");
					$dbh->rollback;
					&erroDBR;
					}
				}
			$sth->finish;

			$rv = $dbh->do("delete from empresa_comp_adicional where computador = '$COMP' ");
			if($dbh->err ne "")
				{
				&erroDBH("Falha na inicialização dos itens do grupo!!!");
				$dbh->rollback;
				exit;
				}

			}
		}
	$sth->finish;



	for($f=0; $f<@COMP_ITEM; $f++)
		{
		if($COMP_ITEM_VALOR[$f] ne "")
			{
			$rv = $dbh->do("insert into empresa_comp_adicional (computador, comp_item, valor) values ('$COMP', '$COMP_ITEM[$f]', '$COMP_ITEM_VALOR[$f]') ");
			if($dbh->err ne "")
				{
				&erroDBH("Falha na inclusão dos itens adicionais do grupo!!!");
				$dbh->rollback;
				exit;
				}
			}
		}
	$dbh->commit;
	}

$SQL = "select distinct tipo_grupo_item.codigo, tipo_grupo_item.descrp, seq, tipo_grupo_item.supervisor as hidden from comp_item join tipo_grupo_item on comp_item.tipo = tipo_grupo_item.codigo ";
if($nacess_tipo ne "s")
	{
	$SQL .= " and tipo_grupo_item.supervisor is false ";
	}
$SQL .= " where comp_item.parceiro = '$LOGEMPRESA' ";
$SQL .= "order by seq";

$sth2 = &select($SQL);
$rv2 = $sth2->rows();
$ncol = 0;
if($rv2 > 0)
	{
	while($row2 = $sth2->fetchrow_hashref)
		{
		$codcol[$ncol] = $row2->{'codigo'};
		$nomecol[$ncol] = $row2->{'descrp'};
		$hiddecol[$ncol] = $row2->{'hidden'};
		$ncol++;
		}
	}
	
if($ncol > 8)
	{
	$ncol = 7;
	}

$SQL = "select *, to_char(dtag, '000000') as dtag_format from empresa_comp ";
$CORDER = $ORDER;
$CORDER =~ s/ desc//;
if($ORDER ne "" && $CORDER ne "nome" && $CORDER ne "dtag")
	{
	$SQL .= " left join empresa_comp_adicional on empresa_comp.codigo = empresa_comp_adicional.computador and empresa_comp_adicional.comp_item = '$CORDER' ";
	}
$SQL .= " where empresa_comp.empresa = '$EMPRESA' ";
if($ORDER =~ /nome/ || $ORDER =~ /dtag/)
	{
	$SQL = $SQL."order by ".$ORDER;
	}
elsif($ORDER =~ /desc/)
	{
	$SQL = $SQL."order by empresa_comp_adicional.valor desc nulls last, nome";
	}
else
	{
	$SQL = $SQL."order by empresa_comp_adicional.valor nulls first, nome";
	}

$sth8 = &select($SQL);
$rv8 = $sth8->rows();
if($rv8 < 1)
	{
	print " &nbsp; Nenhum computador encontrado!";
	}
else
	{
	print "<table width=100% cellpadding=4 cellspacing=2 border=0 id='tblistpc' class='navigateable' align='center'>";
	
	print "<thead><tr>";
	print "<th";
	if($ORDER eq "dtag")
		{
		print " class='asc'";
		}
	elsif($ORDER eq "dtag desc")
		{
		print " class='desc'";
		}
	else
		{
		print " class='thor'";
		}
	print " onClick=\"orderby('listpc', 'dtag')\">DTAG</th>";
	print "<th";
	if($ORDER eq "nome")
		{
		print " class='asc'";
		}
	elsif($ORDER eq "nome desc")
		{
		print " class='desc'";
		}
	else
		{
		print " class='thor'";
		}
	print " onClick=\"orderby('listpc', 'nome')\">Nome</th>";
	for($e=0; $e<$ncol; $e++)
		{
		print "<th";
		if($hiddecol[$e] eq 1)
			{
			print " style='background-color: #cc5555' ";
			}
		if($ORDER eq "$codcol[$e]")
			{
			print " class='asc'";
			}
		elsif($ORDER eq "$codcol[$e] desc")
			{
			print " class='desc'";
			}
		else
			{
			print " class='thor'";
			}
		print " onClick=\"orderby('listpc', '$codcol[$e]')\">$nomecol[$e]</th>";
		}
	print "</tr></thead>";
	print "<tbody>";

	$NREG = 0;
	while($row8 = $sth8->fetchrow_hashref)
		{
		$SQL = "select *, to_char(dtag, '000000') as dtag_format from empresa_comp ";
		if($PESQ ne "")
			{
			$SQL .= " left join empresa_comp_adicional on empresa_comp.codigo = empresa_comp_adicional.computador ";
			}
		$SQL .= " where empresa_comp.codigo = '".$row8->{'codigo'}."' ";
		if($PESQ ne "")
			{
			if($PESQ =~ /^\d+$/)
				{
				$SQL .= " and (empresa_comp.dtag = '$PESQ' or empresa_comp.codigo = '$PESQ' or empresa_comp_adicional.valor = '$PESQ') ";
				}
			else
				{
				$SQL .= "and (empresa_comp.nome <=> '%$PESQ%' or empresa_comp.obs <=> '%$PESQ%' or empresa_comp_adicional.valor <=> '%$PESQ%' ) ";
				}
			}
		$sth3 = &select($SQL);
		$rv3 = $sth3->rows();
		if($rv3 > 0)
			{
			$last = "";
			while($row3 = $sth3->fetchrow_hashref)
				{
				if($last ne $row3->{'codigo'})
					{
					$last = $row3->{'codigo'};
					print "<tr id='$row3->{'codigo'}' onClick='if(parent.bloqueado == true) { parent.unblock(); } else { get_pcdetail(\"$row3->{'codigo'}\"); screenRefresh(\"tblistpc\",\"$row3->{'codigo'}\"); }'>";
					print "<td>$row3->{'dtag_format'}</td>";
					print "<td>$row3->{'nome'}</td>";
					for($e=0; $e<$ncol; $e++)
						{
						$NREG++;
						$SQL = "select * from empresa_comp_adicional where comp_item = '$codcol[$e]' and empresa_comp_adicional.computador = '$row3->{'codigo'}' limit 1 ";
						$sth4 = &select($SQL);
						$rv4 = $sth4->rows();
						print "<td>";
						while($row4 = $sth4->fetchrow_hashref)
							{
							print $row4->{'valor'};
							}
						print "</td>";
						}
					print "</tr>";
					}
				}
			}
		}
	if($last eq "")
		{
		print "<tr><td colspan=$ncol>Nenhum computador encontrado!</td></tr>";
		}
	print "</tbody></table>";
	}
print<<HTML;
<input type='hidden' name='comp_selected' value='$COMP'>
</body></html>


<script>
    \$("#total_itens").text("$rv8");
</script>

HTML


exit;


