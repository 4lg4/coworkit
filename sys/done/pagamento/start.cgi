#!/usr/bin/perl

$nacess = "80";
require "../../cfg/init.pl";

# vars
$ID      = &get('ID');
$COD     = &get('COD');
$empresa = &get('empresa');

print $query->header({charset=>utf8});

print<<HTML;

<!-- Formulario -->
<form>

    <!-- Paginas -->
    <div id="pagamentos_page">
        
            <!-- pagina esquerda -->
            <div id="pagamentos_page_left">
                <!-- listagem -->
                <div id="pagamento_list_container">
                    <div id="pagamento_list"></div>
                </div>
            </div>
            
            <!-- pagina central -->
            <div id="pagamentos_page_center">
                    
                    
                <!-- cliente -->
                <div id="dados_container">
                    
                    <div id="cliente_container">
                        <div> Cliente </div>
                        <div id="cliente"></div>
                    </div>
                    
                    <!-- plano -->
                    <div id="plano_container">
                        <div> Plano </div>
                        <div id="plano"></div>
                    </div>
                </div> 
                
                <!-- plano features -->
                <div id="features_container">
                    <div id="features"></div>
                </div>
                    
                <!-- pagamentos -->
                <div id="pagamentos_container">
                    <div id="pagamentos"></div>
                </div>
                    
            </div>

    </div>
    
    
    <input type="hidden" name="COD" id="COD" value="$COD">
</form>
    


<script> 
    /**
     *   Document Ready
     */
    \$(document).ready(function() { 
        pagto = new Pagamento();
        pagto.initialize();   
    });
</script>


HTML

