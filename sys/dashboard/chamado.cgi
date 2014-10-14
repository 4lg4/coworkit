#!/usr/bin/perl

#
# chamado.cgi
#
# Lista de chamados que aparecem no modulo
#

$nacess = "2";
# $nacess_more = "or menu = 74";
require "../cfg/init.pl";

$ID = &get('ID');
	
print $query->header({charset=>utf8});


#
#   Cliente do Parceiro
#       99 = cliente do parceiro
#
if($USER->{tipo} eq "99") { 
    
    #
    #   Meus chamados
    #
    $ttitle  = "<div class=\"DTouchRadio_list_title\">";
    $ttitle .= " 	<div style=\"width:5%\">Codigo</div>";
    $ttitle .= " 	<div style=\"width:12%\">Data</div>";
    $ttitle .= " 	<div style=\"width:5%\">Tempo</div>";
    $ttitle .= " 	<div style=\"width:20%\">Solicitante</div> ";
    $ttitle .= "    <div style=\"width:55%\">Problema</div> ";
    $ttitle .= "</div>";

    $DB = &DBE("select * from tkt_full where finalizado is null and (usuario = $USER->{usuario} or usuario_executor = $USER->{usuario}) order by data asc");

    if($DB->rows() > 0) {
    	while($t = $DB->fetchrow_hashref) { 
    		# ajustes variaveis
    		$t->{problema} = &get($t->{problema},"NEWLINE_SHOW");
        
    		$t->{data}           = &dateToShow($t->{data});
            $t->{tempo_previsao} = &dateToShow($t->{tempo_previsao});
		        
            # ticket criado pelo usuario logado
            if($t->{usuario} eq $USER->{usuario}){
        		$tar .= "{ ";
                $tar .= "    val : $t->{codigo},";
                $tar .= "    descrp:'";
        		$tar .= "        <div class=\"DTouchRadio_list_line\">";
        		$tar .= " 	        <div style=\"width:5%\">#$t->{codigo}</div> ";
        		$tar .= " 	        <div style=\"width:12%\">$t->{data}</div>";
        		$tar .= " 	        <div style=\"width:5%\">$t->{tempo_previsao}</div>";
                $tar .= " 	        <div style=\"width:20%\">$t->{solicitante}</div> ";
        		$tar .= " 	        <div style=\"width:55%\">$t->{problema}</div> ";
        		$tar .= "        </div>";
                $tar .= "    '";
                $tar .= "},";
            }
    	}
    } else {
        $tar = "{ val:0, descrp:'<div style=\"width:100%\">Nenhum registro encontrado !</div>' }";
    }


    #
    #   Chamados orfaos
    #
    $DB = &DBE("select t.* from tkt_full as t where (select count(ta.codigo) from tkt_acao as ta where ta.tkt = t.codigo) = 0 and t.finalizado is null and empresa_logada = $USER->{empresa}");

    if($DB->rows() > 0) {
    	while($t = $DB->fetchrow_hashref) { 
    		# ajustes variaveis
    		$t->{problema} = &get($t->{problema},"NEWLINE_SHOW");
        
    		$t->{data}           = &dateToShow($t->{data});
            $t->{tempo_previsao} = &dateToShow($t->{tempo_previsao});
		        
            # ticket criado pelo usuario logado
            # if($t->{usuario} eq $USER->{usuario}){
        		$tao .= "{ ";
                $tao .= "    val : $t->{codigo},";
                $tao .= "    descrp:'";
        		$tao .= "        <div class=\"DTouchRadio_list_line\">";
        		$tao .= " 	        <div style=\"width:5%\">#$t->{codigo}</div> ";
        		$tao .= " 	        <div style=\"width:12%\">$t->{data}</div>";
        		$tao .= " 	        <div style=\"width:5%\">$t->{tempo_previsao}</div>";
                $tao .= " 	        <div style=\"width:20%\">$t->{solicitante}</div> ";
        		$tao .= " 	        <div style=\"width:55%\">$t->{problema}</div> ";
        		$tao .= "        </div>";
                $tao .= "    '";
                $tao .= "},";
            # }
    	}
    } else {
        $tao = "{ val:0, descrp:'<div style=\"width:100%\">Nenhum registro encontrado !</div>' }";
    }
    
    
    #
    #   Todos
    #
    $alltitle  = "<div class=\"DTouchRadio_list_title\">";
    $alltitle .= " 	<div style=\"width:5%\">Codigo</div>";
    $alltitle .= " 	<div style=\"width:15%\">Data Abertura</div>";
    $alltitle .= " 	<div style=\"width:10%\">Responsável</div>";
    $alltitle .= " 	<div style=\"width:15%\">Data Previsão</div>";
    $alltitle .= " 	<div style=\"width:10%\">Solicitante</div>";
    $alltitle .= " 	<div style=\"width:40%\">Solicitação</div> ";
    $alltitle .= "</div>";

    $DB = &DBE("
            select 
                * 
            from 
                tkt_full 
            where 
                finalizado is null and 
                usuario = $USER->{usuario} or
                empresa_logada = $USER->{empresa} or
                cliente = $USER->{empresa}
            order by 
                data 
            desc
    ");

    if($DB->rows() > 0) {
    	while($t = $DB->fetchrow_hashref) { 
        
        		# ajustes variaveis
        		$t->{problema}      = &get($t->{problema},"NEWLINE_SHOW");                
        		$t->{data}          = &dateToShow($t->{data});
                $t->{data_previsao} = &dateToShow($t->{data_previsao});
		
                # tarefas
        		$allt .= "{ ";
                $allt .= "    val : $t->{codigo},";
                $allt .= "    descrp:'";
        		$allt .= "        <div class=\"DTouchRadio_list_line\">";
        		$allt .= " 	        <div style=\"width:5%\">#$t->{codigo}</div> ";
        		$allt .= " 	        <div style=\"width:15%\">$t->{data}</div>";
                $allt .= " 	        <div style=\"width:10%\">$t->{responsavel_nome}</div>";
                $allt .= " 	        <div style=\"width:15%\">$t->{data_previsao}</div>";
        		$allt .= " 	        <div style=\"width:10%\">$t->{solicitante}</div>";
        		$allt .= " 	        <div style=\"width:40%\">$t->{problema}</div>";
        		$allt .= "        </div>";
                $allt .= "    '";
                $allt .= "},";     
            }
            
    } else {
        $allt = "{ val:0, descrp:'<div style=\"width:100%\">Nenhum registro encontrado !</div>' }";
    }
    
    
    print "<script>\$('#tkt_all_tab').show();</script>";
    

# retorno do codigo 
print<<HTML;
<script>

    var content  = '<div id="tkt_tabs">';
        content += '    <ul>';
        content += '        <li id="tkt_all_tab"><a href="#tkt_all">Em Andamento</a></li>';
        content += '        <li><a href="#tkt_noresp">Aguardando Atendimento</a></li>';
        content += '        <li><a href="#tkt_resp">Tickets que criei</a></li>';
        content += '    </ul>';
        content += '    <div id="tkt_all"><div></div></div>';
        content += '    <div id="tkt_noresp"><div></div></div>';
        content += '    <div id="tkt_resp"><div></div></div>';
        content += '</div>';

	\$("#dashboard_tkt_container").html(content);
	
        
	\$("#tkt_noresp div").DTouchRadio({ 
        title: '$ttitle',
		addItem:[ $tao ], 
		orientation:'vertical',
		click: function(res) {
            if(res.value === "0"){
                return false;
            }
            
			eos.core.call.module.tkt(res.value); // edita tkt
		}
    });
           
	\$("#tkt_resp div").DTouchRadio({ 
        title: '$ttitle',
		addItem:[ $tar ], 
		orientation:'vertical',
		click: function(res) { 
            if(res.value === "0"){
                return false;
            }
            
			eos.core.call.module.tkt(res.value); // edita tkt
		}
	});
    
	\$("#tkt_all div").DTouchRadio({ 
        title: '$alltitle',
		addItem:[ $allt ], 
		orientation:'vertical',
		click: function(res) { 
            if(res.value === "0"){
                return false;
            }
            
			eos.core.call.module.tkt(res.value); // edita tkt
		}
	});	
    
    
    // ajuste widget chamados
    \$("#dashboard_tkt_container .DTouchBoxes_title").html("Chamados em aberto");
            
    \$("#tkt_tabs").tabs();
    
</script>
HTML
   
   
   
   
   
   
   
   
#
#   Parceiro TI
#
} else {
    
    # Chamados
    $ttitle  = "<div class=\"DTouchRadio_list_title\">";
    $ttitle .= " 	<div style=\"width:5%\">Codigo</div>";
    $ttitle .= " 	<div style=\"width:22%\">Data</div>";
    $ttitle .= " 	<div style=\"width:5%\">Tempo</div>";
    $ttitle .= " 	<div style=\"width:20%\">Solicitante</div> ";
    $ttitle .= "    <div style=\"width:45%\">Problema</div> ";
    $ttitle .= "</div>";

    $DB = &DBE("
        select 
            *,
            to_char(t.data_previsao, 'YYYYMMDDHH24MISS') as data_comparison,
            to_char(t.data_previsao - interval '12 hours', 'YYYYMMDDHH24MISS') as data_warning
        from 
            tkt_full as t where finalizado is null and (usuario = $USER->{usuario} or usuario_executor = $USER->{usuario}) order by data asc");

    if($DB->rows() > 0) {
    	while($t = $DB->fetchrow_hashref) { 
            
            $color = "";
            if($t->{data_warning} <= timestamp("comparison") && $t->{data_comparison} >= timestamp("comparison")) { 
                $color = "background-color: #D2B35F; border-radius:5px;";
            } elsif($t->{data_comparison} <= timestamp("comparison")) {
                $color = "background-color: #BF7877; border-radius:5px;";
            }
            
    		# ajustes variaveis
    		$t->{problema} = &get($t->{problema},"NEWLINE_SHOW");
        
    		$t->{data}           = &dateToShow($t->{data});
            $t->{tempo_previsao} = &dateToShow($t->{tempo_previsao});
            $t->{data_previsao}  = &dateToShow($t->{data_previsao});
		        
            # ticket criado pelo usuario logado
            if($t->{usuario} eq $USER->{usuario}){
        		$tar .= "{ ";
                $tar .= "    val : $t->{codigo},";
                $tar .= "    descrp:'";
        		$tar .= "        <div class=\"DTouchRadio_list_line\"  style=\"$color\">";
        		$tar .= " 	        <div style=\"width:5%\">#$t->{codigo}</div> ";
        		$tar .= " 	        <div style=\"width:22%\">$t->{data} | $t->{data_previsao}</div>";
        		$tar .= " 	        <div style=\"width:5%\">$t->{tempo_previsao}</div>";
                $tar .= " 	        <div style=\"width:20%\">$t->{solicitante}</div> ";
        		$tar .= " 	        <div style=\"width:45%\">$t->{problema}</div> ";
        		$tar .= "        </div>";
                $tar .= "    '";
                $tar .= "},";
            }
    	}
    } else {
        $tar = "{ val:0, descrp:'<div style=\"width:100%\">Nenhum registro encontrado !</div>' }";
    }




    #
    #   Tarefas
    #
    $tatitle  = "<div class=\"DTouchRadio_list_title\">";
    $tatitle .= " 	<div style=\"width:5%\">Codigo</div>";
    $tatitle .= " 	<div style=\"width:15%\">Data</div>";
    $tatitle .= " 	<div style=\"width:10%\">Responsável</div>";
    $tatitle .= " 	<div style=\"width:20%\">Interno</div> ";
    $tatitle .= "	<div style=\"width:45%\">Externo</div> ";
    $tatitle .= "</div>";

    $DB = &DBE("
            select 
                *,
                to_char(tkt_data_previsao, 'YYYYMMDDHH24MISS') as data_comparison,
                to_char(tkt_data_previsao - interval '12 hours', 'YYYYMMDDHH24MISS') as data_warning 
            from 
                tkt_acao_tkt 
            where 
                tkt_finalizado is null and 
                executor = $USER->{usuario} and
                ( 
                    tempo is null or
                    to_char(tempo, 'HH24:MI:SS') = '00:00:00'
                )
            order by 
                tkt_codigo, 
                data 
            desc
    ");

    if($DB->rows() > 0) {
    	while($t = $DB->fetchrow_hashref) { 
        
            if($tkt ne $t->{tkt_codigo}){ # mostra somente o ultimo encaminhamento como sendo a tarefa ativa do ticket
        
                $color = "";
                if($t->{data_warning} <= timestamp("comparison") && $t->{data_comparison} >= timestamp("comparison")) { 
                    $color = "background-color: #D2B35F; border-radius:5px;";
                } elsif($t->{data_comparison} <= timestamp("comparison")) {
                    $color = "background-color: #BF7877; border-radius:5px;";
                }
            
        		# ajustes variaveis
        		$t->{descrp}          = &get($t->{descrp},"NEWLINE_SHOW");
                $t->{executor_descrp} = &get($t->{executor_descrp},"NEWLINE_SHOW");
        
        		$t->{data}     = &dateToShow($t->{data});
                $t->{tempo}    = &dateToShow($t->{tempo});
		
                # tarefas
        		$ta .= "{ ";
                $ta .= "    val : $t->{tkt_codigo},";
                $ta .= "    descrp:'";
        		$ta .= "        <div class=\"DTouchRadio_list_line\" style=\"$color\">";
        		$ta .= " 	        <div style=\"width:5%\">#$t->{tkt_codigo}</div> ";
        		$ta .= " 	        <div style=\"width:15%\">$t->{data}</div>";
        		$ta .= " 	        <div style=\"width:10%\">$t->{usuario_nome}</div>";
        		$ta .= " 	        <div style=\"width:20%\">$t->{descrp}</div>";
        		$ta .= " 	        <div style=\"width:45%\">$t->{executor_descrp}</div> ";
        		$ta .= "        </div>";
                $ta .= "    '";
                $ta .= "},";     
            }
        
            $tkt = $t->{tkt_codigo};
    	}
    } else {
        $ta = "{ val:0, descrp:'<div style=\"width:100%\">Nenhum registro encontrado !</div>' }";
    }
    
    



    #
    # [INI] Chamados por area
    #
    $tareatitle  = "<div class=\"DTouchRadio_list_title\">";
    $tareatitle .= " 	<div style=\"width:15%\">Área</div>";
    $tareatitle .= " 	<div style=\"width:9%\">Empresa</div>";
    $tareatitle .= " 	<div style=\"width:5%\">Cod</div>";
    $tareatitle .= " 	<div style=\"width:20%\">Data Abertura / Previsão</div>";
    $tareatitle .= " 	<div style=\"width:10%\">Responsável</div>";
    $tareatitle .= "	<div style=\"width:25%\">Problema</div> ";
    $tareatitle .= "</div>";
    
    $DB = &DBE("
            select 
                t.*,
    			p.descrp as plano_descrp,
    			ea.img as area_img,
                to_char(t.data_previsao, 'YYYYMMDDHH24MISS') as data_comparison,
                to_char(t.data_previsao - interval '12 hours', 'YYYYMMDDHH24MISS') as data_warning 
            from 
                tkt_full as t 
    		left join
    			empresa_area_tipo as ea on ea.codigo = t.area
            left join
    			prod_servicos as p on p.codigo = t.plano
    		where 
    			t.finalizado is null and 
    			empresa_logada = $USER->{empresa}
            order by
                ea.descrp, t.cliente
    ");

    if($DB->rows() > 0) {
    	while($t = $DB->fetchrow_hashref) { 
    		# ajustes variaveis
    		$t->{problema} = &get($t->{problema},"NEWLINE_SHOW");
        
            $color = "";
            if($t->{data_warning} <= timestamp("comparison") && $t->{data_comparison} >= timestamp("comparison")) { 
                $color = "background-color: #D2B35F; border-radius:5px;";
            } elsif($t->{data_comparison} <= timestamp("comparison")) {
                $color = "background-color: #BF7877; border-radius:5px;";
            }
            
    		$t->{data}           = &dateToShow($t->{data});
            $t->{tempo_previsao} = &dateToShow($t->{tempo_previsao});
            $t->{data_previsao}  = &dateToShow($t->{data_previsao});
		        
            # ticket criado pelo usuario logado
            # if($t->{usuario} eq $USER->{usuario}){
        		$tarea .= "{ ";
                $tarea .= "    val : $t->{codigo},";
                $tarea .= "    descrp:'";
        		$tarea .= "        <div class=\"DTouchRadio_list_line\" style=\"$color\">";
                $tarea .= " 	        <div style=\"width:15%\"><img src=\"$t->{area_img}\" style=\"height:30px\" /> $t->{plano_descrp}</div> ";
                $tarea .= " 	        <div style=\"width:10%\">$t->{cliente_nome}</div>";
        		$tarea .= " 	        <div style=\"width:5%\">#$t->{codigo}</div> ";
        		$tarea .= " 	        <div style=\"width:22%\">$t->{data} | $t->{data_previsao}</div>";
                $tarea .= " 	        <div style=\"width:17%\">$t->{solicitante}</div> ";
        		$tarea .= " 	        <div style=\"width:30%\">$t->{problema}</div> ";
        		$tarea .= "        </div>";
                $tarea .= "    '";
                $tarea .= "},";
            # }
    	}
    } else {
        $tarea = "{ val:0, descrp:'<div style=\"width:100%\">Nenhum registro encontrado !</div>' }";
    }

# retorno do codigo 
print<<HTML;
<script>

    var content  = '<div id="tkt_tabs">';
        content += '    <ul>';
        content += '        <li id="tkt_exec_tab"><a href="#tkt_exec">Minhas Tarefas</a></li>';
        content += '        <li id="tkt_area_tab"><a href="#tkt_area">Pendentes por Área</a></li>';
        // content += '        <li id="tkt_pendente_tab"><a href="#tkt_pendente">Pendentes</a></li>';
        // content += '        <li><a href="#tkt_noresp">Orfãos</a></li>';
        content += '        <li><a href="#tkt_resp">Criados</a></li>';
        content += '    </ul>';
        content += '    <div id="tkt_exec"><div></div></div>';
        content += '    <div id="tkt_area"><div></div></div>';
        // content += '    <div id="tkt_pendente"><div></div></div>';
        // content += '    <div id="tkt_noresp"><div></div></div>';
        content += '    <div id="tkt_resp"><div></div></div>';
        content += '</div>';
    
    \$("#dashboard_tkt_container").html(content);
	
	
    
	\$("#tkt_exec div").DTouchRadio({ 
        title: '$tatitle',
		addItem:[ $ta ], 
		orientation:'vertical',
		click: function(res) {
            if(res.value === "0"){
                return false;
            }
            
			eos.core.call.module.tkt(res.value); // edita tkt
		}
	});
    
    /*
	\$("#tkt_noresp div").DTouchRadio({ 
        title: '$ttitle',
		addItem:[ $tao ], 
		orientation:'vertical',
		click: function(res) {
            if(res.value === "0"){
                return false;
            }
            
			eos.core.call.module.tkt(res.value); // edita tkt
		}
    });
     */
     
	\$("#tkt_resp div").DTouchRadio({ 
        title: '$ttitle',
		addItem:[ $tar ], 
		orientation:'vertical',
		click: function(res) { 
            if(res.value === "0"){
                return false;
            }
            
			eos.core.call.module.tkt(res.value); // edita tkt
		}
	});
    /*
	\$("#tkt_pendente div").DTouchRadio({ 
        title: '$taottitle',
		addItem:[ $taot ], 
		orientation:'vertical',
		click: function(res) { 
            if(res.value === "0"){
                return false;
            }
            
			eos.core.call.module.tkt(res.value); // edita tkt
		}
	});	
    */
    
	\$("#tkt_area div").DTouchRadio({ 
        title: '$tareatitle',
        search      : true,
		addItem:[ $tarea ], 
		orientation:'vertical',
		click: function(res) { 
            if(res.value === "0"){
                return false;
            }
            
			eos.core.call.module.tkt(res.value); // edita tkt
		}
	});	
    
                
    \$("#tkt_tabs").tabs();
    
</script>
HTML

}



