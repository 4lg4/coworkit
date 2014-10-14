#!/usr/bin/perl
require "../init.pl";

#
#   Disk
#       disk.cgi
#
#       disco e espacos disponiveis
#

# pega variaveis
$ID   = &get("ID");    # ID do usuario logado
$acao = &get("acao");  # acao 

# header 
print $query->header('application/json; charset="utf-8"');

#
# if($acao eq "get"){
    # total espaco em disco
    # select valor as total, cfg_default as default, (select sum(tamanho::int) from arquivo where empresa = $USER->{empresa}) as used from parceiro_cfg_full where cfg_id = 'disk-space' and empresa = $USER->{empresa}
    my $DB = &DBE("
        select 
        	custom as total, 
        	\"default\"
        from 
        	coworkit_plan_view
        where 
                (
                coworkit_plan = $USER->{plano} and
				coworkit_plan_feature = 1 and
				empresa = $USER->{empresa}
				)
			or 
				(  
                coworkit_plan = $USER->{plano} and
				coworkit_plan_feature = 1 and 
				empresa is null 
				)
        order by custom asc
        limit 1
    ");
    
    # total usado
    my $DBT = &DBE("select sum(tamanho::int) as used from arquivo where empresa = $USER->{empresa}");
    
    #if($DB->rows() == 0) {
    #    $DB = &DBE("select \"default\"::int as default, (select sum(tamanho::int) from arquivo where empresa = $USER->{empresa}) as used from cfg where internal_descrp = 'disk-space'");
    #}
        
    my $R  = $DB->fetchrow_hashref;
    my $RT = $DBT->fetchrow_hashref;
    
    if(!$R->{total}) {
        $R->{total} = $R->{default};
    }
    
    if(!$RT->{used}) {
        $RT->{used} = 0;
    }
    
    print "
        {
            \"total\" : $R->{total},
            \"used\"  : $RT->{used}
        }
    ";
# }

