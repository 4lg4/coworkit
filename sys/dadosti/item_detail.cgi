#!/usr/bin/perl

$nacess = '204';
require "../cfg/init.pl";

$ID = &get('ID');
$ID       = &get('ID');
$empresa  = &get('empresa');
$endereco = &get('endereco');
$grupo    = &get('grupo');
$linha    = &get('linha');

$insert       = &get('insert');
$empresa_nome = &get('empresa_nome');
$grupo_nome   = &get('grupo_nome');
	
$cfg_3 = &get_cfg(3);
	
print "Content-type: text/html\n\n";


sub insert
	{
	# $out .= "<dl class='form' style='margin-left: 1%; width: 80%;'>";
	$SQL = "select distinct tipo_grupo_item.codigo, tipo_grupo_item.descrp, seq, tipo_grupo_item.supervisor as hidden from grupo_item join tipo_grupo_item on grupo_item.tipo = tipo_grupo_item.codigo ";
	$SQL .= " where grupo_item.grupo = '$grupo' ";
	$SQL .= "order by seq";


	$sth3 = &select($SQL);
	$rv3 = $sth3->rows();
	$ncol = 0;
	if($rv3 > 0)
		{
		while($row3 = $sth3->fetchrow_hashref)
			{
			$codcol[$ncol] = $row3->{'codigo'};
			$nomecol[$ncol] = $row3->{'descrp'};
			$hiddecol[$ncol] = $row3->{'hidden'};
			$ncol++;
			}
		}

	for($e=0; $e<$ncol; $e++)
		{
            # descricao 
            $out .= "<div class='dti_form_left'>$nomecol[$e]";
            #if($descrp_control == 0) {
    		    $out .= "<input type='hidden' name='GRUPO_ITEM_' id='GRUPO_ITEM_$codcol[$e]' value='$codcol[$e]'>";
            #    $descrp_control += 1;
            #} else {
            #    $descrp_control = 0;
            #}
            $out .= "</div>";
            
		#if($hiddecol[$e])
		#	{
		#	$out .= "<dt style='color: #cc5555; font-weight: bold;'>";
		#	}
		#else
		#	{
		#	$out .= "<dt>";
		#	}
        
		#$out .= "$nomecol[$e]<input type='hidden' name='GRUPO_ITEM_$BOX' value='$codcol[$e]'></dt>";
		#$out .= "<dd><input type='text' id='c".$e."' name='GRUPO_ITEM_VALOR_$BOX' value='' onKeyUp='checkChange(\"$BOX\", this.value, \"\")'";
		#if($hiddecol[$e])
	#		{
	#		$out .= " style='border: solid 1px #cc5555'></dd>";
	#		}
	#	else
	#		{
	#		$out .= "></dd>";
	#		}
            
        $out .= "<div class='dti_form_right'><input type='text' name='GRUPO_ITEM_VALOR_' id='GRUPO_ITEM_VALOR_$codcol[$e]' value='' ></div>";
		}
	# $out .= "</dl>";

	# $out =~ s/<ICONEX>/<img src='$dir{'img_syscall'}cancelar.png' border=0 alt='cancelar' style='margin-top: 4px; cursor: pointer;' id='detail_icon_cancel_$BOX' onClick='document.forms[0].reset(); hide(\"detail_icon_save_$BOX\"); hide(\"cx4_$BOX\"); parent.block(false);'><img src='$dir{'img_syscall'}salvar.png' border=0 alt='salvar' style='margin-top: 4px; cursor: pointer;' id='detail_icon_save_$BOX' onClick='hide("detail_icon_save_$BOX"); salvar("$LINHA", "$GRUPO", "$ENDERECO", "$COD");'>/gm;
    
    
    print $out;

    print "<script>
            // dadoti.itens.item.codigo = '$linha';
            \$('#form_item_container').DTouchBoxes('title', 'Novo item de [$grupo_nome] para [$empresa_nome] ');
            </script>";
    
    exit;
	}
    
    
if($insert) {
    insert();
}
    
    


	$SQL = "select distinct tipo_grupo_item.codigo, tipo_grupo_item.descrp, seq, grupo_empresa.endereco, tipo_grupo_item.supervisor as hidden from grupo_item join tipo_grupo_item on grupo_item.tipo = tipo_grupo_item.codigo join grupo_empresa on grupo_item.grupo = grupo_empresa.grupo ";
	$SQL .= " where grupo_empresa.linha = '$linha' and grupo_empresa.grupo = '$grupo' ";
	$SQL .= "and grupo_empresa.empresa = '$empresa' and grupo_empresa.endereco = '$endereco' ";
	if($nacess_tipo ne "s") {
		$SQL .= " and tipo_grupo_item.supervisor is false ";
	}
	$SQL .= "order by seq";

	$sth3 = DBE($SQL);
	$ncol = 0;
	if($sth3->rows() > 0)
		{

		while($row3 = $sth3->fetchrow_hashref)
			{
			$endereco        = $row3->{'endereco'};
			$codcol[$ncol]   = $row3->{'codigo'};
			$nomecol[$ncol]  = $row3->{'descrp'};
			$hiddecol[$ncol] = $row3->{'hidden'};
			$ncol++;
			}

        $descrp_control = 0;
		for($e=0; $e<$ncol; $e++)
			{
            
            # descricao 
            $out .= "<div class='dti_form_left'>$nomecol[$e]";
            #if($descrp_control == 0) {
    		    $out .= "<input type='hidden' name='GRUPO_ITEM_' id='GRUPO_ITEM_$codcol[$e]' value='$codcol[$e]'>";
            #    $descrp_control += 1;
            #} else {
            #    $descrp_control = 0;
            #}
            $out .= "</div>";
            
                
            # conteudo 
			if($empresa) {
				$SQL_emp = "and grupo_empresa.empresa = '$empresa' and grupo_empresa.endereco = '$endereco' ";
			}           
             
			$sth2 = DBE("
                    select 
                        distinct * 
                    from 
                        grupo_empresa 
                    where 
                        grupo_item = '$codcol[$e]' and 
                        linha      = '$linha' and 
                        grupo_empresa.grupo = '$grupo' 
                        $SQL_emp
                    limit 1
                ");
                
			if($sth2->rows() == 0) {
		
				$out .= "<div class='dti_form_right'><input type='text' name='GRUPO_ITEM_VALOR_' id='GRUPO_ITEM_VALOR_$codcol[$e]' value='' ></div>";
					
			} else {
                
				while($row2 = $sth2->fetchrow_hashref) {

					$out .= "<div class='dti_form_right'><input type='text' name='GRUPO_ITEM_VALOR_'  id='GRUPO_ITEM_VALOR_$codcol[$e]' value='".$row2->{'valor'}."' ></div>";
						
				}
			}
		}
        
		
    }



print $out;

print "<script>
            dadoti.itens.item.codigo = '$linha';
            \$('#form_item_container').DTouchBoxes('title', 'Editar item de [$grupo_nome] de [$empresa_nome] ');
            </script>";


exit;






