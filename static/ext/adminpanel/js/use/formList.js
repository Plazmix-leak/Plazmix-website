$(document).ready(function () {
    const formType = $('#formType').val();
    const formStatus = $('#formStatus').val();


    $('#formList').DataTable({
        ajax: {
            url: API_LOCAL_ENDPOINT + '/adminPanel/Forms.getList?form_type='+formType+'&form_status='+formStatus,
            method: "GET",
            dataSrc: '',
            crossDomain: true,
        },
        columns: [
        { data: 'name' },
        { data: 'link' },
    ]

    });
})