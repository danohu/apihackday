function createLink(id, text) {
    //Usage: $(selector).append(createLink(id, text))
    return $('<a id="'+ id +'">' + text + '</a>').bind('click', function() { handleClick($this.attr(id)) } )
}
/*
var d = $('<div></div>');
for (var i=0; i<20; i++) {
    d.append(createLink(i,'link'));
}
console.log(d);
*/