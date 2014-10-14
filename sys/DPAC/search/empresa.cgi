#!/usr/bin/perl

# $nacess = 'nocheck';
$nacess = '';
require "../../cfg/init.pl";

$ID = &get("ID");
$T  = &get('tbl'); # tabela da pesquisa
$S  = &get('term'); # conteudo da pesquisa

# lista de empresa
if($T eq "empresa"){ #ativas
    $W = "where e.ativo is true and (e.nome <=> '%$S%' or e.apelido <=> '%$S%')";
} elsif ($T eq "empresa_inativa"){ # inativas
    $W = "where e.ativo is false  and (e.nome <=> '%$S%' or e.apelido <=> '%$S%')";
} else {
    $W = "where e.nome <=> '%$S%' or e.apelido <=> '%$S%'";
}

print $query->header('application/json;charset=utf-8');

	$DB = DBE("select e.* from empresa as e join parceiro_empresa as pe on pe.empresa = e.codigo and pe.parceiro = $USER->{empresa} $W order by e.nome asc limit 10");
	
	if($DB->rows() > 0) {
		while($row = $DB->fetchrow_hashref) {
			$R .= '{"value":"'.$row->{nome}.'", "id":"'.$row->{codigo}.'"},';	
		}
		$R = "[$R1".substr($R, 0,-1)."]";
	}

	print $R;
	
 
