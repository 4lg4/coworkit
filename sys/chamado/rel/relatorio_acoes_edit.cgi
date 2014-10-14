#!/usr/bin/perl

#
#   relatorio_acoes_edit.cgi
#
#       Lista de acoes salvas para edicao
#

$nacess = "49";
require "../../cfg/init.pl";

$ID          = &get('ID');    # sessao
$COD         = &get('COD');   # codigo para edicao do item

print $query->header({charset=>utf8}); # headers

# dados do pai
$DBC = &DBE("
    select
        *
    from
        cob_tkt_full
    where 
        codigo = $COD
");
$cob = $DBC->fetchrow_hashref;
$cob->{competencia} = &dateToShow($cob->{competencia},"yearmonth");
# $cob->{competencia} = &dateToSave($cob->{competencia},"date");

# filhos
$DB = &DBE("
    select
        *,
        to_char(data_acao, 'DD/MM/YYYY HH24:MIh (TMdy)') as data_acao_
    from
        cob_tkt_item_edit
    where 
        cob_tkt = $COD
");

# conceito de cores por plano
$colors[1] = "colors_blue";
$colors[2] = "colors_orange";
$colors[3] = "colors_green";
$colors[4] = "colors_yellow";
$colors[5] = "colors_red";
$colors[6] = "colors_gray";

if($DB->rows() > 0) {    

    # titulo dos totais
    $totais = "<div class='totais_item_edit'>";
    $totais .= "    <div>Descrição</div>";
    $totais .= "    <div>Executado</div>";
    $totais .= "    <div>Faturado</div>";
    $totais .= "</div>";
    
        
    $tkt_plano_change = "";
    $color = 0;
	while($item = $DB->fetchrow_hashref) {

        # container plano
        if($item->{tkt_plano} ne $tkt_plano_change){
            $color += 1;
            
            # calcula totais por plano
            $DBT = &DBE("select sum(executado) as executado, sum(faturado) as faturado from cob_tkt_item_edit where tkt_plano = $item->{tkt_plano} and cob_tkt = $COD");
            $T = $DBT->fetchrow_hashref;
            $totais .= "<div class='totais_item_edit'>";
            $totais .= "    <div class='$colors[$color]'>$item->{tkt_plano_descrp}</div>";
            $totais .= "    <div class='$colors[$color]'><span>".(&dateToShow($T->{executado}))."h</span> ";
            $totais .= "        <input type='hidden' name='totais_executado_$item->{tkt_plano}' plano='$item->{tkt_plano}' class='totais_executado' value='$T->{executado}'></div>";
            $totais .= "    <div class='$colors[$color]'><span>".(&dateToShow($T->{faturado}))."h</span> ";
            $totais .= "        <input type='hidden' name='totais_faturado_$item->{tkt_plano}' plano='$item->{tkt_plano}'  class='totais_faturado'  value='$T->{faturado}'></div>";
            $totais .= "</div>";
            
            # calcula totais por tipo do plano
            $DBT = &DBE("select tipo_descrp, tipo, sum(executado) as executado, sum(faturado) as faturado from cob_tkt_item_edit where tkt_plano = $item->{tkt_plano} and cob_tkt = $COD group by tipo_descrp, tipo order by tipo_descrp asc");
            while($T = $DBT->fetchrow_hashref) {
                $totais .= "<div class='totais_item_edit totais_item_edit_item'>";
                $totais .= "    <div class='$colors[$color]'> - $T->{tipo_descrp}</div>";
                $totais .= "    <div class='$colors[$color]'><span>".(&dateToShow($T->{executado}))."h</span> ";
                $totais .= "        <input type='hidden' name='totais_executado_$item->{tkt_plano}_$T->{tipo}' plano='$item->{tkt_plano}' tipo='$T->{tipo}' class='totais_executado_$item->{tkt_plano}' value='$T->{executado}'></div>";
                $totais .= "    <div class='$colors[$color]'><span>".(&dateToShow($T->{faturado}))."h</span> ";
                $totais .= "        <input type='hidden' name='totais_faturado_$item->{tkt_plano}_$T->{tipo}'  plano='$item->{tkt_plano}' tipo='$T->{tipo}' class='totais_faturado_$item->{tkt_plano}'  value='$T->{faturado}'></div>";
                $totais .= "</div>";
            }
            
            # subtitulo
            $array_radio_chamado .= "{";
    		$array_radio_chamado .= "val:0,descrp: '";
            $array_radio_chamado .= "<div class=\"DTouchRadio_list_title planos_title $colors[$color]\">";
            $array_radio_chamado .= "       $item->{tkt_plano_descrp}";
            $array_radio_chamado .= "</div>";
            $array_radio_chamado .= "'},";
            
            $tkt_plano_change = $item->{tkt_plano}; # container plano
        }
        
		$item->{descrp} = &get($item->{descrp}, "NEWLINE_SHOW"); 
                
        $array_radio_chamado .= "{";
		$array_radio_chamado .= "val:$item->{codigo},descrp: '";
		$array_radio_chamado .= "<div class=\"DTouchRadio_list_line $colors[$color]\" title=\"Ticket data: ".(&dateToShow($item->{tkt_data}))."h <hr> ".(&get($item->{tkt_problema}, "NEWLINE_SHOW"))."<hr>".(&get($item->{descrp_interno}, "NEWLINE_SHOW"))."\">";
		$array_radio_chamado .= " 	<div style=\"width:5%;\">";
        $array_radio_chamado .= " 	    #$item->{tkt}";
        # $array_radio_chamado .= " 	    <textarea name=\"item_problema_$item->{codigo}\" class=\"item_problema\" style=\"display:none;\">".(&get($item->{tkt_problema}, "NEWLINE_SHOW"))."</textarea> ";
        $array_radio_chamado .= " 	</div> ";
		$array_radio_chamado .= " 	<div style=\"width:15%\">".$item->{data_acao_}."</div>";
		# $array_radio_chamado .= " 	<div style=\"width:15%\">".(&dateToShow($item->{tkt_data}))."</div>";
		$array_radio_chamado .= " 	<div style=\"width:10%\">$item->{tipo_descrp}</div>";
        $array_radio_chamado .= " 	<div style=\"width:15%\">$item->{executor_nome}</div> ";
		$array_radio_chamado .= " 	<div style=\"width:30%\"><textarea name=\"item_descrp_$item->{codigo}\" class=\"item_descrp\">$item->{descrp}</textarea></div> ";
        $array_radio_chamado .= " 	<div style=\"width:10%\"><input type=\"text\" name=\"item_executado_$item->{codigo}\" plano=\"$item->{tkt_plano}\" tipo=\"$item->{tipo}\" class=\"item_tempo item_executado item_executado_$item->{tkt_plano}_$item->{tipo}\" value=\"".(&dateToShow($item->{executado}))."\"></div> ";
        $array_radio_chamado .= " 	<div style=\"width:10%\">";
        $array_radio_chamado .= " 	    <input type=\"text\" name=\"item_faturado_$item->{codigo}\"  plano=\"$item->{tkt_plano}\" tipo=\"$item->{tipo}\" class=\"item_tempo item_faturado item_faturado_$item->{tkt_plano}_$item->{tipo}\" value=\"".(&dateToShow($item->{faturado}))."\"> ";
        $array_radio_chamado .= " 	    <input type=\"hidden\" name=\"item\"  value=\"$item->{codigo}\"> ";
        $array_radio_chamado .= "       <input type=\"hidden\" name=\"item_tkt_acao_$item->{codigo}\"  value=\"$item->{tkt_acao}\"> ";
        $array_radio_chamado .= " 	</div> ";
        $array_radio_chamado .= " 	<div style=\"width:5%\">";
        $array_radio_chamado .= " 	    <div class=\"item_reativar\"><input type=\"hidden\" name=\"item_tkt_acao\"  value=\"$item->{tkt_acao}\"></div>";
        $array_radio_chamado .= " 	</div> ";
        
		# $array_radio_chamado .= " 	<div style=\"width:5%\"> ";
        # $array_radio_chamado .= "       <input type=\"checkbox\" name=\"cobrar\" value=\"$item->{codigo}\" checked />";
        # $array_radio_chamado .= "       <input type=\"hidden\"  name=\"cobrar_tempo_$item->{codigo}\" value=\"$item->{tempo}\" />";
        # $array_radio_chamado .= "       <textarea name=\"cobrar_descrp_$item->{codigo}\" style=\"display:none;\">$item->{descrp}</textarea>";
        # $array_radio_chamado .= " 	</div> ";
		$array_radio_chamado .= "</div>";    
        $array_radio_chamado .= "'},";
    }
    
    # total geral
    $DBT = &DBE("select sum(executado) as executado, sum(faturado) as faturado from cob_tkt_item_edit where cob_tkt = $COD");
    $T = $DBT->fetchrow_hashref;
    $totais_total  = "<span id='totais_executado_text'>".&dateToShow($T->{executado})."h</span> / <span id='totais_faturado_text'>".&dateToShow($T->{faturado})."h</span>";
    $totais_total .= "<input type='hidden' name='totais_executado' value='$T->{faturado}'>";
    $totais_total .= "<input type='hidden' name='totais_faturado'  value='$T->{faturado}'>";
} 
		

    $radio_title  = "<div class=\"DTouchRadio_list_title\">";
	$radio_title .= "	<div style=\"width:5%\">TKT</div>";
	# $radio_title .= "	<div style=\"width:15%\">TKT Data</div>";
	$radio_title .= "	<div style=\"width:15%\">Ação Data</div>";
    $radio_title .= "	<div style=\"width:10%\">Tipo</div> ";
    $radio_title .= "	<div style=\"width:15%\">Executor</div> ";
    $radio_title .= "	<div style=\"width:30%\">Descrição</div> ";
	# $radio_title .= "	<div style=\"width:5%\">Executado</div> ";
    # $radio_title .= "	<div style=\"width:5%\">Faturado</div> ";
	$radio_title .= "	<div style=\"width:10%\">Executado</div> ";
    $radio_title .= "	<div style=\"width:10%\">Faturado</div> ";
    $radio_title .= "	<div style=\"width:5%\"></div> ";
    $radio_title .= "</div>";
	

print<<HTML;
		<script>

            // totais
    		\$("#relatorio_tkt_acao_list").DTouchRadio({ 
                addItem     : [$array_radio_chamado], 
    			orientation : 'vertical',
    			title       : '$radio_title',
    			search      : true,
                click       : "off",
                postFunction : function(x) {
                    \$("#totais").html("$totais");
                    \$("#totais_header_total").html("$totais_total");
        
                    // ajusta box totais
                    \$("#totais").hide();
                    \$("#totais_container").addClass("totais_container_close").show();
                    \$("#totais_header_icon").addClass("totais_header_icon_up");
                    // \$("#competencia").fieldDateTime("disable");
                    \$("#empresa").fieldAutoComplete("disable");
                    \$("#finalizado").fieldCheckbox("disable");
                    
        
                    // campos tempo
                    \$(".item_executado").fieldDateTime({
                        type         : "time",
                        postFunction : function(x){ 
                            relatorio.totais({ 
                                plano : \$(this)[0].getAttribute("plano"),
                                tipo  : \$(this)[0].getAttribute("tipo")
                            });
                        }
                    });
                    \$(".item_faturado").fieldDateTime({
                        type         : "time",
                        postFunction : function(x){ 
                            relatorio.totais({
                                plano : \$(this)[0].getAttribute("plano"),
                                tipo  : \$(this)[0].getAttribute("tipo")
                            });
                        }
                    });
                                        
                    // adiciona tooltip no numero do ticket
                    // \$(".DTouchRadio_list_line div:nth-child(1)")
                    \$(".DTouchRadio_list_line")
                        .tooltip({track: true});
                        /*
                        .click(function(){
                            
                            if(\$(this)[0].getAttribute("dkey")) {
                                \$.DDialog({
                                    type    : "alert",
                                    title   : "Problema / Descrição Interna",
                                    message : \$(this)[0].getAttribute("dkey")
                                });
                            }
                        });
                           */
                                     
                    // outros campos edicao
                    \$("#obs")
                        .show()
                        .val("$cob->{obs}");
                    eos.template.field.show(\$("#descrp"));
                    \$("#descrp").val("$cob->{descrp}");
                    \$("#empresa").fieldAutoComplete("value",{ id: "$cob->{empresa}", val: "$cob->{empresa_nome}"});
                    // \$("#competencia").fieldDateTime("value","$cob->{competencia}");
                    \$("#competencia").val("$cob->{competencia}");
                    if($cob->{finalizado} === 1){
                        \$("#finalizado").fieldCheckbox("check");
                    }
                    
                    // totais flutuantes
                    \$("#totais_container").draggable();
                    
                    
                    // se nao encerrado
                    if("$cob->{encerrar}" === ""){
                        eos.menu.action.show(["icon_rel_save","icon_rel_encerrar","icon_rel_reativar"]);
                        
                        // reativa o item desejado
                        \$(".item_reativar").click(function(){
                            var item = {
                                item : \$(this).parents(".DTouchRadio_items"),
                                val  : \$(this).find("input").val()
                            };
                            relatorio.reativar(item);
                        });
                     
                     
                        // descrp item
                        \$(".item_descrp")
                            .focus(function(){
                        
                                \$(this).addClass("item_descrp_open");
                                \$(this).parents(".DTouchRadio_list_line div").addClass("item_descrp_line_open");
                            })
                            .focusout(function(){
                            
                                \$(this).removeClass("item_descrp_open");
                                \$(this).parents(".DTouchRadio_list_line div").removeClass("item_descrp_line_open");
                            });
                       
                    } else { // encerrado
                        \$(".item_reativar").hide();
                        eos.menu.action.hide(["icon_rel_save","icon_rel_encerrar","icon_rel_reativar"]);
                        
                        // modo de visualizacao somente
                        \$(".item_descrp")
                            .each(function(){
                                \$(this).parent().html("<span class='descrp_show'>"+\$(this).val()+"</span>");
                            });
                            
                            
                        \$(".item_tempo").each(function(){
                            \$(this).parents(".EOS_template_field").parent().html("<span class='descrp_show'>"+\$(this).val()+"h</span>");
                        });
                    }
                    
                    
                    
                }
    		});
                
		</script>
HTML
