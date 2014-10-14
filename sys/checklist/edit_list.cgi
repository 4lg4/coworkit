#!/usr/bin/perl

$nacess = "70";
require "../cfg/init.pl";
$ID = &get('ID');


$DB = DBE("
    select 
        *
    from 
        tkt_full
    where
        empresa_logada = $USER->{empresa}
    order by
        codigo
    desc
");

if($DB->rows() > 0) {
        
    while($tkt = $DB->fetchrow_hashref) {
                 
        if($tkt->{status} == 0) {
            $ckd = "Não";
        } else {
            $ckd = "Sim";
        }
         
        $tkt->{problema} = &get($tkt->{problema}, "NEWLINE_SHOW");
         
        $checklist .= "{";
        $checklist .= "  \"val\"    : \"$tkt->{codigo}\",";
        $checklist .= "  \"descrp\" : \"";
        $checklist .= "     <div class='DTouchRadio_list_line'>";
        $checklist .= "         <div style='width:10%'>$tkt->{codigo}</div>";
        $checklist .= "         <div style='width:40%'>$tkt->{cliente_nome}</div>";
        $checklist .= "         <div style='width:50%'>$tkt->{problema}</div>";
        $checklist .= "     </div>";
        $checklist .= "\"},";
	}
} else {
        $checklist .= "{ val:0, descrp:'<div style=\"width:100%\">Nenhum registro encontrado !</div>' }";
}

$title  = "<div class=\"DTouchRadio_list_title\">";
$title .= "	<div style=\"width:10%\">Tkt</div> ";
$title .= "	<div style=\"width:40%\">Cliente</div> ";
$title .= "	<div style=\"width:50%\">Descrição</div> ";
$title .= "</div>";

# print $query->header('application/json; charset="utf-8"');
print $query->header({charset=>utf8});

# $checklist = substr($checklist, 0,-1);
# $checklist = "{$checklist}";

print<<HTML;
<script>
    \$("#checklist_list").DTouchRadio({
        orientation : "vertical",
    	title       : '$title',
    	search      : true,
        itemAdd     : [$checklist],
        click       : function(x){
            form.edit(x.value);
        }
    });
</script>
HTML

