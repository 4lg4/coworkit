#!/usr/bin/perl

$nacess = "81";
require "../../cfg/init.pl";

# vars
$ID  = &get('ID');
$COD = &get('COD');

print $query->header({charset=>utf8});

print<<HTML;

    <!-- Formulario -->
    <form >
	
        <!-- Paginas -->
        <div id="orcamento_rel_page">
                
                <!-- pagina central -->
                <div id="orcamento_rel_page_center">
                    
                    <!-- search -->
                    <div id="search_container">
                        <div id="filter_cat"></div>
                        
                        <div id="dt_end_container">
                            <input type="text" id="dt_end" name="dt_end" placeholder="Data Final" />
                        </div>
                        <div id="dt_ini_container">
                            <input type="text" id="dt_ini" name="dt_ini" placeholder="Data Inicial" />
                        </div>
                    </div>
                    
                    <!-- listagem -->
                    <div id="list_container">
                        <div id="list"></div>
                    </div>
                       
                </div>
                
                <!-- pagina direita -->
                <div id="orcamento_rel_page_right">
                    <!-- listagem -->
                    <div id="orcamento_list_container">
                        <div id="orcamento_list"></div>
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
    orc_rel = new OrcamentoRel();
    orc_rel.initialize();    
});
</script>

HTML

