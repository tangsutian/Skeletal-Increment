var timeout = 30;
var tics = 0;
var x = setInterval(function () {
    tics+=1;
    document.getElementById("timeRemaining").innerHTML = timeout-tics;
    //document.body.innerHTML = "<b> Time remaining: " + timeout-tics + "</b><";
    if(timeout-tics <= 0){
        document.getElementById("timeRemaining").innerHTML = "TIME UP";
        //document.body.innerHTML = "<b> Times Up </b>";
    }
}, 1000);