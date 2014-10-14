#!/usr/bin/perl

$nacess = "68";
require "../cfg/init.pl";
$ID = &get('ID');

$DB = DBE("
    select 
        u.*, 
        to_char(data, 'DD/MM/YYYY HH:MM') as data, 
        ut.descrp as usuario_tipo, 
        ua.arquivo as imagem
    from 
        usuario as u
    left join 
        usuario_tipo as ut on ut.codigo = u.tipo
    left join 
        usuario_arquivo as ua on ua.usuario = u.usuario
    where
        u.empresa = $USER->{empresa}
    order by
        u.bloqueado, u.nome asc
");

if($DB->rows() > 0) {
    
	while($u = $DB->fetchrow_hashref) {
        if($u->{bloqueado} == 1 && !$bloqueado){
            $bloqueado = "users_bloqueado";
            
            $users .= "{";
            $users .= "  \"val\"    : \"\",";
            $users .= "  \"descrp\" : \"";
            $users .= "     <div class='DTouchRadio_list_title $bloqueado'>";
            $users .= "         <div style='width:100%'>Bloqueados</div>";
            $users .= "     </div>";
            $users .= "\"},";
        }
        
        # redes sociais
        $DBR = &DBE("
            select 
                ul.*, 
                r.link as rede_link,
                r.descrp as rede_descrp,
                r.img as rede_img
            from 
                usuario_login as ul
            left join
                tipo_rede as r on r.codigo = ul.rede
            where ul.usuario = $u->{usuario}
        ");
        
        $user_logins = "";
        if($DBR->rows() > 0) {
            while($user_login = $DBR->fetchrow_hashref) {
                # $user_logins .= '{';
                # $user_logins .= '   "rede"  : {';
                $user_logins .= "<a href='$user_login->{rede_link}' target='_blank' title='$user_login->{rede_descrp}'><img src='$user_login->{rede_img}'></a> ";
                # $user_logins .= '   },';
                # $user_logins .= '   "id"    : "'.$user_login->{id}.'",';
                # $user_logins .= '   "login" : "'.$user_login->{login}.'",';
                # $user_logins .= '   "link"  : "'.$user_login->{link}.'"';
                # $user_logins .= '},';
            }

            # $user_logins = ', "social" : ['.(substr($user_logins, 0,-1)).']';
        }
        
        
        $users .= "{";
        $users .= "  \"val\"    : \"$u->{usuario}\",";
        $users .= "  \"descrp\" : \"";
        $users .= "     <div class='DTouchRadio_list_line $bloqueado'>";
        $users .= "         <div style='width:20%'><img src='/sys/cfg/DPAC/view_avatar.cgi?COD=".$u->{imagem}."&ID=".$ID."' /></div>";
        $users .= "         <div style='width:30%'>$u->{login}</div>";
        $users .= "         <div style='width:30%'>$u->{nome}</div>";
        $users .= "         <div style='width:20%'>$user_logins</div>";
        $users .= "     </div>";
        $users .= "\"},";
	}
} else {
        $users .= "{ val:0, descrp:'<div style=\"width:100%\">Nenhum registro encontrado !</div>' }";
}

$title  = "<div class=\"DTouchRadio_list_title\">";
$title .= "	<div style=\"width:20%\">Usuário</div> ";
$title .= "	<div style=\"width:30%\">Login</div> ";
$title .= "	<div style=\"width:30%\">Nome</div> ";
$title .= "	<div style=\"width:20%\">Logins</div> ";
$title .= "</div>";

# print $query->header('application/json; charset="utf-8"');
print $query->header({charset=>utf8});

# $users = substr($users, 0,-1);
# $users = "{$users}";

print<<HTML;
<script>
    \$("#users_list").DTouchRadio({
        orientation : "vertical",
    	title       : '$title',
    	search      : true,
        itemAdd     : [$users],
        click       : function(x){
            if(x.value !== "") { 
                form.edit(x.value);
            }
        }
    });
</script>
HTML

