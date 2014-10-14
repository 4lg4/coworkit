#!/usr/bin/perl

$nacess = "301";
require "../../cfg/init.pl";
$tipo = &get('COD');
$codusuario = &get('USUARIO');
$MODO = &get('MODO');

print $query->header({charset=>utf8});

#[INI] --------------- Se for edição ele pega a descrição/nome do tipo_usuario -------------------------------------------------------------------------------------
$descricao = "";
if($tipo!="" || $tipo ne "")
	{
	$DB_descrp = &DBE("select * from usuario_tipo where codigo='$tipo'");

		while($row_descrp = $DB_descrp->fetchrow_hashref)
			{
			$descricao = $row_descrp->{'descrp'};
			}
	}
	
#[FIM] --------------- Se for edição ele pega a descrição/nome do tipo_usuario -------------------------------------------------------------------------------------

#[INI] --------------- Pega os direitos padrões -------------------------------------------------------------------------------------

$DB_padroes = &DBE("select * from tipo_direito where codigo ilike 'v' or codigo ilike 'a' order by descrp");
$RS_padroes = $DB_padroes->rows();
$tipo_direito_list = "";
if($RS_padroes < 1)
	{
	$tipo_direito_list .= "Sem direitos cadastrados";
	}
else
	{
	$c = 0;
	while($row3 = $DB_padroes->fetchrow_hashref)
		{
		$tipo_cod[$c] = $row3->{'codigo'};
		$tipo_descr[$c] = $row3->{'descrp'};
		$c++;
		}
	}
	
#[FIM] --------------- Pega os direitos padrões -------------------------------------------------------------------------------------

#Menus com a coluna pai nula
$DB = &DBE("select * from menu where pai is null order by ordem");

#Se não existir menus com a coluna pai nula exibe mensagem
if($DB->rows()<1)
	{
	$modulos="	<div style='position: absolute; top: 50%; width: 100%;'>
				<center><span id='bemvindo_titulo'>Por favor contacte o administrador para solicitar seu acesso</span></center>
			</div>
		  ";
	}
#Popula montando os blocos com os módulos
else
	{
	#contador para as abas
	$i=0;
	#Inicia a variável com o bloco descrição do tipo
	$descrp=ucfirstall($descricao);
	
	$modulos = "<div id='abas'><ul>";

	#Faz um while para montar as abas
	while($row_title = $DB->fetchrow_hashref)
		{
			$modulos .="<li><a href='#t-$i'>$row_title->{'descrp'}</a></li>";
			$i++;
		}
	#Fecho o bloco das abas
	$modulos .="</ul>";
	
	#Faz o mesmo select para montar o blocos com os módulos
	$DB2 = &DBE("select * from menu where pai is null order by ordem");	
	
	#zera o contador para usar no blocos de módulos
	$i=0;
	
	#while que puxa as subclasses para montar os blocos
	while($row = $DB2->fetchrow_hashref)
		{		
		@menu = ("");
		for(my $g=0; $g<$ncol; $g++)
			{
			$menu[$g] .= "<div class='menu menu_".$row->{'codigo'}."'>";
			}
		$modulos .="<div id='t-$i' class='abas'>";

		$modulos .= &get_menu($row->{'codigo'});
		if($linha<5)
			{
			$linha=0;
			}
		for(my $g=0; $g<$ncol; $g++)
			{
			$menu[$g] .= "</div>";
			}

		$cell=0;

		for($f=0; $f<@menu; $f++)
			{
			$modulos .= $menu[$f];
			}
		$modulos .= "</div>"; #div com o conteúdo

		$i++;
		}
		
		#Finaliza o bloco de abas e limpar as quebras de linhas
		$modulos .= "</div>"; # fim da div abas
		$modulos =~ s/\r|\n/ /gm; 
		
		#Exibe o resultado e seta as configurações dos elementos
		print "<script>
				//Criar os bloco no html
				\$('#menu_container').html(\"$modulos\"); 
				\$('#tipo_descrp').val(\"$descrp\"); 
				
				// Cria as abas	
				\$('#abas').tabs();
				
				//Publica o total de radios criados
				\$('#RADIOS').val($i2);
				
			</script>";
			
		#Montas os DTouchRadios
		print $Dtouch;
		
		#Seleciona caso seja para edição.
		print "$selecionados";
	}

#[INI]-- SUBCLASSES --------------------------------------------------------------------------------------------------------------------------------------------

#------------ Pega Menu----------#
sub get_direitos
	{
	my ($cod) = @_;

	if($cod eq "")
		{
		return;
		}
	#Se for administrador tudo será edição
	if($tipo eq "1")
		{
		$selecionados .= "
					<script>\$('#$cod').find('.radio').DTouchRadio('DTouchRadioSetValue', 'a');</script>
						
				";
		}
	#Seleciona qual o tipo de permissão foi marcada no módulo
	else
		{
		if($codusuario ne "")
			{
			$DB_direitos = &DBE("select *, usuario_menu.direito as tipo from usuario_menu join menu on usuario_menu.menu = menu.nacess where usuario_menu.usuario = '$codusuario' and menu.codigo = '$cod' limit 1");
			}
		else
			{
			$DB_direitos = &DBE("select * from menu_default_direitos where usuario_tipo = '$tipo' and menu = '$cod' limit 1");
			}
		$RS_direitos = $DB_direitos->rows();
		if($RS_direitos > 0)
			{
			while($row_direitos = $DB_direitos->fetchrow_hashref)
				{
				$selecionados .= "
							<script>
								\$('#$cod').find('.radio').DTouchRadio('DTouchRadioSetValue', '".$row_direitos->{'tipo'}."');
							</script>
							
						";
				}
			}
		#Quando for "Sem acesso" ele marca
		else
			{
			if($cod ne "")
				{
				$selecionados .= "
							<script>
							\$('#$cod').find('.radio').DTouchRadio('DTouchRadioSetValue', '0');
							</script>
						
						";
				}
			}
		}
	}
	
$i2=0;
$linha=0;
#------------ Pega Menu ----------#
sub get_menu
	{
	my ($pai) = @_;
	my $SQL = "";
	if($pai eq "")
		{
		return;
		}
	
	my $get_menu = &DBE("select * from menu where pai = '$pai' order by ordem ");
	my $rs_get_menu = $get_menu->rows();
	if($rs_get_menu > 0)
		{
		
		while(my $row = $get_menu->fetchrow_hashref)
			{
			
			my $pos = 0;
			if($row->{'codigo'} > $pai)
				{
				$pos = int($row->{'codigo'}/1000);
				}
			else
				{
				$pos = int($pai/1000);
				}
			if($row->{'nacess'} ne "")
				{
				$linha++;
				$i2++;
				$menu[$pos] .= " <div class='modulos'  id='$row->{codigo}'>
							<div class='title'>$row->{'descrp'} </div>
							<input type='hidden' value='$row->{codigo}' name='menu_$i2' id='menu_$i2' />
							<div id='radio$i2' class='radio'>
						";
 				$array_radio .= "{val:'0',descrp:'Sem acesso'},";
				
				if($row->{nacess} ne "")
					{
					$nacess_menu=$row->{nacess};
					}
				else
					{
					$nacess_menu=null;	
					}

				$menu_direito = &DBE("select * from tipo_direito join menu_tipo_direito on tipo_direito.codigo = menu_tipo_direito.tipo_direito where menu_tipo_direito.menu =$nacess_menu order by descrp");
				$rs_menu_direito = $menu_direito->rows();

				if($rs_menu_direito < 1)
					{
					for($f=0; $f<@tipo_cod; $f++)
						{
						$array_radio .= "{val:'".$tipo_cod[$f]."',descrp:'".$tipo_descr[$f]."'},";
						}
					#Verifica qual foi selecionado, em caso de edição.
					&get_direitos($row->{'codigo'});
					}
				else
					{
					while($row3 = $menu_direito->fetchrow_hashref)
						{
						$array_radio .= "{val:'$row3->{codigo}',descrp:'$row3->{descrp}'},";
						}
					#Verifica qual foi selecionado, em caso de edição.
					&get_direitos($row->{'codigo'});
					}
				
				#Array que monta o DTouchRadio, retiro a último vírgula e depois monto array.
				$array_radio = substr($array_radio, 0,-1);
				$Dtouch .= "	<script> 
						\$('#radio$i2').DTouchRadio(
							{ 
							addItem:[$array_radio], 
							orientation:'vertical'
							});
						</script>
						
						";
						
				$array_radio ="";
				
				$menu[$pos] .= "</div></div>";
				if($linha==4)
					{
					$linha=0;
					$menu[$pos] .="<div class='linha'></div>";
					}
				}
			&get_menu($row->{'codigo'});
			}
		}
	return;
	}
#[FIM]-- SUBCLASSES --------------------------------------------------------------------------------------------------------------------------------------------