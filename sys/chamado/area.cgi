#!/usr/bin/perl
 
# 
# area.cgi
# carrega areas da empresa baseado nos planos do cliente
#

$nacess = '10';
require "../cfg/init.pl";

print $query->header({charset=>utf8});

$ID = &get('ID');
$empresa = &get('empresa');
$aream = &get('area');

# Executa pesquisa
# $DB = DBE("select DISTINCT(eat.codigo), eat.descrp, eat.img from empresa_prod_servicos as ep left join prod_servicos as ps on ps.codigo = ep.prod_servicos  left join empresa_area_tipo as eat on eat.codigo = ps.empresa_area_tipo where ep.empresa = $empresa and eat.codigo is not null");
$DB = DBE("
        select 
        	DISTINCT(eat.codigo), eat.descrp, eat.img 
        from 
        	prod_servicos as ps 
        left join 
        	empresa_area_tipo as eat on eat.codigo = ps.empresa_area_tipo 
        where 
        	ps.empresa = $empresa and eat.codigo is not null and ps.status is true and ps.parceiro = $USER->{empresa}
");


if($DB->rows() > 0) { 
    # gera array
    while($a = $DB->fetchrow_hashref) {
    	$area .= "{val:$a->{codigo},descrp:'$a->{descrp}',img:'$a->{img}'},";		
        
        # se existir somente um registro
        if($DB->rows() == 1) {
        	$marca = $a->{codigo};
        }
    }
    
# planos genericos
} else {
    $DB = DBE("
            select 
            	DISTINCT(eat.codigo), eat.descrp, eat.img 
            from 
            	prod_servicos as ps 
            left join 
            	empresa_area_tipo as eat on eat.codigo = ps.empresa_area_tipo 
            where 
            	ps.empresa is null and eat.codigo is not null and ps.status is true and ps.parceiro = $USER->{empresa}
    ");
    
    if($DB->rows() > 0) { 
        # gera array
        while($a = $DB->fetchrow_hashref) {
        	$area .= "{val:$a->{codigo},descrp:'$a->{descrp}',img:'$a->{img}'},";		
            
            # se existir somente um registro
            if($DB->rows() == 1) {
            	$marca = $a->{codigo};
            }
        }
    }
}

# se ja for selecionado
if($aream ne "") {
	$marca = $aream;
}

print<<HTML;


<script>
	// \$('#area').DTouchRadio('reset','hard');
	\$('#area_container').fadeIn('fast');

	\$("#area").DTouchRadio({ 
		addItem:[$area],
		value: '$marca',
        uncheck : false,
		click: function(x){
			empresa.planos(x.value);
            chamado.emails_update();
		}
	});
    
    if("$marca" !== ""){
		empresa.planos($marca);
        chamado.emails_update();
    }
    
</script>
HTML

exit;
