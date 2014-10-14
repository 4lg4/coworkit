#!/usr/bin/perl

# $nacess = 'nocheck';
$nacess = '';
require "../../cfg/init.pl";
$ID = &get("ID");
$Q = &get('term'); # conteudo da pesquisa
$T = &get('tbl'); # tabela da pesquisa
$F = &get('sfield'); # campo usado no where do sql
$RF = &get('rfield'); # campo de retorno do sql descricao q aparece na lista

# seleciona empresas inativas 
$EMPRESA_ATIVA = &get("empresa_ativa");
if($EMPRESA_ATIVA == "true")
	{
	$EMPRESA_ATIVA = " and ativo is true ";
	}
elsif($EMPRESA_ATIVA == "false")
	{
	$EMPRESA_ATIVA = " and ativo is false ";
	}

$S = &get('sql'); # define outros filtros apos primeira clausua do where
$J = &get('join'); # joins.
$O_ = &get('order'); # ordering

if($O_ eq "") 
	{ $O = "order by descrp asc"; }
else
	{ $O = "order by $O_ asc"; }

if($RF eq "") { $RF = "descrp"; }
if($F eq "") { $F = "descrp"; }


$SQL .= "select * from $T $J join parceiro_".$T." on ".$T.".codigo = parceiro_".$T.".".$T." and parceiro_".$T.".parceiro = $USER->{empresa} where $F <=> '%".$Q."%' $S $EMPRESA_ATIVA  $O limit 10";

print $query->header('application/json;charset=utf-8');

	$DB = DBE($SQL);
	$n = $DB->rows();
	
	if($n > 0)
		{
		while($row = $DB->fetchrow_hashref)
			{
			$R .= '{"value":"'.$row->{$RF}.'", "id":"'.$row->{codigo}.'"},';	
			}
		# $R1 = '{"value":"+ Adicionar Novo   ", "id":"0"},';	# create a fake option for add new value
		$R = "[$R1".substr($R, 0,-1)."]";
		}

	print $R;
	
 