#!/usr/bin/perl

#
#   Menu Actions
#
$sth = &DBE("select * from menu_actions order by ordem asc");
while($menu_action = $sth->fetchrow_hashref) {
	$MENACT .= " MENACT[$menu_action->{codigo}] = { ";
	$MENACT .= " 	descrp     : '$menu_action->{descrp}', ";
	$MENACT .= " 	descrp_sub : '$menu_action->{descrp_sub}', ";
	$MENACT .= " 	classe     : '$menu_action->{classe}', ";
	$MENACT .= " 	acao       : function(){ $menu_action->{funcao} } ";
	$MENACT .= " } ;  ";
}



#
#   Secretaria
#       desabilitado ate mvp 2
#
# [INI]  Secretaria, lista de empresas -------------------------------------------------------------------
# adicionar teste se usuario logado tem direitos de secretaria
# $DB = &select("select s.*, e.nome as empresa_nome, e.apelido as empresa_apelido, e.codigo as empresa_codigo from secretaria as s left join empresa as e on e.codigo = s.empresa");
# while($s = $DB->fetchrow_hashref)
#	{
#	if($s->{empresa_apelido} ne "")
#		{ $s->{empresa_nome} = $s->{empresa_apelido}; }
#	$secretaria_menu .= "<p><span class='secretaria_change'>$s->{empresa_nome}</span><span style='display:none'>$s->{empresa_codigo}</span></p>";
#	}
# libera secretaria menu
# $secretaria = 1;
# [END]  Secretaria, lista de empresas -------------------------------------------------------------------



#
#   Imagens card 
#        User / Empresa
# imagem usuario
$USER->{img} = "/sys/cfg/DPAC/view_avatar.cgi?USER=".$USER->{usuario}."&ID=".&URLEncode($ID);

# imagem empresa
$USER->{empresa_img} = "/img/logos/".$USER->{empresa}.".png";
$logo = "/sys/cfg/DPAC/view_avatar.cgi?EMP=".$USER->{empresa}."&ID=".&URLEncode($ID);


#
#   Menu Principal
#
if($USER->{usuario} eq "1") {
	$DB = &DBE("select * from menu where show is true and pai is NULL and acao is NULL order by ordem, codigo");
} else {
    
    if($USER->{empresa} ne "1") {
        $nodone = " and codigo <> 5 "
    }
    
	$DB = &DBE("
            select 
                * 
            from 
                menu 
            left join 
                usuario_menu on menu.nacess = usuario_menu.menu 
            where 
                show is true and 
                pai is null and 
                ((usuario_menu.usuario = '$USER->{usuario}' and acao is not null) or 
                (acao is null)) 
                $nodone
            order by 
                ordem, codigo 
    ");
}

$menu_avo = "<ul style='border-bottom:0px;'>";
while($avo = $DB->fetchrow_hashref)
	{	#{$avo->{coluna}}
	$menu_avo .= "<li style='margin-top: 2px'><a href='#m-$avo->{codigo}'>$avo->{descrp}</a></li>";
	
	# lista os pais TITULO
	$menu_pai_all .= "<div id='m-$avo->{codigo}' class='menu'>";
	$DBM = &DBE("select * from menu where show is true and pai = $avo->{codigo}");
	
	while($menu = $DBM->fetchrow_hashref)
		{
		if($menu->{coluna} eq "")
			{ $menu->{coluna} = 1; }
		
		if(substr($menu->{descrp}, 0, 1) eq "*")
			{ $menu->{descrp} = ""; }
		
		# Lista todos os filhos 
		$menu_filho = "";
		if($USER->{usuario} eq "1")
			{
			$DBM2 = &DBE("select * from menu where show is true and pai = $menu->{codigo} order by ordem, codigo");
			}
		else
			{
			$DBM2 = &DBE("select distinct * from menu left join usuario_menu on menu.nacess = usuario_menu.menu where show is true and pai = $menu->{codigo} and ((usuario_menu.usuario = '$USER->{usuario}' and acao is not null) or (acao is null)) order by ordem, codigo ");
			}
			
		# Verifica se o pai tem filhos...
		if($DBM2->rows() > 0)
			{
			$menu_pai{$menu->{coluna}} .= "<ul><li class='menu_pai'>$menu->{descrp}</li><ul>";

			while($menu2 = $DBM2->fetchrow_hashref)
				{
				$menu2->{acao} =~ s/&#39;/\'/gm;
				$menu2->{acao} =~ s/&quot;/\"/gm;
				$menu2->{acao} =~ s/\"/\'/gm;
				
				# ajusta a impressao do icone
				if($menu2->{icone} ne "")
					{ 
					$icone = "<img src='$menu2->{icone}' /><br>"; 
					$icone_estilo = "menu_icone";
					}
				else
					{ 
					$icone = ""; 
					$icone_estilo = "";
					}
				
				# ajusta funcao do menu whereami
				#  $macao .= "macao[$menu2->{codigo}] = \"$menu2->{acao}\"; ";
				
                # debug($menu2->{descrp},"nofields");
                # exit;
                
				$MENUSER .= " MENUSER[$menu2->{codigo}] = { ";
                $MENUSER .= "   codigo : '$menu2->{codigo}',";
                $MENUSER .= "   descrp : '$menu2->{descrp}',";
                $MENUSER .= "   acao : function(){ ";
                $MENUSER .= "       $menu2->{acao} ";
                $MENUSER .= "   }  ";
                $MENUSER .= " };  ";
				
				$menu_filho .= "<li class='menu_filho $icone_estilo' mcod='$menu2->{codigo}'>";
				$menu_filho .= "	<a>$icone $menu2->{descrp}</a>";
				$menu_filho .= "</li>";
				}
				
			$menu_pai{$menu->{coluna}} .= $menu_filho."</ul></ul>";
			}
		}
	
	$menu_pai_  = "<div class='menu_pai_column'>".$menu_pai{1}."</div>";
	$menu_pai_ .= "<div class='menu_pai_column'>".$menu_pai{2}."</div>";
	$menu_pai_ .= "<div class='menu_pai_column'>".$menu_pai{3}."</div>";
	$menu_pai_ .= "<div class='menu_pai_column'>".$menu_pai{4}."</div>";
	
	undef($menu_pai{1});
	undef($menu_pai{2});
	undef($menu_pai{3});
	undef($menu_pai{4});
	
	$menu_pai_all .= $menu_pai_."</div>";
	}
$menu_avo .= "</ul>".$menu_pai_all;


#
# Menu Home
#   se vazio pega variavel $homescreen do init.pl
if($USER->{home} eq "") {
	$USER->{home} = $homescreen;
}
$MENUSER .= " MENUSER['home'] =  MENUSER['$USER->{home}'];  ";

#
#   validacao do email 
#       verifica usuario
#
if(!$USER->{verified}) {
    $DB = &DBE("
        select
    		to_char((data + interval '8 days') - now(), 'DD') as total
        from 
            usuario
        where
            usuario  = $USER->{usuario} and 
            verified is null
    ");
    if($DB->rows() > 0) {
        $v = $DB->fetchrow_hashref;
        if($v->{total} > 0) {
            $VERIFICADO = "<div id='verify'>você tem ".$v->{total}." dia(s) para validar seu email ! <a onClick='eos.core.call.module.verify();'>validade agora</a></div>";
        } else {
            $MENUSER .= " MENUSER['home'] = { descrp : 'Home', acao : function(){ eos.core.call.module.verify(); } } ;  ";
        }
    }
}

# retorno do menu EOS FLOAT
$MENU  = "<script>";
$MENU .= "	var macao = new Array; ";
$MENU .= "	$MENUSER $MENACT";
$MENU .= "</script>";
$MENU .= "<div id='menu'>".$menu_avo."</div>";
#
# Menu Principal [END]
#




#
#   Endo Marketing  ---------------------------------------------------------------------------------
#       desativado somente para proximas versoes
#
#
# busca campanha ativa
# $DB = &DBE("select * from endomarketing_campaign where to_char(dt_fim, 'YYYY-MM-DD') >= '".(timestamp())."' and encerrada is false ORDER BY RANDOM() LIMIT 1");
# $ec = $DB->fetchrow_hashref;
# if($DB->rows() > 0)
#     {
#     # busca marketings da campanha
#     $DB = &DBE("select * from endomarketing where campaign = $ec->{codigo} ORDER BY RANDOM() LIMIT 1");
#     $endomarketing = $DB->fetchrow_hashref;
#     $endomarketing->{descrp} = $ec->{descrp}." - ".$endomarketing->{descrp};
# 
#     # ajusta views por usuario
#     $DB = &DBE("select * from endomarketing_views where endomarketing = $endomarketing->{codigo} and usuario = $USER->{usuario}");
#     $ev = $DB->fetchrow_hashref;
#     $endomarketing->{descrp} .= " (views: ".($endomarketing->{views} - $ev->{counter}).")";
# 
#     if($DB->rows() > 0) # se ja existir a contagem
#     	{
#     	if($ev->{counter} <= 10)
#     		{
#     		$ev->{counter} ++;
#     		&DBE("update endomarketing_views set counter = $ev->{counter} where endomarketing = $endomarketing->{codigo} and usuario = $USER->{usuario}");
#     		}
#     	else # desativa o endomarketing
#     		{
#     		$endomarketing = "";
#     		}
#     	}
#     else # se nao existir a contagem insere
#     	{
#     	&DBE("insert into endomarketing_views(counter, endomarketing, usuario) values(1, $endomarketing->{codigo}, $USER->{usuario})");
#     	}
#     }
# [END]  Endo Marketing  ---------------------------------------------------------------------------------








return true;
