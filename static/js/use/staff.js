$(document).ready(function() {
    $('.staff').each(function (index, ele) {
        let data = $('.data')[index];
        $.ajax({
            url: "https://team.plazmix.net/ajax/users_in_group?group=" + data.id,
            method: "GET",
            success: function (result) {
                let edit = $('#' + data.id)
                if (result === "None"){
                    $(".staff").eq(index).hide();
                }
                edit.empty();
                edit.append(result);
                $('[data-toggle="tooltip"]').tooltip()
            }
        });
    })
})