#!/usr/bin/perl
 
# 
# planos.cgi
# carrega planos do cliente
#

$nacess = '10';
require "../cfg/init.pl";

print $query->header({charset=>utf8});

$ID      = &get('ID');
$empresa = &get('empresa');
$planom  = &get('plano');
$area    = &get('area');

# debug($planom);

# Planos de Atendimento --------------------------------------------------------------------------------------
# $DB = DBE("select ps.codigo, ps.descrp from empresa_prod_servicos as eps left join prod_servicos as ps on ps.codigo = eps.prod_servicos where eps.empresa = $empresa and ps.empresa_area_tipo = $area order by ps.descrp");
$DB = DBE("
        select 
        	ps.codigo, ps.descrp 
        from 
        	prod_servicos as ps 
        where 
        	ps.empresa = $empresa and 
        	ps.empresa_area_tipo = $area and
            ps.parceiro = $USER->{empresa}
        order by 
        	ps.descrp
");

while($p = $DB->fetchrow_hashref) {
	$plano .= "{val:$p->{codigo},descrp:'$p->{descrp}'},";	
    
    # se existir somente um plano
    if($DB->rows() == 1) {
    	$marca = $p->{codigo};
    }
}


# planos genericos
if($DB->rows() == 0) {
    $DB = DBE("
            select 
            	ps.codigo, ps.descrp 
            from 
            	prod_servicos as ps 
            where 
            	ps.empresa is null and 
            	ps.empresa_area_tipo = $area and
                ps.parceiro = $USER->{empresa} 
            order by 
            	ps.descrp
    ");
    
    if($DB->rows() > 0) {
        while($p = $DB->fetchrow_hashref) {
        	$plano .= "{val:$p->{codigo},descrp:'$p->{descrp}'},";	
            
            # se existir somente um plano
            if($DB->rows() == 1) {
            	$marca = $p->{codigo};
            }
        }
    }
}







# se nao existir registros
if($DB->rows() == 0) {
	print "<script>	
				\$('#plano').DTouchRadio('reset','hard');
				\$('#plano_container').fadeOut('fast');
			</script>";
	exit;
}
	
# se plano vier preenchido
if($planom ne "") {
	$marca = $planom;
}

# debug($planom);
# debug($marca);

print<<HTML;
<script>
    /**
     *  Cliente do Parceiro
     *      usuario tipo 99
     */
    if("$USER->{tipo}" !== "99") {
	    \$('#plano_container').fadeIn('fast');
    } 
    
	// \$("#plano").html();
	\$("#plano").DTouchRadio({ 
		orientation:"vertical", 
		addItem:[$plano],
        uncheck : false,
		value: '$marca'
	});
</script>
HTML

exit;
