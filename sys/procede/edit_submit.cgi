#!/usr/bin/perl

$nacess = "207";
require "../cfg/init.pl";

$codigo = &get('codigo_save');
$titulo = &get('titulo');
$descrp = &get('procedimento');
$empresa = &get('cliente');
$endereco = &get('cliente_endereco_radios');
@tags = &get_array('tags_list');

print $query->header({charset=>utf8});

if($endereco ne "")
	{
	$endereco="'".$endereco."'";
	}
else
	{
	$endereco="NULL";
	}
	
if($empresa ne "")
	{
	$empresa="'".$empresa."'";
	}
else
	{
	$empresa="NULL";
	}

# inicia bloco SQL onde irá voltar no caso de rollback
$dbh->begin_work;
if($codigo ne "")
	{
	# Atualiza o registro
	$DB = &DBE("update procedimentos set titulo='".$titulo."', descrp='".$descrp."', empresa=$empresa, endereco=$endereco where codigo=$codigo ");
	if($DB > 0)
		{
		$procede_codigo = $codigo;
		}
	else
		{
		print "<script> alerta('Procedimento não encontrato no banco!');</script>";
		}
	}
else
	{
	# Insere o registro
	$DB = &DBE("insert into procedimentos (titulo, descrp, empresa, endereco, parceiro) values ('$titulo', '$descrp', $empresa, $endereco, '".$USER->{'empresa'}."')");
	if($DB > 0)
		{
		$procede_codigo = $DB;
		}
	else
		{
		print "<script> alerta('Falha ao incluir o procedimento no banco de dados!');</script>";
		}
	}

# Limpa a lista de TAGs do procedimento
$DB = &DBE("delete from procedimentos_tags where procedimento='$procede_codigo' ");
for($fg=0; $fg<@tags; $fg++)	
	{
	# Verifica se a TAG já existe
	$DB2 = &DBE("select codigo from procedimentos_tags_tipo where descrp = '$tags[$fg]' ");
	if($DB2->rows() > 0)
		{
		$tag=$DB2->fetchrow_hashref;
		$tag_codigo=$tag->{codigo};
		if($tag_codigo eq "")
			{
			print "<script> alerta('Falha ao selecionar a TAG $tags[$fg] no banco de dados!');</script>";
			exit;
			}		
		}
	else
		{
		# cria a TAG
		$tag_codigo = &DBE("insert into procedimentos_tags_tipo (descrp) values ('$tags[$fg]') ");
		if($tag_codigo eq "")
			{
			print "<script> alert('Falha ao incluir a TAG $tags[$fg] no banco de dados!');</script>";
			exit;
			}
		}
		
	# insere a TAG no procedimento
	$DB = &DBE("insert into procedimentos_tags (procedimento, tag, ordem) values ('$procede_codigo', '$tag_codigo', '".($fg+1)."')");
	}
	
if($codigo ne "")
	{
	print "	<script>
			unLoadingObj('detalhe_proced');
			DMessages('Procedimento atualizado com sucesso!');
			procede.list();
			procede.view($procede_codigo);
		</script>";
	}
else
	{
	print "	<script>
			unLoadingObj('detalhe_proced');
			DMessages('Procedimento cadastrado com sucesso!');
			\$('#codigo').val('$procede_codigo');
			procede.list();
			procede.view($procede_codigo);
		</script>";
	}

	
# finaliza sequência de bloco SQL com sucesso
$dbh->commit;