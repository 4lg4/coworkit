#!/usr/bin/perl
require "../init.pl";

#
#   Plano do parceiro
#       parceiro_plan.cgi
#

# pega variaveis
$ID   = &get("ID");    # ID do usuario logado

# header 
print $query->header('application/json; charset="utf-8"');

# db select
my $DB = &DBE("
    select 
        cp.descrp as descrp
    from
        parceiro_plan as pp
    left join
        coworkit_plan as cp on
            cp.codigo = pp.coworkit_plan
    where
        pp.empresa = $USER->{empresa}
");

# adjust vars
# if($DB->rows() > 0) {}
my $R = $DB->fetchrow_hashref;

# return        
print '
    {
        "plan" : "'.$R->{descrp}.'"
    }
';


