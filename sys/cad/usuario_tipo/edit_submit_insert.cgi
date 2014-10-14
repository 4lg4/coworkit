#!/usr/bin/perl

$nacess = "301' and usuario_menu.direito = 'a";
require "../../cfg/init.pl";
$COD = &get('COD');
$MODO = &get('MODO');
$radios=&get('radios');
$tipo_descrp=&get('tipo_descrp');

print $query->header({charset=>utf8});

#Verifica se o tipo já existe
$tipo_descrp_sql = &DBE("select * from usuario_tipo where descrp ilike '$tipo_descrp'");

if($tipo_descrp_sql->rows()==0)
	{
	# Insert o tipo usuario
	$tipo_usuario = &DBE("insert into usuario_tipo (descrp) values ('".ucfirstall($tipo_descrp)."') ");

	#recupera o ultimo codigo cadastrado
	$codigo = &DBE("select currval('usuario_tipo_codigo_seq') ");

	#Se retornar ultima codigo inserido
	if($codigo->rows()>0)
		{
		$codigo = $codigo->fetch;
		#Faz um for para pegar o valor selecionado de todos os radios
		for(my $i=1; $i<=$radios; $i++)
			{
			
			$radio[$i]=&get("radio".$i."_radios");
			$menu[$i]=&get("menu_".$i);
			#printf "<script> alert('$radio[$i]'); </script>";
			#print @$codigo[0];
			if($menu[$i] ne "" && $radio[$i] ne "0" && $radio[$i] ne "")
				{
				# Insert o tipo usuario
				$tipo_usuario = &DBE("insert into menu_default_direitos (usuario_tipo,menu,tipo) values ('@$codigo[0]','$menu[$i]','$radio[$i]') ");
				}
			}
		}
	print "	<script> 
			alerta('Tipo de usuário cadastrado com sucesso');
		</script>";
	}
else
	{
	print "<script> alerta('Tipo já existe!');</script>"
	}