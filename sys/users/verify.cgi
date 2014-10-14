#!/usr/bin/perl

$nacess = "2"; # nacess do dashboard para nenhum usuario ficar sem acesso
require "../cfg/init.pl";
$ID  = &get('ID');
$COD = &get('COD');

print $query->header({charset=>utf8});

print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html id="html">
<head>
	
<script>
/**
 *   Usuario
 *       obj usuario
 */
function Verify(){
    
    /* initialize */
    this.initialize = function() {
        // this.list();
    };
    
    
    // valida 
    this.valida = function(){
        
        if(!\$("#verify_codigo").val()) {
            \$.DDialog({
                type    : "alert",
                message : "Digite um Código !"
            });
            return false;
        }
        
        \$.DActionAjax({
            action : "verify_submit.cgi",
            postFunction : function(x){
                
                try {
                    var r = JSON.parse(x);
                    
                    if(r.status === "error"){
                        \$.DDialog({
                            type    : "alert",
                            message : r.message
                        });
                    } else {
                        eos.logout();
                    }
                    
                } catch(e) {
                    console.log(e);
                }
                
            }
        });
    };
    
    
    // solicita 
    this.solicita = function(){
        
        \$.DActionAjax({
            action : "verify_submit.cgi",
            req    : "solicita=1",
            postFunction : function(x){
                
                try {
                    var r = JSON.parse(x);
                    
                    \$.DDialog({
                        type    : "alert",
                        message : r.message
                    });
                } catch(e) {
                    console.log(e);
                }
                
            }
        });
    };
}


/**
 *   Form
 *       obj formulario
 */
function Form(){
    
    /* initialize */
    this.initialize = function(){
        
            document.getElementById("eye").remove();
            // document.getElementById("corpo").remove();
            document.getElementById("menu_float").remove();
            document.getElementById("user_menu_float").remove();
            document.getElementById("menu_top_right_company_status").remove();
            document.getElementById("DMenuTopRightDropDown").remove();
            document.getElementById("menu_top").remove();        
            // document.getElementById("menu_actions").remove();
            // document.getElementById("main_container").remove();        
            // document.querySelectorAll("#menu_top div").forEach(function(i){ i.remove() });
            
            
            if(document.getElementById("verify")) { 
                document.getElementById("verify").remove();
                // document.getElementById("verify").innerHTML = "Valide seu email !";
            } /* else {
                var d = document.createElement("div");
                    d.id = "verify";
                    d.innerHTML = "Valide seu email !";
                    
                document.getElementById("BODYEOS").appendChild(d);
            } */
            
            
            
    
            var m  = "<div style='height:150px; padding:5px;'>";
                m += "  <input type='text' name='ativacao_codigo' placeholder='Código Ativação ?' style='border:1px solid blue; height:20px;' /> <br>";
                m += "  Digitar Código   <input type='radio' name='ativacao_opt' value='false' checked > <br>";
                m += "  Solicitar Código <input type='radio' name='ativacao_opt' value='true' >";
                m += "</div>";
        
            /*
            \$.DDialog({
                type    : 'confirm',
                title   : 'Valide seu cadastro !',
                message : m, 
                btnYes  : function(){
                    console.log('envia !!');
                }
            });
            */
            
            
            
            \$("#verify_container").DTouchBoxes({
                title : "Insira aqui seu Código Ativação para continuar usando o sistema !"
            });
            eos.template.field.text(\$("#verify_codigo"));
            
            
            this.menu();
            ver = new Verify();
            
    };
    
    this.menu = function(){
        eos.menu.action.new({ // validar
            id       : "icon_verify_valida",
            title    : "validar",
            subtitle : "",
            click    : function(){
                ver.valida();
            }
        });
        
        eos.menu.action.new({ // solicitar
            id       : "icon_users_solicita",
            title    : "código",
            subtitle : "solicitar",
            click    : function(){
                ver.solicita();
            }
        });
    }
}


/**
 *   Document Ready
 */
\$(document).ready(function() { 
    form = new Form();
    form.initialize();
});

</script>
</head>
<body>

    <!-- Formulario -->
    <form >
	
        <div id="verify_container">
            <input type='text' id="verify_codigo" name='verify_codigo' placeholder='Código' /> 
        </div>
                
    </form>
    
</body>
</html>

HTML

