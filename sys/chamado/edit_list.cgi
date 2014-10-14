#!/usr/bin/perl

#
# edit_list.cgi
#
# Lista de chamados que aparecem no modulo
#

$nacess = "10";
require "../cfg/init.pl";

# $empresa = &get('empresa');
# $chamado = &get('COD');
$ID = &get('ID');

print $query->header({charset=>utf8});

# ajusta range de busca se setado
# $entre_datas = " (to_char(data_exec, 'YYYY-MM-DD') >= '".$DATA_ini."' and to_char(data_exec, 'YYYY-MM-DD') <= '".$DATA_fim."') ";
# $range = &dateToSave(&get('filter_date_ini'));
# $filter_tec = &get('filter_tec');
# $filter_client = &get('filter_client');
# $filter_group = &get('filter_group');
# $filter_date_month = &get('filter_date_month');

$filter_search   = &get('search');
$filter_empresa  = &get('filter_empresa');
$filter_empresa_descrp  = &get('filter_empresa_descrp');
$filter_date_ini = &get('filter_date_ini');
$filter_date_end = &get('filter_date_end');

# valores originais das datas (sem tratamento)
$ofilter_date_ini = $filter_date_ini;
$ofilter_date_end = $filter_date_end;

# debug($filter_date_ini);
# debug($filter_date_end);

# lista chamados se supervisor
# if($nacess_tipo eq "s")
#	{
#	$and_supervisor = ""; 
#	$and_user = " and ";
#	}
# else
#	{
#	$and_supervisor=" and ";
#	$and_user="  ";
#	}
	
# range de datas
if(!$filter_date_ini){ 
    $filter_date_ini = "01-".&timestamp("month")."/".&timestamp("year");
}
$filter_date_ini = &dateToSave($filter_date_ini, "DATE");
$range = " (to_char(t.data, 'YYYY-MM-DD') >= '$filter_date_ini') ";

if($filter_date_end) {
    $filter_date_end = &dateToSave($filter_date_end, "DATE");
    $range = " (to_char(t.data, 'YYYY-MM-DD') >= '$filter_date_ini' and to_char(t.data, 'YYYY-MM-DD') <= '$filter_date_end') ";
    }
 
# empresa filtro
if($filter_empresa) {
    $empresa = " and t.cliente = $filter_empresa "; 
}

# search field filtro
if($filter_search) {
    $search = " and (t.problema <=> '%$filter_search%' or t.solicitante <=> '%$filter_search%' or t.cliente_nome <=> '%$filter_search%' or t.responsavel_nome <=> '%$filter_search%' or t.executor_nome <=> '%$filter_search%') "; 
}

$where = "where ".$range.$empresa.$search;

# debug($filter_date_ini);

# debug($range);
# debug($where);

# pega todo o mes 
# if($filter_date_month ne "")
# 	{	
# 	$range = "$and_supervisor (to_char(c.data_agendamento, 'YYYY-MM-DD') >= '$filter_date_month') $and_user ";
# 	}

# filtra por grupo selecionado
# if($filter_group ne "")
# 	{
# 	if(lc($filter_group) eq "abertos")
# 		{ $filter_group = "c.data_conclusao is null and c.cancelado is false"; }
# 	elsif(lc($filter_group) eq "fechados")
# 		{ $filter_group = "c.data_conclusao is not null and c.cancelado is false"; }
# 	elsif(lc($filter_group) eq "vencidos")
# 		{ $filter_group = "(to_char(c.data_agendamento, 'YYYY-MM-DD') < '".(timestamp('date'))."') and c.data_conclusao is null and c.cancelado is false"; }
# 	elsif(lc($filter_group) eq "excluidos")
# 		{ $filter_group = "c.cancelado is true"; }
# 	}
# else
# 	{
# 	$filter_group = "  c.cancelado is false "; 
# 	}
# 
# if($nacess_tipo ne "s")
# 	{
# 	$range .= " and $filter_group";
# 	}
# else
# 	{
# 	$range .= "$filter_group";
# 	}
# 
# 
# if($filter_client ne "")
# 	{
# 	$range .= " and e.codigo = '$filter_client' "; 
# 	}
# 	
# if($filter_tec ne "")
# 	{
# 	$range .= " and c.tecnico = '$filter_tec' "; 
# 	}
# 
# if($USER->{usuario} eq "93" || $USER->{usuario} eq "105" || $USER->{usuario} eq "84" || $USER->{usuario} eq "102")
# 	{
# 	$range =~ s/^ and/ /;
# 	}
# 	
# elsif($nacess_tipo ne "s")
# 	{
# 	$range = " c.tecnico = $USER->{usuario} ".$range;
# 	}
# 
# 
# 
# [INI] Chamados, lista chamados ------------------------------------------------------------------------------------------
# if($chamado eq "" or $range ne "")
# 	{ 
        
        # sub title
        $sub_title  = "<div class=\"tkt_list_title_sub\">";
        $sub_title .= " 	<div class=\"tkt_list_line_icon\" style=\"width:1.5%\"></div>";
    	$sub_title .= " 	<div style=\"width:5%\">Codigo</div>";
    	$sub_title .= " 	<div style=\"width:12%\">Data</div>";
    	$sub_title .= " 	<div style=\"width:5%\">Tempo</div>";
    	$sub_title .= " 	<div style=\"width:12%\">Responsável</div>";
    	$sub_title .= "	    <div style=\"width:12%\">Executor</div> ";
        $sub_title .= " 	<div style=\"width:20%\">Interno</div> ";
        $sub_title .= "	    <div style=\"width:27%\">Externo</div> ";
        $sub_title .= "</div>";
        
    
    #
    #   Cliente do parceiro
    #
    if($USER->{tipo} eq "99") {
        $cli_parceiro = " or cliente = $USER->{empresa}";
    }
    
	# select mostra quando for criador e tecnico 
	# $DB = &DBE("select extract(month from age(now())) AS mes, c.*, e.nome as cliente_nome, e.apelido as cliente_apelido, cp.descrp as chamado_prioridade, ct.img as chamado_tipo_img, ct.descrp as chamado_tipo from chamado as c left join empresa_endereco as ee on ee.codigo = c.cliente_endereco left join empresa as e on e.codigo = ee.empresa left join chamado_tipo as ct on ct.codigo = c.tipo left join chamado_prioridade as cp on cp.codigo = c.prioridade where $range order by c.data desc");
	$DB = &DBE("
        select 
            t.*, 
            ( 
                select 
                    count(ta.codigo) 
                from 
                    tkt_acao as ta where ta.tkt = t.codigo
            ) as total  
        from 
            tkt_full as t 
        $where 
            and empresa_logada = $USER->{empresa}
            $cli_parceiro
        order by 
            data 
        desc
    ");
	
	if($DB->rows() > 0)
		{
		while($c = $DB->fetchrow_hashref)
			{
			#Pega o nome do usuario criador
			#$DB2 = &DBE("select nome from usuario where usuario=$c->{usuario_logado}");
			#$usuario = $DB2->fetchrow_hashref;
			# monta array com todos os itens para adicionar no radio
			#	$array_radio_chamado .= "{val:$c->{codigo},descrp:'";
			#	$array_radio_chamado .= "#$c->{codigo} | ";
			#	$array_radio_chamado .= (&dateToShow($c->{data_agendamento}))." | ";
			#	$array_radio_chamado .= (&dateToShow($c->{tempo_agendamento}))." | ";
			#	$array_radio_chamado .= "$c->{chamado_tipo} | ";
			#	$array_radio_chamado .= (&slimit($c->{cliente_nome},20))." | ";
			#	$array_radio_chamado .= (&slimit($c->{usuario},20))." | ";
			#	$array_radio_chamado .= "$c->{chamado_tipo} | ";
			#	$array_radio_chamado .= "$c->{chamado_prioridade} | ";
			#	$array_radio_chamado .= "(".(&slimit($c->{descrp},20)).") | ";
			#	$array_radio_chamado .= "(".(&slimit($c->{descrp_resolucao},20)).")";
			#	$array_radio_chamado .= " ' },";
			
			# if($c->{cliente_apelido} ne "")
			# 	{ $c->{cliente_nome} = $c->{cliente_apelido}; }
				
			$c->{problema} = &get($c->{problema}, "NEWLINE_SHOW"); # remove problemas de quebra de linha e aspas
			# $c->{descrp_resolucao} = &get($c->{descrp_resolucao}, "NEWLINE_SHOW"); # remove problemas de quebra de linha e aspas
			
			#$array_radio_chamado .= "{val:$c->{codigo},descrp: {";
			#$array_radio_chamado .= "	'Cod.'				: '#$c->{codigo}', ";
			#$array_radio_chamado .= "	'Data de Abertura'	: '".(&dateToShow($c->{data}))."',";
			#$array_radio_chamado .= "	'Data de Agendamento'	: '".(&dateToShow($c->{data_agendamento}))."',";
			#$array_radio_chamado .= "	'Data Conclusão' 	: '".(&dateToShow($c->{data_conclusao}))."', ";
			#$array_radio_chamado .= "	'Duração'			: '".(&dateToShow($c->{tempo_agendamento}))."',";
			#$array_radio_chamado .= "	'Cliente' 			: '<div class=\"chamado_list_line\">$c->{cliente_nome}</div>', ";
			#$array_radio_chamado .= "	'Solicitante' 		: '<div class=\"chamado_list_line\">$c->{usuario}</div>', ";
			#$array_radio_chamado .= "	'Tipo'				: '<div class=\"chamado_list_line\">$c->{chamado_tipo}</div>', ";
			#$array_radio_chamado .= "	'Problema' 			: '<div class=\"chamado_list_line\">$c->{descrp}</div>', ";
			#$array_radio_chamado .= "	'Resolução' 		: '<div class=\"chamado_list_line\">$c->{descrp_resolucao}</div>', ";
			#$array_radio_chamado .= "	'Responsável'		: '<div class=\"chamado_list_line\">$usuario->{nome}</div>'";
			#$array_radio_chamado .= " }},";
			
            # total de acoes do formulario
            # $DBA = DBE("select count(codigo) as total from tkt_acao where tkt = $c->{codigo}");
            # $acoes = $DBA->fetchrow_hashref;
            
            
            if($c->{total} == 0 && $c->{cancelado} == 0 && (!$c->{finalizado})) {
                $status = "aberto";
            } elsif($c->{total} > 0 && $c->{cancelado} == 0 && (!$c->{finalizado})) {
                $status = "atendimento";
            } elsif($c->{cancelado} == 1) {
                $status = "cancelado";
            } elsif($c->{finalizado}) {
                $status = "finalizado";
            }
            
			# 930px MIN width of the table
			$array_radio_chamado .= "{val:$c->{codigo},descrp: ";
			$array_radio_chamado .= "'<div class=\"tkt_list_line\">";
			$array_radio_chamado .= " 	<div style=\"width:5%;\">#$c->{codigo}</div> ";
			$array_radio_chamado .= " 	<div style=\"width:12%\">".(&dateToShow($c->{data}))."</div>";
			$array_radio_chamado .= " 	<div style=\"width:5%\">".(&dateToShow($c->{tempo_previsao}))."</div>";
			$array_radio_chamado .= " 	<div style=\"width:10%\">$c->{cliente_nome}</div>";
			$array_radio_chamado .= " 	<div style=\"width:10%\">$c->{solicitante}</div> ";
			$array_radio_chamado .= " 	<div style=\"width:10%\">$c->{responsavel_nome}</div> ";
			$array_radio_chamado .= " 	<div style=\"width:5%\">$c->{total}</div> ";
			$array_radio_chamado .= " 	<div style=\"width:33%\">$c->{problema}</div> ";
			$array_radio_chamado .= " 	<div style=\"width:7%\">$status</div> ";
			$array_radio_chamado .= " </div>";
            
            # V2 alpha 1 -----
            # acoes list
            # $DBA = DBE("select ta.*, u.nome as usuario_nome, tt.descrp as tipo_descrp, ue.nome as executor_nome  from tkt_acao as ta left join usuario as u on u.usuario = ta.usuario left join usuario as ue on ue.usuario = ta.executor left join tkt_acao_tipo as tt on tt.codigo = ta.tipo where ta.tkt = $c->{codigo} order by ta.data asc");
            # 
            # if($DBA->rows() > 0){
            #     $array_radio_chamado .= $sub_title;  # titulo acoes
            #     
            #     # $aa = $DBA->fetchrow_hashref;
        	# 	while($a = $DBA->fetchrow_hashref) {
            #         # $a->{data}   = dateToShow($a->{data});
            #         # $a->{tempo}  = &dateToShow($a->{tempo});
            #         $a->{descrp} = &get($a->{descrp}, "NEWLINE_SHOW");
            #         $a->{executor_descrp} = &get($a->{executor_descrp}, "NEWLINE_SHOW");
            #         
        	# 		$array_radio_chamado .= "<div class=\"tkt_list_line_sub\">";
            #         $array_radio_chamado .= " 	<div style=\"width:1.5%\"></div>";
        	# 		$array_radio_chamado .= " 	<div style=\"width:5%\">#".$c->{codigo}.".".$a->{codigo}."</div> ";
        	# 		$array_radio_chamado .= " 	<div style=\"width:12%\">".$a->{data}."</div>";
        	# 		$array_radio_chamado .= " 	<div style=\"width:5%\">".$a->{tempo}."</div>";
            #         $array_radio_chamado .= " 	<div style=\"width:12%\">".$a->{usuario_nome}."</div> ";
        	# 		$array_radio_chamado .= " 	<div style=\"width:12%\">".$a->{executor_nome}."</div> ";
            #         $array_radio_chamado .= " 	<div style=\"width:20%\">".$a->{descrp}."</div> ";
        	# 		$array_radio_chamado .= "   <div style=\"width:27%\">".$a->{executor_descrp}."</div> ";
        	# 		$array_radio_chamado .= "</div>";
            #     }
            #     # $array_radio_chamado .= "<div>";
            #     # foreach $k (keys %{ $aa }) {
            #     #   $array_radio_chamado .= "$k -> ".$aa->{$k}."**";
            #     # }
            #     # $array_radio_chamado .= "</div>";
            # }
            
            $array_radio_chamado .= " '},";
            
			}
		# $array_radio_chamado = substr($array_radio_chamado, 0,-1); # remove ultima virgula
        } else {
            $array_radio_chamado .= "{ val:0, descrp:'<div style=\"width:100%\">Nenhum registro encontrado !</div>' }";
        }
		

    $radio_title  = "<div class=\"tkt_list_title\">";
	$radio_title .= "	<div style=\"width:5%\">Codigo</div>";
	$radio_title .= "	<div style=\"width:12%\">Data</div>";
	$radio_title .= "	<div style=\"width:5%\">Tempo</div>";
	$radio_title .= "	<div style=\"width:10%\">Cliente</div>";
	$radio_title .= "	<div style=\"width:10%\">Solicitante</div> ";
	$radio_title .= "	<div style=\"width:10%\">Responsável</div> ";
    $radio_title .= "	<div style=\"width:5%\">Ações</div> ";
    $radio_title .= "	<div style=\"width:32%\">Problema</div> ";
    $radio_title .= "	<div style=\"width:5%\">Status</div> ";
    $radio_title .= "</div>";
	

print<<HTML;
		<script>
            
			\$("#chamados_list_container").DTouchRadio({ 
                itemAdd     : [$array_radio_chamado], 
				orientation : 'vertical',
				title       : '$radio_title',
				search      : true,
                searchFile  : "edit_list",
                searchAdvanced : function(x) {
                    
                },
                postFunction : function(x) {    
                    
                    // script passa 2x por aqui 
                    // verificar problema desconhecido
                    // adicionei esse controle para sanar temporariamente
                    if(!x){
                        return;
                    }
                    
                    var t = \$(".eos_template_chamado_filter").clone().show(); // clona objeto template
                    
                    t.find(".filter_date_ini input")
                        .prop({
                            type : "text",
                            name : "filter_date_ini",
                            id   : "filter_date_ini",
                            placeholder : "Data Inicial"
                        });
                        
                    t.find(".filter_date_end input")
                        .prop({
                            type : "text",
                            name : "filter_date_end",
                            id   : "filter_date_end",
                            placeholder : "Data final"
                        });
                    

                    t.find(".filter_empresa input")
                        .prop({
                            type : "text",
                            name : "filter_empresa",
                            id   : "filter_empresa"
                        });                    

                    
                    var form_adv = x.find(".DTouchRadio_search .DTouchRadio_search_adv_form").empty();
                    t.appendTo(form_adv); 
                    
                    // inicia campos
                    \$("#filter_date_ini")
                        .fieldDateTime({ 
                            type        : "date",
                            // placeholder : "Data inicial"
                        });
                        
                    \$("#filter_date_ini").fieldDateTime("value","$filter_date_ini");
                    
                    \$("#filter_date_end")
                        .fieldDateTime({ 
                            type        : "date",
                            // placeholder : "Data inicial"
                        });

                    \$("#filter_date_end").fieldDateTime("value","$filter_date_end");

                    // Atualiza variáveis de pesquisa
                    odate_ini = "$ofilter_date_ini";
                    odate_end = "$ofilter_date_end";
                    oemp_cod = '$filter_empresa';
                    oemp_desc = '$filter_empresa_descrp';
                    osearch = '$filter_search';
                    
                    \$("#filter_empresa")
                        .fieldAutoComplete({ 
        					sql_tbl      : "empresa",
        					sql_sfield   : "nome",
        					sql_rfield   : "nome",
        					sql_order    : "nome",
        					postFunction :function(x) {
        					},
        					onReset      : function() {
        						// \$("#cliente_endereco").DTouchRadio("reset","hard");
        					},
        					placeholder  : "Selecione o Cliente",
                            filled       : {
                                id  : '$filter_empresa',
                                val : '$filter_empresa_descrp'
                            }
        				});
                        
                    \$("#chamados_list_container_search_field").val("$filter_search");
                                          
                },
				click : function(x) {
                    if(x.value === "0"){
                        return false;
                    }
                    
					\$('#COD').val(x.value);
                    chamado.edit();
					\$('#DTouchPages_chamado').DTouchPages("page","center")
					\$('#info_container').show();
				},
				dblClick : function(x) {
					console.log("dbl click SHIT");
				}
			});
			
		</script>
HTML
