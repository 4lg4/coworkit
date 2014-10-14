#!/usr/bin/perl

$nacess = '204';
require "../cfg/init.pl";

$ID       = &get('ID');
$agrupo   = &get('agrupo');

if($agrupo){
    $agrupo = " and ag.agrupo = $agrupo ";
}

$DB = DBE("
    select 
        distinct g.codigo,
    	g.descrp
    from 
    	parceiro_grupo as pg 
    join
    	grupo as g on g.codigo = pg.grupo
	left join
    	agrupo_grupo as ag on ag.grupo = g.codigo
    where
    	pg.parceiro = $USER->{empresa} 
        $agrupo
    order by 
        g.descrp
    asc
");

if($DB > 0) {
	while($g = $DB->fetchrow_hashref) {
        $grupos .= '{';
        $grupos .= '    "value"  :  '.$g->{codigo}.', ';
        $grupos .= '    "descrp" : "'.$g->{descrp}.'"';
        $grupos .= '},';
    }
    $R  = ' { ';
    $R .= '      "grupos" : ['.(substr($grupos, 0,-1)).'] ';
    $R .= '    , "debug"  :  "agrupo: '.$agrupo.' | grupo: '.$grupo.' | empresa: '.$empresa.' | end: '.$endereco.' | sql: '.$SQL.'" ';
    $R .= ' }';

} else {
    $R = ' "grupos" : []';
}

print $query->header('application/json; charset="utf-8"');
print $R;



