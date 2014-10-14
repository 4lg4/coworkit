#!/usr/bin/perl

$nacess = '3';
require "../cfg/init.pl";

$ID = &get('ID');
$opt = &get('opt');
$MENU = &get('MENU');

$descrp = &get('descrp');
$descrp_sub = &get('descrp_sub');
$id = &get('id');
$nome = &get('nome');
$funcao = &get('funcao');
$funcao_2 = &get('funcao_2');
$classe = &get('classe');
$ordem = &get('ordem');

if($ordem eq "")
	{ $ordem = 0; }

print "Content-type: text/html\n\n";

# [INI] menus edit ------------------------------------------------------------------------------------------------------
if($opt eq "select")
	{
	$DBM = &select("select * from menu_actions where codigo = $MENU");
	$menu = $DBM->fetchrow_hashref;
	
	# marca se menu ativo ou nao
	# if($menu->{show} == 1)
	#	{ $show_ = "\$('input:radio').first().attr('checked',true);" } 
	# else
	#	{ $show_ = "\$('input:radio').last().attr('checked',true);" } 
		
	print "
	<script>
		\$('#descrp').val('$menu->{descrp}');
		\$('#descrp_sub').val('$menu->{descrp_sub}');
		\$('#id').val(\"$menu->{id}\");
		\$('#nome').val('$menu->{nome}');
		\$('#funcao').val(\"$menu->{funcao}\");
		\$('#funcao_2').val(\"$menu->{funcao_2}\");
		\$('#ordem').val('$menu->{ordem}');
		\$('#classe').val('$menu->{classe}');
		$show_
	</script>";

	exit;
	}
# [END] menus edit ------------------------------------------------------------------------------------------------------

# [INI] menus Update ----------------------------------------------------------------------------------------------------
if($opt eq "update")
	{
	$DB = DBE("update menu_actions set descrp='$descrp', descrp_sub='$descrp_sub',id='$id',nome='$nome',funcao='$funcao',funcao_2='$funcao_2',ordem=$ordem,classe='$classe' where codigo = ".$MENU);
	print "<script> \$('#MENU').val($MENU); menus('select'); </script>"
	}
# [END] menus Update ----------------------------------------------------------------------------------------------------

# [INI] menu Insert ------------------------------------------------------------------------------------------------------
if($opt eq "insert")
	{
	$DB = DBE("insert into menu_actions (id,nome,descrp,descrp_sub,funcao,funcao_2,classe,ordem) values ('$id','$nome','$descrp','$descrp_sub','$funcao','$funcao_2','$classe',$ordem)");	
	}
# [END] menu Insert ------------------------------------------------------------------------------------------------------

# [INI] menu Delete ------------------------------------------------------------------------------------------------------
if($opt eq "delete")
	{
	$DB = DBE("delete from menu_actions where codigo = ".$MENU);
	}
# [END] menu Delete ------------------------------------------------------------------------------------------------------

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
		$line .= "		<td>$menu->{id}</td>";
		$line .= "		<td>$menu->{nome}</td>";
		$line .= "		<td>$menu->{descrp}</td>";
		$line .= "		<td>$menu->{descrp_sub}</td>";
		$line .= "		<td>$menu->{funcao}</td>";
		$line .= "		<td>$menu->{funcao_2}</td>";
		$line .= "		<td>$menu->{classe}</td>";
		$line .= "		<td>$menu->{ordem}</td>";
		$line .= "</tr>";
		}
	
	# ajuste do grid	
	$TBINI .= "<table class='menu_tb' id='".$TBID."' style='min-width:100%;'>";
	$TBINI .= "	<thead>";
	$TBINI .= "	<tr>";
	$TBINI .= "		<th style='display:none;'>Cod</th>";
	$TBINI .= "		<th>ID</th>";
	$TBINI .= "		<th>Nome</th>";
	$TBINI .= "		<th>Descrição</th>";
	$TBINI .= "		<th>Descrição Secundária</th>";
	$TBINI .= "		<th>OnClick</th>";
	$TBINI .= "		<th>OnDblClick</th>";
	$TBINI .= "		<th>Classe</th>";
	$TBINI .= "		<th>Ordem</th>";
	$TBINI .= "	</tr>";
	$TBINI .= "	</thead>";
	$TBINI .= "	<tbody>";
	$TBEND .= "	</tbody>";
	$TBEND .= "</table>";
	
	# monta as grids
	$R .= $TBINI.$line.$TBEND;
	
	return $R;
	}
	
$R_active = &menus("select * from menu_actions where ativo is true order by ordem asc","ma");
# $R_inactive = &menus("select m.*, m2.descrp as pai_descrp from menu as m left join menu as m2 on m2.codigo = m.pai where m.show is false","mi");

# Gera visualizacao do menu actions
$sth = &DBE("select * from menu_actions order by ordem asc");
while($menu_action = $sth->fetchrow_hashref)
	{
	$menu_actions .= "['$menu_action->{nome}','$menu_action->{funcao}','$menu_action->{descrp}','$menu_action->{descrp_sub}','$menu_action->{classe}'],";
	}
$menu_actions = substr($menu_actions, 0,-1); # remove ultima virgula

# [END] menu Lists ------------------------------------------------------------------------------------------------------


print<<HTML;

	<script>
		\$("#menu_active").html("$R_active");
		// \$("#menu_inactive").html("$R_inactive");
		
		// gera menu com icones
		\$("#menu_view_int").html("");
		menu_array2 = new Array ($menu_actions);
		for(var f in menu_array2)
			{
			// ajusta exibicao css
			var menu_btn_title = "";
			var menu_btn_title_sub = "";

			// ajusta tamanho fonte na descricao principal
			/*
			if(menu_array[f][2].length == 6)
				menu_btn_title = 'font-size:11px; ';
			else 
			*/
			if(menu_array2[f][2].length >= 7 && menu_array2[f][2].length <= 8)
				menu_btn_title = 'font-size:10px; margin-bottom:1px;';
			else if(menu_array2[f][2].length >= 9)
				menu_btn_title = 'font-size:9px; margin-bottom:1px;';

			// ajusta borda da sub descricao
			if(menu_array2[f][3] == "")
				menu_btn_title_sub = 'border:none; ';

			// ajusta tamanho fonte na descricao principal
			if(menu_array2[f][3].length > 8)
				menu_btn_title_sub += 'font-size:9px;';	

			\$("#menu_view_int").append('<div class="menu_btn menu_btn_control '+menu_array2[f][4]+'" id="'+menu_array2[f][0]+'" onClick="'+menu_array2[f][1]+'"><div class="menu_btn_container"><div class="menu_btn_title_sub" style="'+menu_btn_title_sub+' text-align:center;"><nobr>'+menu_array2[f][3]+'</nobr></div><div class="menu_btn_title" style="'+menu_btn_title+' text-align:center;"><nobr>'+menu_array2[f][2]+'</nobr></div></div></div>');
			}
					
		\$("#menus").tabs();
		
		var ma = new grid("ma","no");
		ma.setQtd('40');
		ma.setHeight('300');
		ma.show();
		
		var mi = new grid("mi");
		
		// var mm = new grid("mm","no");
		// mm.show();
		
		// new grid("menu_tb",1);
		// new grid("menu_close_tb");
		// new grid("menu_refused_tb");
		
		// limpa formulario
		formClean();
	</script>

HTML

