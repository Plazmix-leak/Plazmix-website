$(document).ready(function () {
    $('#paymentHistory').DataTable({
        ajax: {
            url: API_LOCAL_ENDPOINT + '/adminPanel/PaymentHistory.get',
            method: "GET",
            dataSrc: '',
            crossDomain: true,
        },
        columns: [
        { data: 'id' },
        { data: 'user' },
        { data: 'amount' },
        { data: 'comment' },
    ]

    });
})