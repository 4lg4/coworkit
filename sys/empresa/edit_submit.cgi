#!/usr/bin/perl

$nacess = "201";
require "../cfg/init.pl";

$ID = &get('ID');


print $query->header({charset=>utf8});

#debug();
#exit;


	
# exit;

# codigo empresa
$COD = &get('COD');

# Dados principais
$tipo_emp = &get('tipo_emp');
$cod_emp  = &get('COD');
$nome     = &get('nome');
$apelido  = &get('apelido');
$obs      = &get('obs');
$ativo    = &get('ativo');
if($ativo ne "true") {
	$ativo = "false";
}

@grupos_existentes = &get_array('grupos_existentes');

# Dados bancarios
@banco_codigo_	= &get_array('banco_codigo_');
@banco_agencia_	= &get_array('banco_agencia_');
@banco_conta_	= &get_array('banco_conta_');
@banco_obs_ 	= &get_array('banco_obs_');

# Dados dos grupos
@grupo_list_cod = &get_array('grupo_list_cod');
@grupo_list_descrp = &get_array('grupo_list_descrp');
	
# Dados de documentos (CPF / CNPJ)
@tdoc = &get_array('tdoc');
@tdoc_descrp = &get_array('tdoc_descrp');
@doc = &get_array('doc');

# Dados do endereço
@endereco_codigo = &get_array('endereco_codigo');
@endereco_tipo 	= &get_array('endereco_tipo');
@endereco = &get_array('endereco');
@endereco_complemento = &get_array('complemento');
@endereco_bairro = &get_array('bairro');
@endereco_cep = &get_array('cep');
@endereco_cidade = &get_array('cidade');
@endereco_uf = &get_array('uf');
@endereco_pais = &get_array('pais');
@endereco_problemas = &get_array('problemas');

# Contatos dados
for($f=0; $f<@endereco_codigo; $f++)
	{
	# id de todos os contatos
	push @cid, [ &get_array("contatos_".$endereco_codigo[$f]."_id") ];
	}

@grupos_participantes = &get_array('grupos_participantes');
@grupos_existentes = &get_array('grupos_existentes');

@tecnicos_participantes = &get_array('tecnicos_participantes');
@tecnicos_existentes = &get_array('tecnicos_existentes');

@planos_participantes = &get_array('planos_participantes');
@planos_existentes = &get_array('planos_existentes');


#Dados extras
@cmp_extra_nome = ();
@cmp_extra_vlr = ();
$n=0;
$sth9 = &select("select * from pg_tables where tablename='empresa_extra'");
$sth = &select("select column_name from information_schema.columns where table_name = 'empresa_extra' and column_name not like 'codigo' and column_name not like 'empresa' order by ordinal_position");
while($row = $sth->fetch)
	{
	$cmp_extra_nome[$n] = @$row[0];
	$cmp_extra_vlr[$n] = &get($cmp_extra_nome[$n]);
	$n++;
	}

# Service Desk
$tkt_login    = &get('tkt_login');
$tkt_login_confirm = &get('tkt_login_confirm');
$tkt_password = &get('tkt_password');
$tkt_open     = &get('tkt_open');
$tkt_usuario  = &get('tkt_usuario');


# [INI] ----------------------------------------------------------------------------------------------------
#	 Empresa, verifica se nao existe outro documento cadastrado e nao deixa duplicar
# ----------------------------------------------------------------------------------------------------------
for($f=0; $f<@doc; $f++)
	{
	$doca = $doc[$f];
	$doct = $doc[$f];
	$doct =~ s/\.|\-|\/|\ //g;

	if($doc[$f] ne "" && isNumber($doct) eq true)
		{
		$docs_test_alert .= "&nbsp;&nbsp;".$tdoc_descrp[$f]." - ".$doca."<br>";
		$docs_test .= " regexp_replace(ed.descrp, '[ |.|/|-]', '', 'g') = '$doct' or ";
		}
	}
	
# se nao for documentos para testar
if($docs_test ne "")
	{
	$docs_test = " and ( ".substr($docs_test, 0,-3)." )";
	
	# ajusta sql se for Incluir
	if($COD ne "")
		{
		$DB = DBE("select ed.descrp as doc, ed.empresa as empresa, e.nome, pe.parceiro from tipo_doc as td left join empresa_doc as ed on td.codigo = ed.doc left join empresa as e on e.codigo = ed.empresa left join parceiro_empresa as pe on pe.empresa = ed.empresa where ed.empresa <> $COD and pe.parceiro = $USER->{empresa} $docs_test");
		}
	else # ajusta sql se for Edicao
		{
		$DB = DBE("select ed.descrp as doc, ed.empresa as empresa, e.nome, pe.parceiro from tipo_doc as td left join empresa_doc as ed on td.codigo = ed.doc left join empresa as e on e.codigo = ed.empresa left join parceiro_empresa as pe on pe.empresa = ed.empresa where pe.parceiro = $USER->{empresa} $docs_test");
		}
	
	# se ja existir algum documento
	if($DB->rows() > 0)
		{
		while($EMP = $DB->fetchrow_hashref)
			{
			if($t ne $EMP->{nome})
				{
				$docs_test_alert_emp .= $EMP->{nome}."<br>";
				}
			$t = $EMP->{nome};
			}
		
		alerta("Documento(s) Já Cadastrado(s) <br><br> ".$docs_test_alert_emp."<hr>".$docs_test_alert);
		exit;
		}
	}
# [END] Empresa, verifica se nao existe outro documento cadastrado e nao deixa duplicar --------------------



# inicia SQls execs
$dbh->begin_work;

#
#   service desk
#       controle se empresa pode abrir chamados
#       usei como controle o campo tipo do usuario (tipo = 99 {cliente do parceiro})
#
if(!$tkt_usuario && $tkt_login && $tkt_password) { # novo
    
    # verifica se ja existe usuario
    $DB = DBE("
        select 
            usuario
        from
            usuario
        where
            login like '$tkt_login'
    ");
    if($DB->rows > 0) {
        new DDialog("login para cliente já em uso","error",true);
        exit;
    }
    
    # insere usuario
    $tkt_usuario = DBE("
        insert into
            usuario (
                login,
                senha,
                nome,
                email,
                empresa,
                bloqueado,
                tipo
            ) values (
                '$tkt_login',
                password('$tkt_password'),
                '$nome',
                '$tkt_login',
                $COD,
                $tkt_open,
                99
            )
    ");
    
    
    # insere menus
    # plano = 2 (cliente do cliente)
    $DB = DBE("
        select 
            * 
        from
            menu_plano
        where
            plano = 2
    ");
    while($m = $DB->fetchrow_hashref) {
        $mlist .= "($tkt_usuario,$m->{menu},'$m->{direito}'),";
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
    
# update
} elsif($tkt_usuario && $tkt_login && $tkt_password) { 
    
    # se login alterado
    if($tkt_login ne $tkt_login_confirm) {
        $DB = DBE("
            select 
                usuario
            from
                usuario
            where
                login like '$tkt_login'
        ");
        if($DB->rows > 0) {
            new DDialog("login para cliente já em uso","error",true);
            exit;
        }
    }
    
    
    
    if($tkt_password ne "true") {
        $tkt_pwd_change = " , senha = password('$tkt_password') ";
    }
    
    # atualiza
    DBE("
        update 
            usuario
        set
            login = '$tkt_login',
            email = '$tkt_login',
            bloqueado = $tkt_open
            $tkt_pwd_change
        where
            usuario = $tkt_usuario
    ");
}


# chama script para concluir acao 
if($COD ne "")
	{
	require("./edit_submit_update.cgi");
	}
else
	{
	require("./edit_submit_insert.cgi");
	}

exit;
