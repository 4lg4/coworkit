#!/usr/bin/perl

# $nacess = 'nocheck';
$nacess = '';
require "../../cfg/init.pl";
$ID = &get("ID");
$Q = &get('term'); # conteudo da pesquisa
# $T = &get('tbl'); # tabela da pesquisa
$F = &get('sfield'); # campo usado no where do sql
# $RF = &get('rfield'); # campo de retorno do sql descricao q aparece na lista

# $S = &get('sql'); # define outros filtros apos primeira clausua do where
# $J = &get('join'); # joins.
# $O_ = &get('order'); # ordering
# if($O_ eq "") 
#	{ $O = "order by descrp asc"; }
# else
#	{ $O = "order by $O_ asc"; }
# if($RF eq "") { $RF = "descrp"; }
# if($F eq "") { $F = "descrp"; }


# $SQL .= "select * from $T $J join parceiro_".$T." on ".$T.".codigo = parceiro_".$T.".".$T." and parceiro_".$T.".parceiro = $USER->{empresa} where $F <=> '%".$Q."%' $S $EMPRESA_ATIVA  $O limit 10";

$SQL .= "select * from usuario where nome <=> '%".$Q."%' and empresa = $USER->{empresa} and bloqueado is false limit 10";

print $query->header('application/json;charset=utf-8');

	$DB = DBE($SQL); # executa sql
	
    # monta lista
	if($DB->rows() > 0)
		{
		while($row = $DB->fetchrow_hashref)
			{
			$R .= '{"value":"'.$row->{nome}.'", "id":"'.$row->{usuario}.'", "img":"'.$row->{img}.'"},';	
			}
		# $R1 = '{"value":"+ Adicionar Novo   ", "id":"0"},';	# create a fake option for add new value
		$R = "[$R1".substr($R, 0,-1)."]";
		}

	print $R;
	
 
