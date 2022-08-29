$(document).ready(function() {
    const profileUuid = $('#userUuid').val();
    console.log(profileUuid);
    $.ajax({
            url: "https://profile.plazmix.net/ajax/friends?uuid=" + profileUuid,
            method: "GET",
            success: function (result) {
                let friendsBlock = $('#friends');
                friendsBlock.empty();
                friendsBlock.append(result);
                $('[data-toggle="tooltip"]').tooltip()
            }
        });

        $.ajax({
            url: "https://profile.plazmix.net/ajax/gifts?uuid=" + profileUuid,
            method: "GET",
            success: function (result) {
                let friendsBlock = $('#gifts');
                friendsBlock.empty();
                friendsBlock.append(result);
            }
        });
        $.ajax({
            url: "https://profile.plazmix.net/ajax/achievements?uuid=" + profileUuid,
            method: "GET",
            success: function (result) {
                let friendsBlock = $('#achievementsList');
                friendsBlock.empty();
                friendsBlock.append(result);
            }
        });
})