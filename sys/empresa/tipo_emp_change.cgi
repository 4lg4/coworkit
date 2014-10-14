#!/usr/bin/perl
 
# 
# tipo_emp_change.cgi
# carrega os campos especificos pelo tipo da empresa e campos personalizados
#

$nacess = '201';
require "../cfg/init.pl";

$tipo_emp = &get('tipo_emp');
$COD = &get('COD');


# se for inclusao 
if($COD eq "") {
	$SQL = "
        select 
            td.codigo as cod_doc, 
            td.minidescrp as tipo_doc, 
            td.descrp as holder 
        from 
            tipo_doc as td
    ";
} else {
	$SQL = "
        select 
            td.*, 
            td.codigo as cod_doc, 
            td.minidescrp as tipo_doc, 
            empresa_doc.descrp as empresa_doc 
        from 
            tipo_doc as td 
        left join 
            empresa_doc on td.codigo = empresa_doc.doc and 
            empresa_doc.empresa = $COD 
    ";
}
	
# finaliza montagem sql
$SQL .= " where td.empresa_tipo ilike '$tipo_emp' and td.parceiro = $USER->{empresa}";
$SQL .= " order by td.descrp";

# executa sql
$DB = &DBE($SQL);

# gera os campos
if($DB->rows() > 0) {
	while($r = $DB->fetchrow_hashref) {
        $R .= "<div class='empresa_mais_dados_line'>";
		$R .= "     <div class='empresa_mais_dados_descrp'>";
		$R .= "         <input type='hidden' name='tdoc_descrp' value='$r->{tipo_doc}'>";
		$R .= "         $r->{tipo_doc}<input type='hidden' name='tdoc' value='$r->{cod_doc}'>";
        $R .= "     </div>";
        $R .= "     <div class='empresa_mais_dados_input'>";
        $R .= "         <input type='text' name='doc' value='$r->{empresa_doc}' title='$r->{tipo_doc}'  placeholder='$r->{holder}'>";
        $R .= "     </div>";
        $R .= "</div>";
	}
} else {
	$R = "Nenhum campo documento encontrado !";
}


# retorno
print $query->header({charset=>utf8});

print<<HTML;

<script>
	\$(".empresa_mais_dados").html("$R");
    
    \$(".empresa_mais_dados input[type=text]").each(function(){
        eos.template.field.text(\$(this));
    });
</script>

HTML
	
exit;

