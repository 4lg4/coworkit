#!/usr/bin/perl

$nacess = '';
require "../cfg/init.pl";

# loader INICIAL quando vem do login
# $LOGIN = &get('LOGIN');

# inicia impressao HTML
print $query->header({charset=>utf8});


# carrega valores do banco de dados
require "./start_db.cgi";

print<<HTML;
<!DOCTYPE html>
<html id="html" style="margin:0px; padding:0px;">
<head>
	<META HTTP-EQUIV="CONTENT-TYPE" CONTENT="text/html; charset=UTF-8">
	<META NAME="COPYRIGHT" CONTENT="&copy; Done Tecnologia da Informacao LTDA">
        
    <meta name="viewport" content="width=device-width, minimum-scale=1, maximum-scale=1">
    
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
	
    
    
<title>:::: CoworkIT! | $USER->{empresa_apelido} ::::</title>
<link rel="shortcut icon" href="/img/favicon.ico">
    <script language="JavaScript">
        /** 
         *  CORE Loader
         *      Loader para carregamento do CORE basico DPAC
         */
        var L  = '<div id="DLIBSLOADER" style="height:100px; border-radius:100%; position:absolute; z-index:999999; text-align:center; left:30%; width:40%; background:#FF9700; margin-top:20px; overflow:hidden;">';
        	L += '<div style="width:100%;">';
        	L += '	<div style="position:absolute; z-index:101; text-align:center; width:100%; margin-top:40px; color:#fff; font-size:16px; font-family: Tahoma,sans-serif;">Carregando DCORE <span id="DLIBSLOADERCOUNT" style="font-size:16px;"></span>  <span id="DLIBSLOADERCOUNTSTEP" style="float:right; margin-right:2%;"></span></div>';
        	L += '	<div id="DLIBSLOADERCOUNTCONTAINER" style="position:absolute; z-index:100; height:100px; background:#3167b3;"></div>';
        	L += '</div>';
        	L += '</div>';
		
        document.write(L);
    </script>

    <script src="/comum/DPAC.js"></script>

<script>


/*
    EOS App Resize window
        controla quando a janela for redimensionada
*/ 
window.addEventListener("resize", function(){
    eos.DAction.resize();
});
    
/**
 *  Document READY
 *      Quando Documento já estiver completamente carregado
 */
\$(document).ready(function(){

    // console.log("$menu_actions");

	/* [INI]  Menu Botoes de acao (by akgleal.com)  ----------------------------------------------------------------------------- */
    // suporte old menus action usando core v3
    menu_array = [$menu_actions];
    menu_array.forEach(function(m){
        eos.menu.action.new({
			id       : m.id,    // id do item
			title    : m.descrp,   // titulo inferior
            subtitle : m.descrp_sub,          // titulo superior
			click    : function(){ // ao clicar executa funcao
                
                m.function.call(this);
			},       
            class    : m.class          // adiciona classe especifica para botao
        });
    });
    eos.menu.action.hideAll();
	/* [END]  Menu Botoes de acao (by akgleal.com)  ----------------------------------------------------------------------------- */
	
	
	// esconde header
    \$("#lightsoff").hide();
	
	
	// eye (menu iniciar =p)
	\$("#eye, #fechar, #lightsoff").hover(function()
		{
		\$("#eye").addClass("eye_down");
		})
		.mouseleave(function()
			{
			if(!\$("#lightsoff").is(":visible"))
				{
				\$("#eye").removeClass("eye_down");
				}
			})
		.click(function()
			{
			eos.menu.eye();
			\$("#menu_top").show();
			});	
		
	/* [INI] Secretaria ----------------------------------------------------------------------------------------- 
		Libera menu secretaria
	
	if($secretaria == 1)
		{
		\$("#menu_top_right_company").show();
		}
		
	\$(".secretaria_change").click(function(){ top.alerta("Deseja trocar de empresa ? "+\$(this).text()+" - "+\$(this).next("span").text()); });
    */
	/* [END] Secretaria ------------------------------------------------------------------------------------- */
	

HTML

    # Detecta se é uma abertura de dados de TI
    $protocol = &get('protocol');
	$host     = &get('host');
	$port     = &get('port');
	$username = &get('username');
	$password = &get('password');

	if($protocol ne "" && $host ne "") {
		print " 
            callExt(\"/guacamole/client.xhtml\"); 
            unLoading(); 
            main.focus(); \n
        ";
	} else {
		print "	menuWhere(\"home\"); \n";
	}
    
print<<HTML;
	
	// inicializa menu
	\$("#menu").tabs();
	
	// DDebug Dev tools
	// \$(".DDebug_dev").click(function() { DDebug(); });
		
		
	/* [INI] Menu Top Right ---------------------------------------------------------------------------------------------------------- 
	* 
	*  gera menu top right
	*
	---------------------------------------------------------------------------------------------------------------------------------- */
	// logout
	\$("#DMenuTopRight_logout").DMenuTopRight({
		title: "Sair do Sistema",
		img: "$dir{img}ui/logout.svg",
		click: function() {
                        
            \$.DDialog({
                type    : "confirm",
                message : "Deseja realmente sair ?",
                btnYes  : function() {
            		eos.logout();
                }
            })
            
		}
	});
    

	// chat center
	var chat_content  = '<div style="border-bottom:1px solid #ddd; margin-bottom:5px; padding-bottom:3px;">2 Novos Chamados</div>';
		chat_content += '<div style="border-bottom:1px solid #ddd; margin-bottom:5px; padding-bottom:3px;">1 Alerta do Sistema</div>';
	
	\$("#DMenuTopRight_chat").DMenuTopRight(
		{
		title: "Central de Mensagens",
		img: "$dir{img}ui/chat.svg",
		type: "dropdown",
		dropdownContent: chat_content
		});
		
	\$("#DMenuTopRight_user").DMenuTopRight(
		{
		title: "Dados Usuario",
		img: "$dir{img}ui/user.svg",
		// type: "dropdown",
		// dropdownContent: user_info
		click: function()
			{
			eos.menu.eye();
			}
		});
        
	\$("#DMenuTopRight_chamado").DMenuTopRight({
		title: "Abrir Chamado",
		img: "$dir{img}ui/chamado.svg",
		// type: "dropdown",
		// dropdownContent: user_info
		click: function(){
			// eos.chamadoFast();
            eos.core.call.module.tkt();
		}
	});
    
	\$("#DMenuTopRight_dashboard").DMenuTopRight({
		title: "Dashboard",
		img: "/img/ui/dashboard.svg",
		// type: "dropdown",
		// dropdownContent: user_info
		click: function(){
			// eos.chamadoFast();
            eos.core.call.module.dashboard();
		}
	});
        
	/* [INI] Menu Top Right ------------------------------------------------------------------------------------------------------- */
	

	/* [INI] Menu User Float ------------------------------------------------------------------------------------------------------ */
    \$("#user_menu_float_avatar, #user_menu_float_img, #user_menu_float_senha, #user_menu_float_nome, #user_menu_float_login")
        .click(function(){
            // edita usuario
            eos.core.call.module.users($USER->{usuario});

    		// fecha menu eye
    		eos.menu.eye();
    	});
		
	\$("#user_menu_float_company_nome, #user_menu_float_avatar_company, #user_menu_float_avatar_company, #user_menu_float_company_opt")
        .click(function(){
            // edita empresa
            // eos.core.call.module.empresa($USER->{empresa});
            call("empresa/edit.cgi",{COD:$USER->{empresa}, avatar:1});
            
		    // fecha menu eye
		    eos.menu.eye();
		});
        
    /*
	\$("#user_menu_float").DTouchBoxes({ title:"$USER->{empresa_nome}" });
	
	\$("#user_menu_float .DTouchBoxes_title")
        .click(function() {			
    		call("empresa/edit.cgi",{ COD : '$USER->{empresa}' });
		
    		// fecha menu eye
    		eos.menu.eye();
    	});
	*/
    
	/* [END] Menu User Float ------------------------------------------------------------------------------------------------------ */
	
	/* [INI] Menu Principal Float ------------------------------------------------------------------------------------------------- */
	\$(".menu_filho").click(function(event)
		{
		eos.menu.eye(\$(this)[0].getAttribute("mcod"));
		});
	/* [END] Menu Principal Float ------------------------------------------------------------------------------------------------- */
	
	
	// endomarketing, popup
	if("$endomarketing->{codigo}" != ""){
		\$.DDialog({
			type:  "alerta",
			title: "$endomarketing->{descrp}",
			img:   "$endomarketing->{img}"
		});
	}
    
    /**
     *  Disk
     */
    eos.disk.initialize(); // inicia disco do parceiro
    eos.core.limit.empresa.initialize(); // inicia limites empresas
    
    
    /**
     *  Cliente do parceiro
     *      99 = cliente do parceiro
     */
    if("$USER->{tipo}" === "99") { 
        \$("#eos_disk").hide();
    }
    
    
    /**
     *  Plan
     *      carrega plano do parceiro (bg)
     */
    \$.DActionAjax({
        action : "/sys/cfg/DPAC/parceiro_plan.cgi",
        postFunction : function(x){
            x = JSON.parse(x);
            \$("#user_menu_float_company_descrp").text("("+x.plan+")");
        }
    });
    // ajusta clique para modulo plans
	\$("#user_menu_float_company_descrp")
        .click(function(){
            // pagamentos / planos
            eos.core.call.module.pagamento($USER->{empresa})
            
		    // fecha menu eye
		    eos.menu.eye();
		});
        
   
    
})
/**
 *  KeyDown
 *      controle de teclas pressionadas no sistema
 */
.keydown(function(e){
        // console.log("crtl: "+ e.ctrlKey +" | meta: "+ e.metaKey +" | alt: "+ e.altKey +" | shift: "+ e.shiftKey +" | tecla: "+ e.key +" | cod.: "+ e.keyCode);
        
        /**
         *  Backspace control
         *      not navigate with it !
         */
        if(e.keyCode === 8) {
            var el = document.activeElement.nodeName;
            
            if(el !== "TEXTAREA" && el !== "INPUT") {
                e.preventDefault();    
            }
        } 
        
        /**
         *   UP | DOWN | LEFT | RIGHT
         *       controle de navegacao usando setas
         */
        if(e.keyCode === 37 || e.keyCode === 38 || e.keyCode === 39 || e.keyCode === 40){
            
            // DTouchRadio, se foco objetos
            if(document.activeElement.className.search("DTouchRadio") === 0){
                e.preventDefault();                                      // para execucao
                DTouchRadioNavigation(document.activeElement,e.keyCode); // executa opcao desejada
            }
            
            // teclas left | right + <body>
            // se foco estiver na tag body
            if((e.keyCode === 37 || e.keyCode === 39) && lc(document.activeElement.tagName) == "body"){
                e.preventDefault();  // para execucao do comando padrao
                
                // DTouchPages swipe
                if(\$(".DTouchPages").length > 0){
                    if(e.keyCode === 37){
                        \$(".DTouchPages_corner_left").trigger("click");
                    } else if(e.keyCode === 39){
                        \$(".DTouchPages_corner_right").trigger("click");
                    }
                }
            }
        }
        
        
		// salva ctrl + s
		if((e.ctrlKey || e.metaKey) && e.keyCode == 83){
			e.preventDefault();
			if(\$("#icon_save").is(":visible")){
				\$("#icon_save").trigger("click");
			}
        }
		
		// criar novo ctrl + n
		if((e.ctrlKey || e.metaKey) && e.keyCode == 78){
			e.preventDefault();
			if(\$("#icon_insert").is(":visible")){
				\$("#icon_insert").trigger("click");
			} else if(\$("#icon_dashboard_call").is(":visible")){
				\$("#icon_dashboard_call").trigger("click");
            }
		}
		
		// modulo dashboard ctrl + shift + d
		if((e.ctrlKey || e.metaKey) && e.shiftKey && e.keyCode == 68){
			e.preventDefault();
			MENUSER[46].acao();
		}
			
		// modulo chamado ctrl + shift + c
		if((e.ctrlKey || e.metaKey) && e.shiftKey && e.keyCode == 67){
			e.preventDefault();
			MENUSER[33].acao();
		}
		
		// modulo empresas ctrl + shift + e
		if((e.ctrlKey || e.metaKey) && e.shiftKey && e.keyCode == 69){ 
			e.preventDefault();
			callGrid("empresas");
		}
		
		// modulo home ctrl + shift + h
		if((e.ctrlKey || e.metaKey) && e.shiftKey && e.keyCode == 72){
			e.preventDefault();
			MENUSER["home"].acao();
		}
						
		// chama menu eos (ctrl + enter / ctrl + m)
		if(((e.ctrlKey || e.metaKey) && e.keyCode == 13) || ((e.ctrlKey || e.metaKey) && e.keyCode == 77)){
			e.preventDefault();
			eos.menu.eye();
		}
			
		// se esc pressionado 
		if(e.keyCode == 27){
			if(\$("#menu_float").is(":visible")){
				eos.menu.eye();
            }
        }
});	

</script>
</head>
<body ID="BODYEOS" onLoad='history.forward()' style="margin:0px; padding:0px;">
    
<!-- DEagle --> 
<div id="deagle_">
    <div id="deagle_talk">
        <div id="deagle_talk_content"></div>
        <div id="deagle_close"></div>
    </div>
</div>


<!-- Blackout Menu principal -->
<div id="lightsoff"></div>

<!-- Done EYE, icon menu iniciar -->
<div id="eye"><img src="/img/login/coworkit.svg" border="0"></div>

<!-- Menu principal -->
<div id="menu_float">$MENU</div>

<!-- verify -->
$VERIFICADO

<!-- container principal -->
<div id="corpo">

	<!-- barra do menu top -->
	<div id='menu_top'> 

		<!-- menu onde estou -->
		<div id="menu_whereami">
			<div id="menu_top_home"></div>
			<div id="menu_top_modules" class="menu_top_modules"></div>
		</div>
        
		<!-- Menu Top Right, menu empresas, mensagens, dados do usuario, sair -->
		<div id="menu_top_right">
			
			<!-- sair do sistema -->
			<div id="DMenuTopRight_logout"></div>
			
			<!-- Chat -->
			<div id="DMenuTopRight_chat" style="display:none;"></div>
						                
			<!-- Dados empresa
			<div id="DMenuTopRight_company"></div>			
			
			 Fast New
			<div id="DMenuTopRight_fastnew"></div>
			-->
			
			<!-- Dados usuario -->
			<div id="DMenuTopRight_user"></div>
			
			<!--
			< usuario >
			<div id="DMenuTopRight_user_descrp"></div>
			 -->
			 
			<!-- usuario 
			<div id="DMenuTopRight_fullscreen"></div>
            -->
			<!-- chamado fast -->
			<div id="DMenuTopRight_chamado"></div>
			 
			<!-- disk -->
			<div id="eos_disk">
                <div id="eos_disk_total"><span></span></div>
			    <div id="eos_disk_used"></div>
                <div id="eos_disk_stats"></div>
			</div>
            
            
			<!-- dashboard fast -->
			<div id="DMenuTopRight_dashboard"></div>	
            
            
			<!-- Dev Debugger -->
			$DDEBUG			
		</div>
	</div>
	
	<!-- menu actions lateral esquerdo -->
	<div id='menu_actions' align="center"></div>
	
	<!-- div principal para carregamento das paginas -->
	<div id="main_container">
		<div name="main_div" id="main_div"></div>
	</div>
</div>

<!-- DMenu Top Right Drop Down -->
<div id="DMenuTopRightDropDown"></div>

<!-- Loader -->
<div id='loader_eos' class="body_central DLoaders"></div>
<div id='loading' class="DLoaders"></div>
<div id="loading_container" class="DLoaders">
	<div id="fadingBarsG">
		<div id="fadingBarsG_1" class="fadingBarsG"></div>
		<div id="fadingBarsG_2" class="fadingBarsG"></div>
		<div id="fadingBarsG_3" class="fadingBarsG"></div>
		<div id="fadingBarsG_4" class="fadingBarsG"></div>
		<div id="fadingBarsG_5" class="fadingBarsG"></div>
		<div id="fadingBarsG_6" class="fadingBarsG"></div>
		<div id="fadingBarsG_7" class="fadingBarsG"></div>
		<div id="fadingBarsG_8" class="fadingBarsG"></div>
	</div>
	<div id="loader_descrp"></div>
</div>

<!-- Loader Obj -->
<div class='eos_template_loader_obj' style="display:none;">
    <div class='loader_obj_container'>
        <div class='loader_obj loader_obj_1'></div>
        <div class='loader_obj loader_obj_2'></div>
        <div class='loader_obj loader_obj_3'></div>
    </div>
</div>

<!-- menu secretaria -->
<div id="menu_top_right_company_status" class="dbox_menu">
	<div class="dbox_menu_title"><img src="/img/ui/company.png" align="absmiddle"><span>Empresas</span></div>
	<div class="dbox_menu_cont">$secretaria_menu</div>
</div>


<!-- user menu float -->
<div id="user_menu_float">
    <!-- user id -->
	<div id="user_menu_float_user">
	    <div id="user_menu_float_avatar">
	        <img src="$USER->{img}">
        </div>
    	<div id="user_menu_float_nome">
    		$USER->{nome}
    	</div>
    	<div id="user_menu_float_login">
    		($USER->{login})
    	</div>
    	<div id="user_menu_float_opt">
    		<div id="user_menu_float_senha">
                &bull; Trocar Senha
            </div>
    		<div id="user_menu_float_img">
                &bull; Trocar Imagem Usuario
            </div>
    	</div>
    </div>
    
    <!-- company id -->
    <div id="user_menu_float_company_container">
        <div id="user_menu_float_avatar_company">
		    <img src="$logo">
        </div>
        <div id="user_menu_float_company_nome">
    	     $USER->{empresa_apelido}
    	</div>
        <div id="user_menu_float_company_descrp">
            (carregando...)
        </div>
        <div id="user_menu_float_company_opt">
             Trocar Imagem Empresa &bull;
        </div>
    </div>
</div>


<!-- circles -->
<div id="circle_container">
    <div id="circle_one"></div>
    <div id="circle_two"></div>
    <div id="circle_three"></div>
    <div id="circle_four"></div>
</div>

<form id="AUX" name='AUX' method='POST'>
	<input type='hidden' name='ID' value='$ID'>
	<input type='hidden' name='SHOW'>
	<input type='hidden' name='GRUPO'>
	<input type='hidden' name='FROM' value='menu'>
	<input type='hidden' name='TABLE'>
	<input type='hidden' name='FILTRO'>
	<input type='hidden' name='MODULO_PATH'>
	<input type='hidden' name='VOLTAR'>
	
	<!-- usado para manter compatibilidade de modulos IFRAME -->
	<input type='hidden' name='MODO'>
	<input type='hidden' name='COD'>
	 
</form>

<div id="relogon" style="display: none">
<form id="relogin_form" name='relogin_form' method='POST' onSubmit='return relogin_submit()'>
	<div id="login_" align="center">
		
	<div id="login_form_container">
		<div id="login_logo" align="center">
			<img src="$logo" alt="$s->{empresa_nome}" title="$s->{empresa_nome}" border="0" onError="this.src='/img/logos/0.png'" />
		</div>
		<div id="login_form" align="left">
			<input type="text" placeholder="Usuário" name="username" class="login fieldUser" tabindex=1 autocomplete="off" style="margin-bottom:3px;" value="$USER->{login}" readonly><br>
			<input type="password" placeholder="Senha" name="password" class="login fieldPassword" tabindex=2 autocomplete="off"><br>
			<div align="right">
				<input type="submit" value="login" id="btn_login_round" onClick="relogin_submit()">
			</div>
		<input type='hidden' name='empresa' value='$USER->{empresa}'>
		</div>
	</div>
</form>
<div id="relogon_result" style="display: none"></div>

<form name='guacamole' method='POST'>
	  <input type='hidden' name='ID' value='$ID'>
	  <input type='hidden' name='protocol' value='$protocol'>
	  <input type='hidden' name='host' value='$host'>
 	  <input type='hidden' name='port' value='$port'>
	  <input type='hidden' name='username' value='$username'>
	  <input type='hidden' name='password' value='$password'>
</form>

</div>

</body>
</html>
HTML
