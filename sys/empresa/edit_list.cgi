#!/usr/bin/perl

$nacess = "201";
require "../cfg/init.pl";
$ID = &get('ID');

$DB = DBE("
        select 
        	emp_codigo as codigo,
        	emp_nome as nome,
        	emp_apelido as apelido,
        	end_fone as fone,
            emp_ativo as ativo,
            end_codigo as endereco
        from 
        	empresas_lista_distinct 
        where 
        	parceiro = $USER->{empresa}
        order by
            nome 
        asc
");

if($DB->rows() > 0) {
    
	while($emp = $DB->fetchrow_hashref) {
        if($emp->{ativo} == 0){
            $ativo = "emp_inativa";
        } else {
            $ativo = "";
        }
        
        $emps .= "{";
        $emps .= "  \"val\"    : \"$emp->{codigo}\",";
        $emps .= "  \"descrp\" : \"";
        $emps .= "     <div class='DTouchRadio_list_line $ativo'>";
        $emps .= "         <input type='hidden' name='list_end' value='$emp->{endereco}' />";
        $emps .= "         <div style='width:50%'>$emp->{nome}</div>";
        $emps .= "         <div style='width:30%'>$emp->{apelido}</div>";
        $emps .= "         <div style='width:20%'>$emp->{fone}</div>";
        $emps .= "     </div>";
        $emps .= "\"},";
	}
} else {
        $emps .= "{ val:0, descrp:'<div style=\"width:100%\">Nenhum registro encontrado !</div>' }";
}

$title  = "<div class=\"DTouchRadio_list_title\">";
$title .= "	<div style=\"width:50%\">Nome</div> ";
$title .= "	<div style=\"width:30%\">Apelido</div> ";
$title .= "	<div style=\"width:20%\">Telefone</div> ";
$title .= "</div>";

# print $query->header('application/json; charset="utf-8"');
print $query->header({charset=>utf8});

# $emps = substr($emps, 0,-1);
# $emps = "{$emps}";

print<<HTML;
<script>
    \$("#empresa_list").DTouchRadio({
        orientation : "vertical",
    	title       : '$title',
    	// search      : true,
        itemAdd     : [$emps],
        click       : function(x){
            if(x.value !== "") { 
                empresa.edit(x.value);
                // call("/sys/empresa/edit.cgi",{ COD : x.value });
            }
        },
        postFunction : function(){
            // limites empresas
            \$("#empresa_limit").html(eos.core.limit.empresa.stats());
        }
    });
</script>
HTML

