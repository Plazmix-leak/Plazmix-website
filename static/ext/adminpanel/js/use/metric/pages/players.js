$(document).ready(function () {
  let playerTotal = metricDataSorted("accounts_total", "week", "max");
  let playerRegisters = metricDataSorted("accounts_new", "24hours", "sum");
  let serverJoins = metricDataSorted("plzmjoins", "24hours", "sum");
  let playerRegistersWeek = metricDataSorted("accounts_new", "week", "sum");
  let playerRegistersPastWeek = metricDataSorted("accounts_new", "past_week", "sum");

  let joinsComparison = metricComparison("plzmjoins", "day");
  let registerWeekComparison = metricComparison("accounts_new", "week");

  if (joinsComparison.growth){
    $("#joinsComparison").text("Увеличелись на "+joinsComparison.percent + "% по сравнению с прошлым днём");
   } else {
    $("#joinsComparison").text("Уменьшились на "+joinsComparison.percent + "% по сравнению с прошлым днём");
  }

  if (registerWeekComparison.growth){
    $("#registerComparison").text("Увеличелись на "+registerWeekComparison.percent + "% по сравнению с прошлым днём");
   } else {
    $("#registerComparison").text("Уменьшились на "+registerWeekComparison.percent + "% по сравнению с прошлой неделью");
  }

  new Chart(document.getElementById("total_accounts"), {
    type: 'line',
    data: {
      labels: playerTotal.title,
      datasets: [{
          data: playerTotal.data,
          label: "Игроков",
          borderColor: "#7B68EE",
          fill: true
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: 'Колличество аккаунтов на проекте"'
      }
    }
  });

  new Chart(document.getElementById("new_accounts"), {
    type: 'line',
    data: {
      labels: playerRegisters.title,
      datasets: [{
          data: playerRegisters.data,
          label: "Регистраций",
          borderColor: "#00FFFF",
          fill: true
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: 'Колличество регистраций на проекте за последнии 24 ч."'
      }
    }
  });

  new Chart(document.getElementById("server_join"), {
    type: 'line',
    data: {
      labels: serverJoins.title,
      datasets: [{
          data: serverJoins.data,
          label: "Входов",
          borderColor: "#6A5ACD",
          fill: true
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: 'Колличество входов на сервер за последние 24 часа'
      }
    }
  });

  new Chart(document.getElementById("new_accounts_week"), {
    type: 'line',
    data: {
      labels: playerRegistersWeek.title,
      datasets: [{
          data: playerRegistersWeek.data,
          label: "Регистраций за эту неделю",
          borderColor: "#00FF00",
          fill: true
        },
        {
          data: playerRegistersPastWeek.data,
          label: "Регистраций за прошлую неделю",
          borderColor: "#00BFFF",
          fill: true
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: 'Колличество регистраций на прокте за последнии 2 недели'
      }
    }
  });

})