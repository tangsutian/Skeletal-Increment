<script>
    const timeout = {{ timeout_duration }};
    let tics = 0;

    var x = setInterval(function () {
        tics+=1;
        document.getElementById("timeRemaining").innerHTML = 'Time Remaining: '.concat(timeout-tics).toString();
        if(timeout-tics <= 0){
        document.getElementById("timeRemaining").innerHTML = "TIME UP";
        clearInterval(x);
        tics = 0;
        //const Http = new XMLHttpRequest();
        const base_url = window.location.origin;
        //let sector_id = document.getElementById("sector_id").innerText;
        //const target_url = base_url + '/wrong/'.concat(sector_id);
        let target_url = base_url + '/wheel/wrong/{{ point_total }}';

        setTimeout(function () { window.location.href = target_url}, 3000);
        }
    }, 1000);
</script>