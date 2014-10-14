#!/usr/bin/perl

$nacess = '204';
require "../../cfg/init.pl";

$ID = &get('ID');
$COD = &get('cod_empresa');
$MODO = &get('MODO');
$ACAO = &get('ACAO');
$QUAL = &get('qual');
$USUARIO = &get('user_codigo');
$NOME = &get('user_nome');
$EMPRESA = &get('cod_empresa');
@USER_ITEM = &get_array('USER_ITEM');
@USER_ITEM_VALOR = &get_array('USER_ITEM_VALOR');
$PESQ = &get('PESQ_USER');
$ORDER = &get('ORDER_LISTUSER');
if($ORDER eq "")
	{
	$ORDER = "nome";
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
	$rv = $dbh->do("delete from empresa_user_adicional where user = '$QUAL' ");
	if($dbh->err ne "")
		{
		&erroDBH("Falha na inicialização dos itens do grupo!!!");
		$dbh->rollback;
		exit;
		}
	$rv = $dbh->do("delete from empresa_user where codigo = '$QUAL' ");
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
	$rv = $dbh->do("delete from empresa_user_adicional where \"user\" = '$QUAL' ");
	if($dbh->err ne "")
		{
		&erroDBH("Falha na inicialização dos itens do grupo!!!");
		$dbh->rollback;
		exit;
		}
	$rv = $dbh->do("update empresa_user set codigo='$USUARIO', nome='$NOME', empresa='$EMPRESA' where codigo='$QUAL' ");
	if($dbh->err ne "")
		{
		&erroDBH("Falha na inclusão dos itens do grupo!!!");
		$dbh->rollback;
		exit;
		}
	for($f=0; $f<@USER_ITEM; $f++)
		{
		if($USER_ITEM_VALOR[$f] ne "")
			{
			$rv = $dbh->do("insert into empresa_user_adicional (\"user\", user_item, valor) values ('$USUARIO', '$USER_ITEM[$f]', '$USER_ITEM_VALOR[$f]') ");
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
	$rv = $dbh->do("insert into empresa_user (nome, empresa) values ('$NOME', '$EMPRESA') ");
	if($dbh->err ne "")
		{
		&erroDBH("Falha na inclusão dos itens do grupo!!!");
		$dbh->rollback;
		exit;
		}
	$sth = $dbh->prepare("select currval('empresa_user_codigo_seq') ");
	$sth->execute;
	if($dbh->err ne "")
		{
		&erroDBH("Falha ao identificar o código do usuário!!!");
		$dbh->rollback;
		&erroDBR;
		}
	else
		{
		$rv = $sth->rows;
		if($rv == 1)
			{
			$row = $sth->fetch;
			$USUARIO = @$row[0];
			}
		else
			{
			&erroDBH("Falha ao identificar o código do usuário!!!");
			$dbh->rollback;
			&erroDBR;
			}
		}
	$sth->finish;


	for($f=0; $f<@USER_ITEM; $f++)
		{
		if($USER_ITEM_VALOR[$f] ne "")
			{
			$rv = $dbh->do("insert into empresa_user_adicional (\"user\", user_item, valor) values ('$USUARIO', '$USER_ITEM[$f]', '$USER_ITEM_VALOR[$f]') ");
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

$SQL = "select distinct tipo_grupo_item.codigo, tipo_grupo_item.descrp, seq, tipo_grupo_item.supervisor as hidden from user_item join tipo_grupo_item on user_item.tipo = tipo_grupo_item.codigo ";
if($nacess_tipo ne "s")
	{
	$SQL .= " and tipo_grupo_item.supervisor is false ";
	}
$SQL .= " where user_item.parceiro = '$LOGEMPRESA' ";
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

$SQL = "select * from empresa_user ";
$CORDER = $ORDER;
$CORDER =~ s/ desc//;
if($ORDER ne "" && $CORDER ne "nome")
	{
	$SQL .= " left join empresa_user_adicional on empresa_user.codigo = empresa_user_adicional.user and empresa_user_adicional.user_item = '$CORDER' ";
	}
$SQL .= " where empresa_user.empresa = '$EMPRESA' ";
if($ORDER =~ /nome/)
	{
	$SQL = $SQL."order by ".$ORDER;
	}
elsif($ORDER =~ /desc/)
	{
	$SQL = $SQL."order by empresa_user_adicional.valor desc nulls last, nome";
	}
else
	{
	$SQL = $SQL."order by empresa_user_adicional.valor nulls first, nome";
	}

$sth8 = &select($SQL);
$rv8 = $sth8->rows();
if($rv8 < 1)
	{
	print " &nbsp; Nenhum usuário encontrado!";
	}
else
	{
	print "<table width=100% cellpadding=4 cellspacing=2 border=0 id='tblistuser' class='navigateable' align='center'>";
	print "<thead><tr>";
	#print "<th>Código</th>";
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
	print " onClick=\"orderby('listuser', 'nome')\">Nome</th>";
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
		print " onClick=\"orderby('listuser', '$codcol[$e]')\">$nomecol[$e]</th>";
		}
	print "</tr></thead>";
	print "<tbody>";

	$NREG = 0;
	while($row8 = $sth8->fetchrow_hashref)
		{
		$SQL = "select * from empresa_user ";
		if($PESQ ne "")
			{
			$SQL .= " left join empresa_user_adicional on empresa_user.codigo = empresa_user_adicional.user ";
			}
		$SQL .= " where empresa_user.codigo = '".$row8->{'codigo'}."' ";
		if($PESQ ne "")
			{
			if($PESQ =~ /^\d+$/)
				{
				$SQL .= " and (empresa_user.codigo = '$PESQ' or empresa_user_adicional.valor = '$PESQ') ";
				}
			else
				{
				$SQL .= "and (empresa_user.nome <=> '%$PESQ%' or empresa_user_adicional.valor <=> '%$PESQ%') ";
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
					print "<tr id='$row3->{'codigo'}' onClick='if(parent.bloqueado == true) { parent.unblock(); } else { get_userdetail(\"$row3->{'codigo'}\"); screenRefresh(\"tblistuser\",\"$row3->{'codigo'}\"); }'>";
					#print "<td>$row3->{'codigo'}</td>";
					print "<td>$row3->{'nome'}</td>";
					for($e=0; $e<$ncol; $e++)
						{
						$NREG++;
						$SQL = "select * from empresa_user_adicional where user_item = '$codcol[$e]' and empresa_user_adicional.user = '$row3->{'codigo'}' limit 1 ";
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
	if($NREG == 0)
		{
		print "<tr><td colspan=$ncol>Nenhum usuário encontrado!</td></tr>";
		}
	print "</tbody></table>";
	}
print<<HTML;
<input type='hidden' name='user_selected' value='$USUARIO'>
</body></html>


<script>
    \$("#total_itens").text("$rv8");
</script>

HTML


exit;


