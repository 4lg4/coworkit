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

# cfg 7 = configuracoes do dashboard
$DB = DBE("
    select 
        *
    from
        usuario_cfg
    where
        cfg = 7 and
        usuario = $USER->{usuario}
");

if($DB->rows() == 0) {
    $DB = DBE("
        select 
            \"default\" as valor
        from
            cfg
        where
            codigo = 7
    ");
}

$cfg = $DB->fetchrow_hashref; 



if($USER->{tipo} eq "99") { # 99 = cliente do parceiro
    $W = '"quotes","tkt","feedback"';
} else {
    # $W = '"quotes","tkt","customer_status","empresas","orc"';
    $W = $cfg->{valor};
    
    #if($USER->{empresa} eq "1") { # modulos done
     #   $W .= ',"deagle"';
    #}
} 

print $query->header('application/json; charset="utf-8"');

# retorno do codigo 
print<<HTML;

    {
        "status"  : "success",
        "message" : "Dados coletados com sucesso",
        "widgets" : [$W]
    }
    
HTML
