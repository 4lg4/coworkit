#!/usr/bin/perl

$nacess = "48";
require "../cfg/init.pl";
$ID = &get('ID');

$DB = DBE("
    select 
        *
    from 
        contato_empresa_view
    where
        parceiro = $USER->{empresa}
");

if($DB->rows() > 0) {
    
	while($a = $DB->fetchrow_hashref) {
        
		$DBD = &DBE("
            select 
                cd.*, 
                tc.descrp as tipo_contato 
            from 
                contato_dados as cd 
            left join 
                tipo_contato as tc on tc.codigo = cd.tipo 
            where 
                cd.contato_endereco = $a->{codigo}
        ");
        
		while($cdados = $DBD->fetchrow_hashref) {
			$contato_dados .= $cdados->{tipo_contato}.": ".$cdados->{valor}."<br> ";
		}
        
        if(!$a->{apelido}) {
            $a->{apelido} = $a->{nome};
        }
        
        $contatos .= "{";
        $contatos .= "  \"val\"    : \"$a->{empresa}\",";
        $contatos .= "  \"descrp\" : \"";
        $contatos .= "     <div class='DTouchRadio_list_line'>";
        $contatos .= "         <div style='width:30%'>$a->{descrp}</div>";
        $contatos .= "         <div style='width:40%'>$contato_dados</div>";
        $contatos .= "         <div style='width:20%'>$a->{apelido}</div>";
        $contatos .= "     </div>";
        $contatos .= "\"},";
	}
} else {
        $contatos .= "{ val:0, descrp:'<div style=\"width:100%\">Nenhum registro encontrado !</div>' }";
}

$title  = "<div class=\"DTouchRadio_list_title\">";
$title .= "	<div style=\"width:30%\">Contato</div> ";
$title .= "	<div style=\"width:40%\">Dados</div> ";
$title .= "	<div style=\"width:20%\">Empresa</div> ";
$title .= "</div>";

# print $query->header('application/json; charset="utf-8"');
print $query->header({charset=>utf8});

# $contatos = substr($contatos, 0,-1);
# $contatos = "{$contatos}";

print<<HTML;
<script>
    \$("#contatos_list").DTouchRadio({
        orientation : "vertical",
    	title       : '$title',
    	search      : true,
        itemAdd     : [$contatos],
        click       : function(x){
            form.edit(x.value);
        }
    });
</script>
HTML

