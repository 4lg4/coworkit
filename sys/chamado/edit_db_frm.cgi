#!/usr/bin/perl

$nacess = "10";
require "../cfg/init.pl";

$COD = &get('COD');

$DB = &DBE("
        select 
            t.*, 
            e.codigo as cliente, 
            e.nome as cliente_nome, 
            u.nome as responsavel_nome, 
            ue.nome as executor_nome 
        from 
            tkt as t left 
        join 
            empresa_endereco as ee on ee.codigo = t.empresa_endereco 
        left join 
            empresa as e on e.codigo = ee.empresa 
        left join 
            usuario as u on u.usuario = t.usuario  
        left join 
            usuario as ue on ue.usuario = t.usuario_executor 
        where 
            t.codigo = $COD
");

$chamado = $DB->fetchrow_hashref;
	
# ajuste datatime	
$chamado->{data} = &dateToShow($chamado->{data});
$chamado->{data_previsao} = &dateToShow($chamado->{data_previsao});
$chamado->{tempo_previsao} = &dateToShow($chamado->{tempo_previsao});
$chamado->{problema} = &get($chamado->{problema}, "HTML"); # remove quebra de linha e aspas
$chamado->{cancelado_motivo} = &get($chamado->{cancelado_motivo}, "HTML"); # remove quebra de linha e aspas

# pai
if($chamado->{pai}) {
    $chamado->{pai} = "<span style='font-weight:normal; font-size:8px;'>(vinculado #$chamado->{pai})</span>";
}

# recuperar email e popular
$DB = &DBE("select * from tkt_email where tkt = $COD order by email asc");
while($e = $DB->fetchrow_hashref) {
	# $chamado_email .= DTouchList('emails_list',$e->{email},$e->{email});
    $emails .= "{ descrp : '".$e->{email}."' },";
}
$emails = "{".$emails."}";

# retorno do codigo 
print $query->header({charset=>utf8});

print<<HTML;

    <script>
        \$("#solicitante_solicitacao_container_solicitacao span").remove(); // limpa formulario principal
        
    	\$("#descrp")
            .val("$chamado->{problema}")
            .hide()
            .parent()
                .append("<span class='descrp_show'>$chamado->{problema}</span>");
        
        /**
         *  Data preenchida trava modificacoes
         */        
        if("$chamado->{data_previsao}" !== "") {
        	\$("#data_previsao")
                .val("$chamado->{data_previsao}")
                .hide()
                .parent()
                    .append("<span class='input_show'>$chamado->{data_previsao}</span>");
            \$("#data_previsao").fieldDateTime("disable");
        
        
        	\$("#tempo_previsao")
                .val("$chamado->{tempo_previsao}")
                .hide()
                .parent()
                    .append("<span class='input_show'>$chamado->{tempo_previsao}</span>");
            \$("#tempo_previsao").fieldDateTime("disable");
            
        }
        
    	\$("#solicitante")
            .val("$chamado->{solicitante}")
            .hide()
            .parent()
                .append("<span class='input_show'>$chamado->{solicitante}</span>");
	
    	// Info
    	\$("#data_inclusao").text("$chamado->{data}");
    	\$("#responsavel").text("$chamado->{responsavel_nome}");
        \$("#responsavel_codigo").text("$chamado->{usuario}");
    	\$("#protocolo").html("#$chamado->{codigo} $chamado->{pai}");
        
	
        /*  Chamado V2 alpha 1 */
        // \$("#executor").val("$chamado->{usuario_executor}");
        // \$("#executor_descrp").val("$chamado->{executor_nome}");
        \$("#executor_container").DTouchBoxes("hide");
    
    	// cliente
    	\$("#cliente").fieldAutoComplete("value", {
            id  : $chamado->{cliente},
            val : "$chamado->{cliente_nome}"
        });
        \$("#cliente")
            .parent()
            .find(".EOS_template_field_field")
                .append("<span class='input_show'>$chamado->{cliente_nome}</span>")
                .find("input")
                    .hide();
        \$("#cliente").fieldAutoComplete("disable");
    
        // cancelado
        if("$chamado->{cancelado}" === "1") {
            \$("#cancelado_container").show();
            \$("#cancelado").text("Cancelado: $chamado->{cancelado_motivo}");
        } else {
            \$("#cancelado_container").hide();
        }
        
        // cliente endereco
    	empresa.endereco($chamado->{empresa_endereco});
    	empresa.area($chamado->{area});
        empresa.planos($chamado->{area},'$chamado->{plano}');
        
    	chamado.prioridade($chamado->{prioridade});
        chamado.emails();
    
        // mostra protocolo
        \$("#protocolo_container").show();
        
        // finalizado
        \$("#finalizado").val("$chamado->{finalizado}");
        
        
        /* mostra salvar se necessario
        if("$chamado->{data_previsao}" === "") { 
            console.log("save save");
            eos.menu.action.show(["icon_tkt_save"]);
        }
        */
    </script>

HTML
