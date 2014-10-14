#!/usr/bin/perl

$nacess = '204';
require "../cfg/init.pl";

$ID       = &get('ID');
$empresa  = &get('empresa');
$endereco = &get('endereco');
$grupo    = &get('grupo');
$agrupo   = &get('agrupo');

# $ENDERECO = &get('cod_endereco');
# $MODO     = &get('MODO');

print $query->header({charset=>utf8});
# debug($USER->{empresa});
# exit;

if($grupo) {
    $grupo = " where ge.grupo = '$grupo' ";
}

$DB = DBE("
        select 
            distinct ee.codigo as endereco, 
        	e.codigo as empresa, 
        	e.nome,
        	e.apelido, 
        	ee.endereco as endereco_descrp,
        	ee.cidade,
        	ee.uf
        from 
        	grupo_empresa as ge
        join 
        	empresa_endereco as ee on ee.empresa = ge.empresa and ee.codigo = ge.endereco
        join 
        	empresa as e on e.codigo = ee.empresa 
        join 
        	tipo_endereco as te on te.codigo = ee.tipo  
        join 
        	parceiro_empresa as pe on pe.empresa = e.codigo and pe.parceiro = $USER->{empresa}  
        order by 
        	e.nome, ee.uf, ee.cidade, ee.endereco
        asc
");

if($DB > 0) {
	while($e = $DB->fetchrow_hashref) {
        
        if(!$e->{apelido}){
            $e->{apelido} = $e->{nome};
        }
        
        $dados .= "{";
        $dados .= "  \"val\"    : \"$e->{endereco}\",";
        $dados .= "  \"descrp\" : \"";
        $dados .= "     <div class='DTouchRadio_list_line'>";
        $dados .= "         <div style='width:50%'>";
        $dados .= "         <input type='hidden' name='empresa' value='$e->{empresa}' /> ";
        $dados .= "         <input type='hidden' name='endereco' value='$e->{endereco}' /> ";
        # $dados .= "         <input type='hidden' name='grupo' value='$e->{grupo}' /> ";
        $dados .= "         <div style='display:none;'>$e->{nome}</div>";
        $dados .= "         $e->{apelido}";
        $dados .= "         </div>";
        $dados .= "         <div style='width:30%'>$e->{endereco_descrp}</div>";
        $dados .= "         <div style='width:10%'>$e->{cidade}</div>";
        $dados .= "         <div style='width:10%'>$e->{uf}</div>";
        $dados .= "     </div>";
        $dados .= "\"},";
	}
} else {
        $dados .= "{ val:0, descrp:'<div style=\"width:100%\">Nenhum registro encontrado !</div>' }";
}

#$title  = "<div class=\"DTouchRadio_list_title\">";
#$title .= "	<div style=\"width:47%\">Nome</div> ";
#$title .= "	<div style=\"width:30%\">Endereço</div> ";
#$title .= "	<div style=\"width:10%\">Cidade</div> ";
#$title .= "	<div style=\"width:10%\">Uf</div> ";
#$title .= "</div>";

# print $query->header('application/json; charset="utf-8"');
print $query->header({charset=>utf8});

# $dados = substr($dados, 0,-1);
# $dados = "{$dados}";

print<<HTML;
<script>
    \$("#empresa_list").DTouchRadio({
        orientation : "vertical",
    	// title       : '$title',
    	// search      : true,
        // itemAdd     : [$dados],
        itemAdd     : [$dados],
        click       : function(x){
            dadoti.search.reset();
            dadoti.itens.list(x);
        }
    });
</script>
HTML



