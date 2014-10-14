#!/usr/bin/perl

#
# quotes.cgi
#
# carrega aleatoriamente uma quote diaria
#

$nacess = "2";
# $nacess_more = "or menu = 74";
require "../cfg/init.pl";

$ID = &get('ID');

# print $query->header({charset=>utf8});


# gera grafico com as ultimas medicoes
$DB = DBE("
    select 
        distinct monitor_grupo.descrp 
    from 
        monitor_grupo 
    where 
        monitor_grupo.hidden is not true and 
        monitor_grupo.codigo not in (
            select 
                distinct monitor_grupo.codigo 
            from 
                monitor_grupo 
            join 
                monitor_historico on monitor_grupo.codigo = monitor_historico.monitor 
            where 
                monitor_historico.dt > now() - interval '1 day'
        )
");

while($q = $DB->fetchrow_hashref) {
    $itens .= '"'.$q->{descrp}.'",';
}
$itens = '['.substr($itens, 0,-1).']';


# retorno do codigo 
print $query->header('application/json; charset="utf-8"');
print $itens
