#!/usr/bin/perl

$nacess = '204';
require "../../cfg/init.pl";

$ID = &get('ID');
$COD = &get('cod_empresa');
$MODO = &get('MODO');
$EMPRESA = &get('cod_empresa');
$USUARIO = &get('user_codigo');
$ADD = &get('add');
$DEL = &get('del');
$PESQ = &get('PESQ_USERPC');
$SELECTED = &get('selected');

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

$SQL = "";
if($USUARIO ne "" && ($ADD ne "" || $DEL ne ""))
	{
	$rv = $dbh->do("update user_comp set seq_user='0' where codigo = '$USUARIO' ");
	if($dbh->err ne "")
		{
		&erroDBH("Falha na inicialização da exclusão dos usuários do computador!!!");
		$dbh->rollback;
		exit;
		}
	$c = 1;
	@item = &get_array('item[]');
	for($f=0; $f<@item; $f++)
		{
		if($item[$f] ne "")
			{
			$sth2 = &select("select * from user_comp where codigo = '$USUARIO' and computador = '$item[$f]' ");
			$rv2 = $sth2->rows();
			if($rv2 > 0)
				{
				$rv = $dbh->do("update user_comp set seq_user='$c' where codigo = '$USUARIO' and computador = '$item[$f]' ");
				if($dbh->err ne "")
					{
					&erroDBH("Falha na inclusão dos usuários do computador!!!");
					$dbh->rollback;
					exit;
					}
				$c++;
				}
			else
				{
				$rv = $dbh->do("insert into user_comp (codigo, computador, seq_user) values ('$USUARIO', '$item[$f]', '$c') ");
				if($dbh->err ne "")
					{
					&erroDBH("Falha na inclusão dos usuários do computador!!!");
					$dbh->rollback;
					exit;
					}
				}
			$c++;
			}
		}
	$rv = $dbh->do("delete from user_comp where codigo = '$USUARIO' and seq_user='0' ");
	if($dbh->err ne "")
		{
		&erroDBH("Falha na exclusão dos usuários do computador!!!");
		$dbh->rollback;
		exit;
		}


	}


$SQL = "select distinct tipo_grupo_item.codigo, tipo_grupo_item.descrp, seq from comp_item join tipo_grupo_item on comp_item.tipo = tipo_grupo_item.codigo ";
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
		$ncol++;
		}
	}

if($USUARIO ne "")
	{
	$SQL = "select empresa_comp.*, to_char(empresa_comp.dtag, '000000') as dtag_format from empresa_comp ";
	if($SELECTED eq "true")
		{
		$SQL .= " join user_comp on empresa_comp.codigo = user_comp.computador and user_comp.codigo = '$USUARIO' where ";
		}
	else
		{
		$SQL .= " left join user_comp on empresa_comp.codigo = user_comp.computador and user_comp.codigo = '$USUARIO' where user_comp.codigo is null and ";
		if($PESQ ne "")
			{
			if($PESQ =~ /^\d+$/)
				{
				$SQL .= " (empresa_comp.dtag = '$PESQ' or empresa_comp.codigo = '$PESQ') and ";
				}
			else
				{
				$SQL .= "(empresa_comp.nome <=> '%$PESQ%' or empresa_comp.obs <=> '%$PESQ%') and ";
				}
			}
		}
	$SQL .= " empresa_comp.empresa = '$EMPRESA' ";
	$SQL = $SQL."order by user_comp.seq_user";
	$sth3 = &select($SQL);
	$rv3 = $sth3->rows();
	}
else
	{
	$rv3 = 0;
	}

if($ncol > 3)
	{
	$ncol = 2;
	}

print "<table width=100% cellpadding=4 cellspacing=2 border=0 id='tblistuserpc' class='navigateable' align='center'>";
print "<thead><tr class='state-disabled'>";
print "<th width=10%>DTAG</th>";
print "<th>Nome</th>";
for($e=0; $e<$ncol; $e++)
	{
	print "<th width=25%>$nomecol[$e]</th>";
	}
print "</tr></thead>";
print "<tbody>";

if($rv3 > 0)
	{
	while($row3 = $sth3->fetchrow_hashref)
		{
		print "<tr id='item_$row3->{'codigo'}' class='ui-state-default'>";
		print "<td>$row3->{'dtag_format'}</td>";
		print "<td>$row3->{'nome'}</td>";
		for($e=0; $e<$ncol; $e++)
			{
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
print "</tbody></table>";
print<<HTML;
</body></html>
HTML


exit;


