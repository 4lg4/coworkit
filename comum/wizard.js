/**
 *  login.js
 *  
 *  Login    
 *      funcoes basicas para funcionamento do login
 */


/**
 *  DDialog
 *      Modal de mensagem
 */
function DDialog(msg,field){
    wizard.dialog(msg,field);
}


/**
 *  For Each 
 *      implements forEach on node lists
 */
NodeList.prototype.forEach = function (fn, scope) {
    'use strict';
    var i, len;
    for (i = 0, len = this.length; i < len; ++i) {
        if (i in this) {
            fn.call(scope, this[i], i, this);
        }
    }
};






/**
 *  Wizard OBJ 
 */
function Wizard() {
    var w = this;
    
    /* ao inicializar */
    this.initialize = function(){
        this.loader.remove();
    };
    
    /* loader */
    this.loader = {
        /* adiciona loader */
        add : function(msg){
            if(msg) {
                console.log(msg);
            }
            document.getElementById("wizard_loader").classList.add("loading");
        },
    
        /* remove loader */
        remove : function(){
            document.getElementById("wizard_loader").classList.remove("loading");
        }    
    };
    
    
    /* salva */
    this.save = function() {
        
        var username           = document.getElementById("username").value
        ,   password           = document.getElementById("password").value
        ,   password_conf      = document.getElementById("password_conf").value
        ,   nome               = document.getElementById("nome").value
        ,   company_nome       = document.getElementById("company_nome").value
        ,   company_apelido    = document.getElementById("company_apelido").value
        ,   company_tipo       = document.querySelector("input[name=company_tipo]:checked").value
        ,   company_documento  = document.getElementById("company_documento").value
        ,   captcha_challenge  = document.getElementById("recaptcha_challenge_field").value
        ,   captcha_response   = document.getElementById("recaptcha_response_field").value;
        
        if(!this.test.email(username)){
            this.dialog("escolha um email válido","username");
            return false;
        }
        
        if(!this.test.password.equals(password,password_conf)){
            this.dialog("senha inválida","password");
            return false;
        } else if(!this.test.password.strengh(password)){
            this.dialog("senha fraca","password");
            return false;
        }
        
        // salva
        var data = new FormData();
            data.append("username",username);
            data.append("password",password);
            data.append("nome",nome);
            data.append("company_nome",company_nome);
            data.append("company_apelido",company_apelido);
            data.append("company_tipo",company_tipo);
            data.append("company_documento",company_documento);
            data.append("recaptcha_challenge_field",captcha_challenge);
            data.append("recaptcha_response_field",captcha_response);
        
        // facebook login ? get data
        //document.querySelectorAll(".fb").forEach(function(f){
         //   data.append(f.name,f.value);
        //});
        
        // converte retorno em campos
        for(var x in logins ) { 
            data.append("fb_"+x,logins[x]);
            /*
            var f = document.createElement("input");
                f.type  = "hidden";
                f.name  = "fb_"+x;
                f.value = response[x];
                f.classList.add = "fb_fields";
            document.getElementById("wizards").appendChild(f);
            */
        }
        
        // loader
        this.loader.add("Preparando ambiente, por favor aguarde.");
        
        // abre conexao
        req = new XMLHttpRequest();
        req.open('POST', "edit_submit.cgi", false); 
        req.setRequestHeader('Accept-Encoding', 'application/json');
        req.setRequestHeader('Accept-Charset', 'utf-8');
        req.send(data);
                    
        if(req.status == 200){ console.log(req.responseText);
            
            w.loader.remove(); // remove loader
            
            var res = JSON.parse(req.responseText);
            if(res.status === "error"){
                // modal
                w.dialog(res.message,res.field);
                //alert(res.message);
                // atualiza captcha
                Recaptcha.reload();
                
            } else {
                
                // loga no sistema
                var form = document.getElementById("logon");
                    form.action = "/sys/logon/login.cgi";
                    form.target = "temp";
                    form.submit();
                
            }
            
        } else {
			console.log(req);
			return false; 
        }
    };
    
    // testes
    this.test = {
        password : {
            strengh : function(p){
                if(!p.match(/.{6,}/) || p.match(/\s+/) || !p.match(/[a-z]|[A-Z]/) || p.match(/\\|\'|\"/)) {
            		return false;
                } else {
            		return true;
            	}
            },
            equals : function(p,pc){
                if(p === pc){
                    return true;
                } else {
                    return false;
                }
            }
        },
        
        /* testa email */
        email : function(email) {
    	    var regex = new RegExp(/^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i);
	
    	    if(regex.test(email)) {
    		    return true;
    	    } else {
    		    return false;
            }
        },
    };
    
    /**
     *  Modal de mensagem
     */
    this.dialog = function(msg,field){
        // block screen
        document.getElementById("modal_container").setAttribute("class","modal_container_show");
    
        // add text
        document.getElementById("modal_form_text").innerHTML = msg;
    
        document.getElementById("modal_form_btn").removeEventListener("click",function(){}); // remove click do botao
        document.getElementById("modal_form_btn").addEventListener("click",function(){
        
            document.getElementById("modal_container").setAttribute("class","");
            document.getElementById(field).focus();
        });
    }
}

    

