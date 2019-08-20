<script>
    const timeout = {{ timeout_duration }};
    let tics = 0;

    var x = setInterval(function () {
        tics+=1;
        document.getElementById("timeRemaining").innerHTML = 'Time Remaining: '.concat(timeout-tics).toString();

        if(timeout-tics <= 0){
            document.getElementById("timeRemaining").innerHTML = "TIME UP";
            document.getElementById("button").onclick = function() { window.location.href = "#"};
            clearInterval(x);
            tics = 0;

            const base_url = window.location.origin;

            let target_url = base_url + '/wheel/wrong/{{ point_total }}';

            setTimeout(function () { window.location.href = target_url}, 3000);
        }
    }, 1000);
</script>