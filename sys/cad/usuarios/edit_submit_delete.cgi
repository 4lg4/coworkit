#!/usr/bin/perl

$nacess = "203' and usuario_menu.direito = 'a";
require "../../cfg/init.pl";

# Dados principais
$ousuario = &get('COD');
$login = lc(&get('login'));


if($ousuario eq "" || $login eq "")
	{
	print $query->header({charset=>utf8});
print<<HTML;
<script language='JavaScript'>
	alerta("Requisição inválida!");
</script>
HTML
	exit;
	}

print $query->header({charset=>utf8});
$dbh->begin_work;

#Deleta os direitos do usuário
$rv = &DBE("delete from usuario_menu where usuario='$ousuario'");

#Deleta o usuário
$rv = &DBE("delete from usuario where usuario='$ousuario' and login='$login' ");

if($rv)
	{
	$dbh->commit;
	print "<script language='JavaScript'> 
		DMessages('$login excluído com sucesso', 'Exclusão de usuário');
		callGrid('usuario');
		</script>"
	}
	

