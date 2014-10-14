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
# if($USER->{tipo} eq "99") { 
    
    #
    #   Meus chamados
    #
    $ttitle  = "<div class=\"DTouchRadio_list_title\">";
    $ttitle .= " 	<div style=\"width:5%\">Codigo</div>";
    $ttitle .= " 	<div style=\"width:12%\">Data</div>";
    $ttitle .= " 	<div style=\"width:15%\">Tempo Exec.</div>";
    $ttitle .= " 	<div style=\"width:10%\">Solicitante</div> ";
    $ttitle .= "    <div style=\"width:20%\">Problema</div> ";
    $ttitle .= "    <div style=\"width:10%\">Agilidade</div> ";
    $ttitle .= "    <div style=\"width:10%\">Qualidade</div> ";
    $ttitle .= "    <div style=\"width:10%\">Cortesia</div> ";
    $ttitle .= "    <div style=\"width:5%\">Finaliza</div> ";
    $ttitle .= "</div>";

    $DB = DBE("
        select 
            codigo,
            data,  
            solicitante, 
            problema, 
            to_char((finalizado - data), 'DD') as days, 
            to_char((finalizado - data), 'HH24:MI') as time 
        from 
            tkt_full 
        where 
            finalizado is not null and 
            feedback is null and 
            cliente = $USER->{empresa}         
    ");
    # and finalizado >= '2013-12-18'::date - interval '60 days'
    
    if($DB->rows() > 0) {
    	while($t = $DB->fetchrow_hashref) { 
    		# ajustes variaveis
    		$t->{problema} = &get($t->{problema},"NEWLINE_SHOW");
        
    		$t->{data}           = &dateToShow($t->{data});
            
            # tempo exec
            if($t->{days} ne "00") {
                $tempo = $t->{days}." dias e ".$t->{time}."h";
            } else {
                $tempo = $t->{time}."h";
            }            
            
    		$ta .= "{ ";
            $ta .= "    val : $t->{codigo},";
            $ta .= "    descrp:'";
    		$ta .= "        <div class=\"DTouchRadio_list_line\">";
    		$ta .= " 	        <div style=\"width:5%\">#$t->{codigo} <input type=\"hidden\" name=\"feedback_codigo\" value=\"$t->{codigo}\" /> </div> ";
    		$ta .= " 	        <div style=\"width:15%\">$t->{data}</div>";
    		$ta .= " 	        <div style=\"width:15%\">$tempo</div>";
            $ta .= " 	        <div style=\"width:10%\">$t->{solicitante}</div> ";
    		$ta .= " 	        <div style=\"width:20%\">$t->{problema}</div> ";
            
            
            # monta stars
            $DBTS = DBE("
                select 
                    codigo
                from 
                    tkt_feedback_tipo
            ");
            while($ts = $DBTS->fetchrow_hashref) { 
                
                
                $ta .= " 	        <div style=\"width:10%\" class=\"star_group_$ts->{codigo}\">";
                
                
                # verifica estrelas a serem marcadas
                $DBS = DBE("
                    select 
                        *
                    from 
                        tkt_feedback
                    where 
                        tkt  = $t->{codigo} and
                        tipo = $ts->{codigo}
                ");
                
                if($DBS->rows() > 0) {
                    $s = $DBS->fetchrow_hashref;
                    $qtd = $s->{avaliacao};
                } else {
                    $qtd = 0;
                }
                
                for($i=1; $i<6; $i++) {
                    
                    # ajusta para marcar estrelas
                    if($i <= $qtd) {
                        $star_class = "star_checked";
                    } else {
                        $star_class = "";
                    }
                    
                    $ta .= "<div class=\"star s$ts->{codigo} $star_class\" dkey=\"$i\" tkey=\"$ts->{codigo}\"></div>";
                }
                
                $ta .= " 	        </div>";
            }
                
                
            $ta .= " 	        <div style=\"width:5%\"><img src=\"/img/ui/chat.svg\" alt=\"Mensagem\" title=\"Mensagem\" class=\"finaliza\"></div> ";
            $ta .= "        </div>";
            $ta .= "    '";
            $ta .= "},";
    	}
    } else {
        $ta = "{ val:0, descrp:'<div style=\"width:100%\">Nenhum registro encontrado !</div>' }";
    }

# retorno do codigo 
print<<HTML;
<script>
        
	\$("#feedback").DTouchRadio({ 
        title: '$ttitle',
		addItem:[ $ta ], 
		orientation:'vertical',
		click : "off"
    });
    
    
    // controla clique do icone
    \$(".dashboard_form .star").click(function(){
        
        var total = \$(this).get(0).getAttribute("dkey")
        ,   tipo  = \$(this).get(0).getAttribute("tkey")
        ,   stars = \$(this).parent();    
            stars = stars.find(".star");
        
        // remove classe marcados
        stars.removeClass("star_checked"); 
        
        // marca estrelas
        stars.each(function(){ 
            if(\$(this).get(0).getAttribute("dkey") <= total) {
                \$(this).addClass("star_checked");
            }
        });
        
        return; 
        // atualiza feedback
    	\$.DActionAjax({
    		action : "feedback_submit.cgi",
            req    : "feedback_avaliacao="+total+"&feedback_tipo="+tipo+"&feedback_tkt="+\$(this).parents(".DTouchRadio_list_line").find("input[name=feedback_codigo]").val(),
            loader : false
    	});
    });
    
    // controla clique do icone finaliza
    \$(".dashboard_form .finaliza").click(function(){ 
        
        var tkt  = \$(this).parents(".DTouchRadio_list_line").find("input[name=feedback_codigo]").val()
        ,   line = \$(this).parents(".DTouchRadio_list_line");
        
        \$.DDialog({
            type    : "confirm",
            title   : "Finalizar FeedBack do ticket #"+tkt+" ?",
            message : "<textarea name='feedback_descrp' placeholder='Sugestões / Reclamações ?'\></textarea>",
            btnYes  : function(){
                
                var req  = "feedback_descrp="+\$(this).parent().find("textarea[name=feedback_descrp]").val();
                    req += "&feedback_tipo1="+line.find(".star_group_1 .star_checked").length;
                    req += "&feedback_tipo2="+line.find(".star_group_2 .star_checked").length;
                    req += "&feedback_tipo3="+line.find(".star_group_3 .star_checked").length;
                    req += "&feedback_tkt="+tkt;
        
                // atualiza feedback
            	\$.DActionAjax({
            		action : "feedback_submit.cgi",
                    req    : req,
                    loader : false
            	});
            },
        });

    });
</script>
HTML
