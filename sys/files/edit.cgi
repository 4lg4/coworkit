#!/usr/bin/perl

$nacess = "69";
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
function Files(){
    
    /* initialize */
    this.initialize = function() {
        this.list();
    };
    
    /* list, lista de usuarios */
    this.list = function() {
        \$.DActionAjax({
            action : "edit_list.cgi",
            loader : \$("#files_list")
        });
    }
    
    /* editar */
    this.edit = function(){
        
    };
}


/**
 *   Form
 *       obj formulario
 */
function Form(){
    
    /* initialize */
    this.initialize = function(){
        files = new Files();
        files.initialize();
    }
    
    /* menu */
    this.menu = function(){

    };
    
    /* salvar */
    this.save = function(){
        
    };
    
    /* editar */
    this.edit = function(x){
        
    };
    
    /* novo */
    this.new = function(){

    };
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
	
        <!-- DTouchPages -->
        <div id="files_page">
            
                <div class="files_container_center">
                    
                    <!-- lista de usuarios -->
                    <div id="files_list"></div>
                    
                </div>                

        </div>
        
        <input type="hidden" name="COD" id="COD" value="$COD">
    </form>
    
</body>
</html>

HTML

