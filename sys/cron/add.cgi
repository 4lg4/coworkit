#!/usr/bin/perl

use URI::Escape;

$ID = "";
require "../cfg/init.pl";;

$codigo = &get('codigo');
$chave = &get('chave');
$descrp = &get(uri_unescape(valor));



print "Content-type: text/plain; charset='UTF-8'\n\n";

#print "Código: $codigo\n";
#print "Chave: $chave\n";
#print "Valor: $descrp\n";

if($codigo ne "")
	{
	$SQL = "select *, empresa_endereco.empresa as cod_emp, empresa_endereco.codigo as cod_end from cron left join empresa_endereco on cron.endereco = empresa_endereco.codigo where cron.codigo = '$codigo' ";
	$sth = &select($SQL);
	$rv = $sth->rows();
	if($rv > 0)
		{
		while($row = $sth->fetchrow_hashref)
			{
			#print "Empresa: ".$row->{'nome_emp'}." (".$row->{'cod_emp'}.")\n";
			if($row->{'chave'} eq $chave)
				{
				$rv = $dbh->do("insert into cron_historico (cron, dt, ip, descrp) values ('$codigo', now(), '$IP', '$descrp') ");
				if($dbh->err ne "")
					{
					print "Erro!\n$dbh->errstr\n";
					}
				else
					{
					print "OK!\n";
					}
				}
			else
				{
				print "Requisição negada!\n";
				}
			}
		}
	}
else
	{
	print "Acesso negado!\n";
	}

