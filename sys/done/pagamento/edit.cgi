#!/usr/bin/perl

$nacess = "80";
require "../../cfg/init.pl";

# vars
$ID    = &get('ID');
$COD   = &get('COD');
$plano = &get('plano');
$empresa = &get('empresa');

# features
$DBD = DBE("
    select 
        *
    from 
        coworkit_plan_view
    where
        empresa = $empresa or ( coworkit_plan = $plano and empresa is null )
");


if($DBD->rows() > 0) {
    while($defaults = $DBD->fetchrow_hashref){
        
        $itensd .= '{';
        $itensd .= '     "codigo"      :  "'.$defaults->{codigo}.'",  ';
        $itensd .= '     "default"     :  "'.$defaults->{default}.'",  ';
        $itensd .= '     "descrp"      :  "'.$defaults->{descrp}.'",  ';
        $itensd .= '     "internal_descrp"  :  "'.$defaults->{internal_descrp}.'",  ';
        $itensd .= '     "custom"      :  "'.$defaults->{custom}.'",  ';
        $itensd .= '     "tipo"        :  "'.$defaults->{tipo}.'"  ';
        $itensd .= '},';
    }
    $itensd = substr($itensd, 0,-1);
}


# pagamentos
$DBC = DBE("
    select 
        pcp.*,
        cp.descrp as plan_descrp
    from 
        parceiro_coworkit_pagamento as  pcp
    left join
        coworkit_plan as cp on
            cp.codigo = pcp.coworkit_plan
    where
        pcp.empresa = $empresa
");

if($DBC->rows() > 0) {
    while($pagamentos = $DBC->fetchrow_hashref){
        
        $itensc .= '{';
        $itensc .= '     "codigo"          :  "'.$pagamentos->{codigo}.'",  ';
        $itensc .= '     "plan_descrp"     :  "'.$pagamentos->{plan_descrp}.'",  ';
        $itensc .= '     "data_vencimento" :  "'.$pagamentos->{data_vencimento}.'",  ';
        $itensc .= '     "data_pagamento"  :  "'.$pagamentos->{data_pagamento}.'",  ';
        $itensc .= '     "valor"           :  "'.$pagamentos->{valor}.'"  ';
        $itensc .= '},';
    }
    $itensc = substr($itensc, 0,-1);
}

$R  = '{ ';
$R .= '     "features" : ['.$itensd.'],';
$R .= '     "pagamentos"  : ['.$itensc.']';
$R .= '}';

print $query->header({charset=>utf8});
print $R;
