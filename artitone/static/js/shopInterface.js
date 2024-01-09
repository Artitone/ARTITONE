function readHttpGet() {
    var request = {};
    var pairs = location.search.substring(1).split('&');
    for (var i = 0; i < pairs.length; i++) {
        var pair = pairs[i].split('=');
        request[pair[0]] = pair[1];
    }
    return request;
}

function changeSelectByGetValue(id) {
    var request = readHttpGet();
    var mySelect = document.getElementById(id);

    for(var i, j = 0; i = mySelect.options[j]; j++) {
        if(i.value == request["sort"]) {
            mySelect.selectedIndex = j;
            break;
        }
    }
}

function changeColorPickByGetValue(id) {
    var request = readHttpGet();
    if ("color-"+id in request) {
        var color = "#"+request["color-"+id].slice(3);
        
        var myColorPick = document.getElementById(id);
        console.log(myColorPick);
        myColorPick.setAttribute("data-initialcolor", color);
    }
}