function metricRequest(uri, body){
    let result = {};
    $.ajax({
            url: uri,
            dataType: "json",
            crossDomain: true,
            method: "POST",
            async: false,
            data: JSON.stringify(body),
            success: function (apiResult) {
                result = apiResult;
            },
            error: function (){
                alert("Clarence: Ошибка при загрузке данных метрики c API сервера, сообщите разработчику.");
            }
    });
    return result;
}



function metricDataSorted(metricName, sortedDataType, checkType="max") {
    return metricRequest(API_LOCAL_ENDPOINT + "/adminPanel/Metric.sortedData",
        {name: metricName, data_type: sortedDataType, check_type: checkType});
}

function metricMetaData(metricName, dayType) {
    return metricRequest(API_LOCAL_ENDPOINT + "/adminPanel/Metric.data",
        {name: metricName, day: dayType});
}

function metricComparison(metricName, comparisonDataType) {
    return metricRequest(API_LOCAL_ENDPOINT + "/adminPanel/Metric.comparison",
        {name: metricName, data_type: comparisonDataType});
}
