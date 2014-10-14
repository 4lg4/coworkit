#!/usr/bin/perl

# libs
require "../cfg/init.pl";

$plan = &get("plano");

# headers
print $query->header({charset=>utf8});

print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
		<meta name="viewport" content="width=device-width, minimum-scale=1, maximum-scale=1">
		
		<title>:::: CoworkIT : wizard ::::</title>
		<link rel="shortcut icon" href="/done.ico">
        
        <!-- general libs -->
            
		<!-- wizard libs -->
		<link href="/css/wizard.css" rel="stylesheet" type="text/css" />	
		<script language="JavaScript" src="/comum/wizard.js"></script>
        
        <script language="JavaScript" src="/comum/facebook.js"></script>
        <script type="text/javascript" src="/comum/recaptcha_ajax.js"></script>
        
        $DEVPWD
	</head>

<body>
	<form name="logon" id="logon" method="post">

		<div id="coworkit_logo">
			<img />
		</div>
        
		<div id="wizard_container" align="center">
			
    		<div id="wizard_form">
                <div id="wizard_form_bg"><img /></div>
                
                <div id="wizard_form_fields_container">
                    
                    <div id="usuario_aba_form" class="little_forms">
            			<div class="wizard_form_descrp">
                            <div class="form_title">
                                Usuário
                            </div>
                        
                            <div id="face" tooltip="Cadastrar apartir do Facebook" class="tooltip">
                                <img />
                            </div>
            			</div>
                    
                        <div class="wizard_form_fields">
                            <input type="text"     placeholder="Nome" name="nome" id="nome"  tabindex="1" autocomplete="off">
            			    <input type="text"     placeholder="Usuário (email)" name="username" id="username"  tabindex="2" autocomplete="off">
            			    <input type="password" placeholder="Senha"   name="password" id="password"  tabindex="3" autocomplete="off">
                            <input type="password" placeholder="Confirmar Senha"   name="password_conf" id="password_conf"  tabindex="4" autocomplete="off">
                       
                                <div id="captcha" style="display:none">
                                    <div id="captcha_challenge_container">
                                        <div id="recaptcha_image"></div>
                                        <div id="captcha_refresh_container">
                                            <a href="javascript:Recaptcha.reload()">
                                                <img id="captcha_refresh" src="/img/wizard/refresh.svg" />
                                            </a>
                                        </div>
                                    </div>
                                    <div id="captcha_response_container">
                                        <input type="text" id="recaptcha_response_field" name="recaptcha_response_field" placeholder="Conteúdo da imagem" />
                                    </div>
                                 </div>  
                        </div>
                    </div>
                    
                    <div id="empresa_aba_form" class="little_forms">
            			<div class="wizard_form_descrp">
                            <div class="form_title">
                                Empresa
                            </div>
            			</div>
                    
                        <div class="wizard_form_fields">
                            <span id="plan_descrp">Plano:</span>
                            <select name="plan" id="plan">
                                <option value="2">3 meses Trial</option>
                                <option value="3">Autonomous</option>
                                <option value="4">Business</option>
                                <option value="5">Enterprise</option>
                            </select>
                            <br><br>
                            
                            <input type="text"     placeholder="Nome" name="company_nome" id="company_nome"  tabindex="5" autocomplete="off">
                            <input type="text"     placeholder="Apelido" name="company_apelido" id="company_apelido"  tabindex="6" autocomplete="off">
                            
                            <br>
                            <input type="radio"     placeholder="teste" name="company_tipo" id="company_tipo"   tabindex="7" value="F"> Física
                            <input type="radio"     placeholder="teste" name="company_tipo"   tabindex="8" value="J"> Juridica
                            
                            <br>
                            <input type="text"     placeholder="CPF" name="company_documento" id="company_documento"  tabindex="9" autocomplete="off">
                        </div>
                    </div>
                    
                    
                    <div id="more_aba_form" class="little_forms">
            			<div class="wizard_form_descrp">
                            Mais CFG                        
            			</div>
                    
                        <div class="wizard_form_fields">
                            Payment options
                        </div>
                    </div>
                
                
    			<div id="wizard_form_btn" class="wizard_btn">
    				Iniciar USO !
    			</div>
    		</div>
		</div>
    </div>
    
    <div id="abas_container">
        <div id="usuario_aba" tooltip="Dados usuário" class="tooltip abas">
            <img id='usuario' />
        </div>
    
        <div id="empresa_aba" tooltip="Dados da empresa" class="tooltip abas">
            <img id='empresa' />
        </div>
    
        <div id="more_aba" tooltip="Mais configurações" class="tooltip abas">
            <img id='more' />
        </div>
    </div>
    
    
    
	<input type="hidden" name="ID">
	<input type="hidden" name="empresa_codigo" value="$empresa_codigo">
	<input type="hidden" name="LOGIN">
	<iframe name='temp' id='temp' style='display: none'></iframe>
    
	</form>

<!-- circles -->
<div id="circle_container">
    <div id="circle_one"></div>
    <div id="circle_two"></div>
    <div id="circle_three"></div>
    <div id="circle_four"></div>
</div>

<!-- modal -->
<div id="modal_container" >
    <div id="modal_form_container" align="center">
        <div id="modal_form_bg">
            <div id="modal_form_text"></div>
            <div id="modal_form_btn" tooltip="OK Entendi, vou tentar novamente !!" class="tooltip wizard_btn">
                ok
            </div>
        </div>
    </div>
</div>

<!-- footer -->
<div id="wizard_footer_container">
    <div id="wizard_footer" tooltip="Navegadores homologados" class="tooltip_up">
    	<span>
    		<img src="/img/login/browser_safari.png" style="margin-right:15px; height:40px;" border="0">
    		<img src="/img/login/browser_chrome.png" style="margin-right:15px; height:40px;" border="0">
    		<img src="/img/login/browser_firefox.png" style="height:40px;" border="0">
    	</span>
    </div>
</div>

<div id="wizard_loader">
    <div>
        Carregando ... 
    </div>
</div>

<div id="fb-root"></div>
<script>
    
     /* facebook */
     
     // facebook login
     window.fbAsyncInit = function() {
         FB.init({
             appId      : '178169535709072', // App ID
             channelUrl : '//coworkit.com.br/',
             status     : true, 
             cookie     : true, 
             xfbml      : true  
         });
      } 
      
      var logins = {};
      // ao clicar no logo
      document.getElementById("face").addEventListener("click",function(){   
         
          wizard.loader.add(); // loader

          FB.login(function(response) {
              if (response.authResponse) {
                  console.log('Welcome!  Fetching your information.... ');
                  FB.api('/me', function(response) { console.log(response);
                      
                      logins = response;
                      /*
                      // converte retorno em campos
                      for(var x in response ) { 
                          var f = document.createElement("input");
                              f.type  = "hidden";
                              f.name  = "fb_"+x;
                              f.value = response[x];
                              f.classList.add = "fb_fields";
                          document.getElementById("wizards").appendChild(f);
                      }
                      */
  
                      // popula formulario visivel
                      document.getElementById("username").value = response.email;
                      document.getElementById("nome").value     = response.name;
                      document.getElementById("company_nome").value     = response.name;
                      document.getElementById("company_apelido").value  = response.username;
  
                      wizard.loader.remove(); // remove loader
  
                  });
                } else {
                  console.log('User cancelled wizard or did not fully authorize.');
                }
            }, {scope: 'email'});    
        });
</script>


<script>
    // obj principal
    var wizard = new Wizard();
    
    document.getElementById("wizard_loader").classList.add("loading"); // loader
    
    
    // seleciona plano
    if("$plan" !== ""){
        document.querySelectorAll("select[name=plan] option").forEach(function(i){ 
            var test = i.value;
            if(test.toString().toLowerCase() === "$plan".toString().toLowerCase()){
                i.setAttribute("selected",true);
            }
        });
    }
    
    
    /* inicializa */
    var readyStateCheckInterval = setInterval(function() {
        if (document.readyState === "complete") {
            
            // remove controle
            clearInterval(readyStateCheckInterval);
            
            // obj principal
            wizard.initialize();
                         
             // Captcha
             Recaptcha.create("6Lf4xOoSAAAAAPZ82Qgx_NLfXa--3W3lN7Ejh6cN ",
                 "captcha",
                 {
                   theme: "custom",
                   custom_theme_widget: 'captcha',
                   lang : 'pt',
                   callback: Recaptcha.focus_response_field
                 }
             );
             
             
             // foco inicial
             document.getElementById("nome").focus();
        }
    }, 10);
    
    // foco no primeiro campo
    document.forms[0].elements[0].focus();

    // submete formulario com enter
    document.querySelectorAll("#wizard_form_fields input").forEach(function(item){
        item.addEventListener("keydown",function(e){
            if(e.which === 13) {
                checkForm();
                // document.forms[0].submit();
            }
        });
    });


    // submete formulario com enter
    document.querySelector("body").addEventListener("keydown",function(e){
        if(e.which === 13) {
            console.log("aa");
        }
    });
    
    

    // clique nas abas
    var classes = document.getElementById("usuario_aba").classList;
    classes.add("abas_up");
    
    // formulario ativo
    var classes = document.getElementById("usuario_aba_form").classList;
    classes.add("forms_up");
    
    document.querySelectorAll(".abas").forEach(function(i){
        i.addEventListener("click",function(x){
            
            // remove classe aba up
            document.querySelectorAll(".abas").forEach(function(ii){
                var classes = ii.classList;
                classes.remove("abas_up");
            });
            
            // adiciona classe aba up
            var classes = i.classList;
            classes.add("abas_up");
            
            // esconde formularios
            document.querySelectorAll(".little_forms").forEach(function(ii){
                var classes = ii.classList;
                classes.remove("forms_up");
            });
            
            // adiciona classe form up
            var classes = document.getElementById(this.getAttribute("id")+"_form").classList;
            classes.add("forms_up");            
        });
    });


    // submete formulario com click na imagem
    document.getElementById("wizard_form_btn").addEventListener("click",function(){
        wizard.save();
    });

    // adiciona imagem random user
    
    
    
    // abas
    document.getElementById("usuario").setAttribute("src","/img/wizard/usuario.svg");
    document.getElementById("empresa").setAttribute("src","/img/wizard/empresa.svg");
    document.getElementById("more").setAttribute("src","/img/wizard/more.svg");
    
    
    // coworkit img
    document.querySelector("#coworkit_logo img").setAttribute("src","/img/login/coworkit.svg");
        // .setAttribute("src","/img/wizard/user/"+randomInt(1, 6)+".png");
    
    // adiciona imagem random btn
    //var btn = randomInt(1, 25);
    //document.querySelector("#wizard_form_btn img")
      //  .setAttribute("src","/img/wizard/btn/"+btn+".png");
    
    // modal    
    //document.querySelector("#modal_form_btn img")
     //   .setAttribute("src","/img/wizard/btn/"+btn+".png");
    //document.querySelector("#modal_form_bg img")
      //  .setAttribute("src","/img/wizard/modal_bg.svg");
    
    // redes sociais 
    document.querySelector("#face img").setAttribute("src","/img/users/facebook.svg");
    
    // document.getElementById("goog")
      //  .setAttribute("src","/img/users/google.svg");
        
    /* link coworkit website
    document.querySelector("#logo_eos a")
        .setAttribute("href","http://eos.done.com.br");
    document.querySelector("#logo_eos a")
        .setAttribute("target","_blank");    
    document.querySelector("#logo_eos a img")
        .setAttribute("src","/img/wizard/coworkit.svg");
      */  
   // document.querySelector("#wizard_form_bg img")
     //   .setAttribute("src","/img/wizard/form_bg.svg");
     
     
     
     // ao sair do campo nome propaga para cadastro da empresa
     document.getElementById("nome").addEventListener("blur",function(){
         var cn = document.getElementById("company_nome");
         if(!cn.value){
             cn.value = this.value;
             document.getElementById("company_apelido").value = this.value;
         }
     });
     
     // ao trocar tipo de empresa
     document.querySelectorAll("input[name=company_tipo]").forEach(function(x){ 
         x.addEventListener("change",function(){ 
             if(this.value === "F"){
                 document.getElementById("company_documento").placeholder = "CPF";
             } else {
                 document.getElementById("company_documento").placeholder = "CNPJ";
             }
         }); 
     });
     
     document.getElementById("company_tipo").setAttribute("checked",true);
     
</script>


</body>
</html>

HTML
