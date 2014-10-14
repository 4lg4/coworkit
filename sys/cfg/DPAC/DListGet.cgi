#!/usr/bin/perl
require "../init.pl";

# [INI] ----------------------------------------------------------------------------------------------------------------------
#   DListGet / gera select apartir da tabela especifica
#
#	$T = tabela
#	$C = campo de Codigo
#	$D = campo de Descrp
#	$O = campo de ordenacao
#	$L = Limite
#	$W = instrucao where
#	$R = retorno do objeto javascript
# ----------------------------------------------------------------------------------------------------------------------------	
# sub DListGet
#	{ my ($T,$C,$O,$W) = @_;

sub DListGetImgGen {
    my ($img,$table) = @_;
    
    if($table eq "usuario") {
        return " , \"img\" : \"/sys/cfg/DPAC/view_avatar.cgi?MD5=$img\"";
    } else {
        if($img) {
            return " , \"img\" : \"$img\"";
        }
    }
}

# pega variaveis
$ID = &get("ID");   # ID do usuario logado
$T  = &get("T");    # tabela 
$C  = &get("C");    # campo codigo (id)
$D  = &get("D");    # campo descrp (descricao / codigo / titulo)
$L  = &get("L");    # limite de retorno dos registros

    # se tabela especial	
    if($T eq "usuario") { # usuario
        $C = "usuario";
        $D = "nome";
        $W = "where empresa = ".$USER->{empresa}." and bloqueado is false and usuario <> 1";
    } elsif($T eq "usuario_admin" || $T eq "usuario_adm" || $T eq "usuario_administrativo") { # usuario admin
        $T = "usuario_full";
        $C = "usuario";
        $D = "nome";
        $W = "where empresa = ".$USER->{empresa}." and bloqueado is false and usuario <> 1 and grupo = 1"; # tipo = 1 (administrativo)
    } elsif($T eq "usuario_tecnico") { # usuario tecnicos
        $T = "usuario_full";
        $C = "usuario";
        $D = "nome";
        $W = "where empresa = ".$USER->{empresa}." and bloqueado is false and usuario <> 1 and grupo = 2"; # tipo = 2 (tecnicos)
    } elsif($T eq "usuario_dev") { # usuario tecnicos
        $T = "usuario_full";
        $C = "usuario";
        $D = "nome";
        $W = "where empresa = ".$USER->{empresa}." and bloqueado is false and usuario <> 1 and grupo = 3"; # tipo = 3 (devils)
    } elsif($T eq "empresa") {
        $D = "nome";
        $W = "where empresa = ".$USER->{empresa};
    } elsif(
            $T eq "tipo_endereco" || 
            $T eq "prod_unidade"
        ) {
        $W = "where parceiro = ".$USER->{empresa};
    } elsif($T eq "tipo_contato") {
        $W   = "where parceiro = ".$USER->{empresa};
        $IMG = "YES";
        
        if($USER->{empresa} ne "1") {
            $SQL = "select t.codigo as codigo, t.descrp as descrp, tc.img as img from tipo_contato as t left join tipo_contato as tc on tc.codigo = t.pai where t.parceiro = ".$USER->{empresa};
        }
    } 
    
    
    #elsif($T eq "usuario_tipo_freemium") {
     #   $T = "usuario_tipo";
        # $W = "where descrp <=> 'administrador' or descrp <=> 'tecnico' ";
      #  $W = "where descrp <=> 'tecnico' ";
    #}
    
	# codigo
	if(!$C){ 
        $C = "codigo"; 
    }
	
	# descricao
	if(!$D){ 
        $D = "descrp"; 
    }
    
	# descricao
	if(!$I){ 
        $I = "img"; 
    }
			
	# ordenacao
	if(!$O){ 
        $O = "$D"; 
    }
		
	# limite
	if($L){ 
        $L = "limit $L"; 
    }
	    
	# busca
    my $DB;
    if(!$SQL) {
        $DB = &DBE("select * from $T $W order by $O $L");
    } else {
        $DB = &DBE($SQL);
    }
 	# my $Q = $DB->rows();

 	# cria objeto
 	while($r = $DB->fetchrow_hashref){
 		$R .= "{";
        $R .= "  \"codigo\" : \"$r->{$C}\", ";
        $R .= "  \"val\"    : \"$r->{$C}\", ";
		$R .= "  \"descrp\" : \"$r->{$D}\", ";
        $R .= "  \"id\"     : \"$r->{$C}\", ";
        $R .= "  \"value\"  : \"$r->{$D}\" ";
        
        # adiciona imagem a lista
        if($IMG) {
            $R .= ",  \"img\"    : \"$r->{img}\" ";
        }
        
        $R .= DListGetImgGen($r->{$I},$T);
        $R .= "},";
        
		# $R .= "<option value='$r->{$C}'>$r->{$D}</option>";
 	}

	# remove ultima virgula
	$R = "[".substr($R, 0,-1)."]"; 
	
	# finaliza obj
	# $R = "[$R]";
	
	# $R = "<select id='$T'>$R</select>";

# retorno
# print $query->header('application/json');

# print $query->header({charset=>utf8});
print $query->header('application/json; charset="utf-8"');
print $R;
	
	# retorno
# 	return $R;
# 	}
# [END] DListGet -------------------------------------------------------------------------------------------------------------

