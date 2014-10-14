#!/usr/bin/perl

# [INI] -------------------------------------------------------------------------------------------------------------------
#	 Atualiza cadastro Empresa
# -------------------------------------------------------------------------------------------------------------------------
$DB = DBE("update empresa set ativo='$ativo', tipo='$tipo_emp', nome='$nome', apelido='$apelido', obs='$obs' where codigo = $COD ");
# [END] Atualiza cadastro Empresa  ----------------------------------------------------------------------------------------


# [INI] -------------------------------------------------------------------------------------------------------------------
#	 Grupos, Grupos participantes
# -------------------------------------------------------------------------------------------------------------------------
if(@grupos_participantes > 0)
	{
	# remove todos relacionamentos
	$DB = DBE("delete from empresa_relacionamento where empresa = $COD");

	# gera inserts
	for($f=0; $f<@grupos_participantes; $f++)
		{
		$SQL_grupos .= "($COD,".$grupos_participantes[$f]."),";
		}
	
	# insere relacionamentos atualizados
	$DB = DBE("insert into empresa_relacionamento (empresa, relacionamento) values ".substr($SQL_grupos, 0,-1));
	}
# [END] Grupos, Grupos participantes  -------------------------------------------------------------------------------------


# [INI] -------------------------------------------------------------------------------------------------------------------
#	 Tecnicos, tecnicos relacionados
# -------------------------------------------------------------------------------------------------------------------------
if(@tecnicos_participantes > 0)
	{
	# remove todos relacionamentos
	$DB = DBE("delete from empresa_tecnico where empresa = $COD");

	# gera inserts
	for($f=0; $f<@tecnicos_participantes; $f++)
		{
		$SQL_tecnicos .= "($COD,".$tecnicos_participantes[$f]."),";
		}
	
	# insere relacionamentos atualizados
	$DB = DBE("insert into empresa_tecnico (empresa, usuario) values ".substr($SQL_tecnicos, 0,-1));
	}
# [END] Tecnicos, tecnicos relacionados  ----------------------------------------------------------------------------------


# [INI] -------------------------------------------------------------------------------------------------------------------
#	 Planos, Planos relacionados
# -------------------------------------------------------------------------------------------------------------------------
#if(@planos_participantes > 0)
#	{
	# remove todos relacionamentos
#	$DB = DBE("delete from empresa_prod_servicos where empresa = $COD");
	
	# gera inserts
#	for($f=0; $f<@planos_participantes; $f++)
#		{
#		$SQL_planos .= "($COD,".$planos_participantes[$f]."),";
#		}
	
	# insere relacionamentos atualizados
#	$DB = DBE("insert into empresa_prod_servicos (empresa, prod_servicos) values ".substr($SQL_planos, 0,-1));
#	}
# [END] Planos, planos relacionados  --------------------------------------------------------------------------------------


# [INI] -------------------------------------------------------------------------------------------------------------------
#	 Documetos, Documentos extras se for pessoa fisica ou juridica
# -------------------------------------------------------------------------------------------------------------------------
$DOC = DBE("delete from empresa_doc where empresa = $COD");
for($f=0; $f<@doc; $f++)
	{
	if($doc[$f] ne "")
		{
		$DOC = DBE("insert into empresa_doc (empresa, doc, descrp) values ($COD, '$tdoc[$f]', '$doc[$f]') ");
		}
	}
# [END] Documetos, Documentos extras se for pessoa fisica ou juridica  ----------------------------------------------------


# [INI] -------------------------------------------------------------------------------------------------------------------
#	 Bancos, dados bancarios
# -------------------------------------------------------------------------------------------------------------------------
if(@banco_codigo_ > 0)
	{
	# remove todos relacionamentos
	$DB = DBE("delete from empresa_banco where empresa = $COD");

	# gera inserts
	for($f=0; $f<@banco_codigo_; $f++)
		{
		$SQL_bancos .= "($COD,".$banco_codigo_[$f].",'".$banco_agencia_[$f]."','".$banco_conta_[$f]."','".$banco_obs_[$f]."'),";
		}

	# insere relacionamentos atualizados
	$DB = DBE("insert into empresa_banco (empresa, banco, agencia, conta, obs) values ".substr($SQL_bancos, 0,-1));
	}
# [END] Bancos, dados bancarios -------------------------------------------------------------------------------------------


# [INI] -------------------------------------------------------------------------------------------------------------------
#	 Enderecos
# -------------------------------------------------------------------------------------------------------------------------
# exclui enderecos
$SQL_enderecos = "delete from empresa_endereco where empresa = '$COD' ";
for($f=0; $f<@endereco_codigo; $f++) 
	{
	if($endereco_codigo[$f] !~ /^n/)
		{
		$SQL_enderecos .= " and codigo <> '$endereco_codigo[$f]' ";
		}
	}
	$DB = DBE($SQL_enderecos);

# Atualiza / insere registros
for($f=0; $f<@endereco_codigo; $f++) 
	{
	if($endereco_codigo[$f] =~ /^n/)
		{
		$DB = DBE("insert into empresa_endereco (tipo, empresa, endereco, complemento, bairro, cidade, uf, pais, cep) values ('$endereco_tipo[$f]', '$COD', '$endereco[$f]', '$endereco_complemento[$f]', '$endereco_bairro[$f]', '$endereco_cidade[$f]', '$endereco_uf[$f]', '$endereco_pais[$f]', '$endereco_cep[$f]') ");
		
		# recupera ultimo codigo inserido
		$DB = DBE("select currval('empresa_endereco_codigo_seq')");
		$r = $DB->fetch;
		$COD_END = @$r[0];
		}
	else
		{
		$DB = DBE("update empresa_endereco set tipo = '$endereco_tipo[$f]', empresa = '$COD', endereco = '$endereco[$f]', complemento = '$endereco_complemento[$f]', bairro = '$endereco_bairro[$f]', cidade = '$endereco_cidade[$f]', uf = '$endereco_uf[$f]', pais = '$endereco_pais[$f]', cep = '$endereco_cep[$f]' where codigo = '$endereco_codigo[$f]' ");
		$COD_END = $endereco_codigo[$f];
		
		#
		# remove todos contatos da tabela de compatibilidade
		# remover este codigo apos toda tabela de compatibilidade for excluida
		&DBE("delete from endereco_contato where endereco = $endereco_codigo[$f]");
		#
		
		# remove todos os contatos da tabela para inserir novamente
		&DBE("delete from contato_endereco where empresa_endereco = $endereco_codigo[$f]");
		
		# remove todos os dados do contato
		# ver pois quando nao puder mais remover todos os contatos essa logica deve 
		# testar quais devem ser removidos e quais devem ser atualizados
		$DB = DBE("delete from contato_dados where empresa_endereco = $endereco_codigo[$f]");
		}
	
    
	# contatos
	for($g=0; $g<=$#{$cid[$f]}; $g++)
		{			
		# titulo do contato
		$contato_descrp = &get("contatos_".$endereco_codigo[$f]."_".$cid[$f][$g]."_descrp");	
		# print $cid[$f][$g]." - [$contato_descrp] <br>";

		# controla se nao for novo gera sql para delecao
		#if($cid[$f][$g] !~ /^n/)
		#	{
		#	$SQL_DEL_contato_dados .= " and codigo <> '$endereco_codigo[$f]' ";
		#	}
        
        
        # contato principal
        $principal = &get("contatos_".$endereco_codigo[$f]."_".$cid[$f][$g]."_principal");        
        
		# insere contato pai
		$DB = DBE("
            insert into 
                contato_endereco (
                    empresa_endereco, 
                    descrp,
                    \"default\"
                ) values (
                    $COD_END, 
                    '$contato_descrp',
                    $principal
                )
        ");
        
        
        $deb .= "insert into contato_endereco (empresa_endereco, descrp,\\\"default\\\") values ($COD_END, '$contato_descrp',$principal)";
		
		# recupera codigo inserido
		$DB  = DBE("select currval('contato_endereco_codigo_seq') ");
		$CCO = $DB->fetch;
		$CCO = @$CCO[0];

		# dados tipos
		@contato_tipos = &get_array("contatos_".$endereco_codigo[$f]."_".$cid[$f][$g]."_tipo");

		# dados valores
		@contato_valores = &get_array("contatos_".$endereco_codigo[$f]."_".$cid[$f][$g]."_valor");

		# ajusta contatos dados para salvar
		$contato_dados = "";
		for($h=0; $h<@contato_tipos; $h++)
			{
			print $contato_tipos[$h]." - ".$contato_valores[$h]."<br>";
			$contato_dados .= "($contato_tipos[$h],'$contato_valores[$h]',$CCO, $COD_END),";
			}
		$contato_dados = substr($contato_dados, 0,-1); # remove ultima virgula
		
		# insere contato dados
		$DB = DBE("insert into contato_dados (tipo, valor, contato_endereco, empresa_endereco) values ".$contato_dados);
		# print "insert into contato_dados (tipo, valor, contato_endereco, empresa_endereco) values ".$contato_dados;
		
		# print "<hr>";
		}
		
	# deleta vinculos
 	# &DBE("delete from contato_endereco where empresa = '$COD' ");
	# exit;
	
	# remove campo endereco particularidades
	$END = DBE("delete from endereco_particularidades where endereco = $COD_END");
	
	# adiciona campo endereco particularidades
	$END = DBE("insert into endereco_particularidades (endereco, descrp) values ($COD_END, '$endereco_problemas[$f]') ");
	}
# [END] Enderecos ---------------------------------------------------------------------------------------------------------

# finaliza SQLs
$dbh->commit;

print<<HTML;
<script>
	DMessages('Empresa [$nome] atualizada com sucesso !!');
	call("/sys/empresa/edit.cgi",{COD:$COD,MODO:'editar'});
</script>
HTML

exit;
