#!/usr/bin/perl

$nacess = "2";
require "../cfg/init.pl";
require "../cfg/DPAC/DefaultModule.pl";

# vars
$ID   = &get('ID');
$COD  = &get('COD');
$TBL  = &get('TBL');

# print
print $query->header({charset=>utf8});

# statment
$DB = DBE("
    select 
	    *
    from 
        $TBL
    where
        codigo = $COD
");

# novo defaultmod
if($DB->rows == 1) {
    $defaultmod = $DB->fetchrow_hashref;
    
    $R  = '{ ';
    $R .= '     "status"   : "success", ';
    $R .= '     "message"  : "Sucesso !", ';
    $R .= '     "COD"      : "'.$defaultmod->{codigo}.'", ';
    $R .= '     "descrp"   : "'.$defaultmod->{descrp}.'" ';
    $R .= '}  ';
} else {
    $R  = '{ ';
    $R .= '     "status"   : "error", ';
    $R .= '     "message"  : "Erro ao selecionar !" ';
    $R .= '}  ';
}

print $R;
exit;

