$(document).ready(function() {
    const playersWord = caseNum(["игрок", "игрока", "игроков"])
    function updateOnline() {
        $.ajax({
            url: API_ENDPOINT + "/siteV1/Online.get",
            dataType: "json",
            method: "POST",
            success: function (result) {
                let serverOnline = result.online;
                $("#serverOnline").text(serverOnline + " " + playersWord(serverOnline));
            }
        });
    }

    updateOnline();
    setInterval(updateOnline, 15000);

    $.ajax({
            url: "https://plazmix.net//ajax/news",
            method: "GET",
            beforeSend: function(){
                $('#news').empty();
            },
            success: function (result) {
                $('#news').append(result);
            },
            error: function(){
                alert("Не удалось загрузить новости!");
            }
        });
});
