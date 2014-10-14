#!/usr/bin/perl

$nacess = "80";
require "../../cfg/init.pl";
$ID = &get('ID');


$DB = DBE("
    select 
        e.codigo,
        e.nome,
        p.codigo as plano_codigo,
        p.descrp,
        (select uh.dt from usuario_historico as uh where uh.empresa = e.codigo order by uh.dt desc limit 1) as last_access
    from 
        parceiro_plan as pp
    left join
        empresa as e on e.codigo = pp.empresa
    left join
        coworkit_plan as p on p.codigo = pp.coworkit_plan
");

if($DB->rows() > 0) {
        
    while($l = $DB->fetchrow_hashref) {
                
        # valor
        if($l->{valor} !~ /\./){
            $l->{valor} .= ".00";
        } elsif($l->{valor} =~ /\.\d{1}$/){ 
            $l->{valor} .= "0";
        }
        $l->{valor} =~ s/\./\,/g;
           
        $list .= "{";
        $list .= "  \"val\"    : \"$l->{codigo}\",";
        $list .= "  \"descrp\" : \"";
        $list .= "     <div class='DTouchRadio_list_line $nochange'>";
        $list .= "         <input type='hidden' name='empresa_nome' value='$l->{nome}'> ";
        $list .= "         <input type='hidden' name='plano' value='$l->{plano_codigo}'> ";
        $list .= "         <input type='hidden' name='plano_descrp' value='$l->{descrp}'> ";
        
        $list .= "         <div style='width:10%'>$l->{codigo}</div>";
        $list .= "         <div style='width:40%'>$l->{nome}</div>";
        $list .= "         <div style='width:30%'>$l->{descrp}</div>";
        $list .= "         <div style='width:10%'>".(&dateToShow($l->{last_access}))."</div>";
        $list .= "     </div>";
        $list .= "\"},";
	}
} else {
        $list .= "{ val:0, descrp:'<div style=\"width:100%\">Nenhum registro encontrado !</div>' }";
}

$title  = "<div class=\"DTouchRadio_list_title\">";
$title .= "	<div style=\"width:10%\">Código</div> ";
$title .= "	<div style=\"width:40%\">Empresa</div> ";
$title .= "	<div style=\"width:30%\">Plano</div> ";
$title .= "	<div style=\"width:10%\">Último Acesso</div> ";
$title .= "</div>";

# print $query->header('application/json; charset="utf-8"');
print $query->header({charset=>utf8});

# $list = substr($list, 0,-1);
# $list = "{$list}";

print<<HTML;
<script>
    \$("#pagamento_list").DTouchRadio({
        orientation : "vertical",
    	title       : '$title',
    	search      : true,
        itemAdd     : [$list],
        uncheck     : false,
        click       : function(x){
            pagto.edit();
        }
    });
</script>
HTML

