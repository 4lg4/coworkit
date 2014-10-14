var fs      = require('fs'),
    cfg     = JSON.parse(fs.readFileSync("/etc/done/conn.eos.node")),
    express = require(cfg.sys.libpath +'express'),
    app     = express(),
    server  = require('http').createServer(app),
    pg      = require(cfg.sys.libpath +'pg'); // modulo postgres
	// io = require(cfg.sys.libpath +'socket.io').listen(server);
	
    /*
    * se for HTTPS implementar
    if(cfg.sys.protocol === "https") {
        var http = require("https");
        var server  = require('http').createServer(cfg.cert,app);
    }
    */  
    
    server.listen(cfg.sys.port, function(){
        console.log("listening");
    });

    // app.use(express.static(__dirname +"/public"));
    app.use(app.router);
    
    app.get('/', function(req, res){
        res.sendfile(__dirname +"/index.html");
    });
    
    app.get('/login/:user&:pwd', function(req, res){
        // res.sendfile(__dirname + '/index.html');
        res.send(req.params.user+" - "+req.params.pwd);
    });
    
    app.get('/get/:t', function(req, res){
        
        var r = getList(req.params.t, function(r){
            var re = "";
            
            if(req.params.t === "usuario") {
                re = "<style> div { width:33%; height:20px; border:1px solid gray; float:left; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; } </style>";
                
                r.forEach(function(item){
                    re += "<div> "+ item.usuario +" </div><div> "+ item.login +" </div><div> "+ item.nome +" </div>";
                });  
            } else if(req.params.t === "empresa") {
                re = "<style> div { width:33%; height:20px; border:1px solid gray; float:left; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; } </style>";
                
                r.forEach(function(item){
                    re += "<div> "+ item.codigo +" </div><div> "+ item.nome +" </div><div> "+ item.apelido +" </div>";
                });  
            } else {
                re = "<style> div { width:49%; height:20px; border:1px solid gray; float:left; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; } </style>";
                
                r.forEach(function(item){
                    re += "<div> "+ item.codigo +" </div><div> "+ item.descrp +" </div>";
                });
            }
            
            res.send(re);
        });
        
        
    });
    
    /*
    io.sockets.on('connection', function(socket){
    	socket.on('send message', function(data){
    		io.sockets.emit('new message', data);
    	});
    });
    */
    
function getList(t,callback){
    // string de conexao
    var conString = "postgres://"+ cfg.db.user+ ":"+ cfg.db.pwd +"@"+ cfg.db.host +":"+ cfg.db.port +"/"+ cfg.db.db;
    
    pg.connect(conString, function(err, client, done) {
        if(err) {
          return console.error('error fetching client from pool', err);
        }
  
        client.query('SELECT * from '+t, function(err, result) {

            if(err) {
                return console.error('error running query', err);
            }            
            /*
            result.rows.forEach(function(item){
                retorno += item.nome+" ++ ";
                
                console.log("> "+ item.usuario +" : "+ item.login +" | "+ item.nome);
            });
            */
            
            callback.call(this,result.rows);
            
        });
    });   
}