#!/usr/bin/perl

$nacess = "68";
require "../cfg/init.pl";
$ID  = &get('ID');
$COD = &get('COD');

print $query->header({charset=>utf8});

print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html id="html">
<head>
	
<script>
/**
 *   Usuario
 *       obj usuario
 */
function Users(){
    
    var u = this;
    
    /* initialize */
    this.initialize = function() {
        // this.list();
    };
    
    /* list, lista de usuarios */
    this.list = function() {
        \$.DActionAjax({
            action : "edit_list.cgi",
            loader : \$("#users_list")
        });
    };
    
    /* new */
    this.new = function(){
        \$("#users_page").DTouchPages("page","right");
    };
    
    /* desbloquear usuario */
    this.unlock = function(){
        \$.DActionAjax({
            action : "edit_submit.cgi",
            req    : "COD="+\$("#COD").val()+"&acao=unlock",
            serializeForm : false,
            postFunction : function(x) {
                if(x){
                    // atualiza limites
                    eos.core.limit.user.get(function(x){
                        \$("#users_limit").html(x);
                    });
                }
            }
        });
    };
    
    /* bloquear usuario */
    this.lock = function(){
        \$.DDialog({
            type    : "confirm",
            message : "Deseja bloquear o usuário",
            btnYes  : function() {
                \$.DActionAjax({
                    action : "edit_submit.cgi",
                    req    : "COD="+\$("#COD").val()+"&acao=lock",
                    serializeForm : false,
                    postFunction : function(x) {
                        if(x){
                            // atualiza limites
                            eos.core.limit.user.get(function(x){
                                \$("#users_limit").html(x);
                            });
                        }
                    }
                });
            }
        });
    };
    
    
    /* modificar senha */
    this.changePwd = function(){
        \$("#users_login_senha").show();
        \$("#users_login_senha_change").hide();
        eos.menu.action.hide("icon_users_pwd");
    };
    
    /* redes sociais */
    this.social = {
        /* lista redes do usuario */
        list : function(x){
            x.forEach(function(i){
                console.log(i); 
                
                var s  = "<div class='social'>";
                    s += "      <a href='"+i.rede.link+"' target='_blank' title='"+i.rede.descrp+"'>";
                    s += "          <img src='"+i.rede.img+"'>";
                    s += "      </a> ";
                    s += "      <a href='"+i.link+"' target='_blank' title='meu perfil'>";
                    s +=            i.login;
                    s += "      </a> ";
                    s += "</div>";
                \$("#users_logins").append(s);
            });
        }
    }
    
    
    /* menus */
    this.menus = {
        // adiciona item
        add : function(i) {
            \$("#menus").DTouchRadio("addItem",i);
        },
        list : function(menus) {
            \$("#menus").DTouchRadio("addItem",menus);
        }
    };
    
    /* editar */
    this.edit = function(){
        // remove imagem
        \$("#users_avatar").prop("src","");  
        \$("#CODIMG").val("");
        \$("#senha, #senha_new, #senha_conf").val("");
        \$("#users_avatar_container").hide();
        
        // senha
        \$("#users_login_senha_change").show();
        \$("#users_login_senha_new, #users_login_senha_conf, #users_login_senha_old").show();
        \$("#users_login_senha").hide();
        
        // mostra upload imagem
        \$("#users_dados_imagem").show();
        \$("#imagem").DUpload({
            link : {
                tbl    : "usuario",
                codigo : \$("#COD").val()
            },
            placeholder : "Imagem Usuário",
            automatic   : true,
            mimetype    : ["image"],
            postFunction : function(x){
                
                // atualiza avatar
                function refreshAvatar(){
                    \$("#CODIMG").val(x.codigo);
                    \$("#users_avatar").prop("src","");    // remove imagem ao trocar
                    \$("#users_avatar_container, #users_avatar_change, #users_avatar_del").show(); // mostra imagem
                    \$("#users_dados_imagem").hide(); // esconde formulario
            
                    // atualiza imagem
                    \$("#users_avatar").prop("src","/sys/cfg/DPAC/view_avatar.cgi?COD="+x.codigo+"&ID="+\$("#AUX input[name=ID]").val());
                    \$("#user_menu_float_avatar img").prop("src","/sys/cfg/DPAC/view_avatar.cgi?COD="+x.codigo+"&ID="+\$("#AUX input[name=ID]").val());
                }
                
                // deleta imagem antiga
                if(\$("#CODIMG").val()){
                    eos.core.upload.delete(\$("#CODIMG").val(), function(){
                        refreshAvatar();
                    });
                } else {
                    refreshAvatar();
                }                    
            }
        });
        
        // trocar imagem
        \$("#users_avatar_change").click(function(){
            \$("#users_avatar_container").hide(); // esconde imagem
            \$("#users_dados_imagem").show();     // mostra formulario
            \$("#imagem").DUpload("reset");
            \$("#imagem").DUpload("focus");
        });
        
        // remove imagem
        \$("#users_avatar_del").click(function(){
            \$.DDialog({
                type    : "confirm",
                message : "Deseja remover o avatar ?",
                btnYes  : function(){
                    eos.core.upload.delete(\$("#CODIMG").val(), function(){
                        \$("#CODIMG").val("");
                    });
                    
                    \$("#users_avatar_container").hide();  // esconde imagem
                    \$("#users_dados_imagem").show();      // mostra formulario
                    \$("#users_avatar").prop("src","");    // remove imagem
                }
            })
        });
        
        /* edita formulario */
        \$.DActionAjax({
            action : "edit_edit.cgi",
            req    : "COD="+\$("#COD").val(),
            loader : \$("#users_page_right"),
            postFunction : function(x){ // console.log(x);
                var user = JSON.parse(x);
                
                \$("#nome").val(user.nome);
                \$("#email").val(user.email);
                \$("#login").val(user.login);
                \$("#phone").val(user.phone);
                
                \$("#login").fieldEmail("disable"); // somente leitura
                
                // tipo
                \$("#users_tipo").DTouchRadio("value",user.tipo);
                
                // imagem
                if(user.imagem.codigo) { 
                    \$("#users_dados_imagem").hide(); // esconde imagem
                    \$("#users_avatar_container, #users_avatar_change, #users_avatar_del").show(); // mostra formulario
                    
                    \$("#users_avatar").prop("src",user.imagem.url); // atualiza imagem
                    \$("#CODIMG").val(user.imagem.codigo);
                } else {  // campo upload
                    \$("#users_dados_imagem").show(); // mostra formulario
                }
                
                
                //u.menus.list(i);
                \$("#menus_container").show();
                user.menu.forEach(function(i){
                    u.menus.add(i);
                });
                
                
                // icones
                eos.menu.action.hideAll();
                eos.menu.action.show(["icon_users_new","icon_users_save"]);
                
                // ajustes por nivel do usuario logado
                if(user.secure.logado === user.usuario){
                    \$("#users_login_senha_change").show();
                    eos.template.field.unlock(\$("#nome"));
                    eos.template.field.unlock(\$("#phone"));
                    \$("#email").fieldEmail("enable");
                    \$("#phone").fieldNumber("enable");
                } else if(user.secure.tipo === 1) { // adm
                    \$("#users_login_senha_old").hide();
                    
                    if(user.lock === "0"){
                        eos.menu.action.show(["icon_users_lock"]);
                    } else {
                        eos.menu.action.show(["icon_users_unlock"]);
                    }
                    
                } else { // nao pode alterar cadastro
                    \$("#users_dados_imagem").hide();
                    \$("#users_login_senha_change").hide();
                    eos.template.field.lock(\$("#nome"));
                    eos.template.field.lock(\$("#phone"));
                    \$("#email").fieldEmail("disable");
                    \$("#phone").fieldNumber("disable");
                }
                
                
                // redes sociais
                if(user.social) { 
                    users.social.list(user.social);
                }
            }
        });
        
    };
}


/**
 *   Form
 *       obj formulario
 */
function Form(){
    
    /* initialize */
    this.initialize = function(){
		\$("#users_page").DTouchPages({
            // pageChange: "center",
            pageCenter : \$("#users_page_center"),
            pageRight  : \$("#users_page_right"),
			postFunctionCenter : function() {
                users.list();
                
                eos.menu.action.hideAll();
                eos.menu.action.show("icon_users_new");
                form.reset();
            },
			postFunctionRight : function() {
                if(!\$("#COD").val()) {
                    // icones
                    eos.menu.action.hideAll();
                    eos.menu.action.show(["icon_users_new","icon_users_save"]);
                }
            },
			onCreate : function() {
                
                /* inicializa objs *
                \$("#users_list").DTouchRadio({
                    orientation : "horizontal"
                })
                 */
                
                \$("#users_dados_container").DTouchBoxes({ title : "Dados Pessoais" });
                \$("#users_login_container").DTouchBoxes({ title : "Login" });
                \$("#users_tipo_container").DTouchBoxes({ title : "Tipo de Usuário" });
                \$("#users_logins_container").DTouchBoxes({ title : "Logins Social" });
                \$("#menus_container").DTouchBoxes({ title : "Menus" });
                
                // menus
                \$("#menus").DTouchRadio({
                    orientation : "vertical",
                    unique  : false //,
                    // itemDel : true
                });
                
                // tipos de usuario
                \$("#users_tipo").DTouchRadio({
                    orientation : "horizontal",
                    tbl : "usuario_tipo_freemium",
                    postFunction : function(x){ 
                       //  x.DTouchRadio("disable");
                    }
                });
                \$("#users_tipo").DTouchRadio("disable");
                
                
                \$("#users_avatar_container").hide();
                \$("#users_login_senha").hide();
                \$("#users_login_senha_change").click(function(){
                    users.changePwd();
                });
                
                
                eos.template.field.text(\$("#nome"));
                // eos.template.field.text(\$("#phone"));
                eos.template.field.password(\$("#senha"));
                eos.template.field.password(\$("#senha_new"));
                eos.template.field.password(\$("#senha_conf"));
                \$("#login").fieldEmail();
                \$("#email").fieldEmail();
                \$("#phone").fieldNumber();
                
                users = new Users();
                users.initialize();

                // inicializa limites
                eos.core.limit.user.get(function(x){
                    \$("#users_limit").html(x);
                });
                    
                         
                // inicia no formulario
                if(\$("#COD").val() === "0"){ // novo
                    
                    form.reset(); // limpa formulario
                    \$("#users_page").DTouchPages("page","right");
                    
                } else if(\$("#COD").val()){ // edicao
                    
                    form.edit(\$("#COD").val());
                }                
            }
        });   
        
        this.menu(); // inicia menu
    }
    
    /* menu */
    this.menu = function(){
        
        eos.menu.action.new({ // salvar
            id       : "icon_users_save",
            title    : "salvar",
            subtitle : "usuário",
            click    : function(){
                form.save();
            }
        });
        
        eos.menu.action.new({ // excluir
            id       : "icon_users_lock",
            title    : "excluir",
            subtitle : "usuário",
            click    : function(){
                users.lock();
            }
        });
        
        eos.menu.action.new({ // senha
            id       : "icon_users_pwd",
            title    : "senha",
            subtitle : "alterar",
            click    : function(){
                users.changePwd();
            }
        });
        
        eos.menu.action.new({ // reativar
            id       : "icon_users_unlock",
            title    : "reativar",
            subtitle : "usuário",
            click    : function(){
                if(eos.core.limit.user.verify()){ // dentro do limite
                    users.unlock();
                } else {
                    \$.DDialog({
                        type    : "error",
                        message : "Limite de usuários excedido ! <br><br> Become a premium !" 
                    });
                }
            }
        });
        
        // esconde icones
        eos.menu.action.hideAll();
        
        eos.menu.action.new({ // novo
            id       : "icon_users_new",
            title    : "novo",
            subtitle : "usuário",
            click    : function(){
                if(eos.core.limit.user.verify()){ // dentro do limite
                    form.new();
                } else {
                    \$.DDialog({
                        type    : "error",
                        message : "Limite de usuários excedido ! <br><br> Become a premium !" 
                    });
                }
            }
        });
    };
    
    /* salvar */
    this.save = function(){
        
        if(\$("#COD").val() === "0"){
            \$("#COD").val("");
        }
        
        \$.DActionAjax({
            action : "edit_submit.cgi",
            postFunction : function(x) { // console.log(x);
                
                if(x){
                    x = JSON.parse(x);
                    
                    if(x.status === "error") {
                        \$.DDialog({
                           type    : x.status,
                           message : x.message
                        });
                    } else {
                        // atualiza limites
                        eos.core.limit.user.get(function(x){
                            \$("#users_limit").html(x);
                        });
                    }
                }
            }
        });
    };
    
    /* editar */
    this.edit = function(x){
        
        \$("#COD").val(x);
        users.edit();
        
        \$("#users_page").DTouchPages("page","right");
    };
    
    /* novo */
    this.new = function(){        
        this.reset();
        
        users.new();
    };
    
    
    /* reset form */
    this.reset = function(){
        // imagem
        \$("#users_avatar_container").hide();
        \$("#users_dados_imagem").hide();
        \$("#users_avatar").prop("src",""); 
        
        // campos
        \$("#users_page_right input[type=text]").val("");
        \$("#users_page_right input[type=password]").val("");
        \$("#COD").val("");
        \$("#CODIMG").val("");
        
        // senha
        \$("#users_login_senha_change, #users_login_senha_old").hide();
        \$("#users_login_senha, #users_login_senha_new, #users_login_senha_conf").show();
        
        // login / email
        \$("#login").fieldEmail("enable");
        \$("#email").fieldEmail("enable");
        
        // tipo
        \$("#users_tipo").DTouchRadio("value",2);
        
        // menus
        \$("#menus").DTouchRadio("reset","content");
        \$("#menus_container").hide();
        
        \$("#users_logins").empty();
    }
}


/**
 *   Document Ready
 */
\$(document).ready(function() { 
    form = new Form();
    form.initialize();
});

</script>
</head>
<body>

    <!-- Formulario -->
    <form >
	
        <!-- DTouchPages -->
        <div id="users_page">
            
            <!-- Page Center -->
            <div id="users_page_center">
                <div class="users_container_center">
                    
                    <div class="users_page_line">
                        
                        <!-- lista de usuarios -->
                        <div id="users_list"></div>
                        
                        <!-- limite de usuarios -->
                        <div id="users_limit"></div>
                        
                    </div>
                    
                </div>                
            </div>
        
            <!-- Page Right -->
            <div id="users_page_right">
                
                <div class="users_page_line">
                    
        			<!-- dados principais -->
        			<div id="users_dados_container">
    					<div id="users_dados_nome">
    						<input type="text" name="nome" id="nome" placeholder="Nome Completo">
                        </div>
                        <div id="users_dados_email">
    						<input type="text" name="email" id="email" placeholder="Email">
    					</div>
                        <div id="users_dados_phone">
    						<input type="text" name="phone" id="phone" placeholder="Celular">
    					</div>
                        <div id="users_dados_imagem">
    						<input name="imagem" id="imagem" >
    					</div>
                        <div id="users_avatar_container">
                            <div id="users_avatar_change">alterar imagem</div>
                            <div id="users_avatar_del">remover imagem</div>
                            <img id="users_avatar">
                        </div>
        			</div>				

        			<!-- senha -->
        			<div id="users_login_container">
                        <div id="users_login_login">
                            <input type="text" name="login" id="login" placeholder="Login">
                        </div>
                        <div id="users_login_senha_change">alterar senha?</div>
    					<div id="users_login_senha">
                            <div id="users_login_senha_old">
    						    <input type="password" name="senha" id="senha" placeholder="Senha antiga">
                            </div>
                            <div id="users_login_senha_new">
    						    <input type="password" name="senha_new" id="senha_new" placeholder="Senha nova">
                            </div>
                            <div id="users_login_senha_conf">
    						    <input type="password" name="senha_conf" id="senha_conf" placeholder="Senha nova confirmar">
                            </div>
    					</div>
        			</div>
                
        			<!-- tipo usuario -->
        			<div id="users_tipo_container">
        				<div id="users_tipo"> tipo </div>
        			</div>
                    
        			<!-- menus -->
        			<div id="menus_container">
        				<div id="menus"></div>
        			</div>
                    
        			<!-- logins usuario -->
        			<div id="users_logins_container">
        				<div id="users_logins"></div>
        			</div>
                </div>
                
            </div>
        </div>
        
        <input type="hidden" name="COD" id="COD" value="$COD">
        <input type="hidden" name="CODIMG" id="CODIMG">
    </form>
    
</body>
</html>

HTML

