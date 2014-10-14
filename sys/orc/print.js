/*
// You'll need to make your image into a Data URL
// Use http://dataurl.net/#dataurlmaker
var imgData = 'data:image/jpeg;base64,';
*/

var doc = new jsPDF();

// logo sistema
doc.addImage(eos.core.img(300), 'JPEG', 175, 8, 25, 23);


doc.setFontSize(10);
doc.text(40, 20, ""+eos.company.name()+"");
doc.text(40, 25, "Endereço : "+eos.company.address()+"");

doc.setFontSize(20);
doc.text(10, 40, "Orçamento ["+\$("#COD").val()+"]");

doc.setLineWidth(0.5);
doc.line(10, 30, 200, 30);

// servicos
doc.setFontSize(10);
var top = 50;
var serv = \$("input[name=servico_id]");
serv.each(function(){
    doc.text(40, top, \$("input[name=servico_descrp_"+\$(this).val()+"]").val());
    doc.text(80, top, \$("input[name=servico_qtd_"+\$(this).val()+"]").val());
    doc.text(90, top, \$("input[name=servico_valor_"+\$(this).val()+"]").val());
    doc.text(110, top, \$("input[name=servico_valor_total_"+\$(this).val()+"]").val());
    top += 10;
});



// Produtos
doc.setFontSize(10);
// var top = 50;
var prod = \$("input[name=produto_id]");
prod.each(function(){
    doc.text(40, top, \$("input[name=produto_descrp_"+\$(this).val()+"]").val());
    doc.text(80, top, \$("input[name=produto_qtd_"+\$(this).val()+"]").val());
    doc.text(90, top, \$("input[name=produto_valor_"+\$(this).val()+"]").val());
    doc.text(110, top, \$("input[name=produto_valor_total_"+\$(this).val()+"]").val());
    top += 10;
});


// Despesas
doc.setFontSize(10);
// var top = 50;
var prod = \$("input[name=despesa_id]");
prod.each(function(){
    doc.text(40, top, \$("input[name=despesa_descrp_"+\$(this).val()+"]").val());
    doc.text(90, top, \$("input[name=despesa_valor_"+\$(this).val()+"]").val());
    top += 10;
});



/*
HTML render

var specialElementHandlers = {
	'#editor': function(element, renderer){
		return true;
	}
};

doc.fromHTML(\$('#servico_list').get(0), 15, 15, {
	'width': 170 // , 
	// 'elementHandlers': specialElementHandlers
});
*/
                




doc.save("orc_"+\$("#COD").val()+".pdf");
// doc.save("print.pdf",{type: "Content-type:application/octet-stream; Content-Disposition:attachment;"});
// doc.save("print.pdf",{type: "application/pdf"});