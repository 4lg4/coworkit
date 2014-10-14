#!/usr/bin/perl

use Captcha::reCAPTCHA;
require "../cfg/init.pl";
require "../cfg/DPAC/DSendmail.pl";

my $c = Captcha::reCAPTCHA->new;

# vars
$username = &get('username');
$password = &get('password');
$nome     = &get('nome');
$plan     = &get('plan');

$company_nome      = &get('company_nome');
$company_apelido   = &get('company_apelido');
$company_tipo      = &get('company_tipo');
$company_documento = &get('company_documento');

$fb_login = &get('fb_email');
$fb_id    = &get('fb_id');
$fb_link  = &get('fb_link');

# valida captcha 
$challenge = &get('recaptcha_challenge_field');
$response  = &get('recaptcha_response_field');

# ajuste plano
# se nao tiver plano selecionado seta como freemium
if(!$plan) {
    $plan = "2";
}

print $query->header('application/json; charset="utf-8"');

# se nao for desenvolvimento
if(!$DEV) {
    my $result = $c->check_answer(
        "6Lf4xOoSAAAAAD_6nna1vzSr33EBh79NvbDdfPyq", $ENV{'REMOTE_ADDR'},
        $challenge, $response
    );

    if(!$result->{is_valid}) {
        $R  = '{';
        $R .= '     "status"  : "error",';
        $R .= '     "message" : "frase de segurança inválida",';
        $R .= '     "field"   : "recaptcha_response_field"';
        $R .= '}';
        print $R;
        exit;
    } 
}


# verifica se ja existe usuario
$DB = DBE("
    select 
        usuario
    from
        usuario
    where
        login like '$username'
");
if($DB->rows > 0) {
    $R  = '{';
    $R .= '     "status"  : "error",';
    $R .= '     "message" : "email já cadastrado",';
    $R .= '     "field"   : "username"';
    $R .= '}';    
    print $R;
    
    exit;
    
}

# verifica se ja existe rede social
# 2 = facebook
if($fb_login && $fb_id) {
    $DB = DBE("
        select 
            login
        from
            usuario_login
        where
            (
                login like '$fb_login' or
                id like '$fb_id' 
            ) and 
                rede = 2
    ");
    if($DB->rows > 0) {
        $R  = '{';
        $R .= '     "status"  : "error",';
        $R .= '     "message" : "email facebook já cadastrado ",';
        $R .= '     "field"   : "username"';
        $R .= '}';    
        print $R;
    
        exit;
    
    }
}


#
# Novo usuario
#

# inicia transacao
$dbh->begin_work;

# insere parceiro
$parceiro = DBE("
    insert into
        empresa (
            nome,
            apelido,
            tipo
        ) values (
            '$company_nome',
            '$company_apelido',
            '$company_tipo'
        )
"); 

# insere empresa
$empresa = DBE("
    insert into
        empresa (
            nome,
            apelido,
            tipo
        ) values (
            '$company_nome',
            '$company_apelido',
            '$company_tipo'
        )
");    

# insere vinculo 
DBE("
    insert into
        parceiro_cadastro (
            parceiro,
            empresa
        ) values (
            $parceiro,
            $empresa
        )
"); 

DBE("
    insert into
        parceiro_empresa (
            parceiro,
            empresa
        ) values (
            $parceiro,
            $empresa
        )
");  

# insere usuario
$usuario = DBE("
    insert into
        usuario (
            login,
            senha,
            nome,
            email,
            empresa
        ) values (
            '$username',
            password('$password'),
            '$nome',
            '$email',
            $parceiro
        )
");    

# plano
# insere vinculo 
DBE("
    insert into
        parceiro_plan (
            parceiro,
            coworkit_plan
        ) values (
            $parceiro,
            $plan
        )
"); 

# insere menus
# plano = 1 (freemium)
$DB = DBE("
    select 
        * 
    from
        menu_plano
    where
        plano = 1
");
while($m = $DB->fetchrow_hashref) {
    $mlist .= "($usuario,$m->{menu},'$m->{direito}'),";
}
$mlist = substr($mlist, 0,-1); # remove ultima virgula

# sql exec
DBE("
    insert into
        usuario_menu (
            usuario,
            menu,
            direito
        ) values 
            $mlist
");    


# insere logins
# 2 = facebook
if($fb_login && $fb_id) {
    DBE("
        insert into
            usuario_login (
                usuario,
                rede,
                login,
                id,
                link
            ) values (
                $usuario,
                2,
                '$fb_login',
                '$fb_id',
                '$fb_link'
            )   
    ");  
}

# tipos de endereco
$DB = DBE("
    select 
        * 
    from 
        tipo_endereco
    where 
        restrito is true and
        parceiro = 1
");

while($te = $DB->fetchrow_hashref) {
    if($te->{obrigatorio} == 0){
        $te->{obrigatorio} = "false";
    } else {
        $te->{obrigatorio} = "true";
    }
    $telist .= "('$te->{descrp}',$te->{obrigatorio},true,$te->{codigo},$parceiro),";
}
$telist = substr($telist, 0,-1); # remove ultima virgula

# sql exec
DBE("
    insert into
        tipo_endereco (
            descrp,
            obrigatorio,
            restrito,
            pai,
            parceiro
        ) values 
            $telist
"); 

# tipo contatos
$DB = DBE("
    select 
        * 
    from 
        tipo_contato
    where 
        restrito is true and 
        parceiro = 1
");

while($tc = $DB->fetchrow_hashref) {
    $tclist .= "('$tc->{descrp}',$parceiro,$tc->{codigo},true),";
}
$tclist = substr($tclist, 0,-1); # remove ultima virgula

# sql exec
DBE("
    insert into
        tipo_contato (
            descrp,
            parceiro,
            pai,
            restrito
        ) values 
            $tclist
"); 


# grupos empresas /tipo relacionamentos
$DB = DBE("
    select 
        * 
    from 
        tipo_relacionamento
    where 
        restrito is true and 
        parceiro = 1
");

while($r = $DB->fetchrow_hashref) {
    $rlist .= "('$r->{descrp}',$parceiro,$r->{codigo},true),";
}
$rlist = substr($rlist, 0,-1); # remove ultima virgula

# sql exec
DBE("
    insert into
        tipo_relacionamento (
            descrp,
            parceiro,
            pai,
            restrito
        ) values 
            $rlist
"); 



# planos
$DB = DBE("
    select 
        * 
    from 
        prod_servicos
    where 
        restrito is true and
        parceiro = 1
");

while($p = $DB->fetchrow_hashref) {
    $plist .= "('$p->{descrp}',1,$p->{empresa_area_tipo},true,$p->{codigo},$parceiro),";
}
$plist = substr($plist, 0,-1); # remove ultima virgula

# sql exec
DBE("
    insert into
        prod_servicos (
            descrp,
            cobranca,
            empresa_area_tipo,
            restrito,
            pai,
            parceiro
        ) values 
            $plist
"); 



# tipo documentos
$DB = DBE("
    select 
        * 
    from 
        tipo_doc
    where 
        restrito is true and 
        parceiro = 1
");

while($td = $DB->fetchrow_hashref) {
    $tdlist .= "('$td->{descrp}','$td->{minidescrp}',$parceiro,$td->{codigo},true,'$td->{empresa_tipo}'),";
}
$tdlist = substr($tdlist, 0,-1); # remove ultima virgula

# sql exec
DBE("
    insert into
        tipo_doc (
            descrp,
            minidescrp,
            parceiro,
            pai,
            restrito,
            empresa_tipo
        ) values 
            $tdlist
"); 



##################################
#
#   dados de ti
#
##################################


#
#   Agrupos + grupos template
#

# seleciona agrupamentos + grupos a serem exportados
$DB = DBE("
        select 
            a.codigo as agrupo,
			a.descrp as agrupo_descrp,
			g.codigo as grupo,
			g.descrp as grupo_descrp
			
        from
            agrupo_grupo as ag
		join
			grupo as g on g.codigo = ag.grupo
		join
			agrupo as a on a.codigo = ag.agrupo
	    where 
            a.parceiro = 1 and
			a.exportar is true
");

while($ag = $DB->fetchrow_hashref) {
    # insere agrupo
    if($agrupo_controle ne $ag->{agrupo}){
        $agrupo_new = DBE("
            insert into
                agrupo (
                    descrp,
                    parceiro,
                    exportar,
                    pai
                ) values (
                    '$ag->{agrupo_descrp}',
                    $parceiro, 
                    true, 
                    $ag->{agrupo}
                )
        ");
        
        # insere vinculo parceiro agrupo (tosco)
        DBE("
            insert into
                parceiro_agrupo (
                    parceiro,
                    agrupo
                ) values (
                    $parceiro, 
                    $agrupo_new
                )
        ");
        
        # inicia sequencia de agrupo_grupo
        $agrupo_grupo_seq = 1;
    } 
        
        # insere grupos padroes
        $grupo_new = DBE("
            insert into
                grupo (
                    descrp,
                    parceiro,
                    exportar,
                    pai
                ) values (
                    '$ag->{grupo_descrp}',
                    $parceiro, 
                    true,
                    $ag->{grupo}
                )
        "); 
        
        # insere vinculo parceiro grupo (tosco)
        DBE("
            insert into
                parceiro_grupo (
                    parceiro,
                    grupo
                ) values (
                    $parceiro, 
                    $grupo_new
                )
        ");
        
        # insere vinculo agrupo + grupo
        DBE("
            insert into
                agrupo_grupo (
                    agrupo,
                    grupo,
                    seq
                ) values (
                    $agrupo_new,
                    $grupo_new,
                    $agrupo_grupo_seq
                )
        ");
        
        $agrupo_grupo_seq += 1;
        
        
        #
        #   Atributos (grupo itens)
        #       insere itens (atributos)
        $tgi_controle_final = 0;
        if($grupo_controle ne $ag->{grupo}){
            
            
            $DBI = DBE("
                    select 
                        gi.tipo,
                        gi.seq, 
                        tgi.descrp, 
                        tgi.supervisor
		            from                        
                        grupo_item as gi
                    join
                        grupo as g on g.codigo = gi.grupo
                    join
                        tipo_grupo_item as tgi on tgi.codigo = gi.tipo
                    where 
                        g.parceiro = 1 and
                        g.exportar is true and
                        g.codigo = $ag->{grupo}
            ");
             
            while($gi = $DBI->fetchrow_hashref) { 
                
               
                #
                #   Tipo Grupo Item
                #       insere tipo grupo item se ja nao cadastrado
                # 
                $DBPGI = DBE("
                        select
                            tgi.codigo
                        from
                            parceiro_tipo_grupo_item as ptgi
                		join
                			tipo_grupo_item as tgi on tgi.codigo = ptgi.tipo_grupo_item
                        where
                            ptgi.parceiro = $parceiro and
                            tgi.descrp like '$gi->{descrp}'
                ");
                
                if($DBPGI->rows > 0) {
                    $tgi_controle = $DBPGI->fetchrow_hashref;
                    $tgi_new = $tgi_controle->{codigo};
                } else {
                    
                    # ajusta supervisor
                    if($gi->{supervisor} == 0){
                        $gi->{supervisor} = "false";
                    } else {
                        $gi->{supervisor} = "true";
                    }
                
                    #
                    #   Tipo Grupo Item
                    #       insere tipo grupo item
                    $tgi_new = DBE("
                        insert into
                            tipo_grupo_item (
                                descrp,
                                supervisor
                            ) values (
                                '$gi->{descrp}',
                                $gi->{supervisor}
                            )
                    "); 
                    
                    # insere vinculo parceiro tipo grupo item
                    DBE("
                        insert into
                            parceiro_tipo_grupo_item (
                                parceiro,
                                tipo_grupo_item
                            ) values (
                                $parceiro,
                                $tgi_new
                            )
                    ");
                } 
                
                
                
                #
                #   Grupo Item
                #       insere grupo item
                $gi_new = DBE("
                    insert into
                        grupo_item (
                            grupo,
                            tipo,
                            seq
                        ) values (
                            $grupo_new,
                            $tgi_new,
                            $gi->{seq}
                        )
                "); 
                
                
                # insere vinculo parceiro grupo item
                # DBE("
                #     insert into
                #         parceiro_grupo_item (
                #             parceiro,
                #             grupo_item
                #         ) values (
                #             $parceiro,
                #             $gi_new
                #         )
                # ");
                
                
            }
        } 
        # atualiza controle
        $grupo_controle = $ag->{grupo};
        
        
    # atualiza controle
    $agrupo_controle = $ag->{agrupo};
}


# Envia e-mail
sendmail($username, "Bem Vindo ao CoworkIT!", "<hr><a href='https://coworkit.done.com.br'>Faça seu Login</a> <br> usuario: $username</hr>");

$dbh->commit; 

# tudo OK 
$R  = '{';
$R .= '     "status" : "success"';
$R .= '}';
print $R;
