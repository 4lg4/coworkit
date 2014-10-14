#!/usr/bin/perl
 
$nacess = "201' and usuario_menu.direito = 'a";
require "../cfg/init.pl";

$COD = &get('COD');

print $query->header({charset=>utf8});

# executa exclusao da empresa
$DB = DBE("delete from empresa where codigo = $COD","","noerror");

# se erro empresa tem tabelas vinculadas e nao pode ser excluida
# if($DB->rows() < 1)
if($DB == false)
	{
	$DB = DBE("update empresa set ativo='false' where codigo = $COD ");
	
	print "<script>
				\$(\"#ativo\").prop(\"checked\", false);
				alerta('Empresa não pode ser excluida pois existem vinculos com outros registros ! <br><br> Empresa Inativada !');
			</script>";
	}
else
	{
	print "<script>
				var callafter = function(){ callGrid('empresas'); }; 
				alerta('Empresa Excluida com sucesso !',callafter);
			</script>";
	}

exit;

