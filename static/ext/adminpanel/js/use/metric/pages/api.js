$(document).ready(function () {
  let lastHours = metricDataSorted("api", "24hours", "sum");
  let yesterday = metricDataSorted("api", "yesterday", "sum");
  let week = metricDataSorted("api", "week", "sum");
  let before_week = metricDataSorted("api", "past_week", "sum");

  let day_comparison = metricComparison("api", "day");
  let week_comparison = metricComparison("api", "week");

  if (day_comparison.growth){
    $("#comparison_days").text("Увеличелись на "+day_comparison.percent + "% по сравнению с прошлым днём");
  } else {
    $("#comparison_days").text("Уменьшились на "+day_comparison.percent + "% по сравнению с прошлым днём");
  }

  if (week_comparison.growth){
    $("#comparison_week").text("Увеличелись на "+week_comparison.percent + "% по сравнению с прошлым днём");
  } else {
    $("#comparison_week").text("Уменьшились на "+week_comparison.percent + "% по сравнению с прошлой неделью");
  }
  new Chart(document.getElementById("last_hours"), {
    type: 'line',
    data: {
      labels: lastHours.title,
      datasets: [{
          data: lastHours.data,
          label: "Колличество запросов",
          borderColor: "#32CD32",
          fill: false
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: 'Колличество запросов к серверу API'
      }
    }
  });

  new Chart(document.getElementById("yesterday"), {
    type: 'line',
    data: {
      labels: yesterday.title,
      datasets: [{
          data: yesterday.data,
          label: "Запросов к серверу",
          borderColor: "#3e95cd",
          fill: false
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: 'Колличество запросов за вчерашний день'
      }
    }
  });

  new Chart(document.getElementById("week"), {
    type: 'line',
    data: {
      labels: week.title,
      datasets: [{
          data: week.data,
          label: "Запросов к серверу",
          borderColor: "#9932CC",
          fill: false
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: 'Колличество запросов за вчерашний день'
      }
    }
  });

  new Chart(document.getElementById("two_week"), {
    type: 'line',
    data: {
      labels: week.title,
      datasets: [{
          data: week.data,
          label: "Запросов к серверу за текущую неделю",
          borderColor: "#FF8C00",
          fill: false
        },
        {
          data: before_week.data,
          label: "Запросов к серверу за прошлую неделю",
          borderColor: "#006400",
          fill: false
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: 'Колличество запросов за две недели'
      }
    }
  });
})