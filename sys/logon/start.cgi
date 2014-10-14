#!/usr/bin/perl

# libs
require "../cfg/init.pl";

# vars
# $empresa{nome}   = &get("empresa");
$nomobileme      = &get("nomobileme");
# $empresa{codigo} = "";


# se for o ambiente de testes
if($VER ne ""){
    $freeze_color  = "<style>";
    $freeze_color .= "  #login_form {";
    $freeze_color .= "      background: linear-gradient(45deg, rgb(0, 106, 255) 0%, rgb(0, 106, 255) 50%) repeat scroll 0% 0% transparent !important;";
    $freeze_color .= "  }";
    $freeze_color .= "</style>";
}    



# headers
print $query->header({charset=>utf8});

# verfica empresa
# if($empresa{nome} ne "") {
#    
#     	$query_emp = &DBE("select * from empresa where apelido <=> '$empresa_nome' ");
#     	if($query_emp->rows == 1) {
#     		$linha           = $query_emp->fetchrow_hashref;
#     		$empresa{codigo} = $linha->{'codigo'};
#     		$empresa{nome}   = $linha->{'nome'};
#     		$empresa{logo}   = $linha->{'codigo'};
#     	} else {
#     		$empresa{nome} = "EOS - IT Software for IT People";
#     		$empresa{logo} = 0;
#     	}
#         
# } else {
# 	$empresa{nome} = "EOS - IT Software for IT People";
# 	$empresa{logo} = 0;
# }

# monta o caminho do logotipo
# $logo = "/img/logos/".$logo.".png";

# arquivo de login
# pegar todos os dados da empresa baseado na string do nome da empresa

print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
		<meta name="viewport" content="width=device-width, minimum-scale=1, maximum-scale=1">
		
		<title>:::: CoworkIT! :::: $VER</title>
		<link rel="shortcut icon" href="/done.ico">
        
        <!-- general libs -->
            
		<!-- login libs -->
		<link href="/css/login.css" rel="stylesheet" type="text/css" />	
		<script language="JavaScript" src="/comum/login.js"></script>
        
        
        <!-- <script language="JavaScript" src="/comum/facebook.js"></script> -->
        
        
        $DEVPWD
        $freeze_color
	</head>

<body>
	<form name="logon" id="logon" method="post">

		<div id="login_container" align="center">
			
    		<div id="login_form">
                <div id="login_form_bg"><img /></div>
                
                <div id="login_form_fields_container">
        			<div id="login_form_user">
        				<img />
        			</div>
                    <div id="login_form_fields">
        			    <input type="text"     placeholder="Usuário" name="username" id="username"  tabindex="1" autocomplete="off">
        			    <input type="password" placeholder="Senha"   name="password" id="password"  tabindex="2" autocomplete="off">
                    </div>
        			<div id="login_form_btn">
        				<div tooltip="Login !" class="tooltip"><img name="btn_login" id="btn_login" tabindex="3" /></div>
        			</div>
                </div>
    		</div>
            
            <div id="logins_form" tooltip="Entre com seu login do Facebook" class="tooltip">
                <img id='face'  />
                <img id='goog'  />
            </div>
            
            <!--
            <div id="logo_eos" >
            	<a><img /></a>
            </div>
            -->
		</div>

    <div id="logins"></div>
    
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
            <div id="modal_form_btn" tooltip="OK Entendi, vou tentar novamente !!" class="tooltip" tabindex="-1"><img name="modal_btn" id="modal_btn" /></div>
        </div>
    </div>
</div>

<!-- footer -->
<div id="login_footer_container">
    <div id="login_footer" tooltip="Navegadores homologados" class="tooltip_up">
    	<span>
    		<img src="/img/login/browser_safari.png" style="margin-right:15px; height:40px;" border="0">
    		<img src="/img/login/browser_chrome.png" style="margin-right:15px; height:40px;" border="0">
    		<img src="/img/login/browser_firefox.png" style="height:40px;" border="0">
    	</span>
    </div>
</div>

<!--
<div id="login_google" style="top:40px; min-height:20px; position:absolute; right:0px; z-index:9999; ">
<span id="signinButton">
  <span
    class="g-signin"
    data-callback="signinCallback"
    data-clientid="192681868087.apps.googleusercontent.com"
    data-cookiepolicy="single_host_origin"
    data-requestvisibleactions="http://schemas.google.com/AddActivity"
    data-scope="https://www.googleapis.com/auth/plus.login">
  </span>
</span>
</div>
-->

<div id="fb-root"></div>
<script>
    (function(d, s, id) {
        var js, fjs = d.getElementsByTagName(s)[0];
        
        if (d.getElementById(id)) {
            return;
        }
        
        js = d.createElement(s); 
        js.id = id;
        js.src = "//connect.facebook.net/en_US/all.js#xfbml=1&appId=178169535709072";
        fjs.parentNode.insertBefore(js, fjs);
        
    }(document, 'script', 'facebook-jssdk'));
</script>

<!-- <div class="fb-login-button" data-max-rows="1" data-size="icon" data-show-faces="false" data-auto-logout-link="false"></div> -->

<script>
/*
    window.fbAsyncInit = function() {
        FB.init({
            appId      : '178169535709072', // App ID
            channelUrl : '//coworkit.com.br/',
            status     : true, 
            cookie     : true, 
            xfbml      : true  
        });
     } 
     
  */   
     
     document.getElementById("face").addEventListener("click",function(){
         FB.login(function(response) {
            if (response.authResponse) {
              //console.log('Welcome!  Fetching your information.... ');
              FB.api('/me', function(response) {
                
                  var fi = document.createElement("input");
                      fi.type  = "hidden";
                      fi.name  = "fb_id";
                      fi.value = response.id;
                     //  1451834662
                  var fl = document.createElement("input");
                      fl.type  = "hidden";
                      fl.name  = "fb_login";
                      fl.value = response.email;
                      
                      
                  document.getElementById("username").value = response.email;
                  document.getElementById("password").value = "*";
                      
                  document.getElementById("logins").appendChild(fi);
                  document.getElementById("logins").appendChild(fl);
                  
                  checkForm(1);
              });
            } else {
                DDialog("Usuário não logado ou autorizado","username");
            }
          }, {scope: 'email'});    
     });
</script>

<!-- <fb:login-button show-faces="true" width="200" max-rows="1" style="position: absolute; top:0px; left:0px; z-index:999"></fb:login-button> -->



<!-- Place this asynchronous JavaScript just before your </body> tag -->
    <script type="text/javascript">
    /*
      (function() {
       var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;
       po.src = 'https://apis.google.com/js/client:plusone.js';
       var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);
     })();
     
     
     
     function signinCallback(authResult) {
       if (authResult['access_token']) {
         // Update the app to reflect a signed in user
         // Hide the sign-in button now that the user is authorized, for example:
         // document.getElementById('signinButton').setAttribute('style', 'display: none');
         console.log('Sign-in state: conectado ');
         console.log(authResult);
       } else if (authResult['error']) {
         // Update the app to reflect a signed out user
         // Possible error values:
         //   "user_signed_out" - User is signed-out
         //   "access_denied" - User denied access to your app
         //   "immediate_failed" - Could not automatically log in the user
         console.log('Sign-in state: ' + authResult['error']);
       }
     }
    */
    </script>


<!--
    <div id="login_logo" align="center">
	    <img src="$logo" alt="$emp_nome" title="$emp_nome" border="0" onError="this.src='/img/logos/1.png'" />
    </div>
-->

<script>
    // inicia login obj
    var login = new Login();
        login.initialize();
    
    // ajusta css se for mobile
    if(login.device.check() === "mobile") {
        login.css.load("/css/login_mobile.css");
    }
        
    // foco no primeiro campo
    document.forms[0].elements[0].focus();

    // username looses focus, put all 
    /*
    document.getElementById("username").addEventListener("blur", function(){
        this.value = this.value.toLowerCase();
    });
    */
    
    // submete formulario com enter
    document.querySelectorAll("#login_form_fields input").forEach(function(item){
        item.addEventListener("keydown",function(e){
            if(e.which === 13) {
                e.stopPropagation();
                checkForm();
                // document.forms[0].submit();
            }
        })
    });
    
    // controle body
    // document.querySelector("body").addEventListener("focus",function(e){ console.log(e); document.forms[0].elements[0].focus(); });
    /*
    document.querySelector("body").addEventListener("keydown",function(e){
        if(e.which === 37 || e.which === 38 || e.which === 39 || e.which === 40) {
            e.preventDefault();
        }
    });
    */
    
    // submete formulario com click na imagem
    document.getElementById("btn_login").addEventListener("click",function(){
        checkForm();
        // document.forms[0].submit();
    });

    // adiciona imagem random user
    
    document.querySelector("#login_form_user img")
        .setAttribute("src","/img/login/coworkit.svg");
        // .setAttribute("src","/img/login/user/"+randomInt(1, 6)+".png");
    
    // adiciona imagem random btn
    var btn = randomInt(1, 25);
    document.querySelector("#login_form_btn img")
        .setAttribute("src","/img/login/btn/"+btn+".png");
    
    // modal    
    document.querySelector("#modal_form_btn img")
        .setAttribute("src","/img/login/btn/"+btn+".png");
    // document.querySelector("#modal_form_bg img")
       // .setAttribute("src","/img/login/modal_bg.svg");
    
    // redes sociais 
    document.getElementById("face")
        .setAttribute("src","/img/users/facebook.svg");
    document.getElementById("goog")
        .setAttribute("src","/img/users/google.svg");
        
    /* link coworkit website
    document.querySelector("#logo_eos a")
        .setAttribute("href","http://eos.done.com.br");
    document.querySelector("#logo_eos a")
        .setAttribute("target","_blank");    
    document.querySelector("#logo_eos a img")
        .setAttribute("src","/img/login/coworkit.svg");
      */  
   // document.querySelector("#login_form_bg img")
     //   .setAttribute("src","/img/login/form_bg.svg");
</script>

</body>
</html>

HTML
