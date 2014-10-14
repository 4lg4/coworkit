#!/usr/bin/perl

$nacess = '';
require "../cfg/init.pl";
$Q = &get('term'); # conteudo da pesquisa
$T = &get('tbl'); # tabela da pesquisa
$F = &get('sfield'); # campo usado no where do sql
$RF = &get('rfield'); # campo de retorno do sql descricao q aparece na lista

$S = &get('sql'); # define outros filtros apos primeira clausua do where
if($S ne "")
	{
	$S = "and ".$S;
	}
$J = &get('join'); # joins.
$O_ = &get('order'); # ordering

if($O_ eq "") 
	{ $O = "order by descrp asc"; }
else
	{ $O = "order by $O_ asc"; }

if($RF eq "") { $RF = "descrp"; }
if($F eq "") { $F = "descrp"; }

print $query->header('application/json; charset=utf-8');

$SQL = "select * from $T $J ";
$sth9 = &select("select * from pg_tables where tablename='parceiro_".$T."'");
$rv9 = $sth9->rows();
if($rv9 > 0)
	{
	$SQL .= " join parceiro_".$T." on ".$T.".codigo = parceiro_".$T.".".$T." and parceiro_".$T.".parceiro = '$LOGEMPRESA' ";
	}
$SQL .= " where $F <=> '%".$Q."%' $S $O limit 10";

$sth = &select($SQL);
$n = $sth->rows();

if($n > 0)
	{
	while($row = $sth->fetchrow_hashref)
		{
		$R .= '{"value":"'.$row->{$RF}.'", "id":"'.$row->{codigo}.'"},';	
		}
	# $R1 = '{"value":"+ Adicionar Novo   ", "id":"0"},';	# create a fake option for add new value
	$R = "[$R1".substr($R, 0,-1)."]";
	}
else
	{
	$R .= '{"value":"'.$SQL.'", "id":"'.$SQL.'"},';	
	}

print $R;
	
 
