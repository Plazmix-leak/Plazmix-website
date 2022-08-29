$(document).ready(function () {
    const cluster = $('#staffCluster').val();

    $('#staffTable').DataTable({
        ajax: {
            url: API_LOCAL_ENDPOINT + '/adminPanel/Staff.getFromGroups?cluster='+cluster,
            method: "GET",
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