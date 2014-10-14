#!/usr/bin/perl

$nacess = "301' and usuario_menu.direito = 'a";
require "../../cfg/init.pl";
$tipo_codigo = &get('COD');
$MODO = &get('MODO');
$radios=&get('radios');
$tipo_descrp=&get('tipo_descrp');

print $query->header({charset=>utf8});

#Verifica se o tipo encontra-se no banco
$tipo_usuario = &DBE("select * from usuario_tipo where codigo='$tipo_codigo'");

if($tipo_usuario->rows()==1)
	{
	$codigo=$tipo_usuario->fetch;
	
	# Atualiza a descrição do tipo usuario
	$update_tipo_descrp = &DBE("update usuario_tipo set descrp='".ucfirstall($tipo_descrp)."' where codigo='@$codigo[0]'  ");

	#Faz um for para pegar o valor selecionado de todos os radios
	for(my $i=1; $i<=$radios; $i++)
		{
		$radio[$i]=&get("radio".$i."_radios");
		$menu[$i]=&get("menu_".$i);
# 		print "update menu_default_direitos set tipo='$radio[$i]' where usuario_tipo='@$codigo[0]' and menu='$menu[$i]'";
		#printf "<script> alert('$radio[$i]'); </script>";
		#print @$codigo[0];			
		if($menu[$i] ne "")
			{
			#Se o usuario marcar sem acesso exclui o registro se tiver no banco.
			if($radio[$i] eq "0" || $radio[$i] eq "")
				{
				#Retirar permissão de acesso (sem acesso)
				$tipo_usuario = &DBE("delete from menu_default_direitos where menu='$menu[$i]' and usuario_tipo='@$codigo[0]'");
				#print "Deletou";
				}
			else
				{
				$existencia = &DBE("select * from menu_default_direitos where menu='$menu[$i]' and usuario_tipo='@$codigo[0]'");
				
				#Verifica se existe registro no banco, então atualiza
				if($existencia->rows()>0)
					{
					# Atualiza a permissao
					$tipo_usuario = &DBE("update menu_default_direitos set tipo='$radio[$i]' where usuario_tipo='@$codigo[0]' and menu='$menu[$i]'");	
					#print "Atualizou";
					}
				#Se não existir registro no banco ele insere.
				else
					{
					# Insere a permissao
					$tipo_usuario = &DBE("insert into menu_default_direitos (menu,tipo,usuario_tipo) values ('$menu[$i]','$radio[$i]','@$codigo[0]')");
					#print "Inseriu";
					}
				}
			
			}
			
			
			print "	<script> 
					alerta('Tipo de usuário atualizado com sucesso');
				</script>";
		
		}
	}
else
	{
	print "<script> alerta('Tipo não existe no banco!');</script>"
	}