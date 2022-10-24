function arrForm(data, key) {
    let arr = [];
    for (let i = 0; i < data.length; i++) {
        arr[i] = data[i][key];
    }
    return arr
}

function dataForChart(dataRe, dataAv, labels) {
    return {
        labels: labels,
        datasets: [{
            label: 'Number of Reservations',
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: dataRe,
        }, {
            label: 'Number of Available Seats',
            backgroundColor: 'rgb(99, 255, 222)',
            borderColor: 'rgb(99, 255, 222)',
            data: dataAv,
        }
        ]
    };
}

function plotChart(idChart, countryData) {
    let dateArr = arrForm(countryData, "date");
    let dataArrReTotal = arrForm(countryData, "reserved_total");
    let dataArrAvTotal = arrForm(countryData, "available_total");
    let labels = dateArr;
    let config = {
        type: 'line',
        data: dataForChart(dataArrReTotal, dataArrAvTotal, labels),
        options: {}
    };

    return new Chart(
        document.getElementById(idChart),
        config
    );
}