#!/usr/bin/perl

$nacess = "2";
require "../cfg/init.pl";
require "../cfg/DPAC/DefaultModule.pl";

$ID  = &get('ID'); 
$TBL = &get('TBL');

print $query->header({charset=>utf8});



# Lista o nome das colunas para montar o formulário
$DB = DBE("
        select 
            column_name as name, 
            data_type as type, 
            character_maximum_length as maxlength, 
            is_nullable as null, 
            column_default as default   
        from 
            information_schema.columns 
        where 
            table_name = '$TBL' $SQL 
        order by 
            ordinal_position
");

if($DB->rows() > 0) {
    $i = 0;
    $e = 0;
    $o = 0;
    while($c = $DB->fetchrow_hashref) {
        $c->{default} =~ s/'/\\\'/gm;
        
        if(listField($c->{name}) eq "show"){
            # $title .= "	<div style=\"width:20%\">$c->{name} (".listField($c->{name})." | $c->{maxlength} | $c->{type} | $c->{default}  | $c->{null}</div> ";            
            $fieldsprint[$i] = $c->{name};
            $i += 1;
        } elsif(listField($c->{name}) eq "hidden") {
            $fieldshidden[$e] = $c->{name};
            $e +=1;
        }
        
        $fields .= $c->{name}.",";
        $fieldsall[$o] = $c->{name};
        $o += 1;
    }
    $fields  = substr($fields, 0,-1); # remove ultima virgula
    
    # largura das colunas
    $width = 100 / $i;
    
    # gera titulo da listagem
    foreach $f (@fieldsprint) { 
        $title .= "	<div style=\"width:$width%\">".translateTitle($f)."</div> ";
    }
    
    
    # ajusta where baseado nos campos
    $w = 0;
    foreach $f (@fieldsall){ 
        if($f eq "parceiro"){
            $WHERE .= "parceiro = ".$USER->{empresa};
            $w += 1;
        }    
    }
    if($w > 0) {
        $WHERE = " where ".$WHERE." ";
    }
        
    # lista tabela
    $DB = DBE("
        select 
            $fields
        from 
            $TBL
        $WHERE
        $ORDER
    "); 

# foreach $k (keys %{ $aa }) {
            #     #   $array_radio_chamado .= "$k -> ".$aa->{$k}."**";
            #     # }
            #$i=0;
            #foreach $c (@acao_descrp) {
            #    print " -> ".$c."<hr>";
            #    $i+=1;
            #}
        
        
    while($line = $DB->fetchrow_hashref) {
                 
        if($line->{status} == 0) {
            $ckd = "Não";
        } else {
            $ckd = "Sim";
        }
         
        # $line->{problema} = &get($line->{problema}, "NEWLINE_SHOW");
         
        $defaultmod .= "{";
        $defaultmod .= "  \"val\"    : \"$line->{codigo}\",";
        $defaultmod .= "  \"descrp\" : \"";
        $defaultmod .= "     <div class='DTouchRadio_list_line'>";
        
        foreach $f (@fieldshidden) {
            $defaultmod .= "         <input type='hidden' name='$f' value='$line->{$f}' />";
        }
        
        foreach $f (@fieldsprint) {
            $defaultmod .= "         <div style='width:$width%'>$line->{$f}</div>";
        }
        #$defaultmod .= "         <div style='width:50%'>$line->{problema}</div>";
        $defaultmod .= "     </div>";
        $defaultmod .= "\"},";
	}
    
} else {
        $defaultmod .= "{ val:0, descrp:'<div style=\"width:100%\">Nenhum registro encontrado !</div>' }";
}

# title
$title  = "<div class=\"DTouchRadio_list_title\">".$title."</div>";

print<<HTML;
<script>
    \$("#defaultmod_list").DTouchRadio({
        orientation : "vertical",
    	title       : '$title',
    	search      : true,
        itemAdd     : [$defaultmod],
        click       : function(x){
            form.edit(x.value);
            // console.log(x.value);
        }
    });
</script>
HTML

