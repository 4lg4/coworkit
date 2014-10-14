#!/usr/bin/perl

$nacess = "207";
require "../cfg/init.pl";

$codigo = &get('codigo');

print $query->header({charset=>utf8});


if($codigo ne "")
	{
	# Atualiza o registro
	$DB = &DBE("delete from procedimentos where codigo='$codigo'");
	
	if($DB > 0)
		{
		print "	<script>
				unLoadingObj('detalhe_proced');
				DMessages('Procedimento excluido com sucesso!');
				\$('#codigo').val('');
				call('procede/start.cgi', 1);
			</script>";
		}
	else
		{
		print "<script> alerta('Procedimento não encontrato no banco!');</script>"
		}
	}
else
	{
	print "	<script>
			unLoadingObj('detalhe_proced');
			DMessages('Você não informou o código do procedimento!');
		</script>";
	}
