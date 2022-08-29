$(document).ready(function () {
    let serverJoins = metricDataSorted("plzmjoins", "24hours", "sum");
    let onlineLastDat = metricDataSorted("online_summary_total", "24hours", "max");

      new Chart(document.getElementById("chartOnlineLastDay"), {
        type: 'line',
        data: {
          labels: onlineLastDat.title,
          datasets: [{
              data: onlineLastDat.data,
              label: "Онлайн проекта",
              borderColor: "#7B68EE",
              fill: true
            }
          ]
        },
        options: {
          title: {
            display: false,
            text: 'Колличество аккаунтов на проекте'
          }
        }
      });

      new Chart(document.getElementById("serverJoinsLastDay"), {
        type: 'line',
        data: {
          labels: serverJoins.title,
          datasets: [{
              data: serverJoins.data,
              label: "Входов на сервер",
              borderColor: "#D2691E",
              fill: true
            }
          ]
        },
        options: {
          title: {
            display: false,
            text: 'Колличество входов на сервер'
          }
        }
      });


})