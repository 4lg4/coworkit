#!/usr/bin/perl

$nacess = "69";
require "../cfg/init.pl";
$ID = &get('ID');

$DB = DBE("
    select 
        *
    from 
        arquivo        
    where
        empresa = $USER->{empresa}
");

if($DB->rows() > 0) {
    
	while($a = $DB->fetchrow_hashref) {
        $files .= "{";
        $files .= "  \"val\"    : \"$a->{usuario}\",";
        $files .= "  \"descrp\" : \"";
        $files .= "     <div class='DTouchRadio_list_line'>";
        $files .= "         <div style='width:30%'>$a->{descrp}</div>";
        $files .= "         <div style='width:20%'>$a->{nome}</div>";
        $files .= "         <div style='width:10%'>$a->{tipoaaaa}</div>";
        $files .= "         <div style='width:10%'>$a->{tamanho}</div>";
        $files .= "         <div style='width:10%'>$a->{link}</div>";
        $files .= "         <div style='width:10%'>[Down] [Del]</div>";
        $files .= "     </div>";
        $files .= "\"},";
	}
} else {
        $files .= "{ val:0, descrp:'<div style=\"width:100%\">Nenhum registro encontrado !</div>' }";
}

$title  = "<div class=\"DTouchRadio_list_title\">";
$title .= "	<div style=\"width:30%\">Descrição</div> ";
$title .= "	<div style=\"width:20%\">Nome</div> ";
$title .= "	<div style=\"width:10%\">Tipo</div> ";
$title .= "	<div style=\"width:10%\">Tamanho</div> ";
$title .= "	<div style=\"width:10%\">Módulo</div> ";
$title .= "	<div style=\"width:10%\">Ação</div> ";
$title .= "</div>";

# print $query->header('application/json; charset="utf-8"');
print $query->header({charset=>utf8});

# $files = substr($files, 0,-1);
# $files = "{$files}";

print<<HTML;
<script>
    \$("#files_list").DTouchRadio({
        orientation : "vertical",
    	title       : '$title',
    	search      : true,
        itemAdd     : [$files],
        click       : function(x){
            form.edit(x.value);
        }
    });
</script>
HTML

