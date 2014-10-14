#!/usr/bin/perl

$nacess = '';
require "../cfg/init.pl";

$ID = &get('ID');
$Q  = &get('term'); # conteudo da pesquisa
$T  = &get('tbl'); # tabela da pesquisa

# pesquisa padrao


if($T eq "produtos") {
    $W  = " descrp <=> '%".$Q."%'";
    $W .= " or modelo <=> '%".$Q."%' ";
    $W .= " or obs <=> '%".$Q."%' ";
    $W .= " or partnumber <=> '%".$Q."%' ";
    $W .= " or marca_descrp <=> '%".$Q."%' ";
    # $W  = "($W) ";
    
    $SQL = "select *, preco_venda as valor from prod_mercadorias_full where ($W) and parceiro = $USER->{empresa} order by descrp asc limit 10;";
    
} elsif($T eq "despesas") {   
    $SQL = "select * from prod_despesas where descrp <=> '%".$Q."%' and parceiro = $USER->{empresa} order by descrp asc limit 10;";
    
} elsif($T eq "servicos") {   
    $SQL = "select * from prod_serv where descrp <=> '%".$Q."%' and parceiro = $USER->{empresa} order by descrp asc limit 10;";
        
} elsif($T eq "empresa") {    
    $SQL = "
        select 
            e.nome as descrp,
            ee.*,
            e.codigo as codigo,
            te.descrp as tipo_descrp
        from 
            empresa as e 
        join 
            parceiro_empresa as pe on 
                pe.empresa = e.codigo and 
                pe.parceiro = $USER->{empresa}
        join 
            empresa_endereco as ee on 
                ee.empresa = e.codigo
        left join 
            tipo_endereco as te on 
                te.codigo = ee.tipo
        where 
            e.nome <=> '%".$Q."%' or 
            e.apelido <=> '%".$Q."%' 
        order by 
            nome asc 
        limit 10
    ";
}                    

print $query->header('application/json; charset="utf-8"');
# print $query->header({charset=>utf8});	
# print "$ID - $Q - $T"; exit;
	$DB = DBE($SQL);
    	
	if($DB->rows() > 0) {
		while($row = $DB->fetchrow_hashref) {
                        
            $row->{valor} =~ s/R\$//gm;
            $row->{valor} =~ s/\s+//gm;
            
            if(!$row->{valor}) {
                $row->{valor} = 0;   
            }
            $row->{valor} = sprintf("%.2f", $row->{valor});
            $valor_show   = ' - R$ '.$row->{valor};
            
            
            if($T eq "prod_mercadorias_full") {
                $valor_show = "(".$row->{modelo}."  ".$row->{marca_descrp}."  ".$row->{partnumber}.")".$valor_show." ".$row->{unidade_descrp};
            } elsif($T eq "empresa") {
                $end_show = "($row->{tipo_descrp} - $row->{endereco}, $row->{complemento} - $row->{bairro} / $row->{cidade} - $row->{uf})";
            }
            
			$R .= '{';
            $R .= '     "label" : "'.$row->{descrp}.' '.$valor_show.$end_show.'",';
            $R .= '     "value" : "'.$row->{descrp}.' '.$end_show.'",';
            $R .= '     "id"    : "'.$row->{codigo}.'",';
            $R .= '     "valor" : "'.$row->{valor}.'",';
            $R .= '     "unidade" : "'.$row->{unidade_descrp}.'",';
            $R .= '     "modelo"  : "'.$row->{modelo}.'",';
            $R .= '     "marca"   : "'.$row->{marca_descrp}.'",';
            $R .= '     "partnumber"  : "'.$row->{partnumber}.'",';
            $R .= '     "endereco"  :  { ';
            $R .= '         "codigo"  :  "'.$row->{codigo}.'",';
            $R .= '         "descrp"  :  "'.$row->{endereco}.'"';
            $R .= '     }';
            $R .= '},';
		}
		# $R1 = '{"value":"+ Adicionar Novo   ", "id":"0"},';	# create a fake option for add new value
		$R = "[".substr($R, 0,-1)."]";
        
    # novo
	}
    # else {
	#	$R .= '[{';
    #    $R .= '     "label" : "Adicionar novo item ?",';
    #    $R .= '     "value" : "Adicionar novo item ?",';
    #    $R .= '     "id"    : "new"';
    #    $R .= '}]';
	# }

	print $R;
	
 
