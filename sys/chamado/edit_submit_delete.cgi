#!/usr/bin/perl

$nacess = "10";
require "../cfg/init.pl";

# get vars
$ID = &get('ID');
$COD = &get('COD');

# atualiza tabela chamado para que item seja arquivado / motivo
# $DB = &DBE("update chamado set cancelado = true where codigo = $COD ");


print $query->header({charset=>utf8});

# debug();
exit;

print<<HTML;

<script language='JavaScript'>
	formularioReset();
</script>

HTML
