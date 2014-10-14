#!/usr/bin/perl

$nacess = '204';
require "../cfg/init.pl";

$ID = &get('ID');

# $DB = DBE("
#         select 
#             distinct ee.codigo as endereco, 
#         	e.codigo as empresa, 
#         	e.nome,
#         	e.apelido, 
#         	ee.endereco as endereco_descrp,
#         	ee.cidade,
#         	ee.uf
#         from 
#         	grupo_empresa as ge
#         join 
#         	empresa_endereco as ee on ee.empresa = ge.empresa and ee.codigo = ge.endereco
#         join 
#         	empresa as e on e.codigo = ee.empresa 
#         join 
#         	tipo_endereco as te on te.codigo = ee.tipo  
#         join 
#         	parceiro_empresa as pe on pe.empresa = e.codigo and pe.parceiro = $USER->{empresa}  
#         order by 
#         	e.nome, ee.uf, ee.cidade, ee.endereco
#         asc
# ");

#print $query->header({charset=>utf8});
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
        	empresa_endereco as ee
        join 
        	empresa as e on e.codigo = ee.empresa 
        join 
        	tipo_endereco as te on te.codigo = ee.tipo  
        join 
        	parceiro_empresa as pe on pe.empresa = e.codigo and pe.parceiro = '$USER->{empresa}'
        order by 
        	e.nome, ee.uf, ee.cidade, ee.endereco
        asc
");

if($DB > 0) {
	while($e = $DB->fetchrow_hashref) {
        
        if(!$e->{apelido}){
            $e->{apelido} = $e->{nome};
        }
        
        $dados = "     <div class='DTouchRadio_list_line'>";
        $dados .= "         <div style='width:50%'>";
        $dados .= "         <input type='hidden' name='empresa' value='".&get($e->{empresa}, "NEWLINE")."' /> ";
        $dados .= "         <input type='hidden' name='endereco' value='".&get($e->{endereco}, "NEWLINE")."' /> ";
        # $dados .= "         <input type='hidden' name='grupo' value='$e->{grupo}' /> ";
        $dados .= "         <div style='display:none;'>$e->{nome}</div>";
        $dados .= "         $e->{apelido}";
        $dados .= "         </div>";
        $dados .= "         <div style='width:30%'>".&get($e->{endereco_descrp}, "NEWLINE")."</div>";
        $dados .= "         <div style='width:10%'>$e->{cidade}</div>";
        $dados .= "         <div style='width:10%'>$e->{uf}</div>";
        $dados .= "     </div>";
        
    	$R .= "{";
        $R .= "  \"codigo\" : \"$e->{endereco}\", ";
        $R .= "  \"val\"    : \"$e->{endereco}\", ";
    	$R .= "  \"descrp\" : \"$dados\" ";
        $R .= "},";
    }
    $R = "[".substr($R, 0,-1)."]";
}

print $query->header('application/json; charset="utf-8"');
print $R;
