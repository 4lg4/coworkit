#!/usr/bin/perl
require "../init.pl";

#
#   User Limit
#       user_limit.cgi
#
#       quantidade de usuarios disponiveis
#

# pega variaveis
$ID   = &get("ID");    # ID do usuario logado
$acao = &get("acao");  # acao 

# header 
print $query->header('application/json; charset="utf-8"');

#
# if($acao eq "get"){
    # total espaco em disco
    my $DB = &DBE("select valor as total, cfg_default as default, (select count(usuario) from usuario where empresa = $USER->{empresa} and bloqueado is false) as used from parceiro_cfg_full where cfg_id = 'user-limit' and empresa = $USER->{empresa}");
    if($DB->rows() == 0) {
        $DB = &DBE("select \"default\"::int as default, (select count(usuario) from usuario where empresa = $USER->{empresa} and bloqueado is false) as used from cfg where internal_descrp = 'user-limit'");
    }    
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

