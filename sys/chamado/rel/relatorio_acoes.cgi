#!/usr/bin/perl

#
#   relatorio_acoes.cgi
#
#       Lista de acoes dos tickes para gerar relatorio de cobranca
#

$nacess = "49";
require "../../cfg/init.pl";

$ID          = &get('ID');   # sessao
$competencia = &dateToSave(&get('competencia'));
$finalizado  = &get('finalizado');
$empresa     = &get('empresa');

print $query->header({charset=>utf8}); # headers

# finalizados
if($finalizado eq "true") { # ajusta query se finalizados somente
    $finalizado_where = " and tkt_finalizado is not null ";
}

# statment
$where  = " tkt_empresa = $empresa and tkt_empresa_logada = $USER->{empresa} and tempo > '00:00'::time ";
$where .= " and to_char(data, 'YYYY-MM') <= '$competencia' $finalizado_where and faturado is null";
$DB = &DBE("
    select 
        codigo, data, executor_descrp as descrp, descrp as descrp_interno, tkt_problema, tempo, tkt_codigo as tkt, tkt_data, tipo_descrp, 
        executor_nome, tkt_plano_descrp, tkt_plano, data_execucao as data_acao, to_char(data_execucao, 'DD/MM/YYYY HH24:MIh (TMdy)') as data_acao_
    from tkt_acao_tkt_full where 
        $where
    order by tkt_plano, tkt_codigo, codigo
");

# conceito de cores por plano
$colors[1] = "colors_blue";
$colors[2] = "colors_orange";
$colors[3] = "colors_green";
$colors[4] = "colors_yellow";
$colors[5] = "colors_red";
$colors[6] = "colors_gray";

$item_qtd = $DB->rows(); # itens

if($item_qtd > 0) {    
        
    # titulo dos totais
    $totais = "<div class='totais_item'>";
    $totais .= "    <div>Descrição</div>";
    $totais .= "    <div>Executado</div>";
    $totais .= "</div>";
    
    $tkt_plano_change = "";
    $color = 0;
	while($item = $DB->fetchrow_hashref) {

        # container plano
        if($item->{tkt_plano} ne $tkt_plano_change){
            $color += 1;
            
            # calcula totais por plano
            $DBT = &DBE("select sum(tempo) as total from tkt_acao_tkt where tkt_plano = $item->{tkt_plano} and $where");
            $T = $DBT->fetchrow_hashref;
            $totais .= "<div class='totais_item'><div class='$colors[$color]'>$item->{tkt_plano_descrp}</div><div class='$colors[$color]'>".(&dateToShow($T->{total}))."h</div></div>";
            
            # calcula totais por tipo do plano
            $DBT = &DBE("select tipo_descrp, tipo, sum(tempo) as executado from tkt_acao_tkt where tkt_plano = $item->{tkt_plano} and $where group by tipo_descrp, tipo order by tipo_descrp asc");
            while($T = $DBT->fetchrow_hashref) {
                $totais .= "<div class='totais_item'>";
                $totais .= "    <div class='$colors[$color]'> - $T->{tipo_descrp}</div>";
                $totais .= "    <div class='$colors[$color]'>".(&dateToShow($T->{executado}))."h</div>";
                $totais .= "</div>";
            }
            
            # subtitulo
            $array_radio_chamado .= "{";
    		$array_radio_chamado .= "val:0,descrp: '";
            $array_radio_chamado .= "<div class=\"DTouchRadio_list_title planos_title $colors[$color]\">$item->{tkt_plano_descrp}</div>";
            $array_radio_chamado .= "'},";
            
            $tkt_plano_change = $item->{tkt_plano}; # container plano
        }
        
		$item->{descrp} = &get($item->{descrp}, "NEWLINE_SHOW"); 
                
        $array_radio_chamado .= "{";
		$array_radio_chamado .= "val:$item->{codigo},descrp: '";
		$array_radio_chamado .= "<div class=\"DTouchRadio_list_line $colors[$color]\" title=\"Ticket data: ".(&dateToShow($item->{tkt_data}))."h <hr> ".(&get($item->{tkt_problema}, "NEWLINE_SHOW"))."<hr>".(&get($item->{descrp_interno}, "NEWLINE_SHOW"))."\">";
		# $array_radio_chamado .= " 	<div style=\"width:5%;\">#$item->{tkt}</div> ";
        $array_radio_chamado .= " 	<div style=\"width:5%;\">#$item->{tkt}</div> ";
		$array_radio_chamado .= " 	<div style=\"width:15%\">".(&dateToShow($item->{data}))."</div>";
		$array_radio_chamado .= " 	<div style=\"width:15%\">".$item->{data_acao_}."</div>";
		$array_radio_chamado .= " 	<div style=\"width:10%\">$item->{tipo_descrp}</div>";
        $array_radio_chamado .= " 	<div style=\"width:15%\">$item->{executor_nome}</div> ";
		$array_radio_chamado .= " 	<div style=\"width:25%\">$item->{descrp}</div> ";
        $array_radio_chamado .= " 	<div style=\"width:5%\">".(&dateToShow($item->{tempo}))."</div> ";
		$array_radio_chamado .= " 	<div style=\"width:5%\"> ";
        $array_radio_chamado .= "       <input type=\"checkbox\" name=\"cobrar\" value=\"$item->{codigo}\" checked />";
        $array_radio_chamado .= "       <input type=\"hidden\"  name=\"cobrar_tempo_$item->{codigo}\" value=\"$item->{tempo}\" />";
        $array_radio_chamado .= "       <textarea name=\"cobrar_descrp_$item->{codigo}\" style=\"display:none;\">$item->{descrp}</textarea>";
        $array_radio_chamado .= " 	</div> ";
		$array_radio_chamado .= "</div>";    
        $array_radio_chamado .= "'},";
        
        
    }
    
    # total geral
    $DBT = &DBE("select sum(tempo) as total from tkt_acao_tkt where $where");
    $T = $DBT->fetchrow_hashref;
    $totais_total = &dateToShow($T->{total})."h";
    
} 
#else {
    # $array_radio_chamado .= "{ val:0, descrp:'<div style=\"width:100%\">Nenhum registro encontrado !</div>' }";
    #$array_radio_chamado .= "<div style='width:100%'>Nenhum registro encontrado !</div>";
    #}
		

    $radio_title  = "<div class=\"DTouchRadio_list_title\">";
	$radio_title .= "	<div style=\"width:5%\">TKT</div>";
	$radio_title .= "	<div style=\"width:15%\">TKT Data</div>";
	$radio_title .= "	<div style=\"width:15%\">Ação Data</div>";
    $radio_title .= "	<div style=\"width:10%\">Tipo</div> ";
    $radio_title .= "	<div style=\"width:15%\">Executor</div> ";
    $radio_title .= "	<div style=\"width:25%\">Descrição</div> ";
	$radio_title .= "	<div style=\"width:5%\">Hora</div> ";
    $radio_title .= "	<div style=\"width:5%\">Cobrar</div> ";
    $radio_title .= "</div>";
	

print<<HTML;
		<script>
			
            
            // totais
			if("$item_qtd" !== "0") {
    			\$("#relatorio_tkt_acao_list").DTouchRadio({ 
                    addItem     : [$array_radio_chamado], 
    				orientation : 'vertical',
    				title       : '$radio_title',
    				search      : true,
                    click       : "off",
                    postFunction : function(x) {
                        
                        // formulario principal
                        \$("#obs").show();
                        eos.template.field.show(\$("#descrp"));
                        // \$("#competencia").fieldDateTime("disable");
                        \$("#empresa").fieldAutoComplete("disable");
                        \$("#finalizado").fieldCheckbox("disable");
                            
                        // ajusta box totais    
                        \$("#totais").html("$totais");
                        \$("#totais_header_total").html("$totais_total");
                        \$("#totais_container").addClass("totais_container_close").show();
                        \$("#totais_header_icon").addClass("totais_header_icon_up");
                        \$("#totais").hide();
                
                        // totais flutuantes
                        \$("#totais_container").draggable();
                        
                        // adiciona tooltip no numero do ticket
                        \$(".DTouchRadio_list_line")
                        // \$(".DTouchRadio_list_line div:nth-child(1)")
                            .tooltip();
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
                    }
    			});
                
                
                
            } else {
                \$("#totais_container").hide();
                \$("#relatorio_tkt_acao_list").html("<div style='width:100%'>Nenhum registro encontrado !</div>");
                
                // aviso 
                \$.DDialog({
                   type    : "alert",
                   message : "Nenhum lançamento de horas <br> para este cliente",
                   btnOK  : function(){
                       // vai para esquerda
                       \$("#relatorio_page").DTouchPages("page","left");
                   }
                });
            
            }
            
            /*
            // marca todos checkboxes
            \$("input[name=cobrar]").click(function(e){
                e.preventDefault();
            });
            */
		</script>
HTML
