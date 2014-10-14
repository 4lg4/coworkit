#!/usr/bin/perl

$nacess = "55";
require "../cfg/init.pl";

# vars
$ID  = &get('ID');
$COD = &get('COD');

# statment
$DB = DBE("
    select 
        ps.*,
        e.nome as empresa_nome
    from 
        prod_servicos as ps
    left join
        empresa as e on e.codigo = ps.empresa
    where
        ps.codigo = $COD
");

# plano
$plano = $DB->fetchrow_hashref;

# print
print $query->header({charset=>utf8});

    $R  = '{ ';
    $R .= '     "empresa"       : "'.$plano->{empresa}.'",  ';
    $R .= '     "empresa_nome"  : "'.$plano->{empresa_nome}.'",  ';
    $R .= '     "cobranca_dia"  : "'.$plano->{cobranca_dia}.'", ';
    $R .= '     "cobranca"      : "'.$plano->{cobranca}.'", ';
    $R .= '     "descrp"        : "'.$plano->{descrp}.'",  ';
    $R .= '     "obs"           : "'.$plano->{obs}.'",  ';
    $R .= '     "area"          : "'.$plano->{empresa_area_tipo}.'",  ';
    $R .= '     "status"        : "'.$plano->{status}.'",  ';
    $R .= '     "hora"          : "'.$plano->{horas_plano}.'",  ';
    $R .= '     "lock"          : "'.$plano->{restrito}.'",  ';
    $R .= '     "vigencia_ini"  : "'.(&dateToShow($plano->{vigencia_ini},"date")).'",  ';
    $R .= '     "vigencia_fim"  : "'.(&dateToShow($plano->{vigencia_fim},"date")).'"  ';
    $R .= '}  ';

print $R;
