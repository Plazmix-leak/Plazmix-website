$(document).ready(function () {
    const profileUuid = $('#userUuid').val();
    $('#authLogs').DataTable({
        order: [[ 0, "desc" ]],
        ajax: {
            url:  API_LOCAL_ENDPOINT + '/adminPanel/Logs.getUser?uuid=' + profileUuid,
            method: "get",
            dataSrc: '',
            crossDomain: true,
        },
        columns: [
        { data: 'id' },
        { data: 'service' },
        { data: 'datetime' },
        { data: 'ip' },
        { data: 'location' }
    ]

    });

    $('#moneyLog').DataTable({
        order: [[ 0, "desc" ]],
        ajax: {
            url:  API_LOCAL_ENDPOINT + '/adminPanel/Balance.get?uuid=' + profileUuid,
            method: "get",
            dataSrc: '',
        },
        columns: [
        { data: 'id' },
        { data: 'datetime' },
        { data: 'amount' },
        { data: 'comment' },
        { data: 'ip' }
    ]

    });
})