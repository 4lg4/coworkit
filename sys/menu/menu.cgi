#!/usr/bin/perl

$nacess = '5';
require "../cfg/init.pl";

$ID = &get('ID');
$opt = &get('opt');
$MENU = &get('MENU');

$descrp = &get('descrp');
$acao = &get('acao');
$path = &get('path');
$pai = &get('pai');
$mobile = &get('mobile');
$ordem = &get('ordem');
$coluna = &get('coluna');
$show = &get('show');
$nacess_ = &get('nacess');
$icone = &get('icone');
	
print "Content-type: text/html\n\n";

# [INI] menus edit ------------------------------------------------------------------------------------------------------
if($MENU ne "")
	{
	$DBM = &select("select * from menu where codigo = $MENU");
	$menu = $DBM->fetchrow_hashref;
	
	# marca se menu ativo ou nao
	if($menu->{show} == 1)
		{ $show_ = "\$('input:radio').first().attr('checked',true);" } 
	else
		{ $show_ = "\$('input:radio').last().attr('checked',true);" } 
		
	print "
	<script>
		\$('#descrp').val('$menu->{descrp}');
		\$('#icone').val('$menu->{icone}');
		\$('#acao').val(\"$menu->{acao}\");
		\$('#pai').val('$menu->{pai}');
		\$('#mobile').val(\"$menu->{mobile}\");
		\$('#ordem').val('$menu->{ordem}');
		\$('#coluna').val('$menu->{coluna}');
		\$('#nacess').val('$menu->{nacess}');
		$show_
		";
		
	if($menu->{acao} ne "")
		{
		print "	fieldOptEnable(['acao','nacess','coluna','mobile']);";
		}
	else
		{
		print "	fieldOptDisable(['coluna','mobile','acao']);";
		}
		
	print "	</script>";
	}
# [END] menus edit ------------------------------------------------------------------------------------------------------

# [INI] menus Update ----------------------------------------------------------------------------------------------------
if($opt eq "update")
	{
	# ajusta variaveis para salvar no banco
	if($pai ne "")
		{ $pai2 = ", pai=$pai"; }
	if($ordem ne "")
		{ $ordem2 = ", ordem=$ordem"; }
	if($coluna ne "")
		{ $coluna2 = ", coluna=$coluna";
		  $coluna_script .="\$('#coluna').val(\"$coluna\");";
		}
	if($show eq "1")
		{ $show2 = true; }
	else
		{ $show2 = false; }
	if($nacess_ ne "")
		{ $nacess2 = ", nacess=$nacess_"; }
	
	if($mobile eq "")
		{ $mobile2 = NULL; }	
	else
		{ $mobile2 = "'$mobile'"; }		
	if($acao eq "")
		{ $acao2 = NULL; }
	else
		{ $acao2 = "'$acao'"; }
			
	# executa
	$DB = DBE("update menu set descrp='$descrp', acao=$acao2, mobile=$mobile2 $pai2 $ordem2 $coluna2 $nacess2, show=$show2, icone='$icone' where codigo = ".$MENU);
	
	print "<script>";
	# marca se menu ativo ou nao
	if($show == 1)
		{ $show_ = "\$('input:radio').first().attr('checked',true);"; }
	else
		{ $show_ = "\$('input:radio').last().attr('checked',true);"; }
		
	print " 
		\$('#descrp').val('$descrp');
		\$('#icone').val('$icone');
		\$('#acao').val(\"$acao\");
		\$('#pai').val('$pai');
		\$('#mobile').val(\"$mobile\");
		\$('#ordem').val('$ordem');
		$coluna_script
		\$('#nacess').val('$nacess_');
		$show_
		
		\$('#MENU').val('');
		menus();
		\$('#MENU').val($MENU);
		
		</script>
		";
	
	}
# [END] menus Update ----------------------------------------------------------------------------------------------------

# [INI] menu Save ------------------------------------------------------------------------------------------------------
if($opt eq "insert")
	{
	if($pai eq "")
		{ $pai = NULL; }
	if($ordem eq "")
		{ $ordem = NULL; }
	if($coluna eq "")
		{ $coluna = NULL; }
	if($nacess_ eq "")
		{ $nacess_ = NULL; }
	if($show eq "1")
		{ $show = true; }
	else
		{ $show = false; }
	
	if($mobile eq "")
		{ $mobile = NULL; }	
	else
		{ $mobile = "'$mobile'"; }		
	if($acao eq "")
		{ $acao = NULL; }
	else
		{ $acao = "'$acao'"; }
	
	$DB = DBE("insert into menu (descrp,acao,mobile,pai,ordem,coluna,nacess,show,icone) values ('$descrp',$acao,$mobile,$pai,$ordem,$coluna,$nacess_,$show,'$icone')");	
	print "<script>menus(); top.alerta('Menu adicionado com sucesso!'); incluir();  </script>";
	}
# [END] menu Save ------------------------------------------------------------------------------------------------------

# [INI] menu Excluir ------------------------------------------------------------------------------------------------------
if($opt eq "excluir")
	{
	# Verifica se tem filho, se tiver exclui.
	$DB = DBE("select * from menu where pai = $MENU ");
	if($DB->rows()>0)
		{
		$DB2 = DBE(" delete from menu where pai =$MENU ");	
		}
	#Exclui o menu
	$DB3 = DBE(" delete from menu where codigo =$MENU ");
	print "<script>\$('#MENU').val(''); menus(); top.alerta('Menu excluído com sucesso!'); cancelar(); </script>";
	}


if($opt eq "verificar")
	{
	#Verifica o menu é pai e se tem submenus
	$DB = DBE("select * from menu where pai = $MENU ");
	if($DB->rows()>0)
		{
		print "<script>top.confirma('Este é um menu pai, se você esclui-lo irá apagar os demais submenus, Deseja fazer isto?','main.excluir(\"1\")'); </script>";
		}
	else
		{
		#Exclui o menu
		$DB3 = DBE(" delete from menu where codigo =$MENU ");
		print "<script> \$('#MENU').val(''); menus(); top.alerta('Menu excluído com sucesso!'); cancelar(); </script>";
		}
	}
# [END] menu Excluir ------------------------------------------------------------------------------------------------------

if($MENU ne "")	
	{ exit; }

# [INI] menu Lists ------------------------------------------------------------------------------------------------------
sub menus	
	{ my ($SQL,$TBID) = @_;
	
	my $R="", $TBINI="", $TBEND="", $line="";
		
	# $DB = &select("select m.*, m2.descrp as pai_descrp from menu as m left join menu as m2 on m2.codigo = m.pai");
	$DB = &select($SQL);
	while($menu = $DB->fetchrow_hashref)
		{
		$line .= "<tr>";
		$line .= "		<td style='display:none;'>$menu->{codigo}</td>";
		$line .= "		<td style='width:25px;'>$menu->{nacess}</td>";
		$line .= "		<td>$menu->{descrp}</td>";
		$line .= "		<td>$menu->{acao}</td>";
		$line .= "		<td>$menu->{pai_descrp}</td>";
		$line .= "		<td>$menu->{mobile}</td>";
		# $line .= "		<td>$menu->{show}</td>";
		$line .= "		<td>$menu->{ordem}</td>";
		$line .= "		<td>$menu->{coluna}</td>";
		$line .= "</tr>";
		}
	
	# ajuste do grid	
	$TBINI .= "<table class='menu_tb' id='".$TBID."' style='min-width:100%; min-height:100px;'>";
	$TBINI .= "	<thead>";
	$TBINI .= "	<tr>";
	$TBINI .= "		<th style='display:none;'>Cod</th>";
	$TBINI .= "		<th style='font-weight:normal;'>N.Acess</th>";
	$TBINI .= "		<th>Descrição</th>";
	$TBINI .= "		<th>Ação</th>";
	$TBINI .= "		<th>Pai</th>";
	$TBINI .= "		<th>Mobile</th>";
	# $TBINI .= "		<th>Ativo</th>";
	$TBINI .= "		<th>ordem</th>";
	$TBINI .= "		<th>Coluna</th>";
	$TBINI .= "	</tr>";
	$TBINI .= "	</thead>";
	$TBINI .= "	<tbody>";
	$TBEND .= "	</tbody>";
	$TBEND .= "</table>";
	
	# monta as grids
	$R .= $TBINI.$line.$TBEND;
	
	return $R;
	}
	
$R_active = &menus("select m.*, m2.descrp as pai_descrp from menu as m left join menu as m2 on m2.codigo = m.pai where m.show is true and m.codigo <> '2' and m.codigo <> '17' and m.codigo <> '28' and m.codigo <> '29' ","ma");
$R_inactive = &menus("select m.*, m2.descrp as pai_descrp from menu as m left join menu as m2 on m2.codigo = m.pai where m.show is false and m.codigo <> '2' and m.codigo <> '17' and m.codigo <> '28' and m.codigo <> '29' ","mi");

# Gera visualizacao do novo menu usando jquery tabs 
$DB = &select("select * from menu where show is true and pai is NULL and acao is NULL order by ordem");

$menu_avo = "<ul style='border-bottom:0px;'>";
while($avo = $DB->fetchrow_hashref)
	{	#{$avo->{coluna}}
	$menu_avo .= "<li style='margin-top: 2px'><a href='#m-$avo->{codigo}'>$avo->{codigo} - $avo->{descrp}</a></li>";
	
	# lista os pais
	$menu_pai_all .= "<div id='m-$avo->{codigo}' class='menu'>";
	$DBM = &select("select * from menu where show is true and pai = $avo->{codigo}");
	while($menu = $DBM->fetchrow_hashref)
		{
		if($menu->{coluna} eq "")
			{ $menu->{coluna} = 1; }
		
		$menu_pai{$menu->{coluna}} .= "<ul>$menu->{descrp} - $menu->{acao}"; # " - $menu->{codigo} - ".$menu->{acao};
		
		# Lista todos os filhos 
		$menu_filho = "<li>";
		$DBM2 = &select("select * from menu where show is true and pai = $menu->{codigo}");
		while($menu2 = $DBM2->fetchrow_hashref)
			{
			# $menu_filho .= "@@ $menu2->{codigo} - ";
			# $menu_filho .= "$menu2->{pai} | ";
			$menu_filho .= "$menu2->{descrp} | ";
			$menu_filho .= "$menu2->{acao} <br> ";
			# $menu_filho .= "$menu2->{show} <br>";
			}
			
		$menu_pai{$menu->{coluna}} .= $menu_filho."</li></ul>";
		}
	$menu_pai_ = "<div style='width:30%; float:left;'>".$menu_pai{1}."</div><div style='width:30%; float:left;'>".$menu_pai{2}."</div><div style='width:30%; float:left;'>".$menu_pai{3}."</div>";
	undef($menu_pai{1});
	undef($menu_pai{2});
	undef($menu_pai{3});
	
	$menu_pai_all .= $menu_pai_."</div>";
	}
$menu_avo .= "</ul>".$menu_pai_all;


$R_view = "<div id='menus'>".$menu_avo."</div>";
# [END] menu Lists ------------------------------------------------------------------------------------------------------


print<<HTML;

	<script>
		\$("#menu_active").html("$R_active");
		\$("#menu_inactive").html("$R_inactive");
		\$("#menu_view").html("$R_view");
		
		\$("#menus").tabs();
		
		var ma = new grid("ma","no");
		ma.setQtd('40');
		ma.setHeight('300');
		ma.show();
		
		var mi = new grid("mi","no");
		mi.setQtd('40');
		mi.setHeight('300');
		mi.show();
	</script>

HTML

