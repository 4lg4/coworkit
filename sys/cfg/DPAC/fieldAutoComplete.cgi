#!/usr/bin/perl

$nacess = 'nocheck';
require "../../cfg/init.pl";
$Q  = &get('term'); # conteudo da pesquisa
$T  = &get('tbl'); # tabela da pesquisa
$F  = &get('sfield'); # campo usado no where do sql
$RF = &get('rfield'); # campo de retorno do sql descricao q aparece na lista

$S  = &get('sql'); # define outros filtros apos primeira clausua do where
$J  = &get('join'); # joins.
$O_ = &get('order'); # ordering

# ajuste se tabela nao tiver campo codigo
if($T eq "usuario") { 
    $CODRET = "usuario"; 
} else { 
    $CODRET = "codigo"; 
}


if($O_ eq "") { 
    $O = "order by descrp asc"; 
} else { 
    $O = "order by $O_ asc"; 
}

if($RF eq "") { 
    $RF = "descrp"; 
}

if($F eq "") { 
    $F = "descrp"; 
}


# } elsif($T eq "empresa") {
#    $D = "nome";
#    $W = "where empresa = ".$USER->{empresa};
# }

                    

print $query->header('application/json; charset="utf-8"');
	
	$sth = &select("select * from $T $J where $F <=> '%".$Q."%' $S $O limit 10;");
	$n = $sth->rows();
	
	if($n > 0) {
		while($row = $sth->fetchrow_hashref) {				
			$R .= '{';
            $R .= '     "label" : "'.$row->{descrp}.'",';
            $R .= '     "value" : "'.$row->{$RF}.'",';
            $R .= '     "id"    : "'.$row->{$CODRET}.'"';
            $R .= '},';
		}
		# $R1 = '{"value":"+ Adicionar Novo   ", "id":"0"},';	# create a fake option for add new value
		$R = "[$R1".substr($R, 0,-1)."]";
	}

	print $R;
	
 
