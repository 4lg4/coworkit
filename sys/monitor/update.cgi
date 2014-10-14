#!/usr/bin/perl

use URI::Escape;

$ID = "";
require "../cfg/init.pl";

$vers = 'Ver. 20130310';
$arq = './history/'.'20130318lin';


$codigo = &get('codigo');
$chave = &get('chave');


print "Content-type: text/plain; charset='UTF-8'\n\n";


if($codigo eq "")
	{
	print  "ERRO: Não foi informado o código.\n";
	exit;
	}
if($chave eq "")
	{
	print  "ERRO: Não foi informada a chave.\n";
	exit;
	}

$SQL = "select *, empresa_endereco.empresa as cod_emp, empresa_endereco.codigo as cod_end from monitor_grupo left join empresa_endereco on monitor_grupo.endereco = empresa_endereco.codigo where monitor_grupo.codigo = '$codigo' and chave = '$chave' ";
$sth = &select($SQL);
$rv = $sth->rows();
if($rv < 1)
	{
	print  "ERRO: Acesso negado!\n";
	exit;
	}


# Inicia o download do script de monitoramento atualizado
if(!open (BAT, "<", $arq))
	{
	# Erro no caso de não ter arquivo de configuração
	print  "ERRO: Não foi encontrado arquivo de configuração.\n";
	exit;
	}
while(<BAT>)
	{
	print $_;
	}
