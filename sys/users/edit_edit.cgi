#!/usr/bin/perl

$nacess = "68";
require "../cfg/init.pl";

# vars
$ID  = &get('ID');
$COD = &get('COD');

# statment
$DB = &DBE("
    select 
        u.*, ua.arquivo as imagem
    from 
        usuario as u 
    left join
        usuario_arquivo as ua on ua.usuario = u.usuario
    where u.usuario = $COD
");

# usuario
$user = $DB->fetchrow_hashref;

# avatar
$avatar = "/sys/cfg/DPAC/view_avatar.cgi?COD=".$user->{imagem}."&ID=".&URLEncode($ID);


# redes sociais
$DB = &DBE("
    select 
        ul.*, 
        r.link as rede_link,
        r.descrp as rede_descrp,
        r.img as rede_img
    from 
        usuario_login as ul
    left join
        tipo_rede as r on r.codigo = ul.rede
    where ul.usuario = $COD
");

if($DB->rows() > 0) {
    while($user_login = $DB->fetchrow_hashref) {
        $user_logins .= '{';
        $user_logins .= '   "rede"  : {';
        $user_logins .= '       "link"   : "'.$user_login->{rede_link}.'",';
        $user_logins .= '       "descrp" : "'.$user_login->{rede_descrp}.'",';
        $user_logins .= '       "img"    : "'.$user_login->{rede_img}.'"';
        $user_logins .= '   },';
        $user_logins .= '   "id"    : "'.$user_login->{id}.'",';
        $user_logins .= '   "login" : "'.$user_login->{login}.'",';
        $user_logins .= '   "link"  : "'.$user_login->{link}.'"';
        $user_logins .= '},';
    }

    $user_logins = ', "social" : ['.(substr($user_logins, 0,-1)).']';
}

#
# menus
#
$DB = &DBE("
    select 
        DISTINCT(um.menu),
        m.descrp
    from 
        usuario_menu as um
    left join
        menu as m on m.nacess = um.menu
    where 
        um.usuario = $COD and
        m.show is true
    order by
        m.descrp 
    asc
");

if($DB->rows() > 0) {
    while($user_menu = $DB->fetchrow_hashref) {
        $user_menus .= '{';
        $user_menus .= '   "val"  : "'.$user_menu->{menu}.'",';
        $user_menus .= '   "descrp" : "'.$user_menu->{descrp}.'"';
        $user_menus .= '},';
    }

    $user_menus = '['.(substr($user_menus, 0,-1)).']';
}


# print
print $query->header({charset=>utf8});

    $R  = '{ ';
    $R .= '     "usuario" : '.$user->{usuario}.', ';
    $R .= '     "nome"    : "'.$user->{nome}.'",  ';
    $R .= '     "email"   : "'.$user->{email}.'",  ';
    $R .= '     "login"   : "'.$user->{login}.'",  ';
    $R .= '     "phone"   : "'.$user->{phone}.'",  ';
    $R .= '     "tipo"    : "'.$user->{tipo}.'",  ';
    $R .= '     "lock"    : "'.$user->{bloqueado}.'",  ';
    $R .= '     "imagem"  : { ';
    $R .= '         "codigo" : "'.$user->{imagem}.'",  ';
    $R .= '         "url"    : "'.$avatar.'"  ';
    $R .= '     },  ';
    $R .= '     "menu"    : '.$user_menus.',';
    $R .= '     "secure"  : { ';
    $R .= '         "logado" : '.$USER->{usuario}.',  ';
    $R .= '         "tipo"   : '.$USER->{tipo}.'  ';
    $R .= '     }  ';
    $R .=       $user_logins;
    $R .= '}  ';

print $R;
