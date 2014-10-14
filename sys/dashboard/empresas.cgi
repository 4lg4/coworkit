#!/usr/bin/perl

#
# estatisticas.cgi
#   estatisticas dos clientes
#

$nacess = "2";
require "../cfg/init.pl";

$ID      = &get('ID');

print $query->header({charset=>utf8});

# empresas top 10
$DB = DBE("
        select 
        	lv.codigo, e.nome 
        from 
        	last_view as lv 
        	left join empresa as e on e.codigo = lv.codigo 
        where
        	lv.tabela = 'empresa' and lv.usuario = $USER->{usuario}	
        ORDER BY
        	lv.dt desc
        LIMIT 10
");

if($DB->rows() > 0) {
    while($E = $DB->fetchrow_hashref) {
        $R .= "{";
    	$R .= "     val    : $E->{codigo},";
    	$R .= "     descrp : '";
        $R .= "         <div style=\"width:100%\">$E->{nome}</div>";
        $R .= "'},";
    }
} else {
    $R = "{ val:0, descrp:'<div style=\"width:100%\">Nenhum registro encontrado !</div>' }";
}


# $title .= "<div class=\"DTouchRadio_list_title\">";
# $title .= " 	<div style=\"width:100%\">Empresa</div>";
# $title .= "</div>";

    
# retorno do codigo 
print<<HTML;
<script>
	\$("#empresas").DTouchRadio({
        orientation  : "vertical",
        // title        : '$title',
        addItem      : [$R],
		click: function(res) { 
            if(res.value === "0"){
                return false;
            }  
            
            call("empresa/edit.cgi",{COD:res.value}); // edicao empresa
        }
	});
</script>

HTML
