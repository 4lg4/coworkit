#!/usr/bin/perl
require "../init.pl";

#
#   Empresa Limit
#       emp_limit.cgi
#
#       quantidade de empresas disponiveis
#

# pega variaveis
$ID   = &get("ID");    # ID do usuario logado
$acao = &get("acao");  # acao 

# header 
print $query->header('application/json; charset="utf-8"');

#
# if($acao eq "get"){
    # total espaco em disco
    # select valor as total, cfg_default as default, (select count(empresa) from parceiro_empresa where parceiro = $USER->{empresa}) as used from parceiro_cfg_full where cfg_id = 'emp-limit' and empresa = $USER->{empresa}
    my $DB = &DBE("
        select 
        	custom as total, 
        	\"default\"
        from 
        	coworkit_plan_view
        where 
        	empresa = $USER->{empresa} or 
            (   
                coworkit_plan_feature = 1 and 
                empresa is null 
            )
    ");
    
    
    # if($DB->rows() == 0) {
    #    $DB = &DBE("
    #        select \"default\"::int as default, (select count(empresa) from parceiro_empresa where parceiro = $USER->{empresa}) as used from cfg where internal_descrp = 'emp-limit'
    #    ");
    # }    
    
    my $R = $DB->fetchrow_hashref;
    
    if(!$R->{total} || $R->{total} eq "0") {
        $R->{total} = $R->{default};
    }
    
    if(!$R->{used}) {
        $R->{used} = 0;
    }
    
    print "
        {
            \"total\" : $R->{total},
            \"used\"  : $R->{used}
        }
    ";
# }

