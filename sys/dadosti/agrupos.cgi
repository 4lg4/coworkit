#!/usr/bin/perl

$nacess = '204';
require "../cfg/init.pl";

$ID       = &get('ID');

$DB = DBE("
    select 
    	a.*
    from 
    	parceiro_agrupo as pa 
    join
    	agrupo as a on a.codigo = pa.agrupo
    where
    	pa.parceiro = $USER->{empresa}
    order by 
        a.descrp
    asc
");

if($DB > 0) {
	while($a = $DB->fetchrow_hashref) {
        $agrupos .= '{';
        $agrupos .= '    "value"  :  '.$a->{codigo}.', ';
        $agrupos .= '    "descrp" : "'.$a->{descrp}.'"';
        $agrupos .= '},';
    }
    $R  = ' { ';
    $R .= '      "agrupos" : ['.(substr($agrupos, 0,-1)).'] ';
    $R .= '    , "debug"  :  "agrupo: '.$agrupo.' | grupo: '.$grupo.' | empresa: '.$empresa.' | end: '.$endereco.' | sql: '.$SQL.'" ';
    $R .= ' }';

} else {
    $R = ' "agrupos" : []';
}

print $query->header('application/json; charset="utf-8"');
print $R;
