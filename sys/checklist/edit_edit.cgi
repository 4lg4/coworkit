#!/usr/bin/perl

$nacess = "70";
require "../cfg/init.pl";

# vars
$ID  = &get('ID');
$tkt = &get('tkt');

# print
print $query->header({charset=>utf8});

# statment
$DB = DBE("
    select 
	    c.*,
	    tkt.cliente_nome
    from 
        checklist as c
	left join 
		tkt_full as tkt on tkt.codigo = c.tkt
    where
        c.tkt = $tkt
");
# checklist
$checklist = $DB->fetchrow_hashref;


# novo checklist
if($DB->rows == 0) { 
    
    $COD = DBE("
        insert into
            checklist (
                tkt,
                parceiro
            ) values (
                $tkt, $USER->{empresa}
            )
    ");
    
    $checklist->{codigo} = $COD;
    
    $DB = DBE("
        select 
    	    cliente_nome
        from 
    		tkt_full as tkt
        where
            codigo = $tkt
    ");
    # checklist
    $t = $DB->fetchrow_hashref;
    
    $checklist->{cliente_nome} = $t->{cliente_nome};

# edicao    
} else {
    
    # inventario acoes
    $DB = DBE("
        select 
    	    ai.*,
    	    i.descrp
        from 
            checklist_acao_inventario as ai
    	left join 
    		checklist_inventario as i on i.codigo = ai.inventario
        where
            ai.checklist = $checklist->{codigo}
    ");

    if($DB->rows > 0) {
        while($i = $DB->fetchrow_hashref) {
            $inventario .= '{';
            $inventario .= '    "value" : '.$i->{inventario}.', ';
            $inventario .= '    "descrp" : "'.$i->{descrp}.'"';
            $inventario .= '},';
        }
        $inventario = ' , "inventario" : ['.(substr($inventario, 0,-1)).']';
    }
    
    
    # servico acoes
    $DB = DBE("
        select 
    	    ai.*,
    	    i.descrp
        from 
            checklist_acao_servico as ai
    	left join 
    		checklist_servico as i on i.codigo = ai.servico
        where
            ai.checklist = $checklist->{codigo}
    ");

    if($DB->rows > 0) {
        while($i = $DB->fetchrow_hashref) {
            $servico .= '{';
            $servico .= '    "value"    : '.$i->{servico}.', ';
            $servico .= '    "descrp"   : "'.$i->{descrp}.'", ';
            $servico .= '    "usuario_ini"  : "'.$i->{usuario_ini}.'", ';
            $servico .= '    "usuario_end"  : "'.$i->{usuario_end}.'", ';
            $servico .= '    "hora_ini" : "'.(dateToShow($i->{hora_ini})).'", ';
            $servico .= '    "hora_end" : "'.(dateToShow($i->{hora_end})).'"';
            $servico .= '},';
        }
        $servico = ' , "servico" : ['.(substr($servico, 0,-1)).']';
    }
}



    $R  = '{ ';
    $R .= '     "COD"      : "'.$checklist->{codigo}.'", ';
    $R .= '     "tkt"      : "'.$tkt.'", ';
    $R .= '     "cliente"  : "'.$checklist->{cliente_nome}.'", ';
    $R .= '     "dtag"     : "'.$checklist->{dtag}.'"  ';
    $R .= $inventario;
    $R .= $servico;
    $R .= '}  ';

print $R;
