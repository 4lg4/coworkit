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
    // block screen
    document.getElementById("modal_container").setAttribute("class","modal_container_show");
    
    // add text
    document.getElementById("modal_form_text").innerHTML = msg;
    
    var btn = document.getElementById("modal_form_btn");
        btn.focus();
        btn.removeEventListener("click",function(){}); // remove click do botao    
        btn.addEventListener("keydown",function(){}); // remove enter event
    
    // enter, controle      
    btn.addEventListener("keydown",function(e){
        if(e.which === 13) {
            d.retorno();
        }
    });
    
    // click, controle 
    btn.addEventListener("click",function(){
        d.retorno();
    });
    
    // retorno do dialog
    d = this;
    this.retorno = function(){
        document.getElementById("modal_container").setAttribute("class","");
        document.getElementById(field).focus();
    };
}


/**
 *  Check Form
 *      executa testes no formulario
 */
function checkForm(l) {
    
    //if(!l) {
        var user  = document.getElementById("username").value
        ,   pwd   = document.getElementById("password").value
        ,   field;
    
        /* verifica password */
    	if(!pwd || !checkPwd(pwd)) {
    		field = document.getElementById("password");
    	}
    
        /* verifica usuario */
        if((user.search(/\@/) > -1 && !isMail(user)) || !user.toLowerCase().match(/[a-z]/)) { // se for login com email
            field = document.getElementById("username");
        }
        //}
    
    if(field && !l){
        DDialog("usuário ou senha inválidos",field.name);
    } else { 
        // if(!l){
        //    document.getElementById("logins").innerHTML = "";  // limpa variaveis de outros logins
        // }
        
        // atualiza cookies
        login.form.save();
        
        // submete formulario
        document.forms[0].action = "/sys/logon/login.cgi";
        // document.forms[0].action = "/login";
        document.forms[0].target = "temp";
        document.forms[0].submit();
    }
}

/**
 *  Check Pwd 
 *      testa campos do formulario antes do envio 
 */
function checkPwd(p) {
    if(!p || !p.match(/.{6,}/) || p.match(/^\\s+$/)) {
		return false;
    } else {
		return true;
	}
}

/**
 *  is Mail
 *      chek if string are email
 */
function isMail(email) {
	var regex = new RegExp(/^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i);
	
	if(regex.test(email)) {
		return true;
	} else {
		return false;
    }
}

/**
 *  Random Int
 *      generate random integer numbers from a range
 */
function randomInt(min, max) {
      return Math.floor(Math.random() * (max - min + 1) + min);
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


function Login() {
    var l = this;
    
    /* initialize */
    this.initialize = function(){
        this.form.fill();
    };
    
    /* verifica device */
    this.device = {
        check : function(){
            if( /Android|webOS|iPhone|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
                return "mobile";
            } else if( /iPad/i.test(navigator.userAgent) ) {
                return "ipad";
            } else {
                return "desktop";
            }
        }
    };
    
    /* carrega / remove CSS */
    this.css = {
        load : function(file) {
        	var fileref=document.createElement("link")
        		fileref.setAttribute("rel", "stylesheet")
        	  	fileref.setAttribute("type", "text/css")
        	  	fileref.setAttribute("href", file)
	
        	document.getElementsByTagName("head")[0].appendChild(fileref);
        },
        remove : function(file) {
        	document.querySelector('link[rel=stylesheet][href="'+file+'"]').remove();
        }
	};
    
    
    /* formulario preenchimento */
    this.form = {
        fill : function(){
            // verifica cookie para preenchimento do formulario
            if(l.cookies.check("coworkit_username")){
                document.getElementById("username").value = l.cookies.get("coworkit_username");
                document.getElementById("password").value = l.cookies.get("coworkit_password");
            }
        },
        
        save : function(){
            l.cookies.set("coworkit_username",document.getElementById("username").value);
            l.cookies.set("coworkit_password",document.getElementById("password").value);
        }
    }
    
    
    /* manipula cookies */
    this.cookies = {
 
        // this gets a cookie and returns the cookies value, if no cookies it returns blank ""
        get: function(c_name) {
            if (document.cookie.length > 0) {
                var c_start = document.cookie.indexOf(c_name + "=");
                if (c_start != -1) {
                    c_start = c_start + c_name.length + 1;
                    var c_end = document.cookie.indexOf(";", c_start);
                    if (c_end == -1) {
                        c_end = document.cookie.length;
                    }
                    return unescape(document.cookie.substring(c_start, c_end));
                }
            }
                return "";
        },
 
        // this sets a cookie with your given ("cookie name", "cookie value", "good for x days")
        set: function(c_name, value, expiredays) {
            var exdate = new Date();
            exdate.setDate(exdate.getDate() + expiredays);
            document.cookie = c_name + "=" + escape(value) + ((expiredays == null) ? "" : "; expires=" + exdate.toUTCString());
        },
 
        // this checks to see if a cookie exists, then returns true or false
        check: function(c_name) {
            c_name = l.cookies.get(c_name);
            if (c_name != null && c_name != "") {
                return true;
            } else {
                return false;
            }
        }
 
    };
};
