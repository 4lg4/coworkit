#!/usr/bin/perl

$nacess = "301";
require "../../cfg/init.pl";
$tipo_codigo = &get('COD');
$MODO = &get('MODO');


print $query->header({charset=>utf8});

#Deleta o tipo usuario
$tipo_usuario = &DBE("delete from usuario_tipo where codigo='$tipo_codigo'");

#Deleta direitos do tipo usuario
$direitos = &DBE("delete from menu_default_direitos where usuario_tipo='$tipo_codigo'");

print "<script> 
	
	alerta('Tipo Usuário excluído com sucesso! ');
	callGrid('tipo_usuario');
	</script>"
