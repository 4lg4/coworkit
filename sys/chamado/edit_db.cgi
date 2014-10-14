#!/usr/bin/perl

$nacess = "10";
require "../cfg/init.pl";

# Prioridade do chamado
$DB = DBE("select * from tkt_prioridade order by descrp");
while($p = $DB->fetchrow_hashref) {
	$chamado_prioridade .= "{val:$p->{codigo},descrp:'$p->{descrp}',img:'$p->{img}'},";
}

# Data, pega data atual
$now = timestamp("human");


# retorno
print $query->header({charset=>utf8});
print<<HTML;

<script>	
	\$("#prioridade").DTouchRadio({ 
		addItem:[$chamado_prioridade] 
	});	
    
    \$("#prioridade").DTouchRadio("value",1);
</script>

HTML

# foreach $k (keys %{ $USER }) {
#    $R .= "console.log('$k - $USER->{$k}');"
# }
# se for cliente do parceiro
#
if($USER->{tipo} eq "99") {
    $DB = DBE("
        select 
            * 
        from 
            parceiro_empresa 
        where 
            empresa = $USER->{empresa}
    ");
    
    if($DB->rows() > 0){
        print " 
            <script>
                \$('#cliente').val('$USER->{empresa}');
                
                
				empresa.endereco();
                \$('#plano').DTouchRadio('reset','hard'); // zera planos
                \$('#plano_container').DTouchBoxes('hide'); // esconde planos
				empresa.area();
				chamado.prioridade();
            </script>";
    }
} else {
    print " 
        <script>
            \$('#cliente_descrp_container').show();
            \$('#data_previsao_container').show();
        </script>
    ";
}


