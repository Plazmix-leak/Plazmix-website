$(document).ready(function () {
    $('#staffTable').DataTable({
        ajax: {
            url: API_LOCAL_ENDPOINT + '/adminPanel/Staff.get',
            method: "POST",
            dataSrc: '',
            crossDomain: true,
        },
        columns: [
        { data: 'nickname' },
        { data: 'group' },
        { data: 'level' },
        { data: 'online' },
        { data: 'action' }
    ]

    });
})