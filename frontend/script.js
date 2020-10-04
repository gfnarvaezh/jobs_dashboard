function submit() {
    var xhr = new XMLHttpRequest();
    var request = { headers:{
                    "Access-Control-Allow-Origin": "http://narvaezfelipe.com",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"},
                    "language": "Python",
                    "country": "ar",
                    "platform": "indeed",
                    "category": "Any_Time"};
    var json_file = JSON.stringify(request)
    console.log(json_file)
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) { 
                // let result = JSON.parse(xhr.response);
                console.log(xhr.response)
                
            } 
            else {}
        }
    }

    xhr.open("POST", 'https://sqlmazqg7c.execute-api.us-east-2.amazonaws.com/prod/jobs-num', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(json_file);
}

function test(){
    var result = {
        "HTTPStatusCode": 200,
        "data": {
            "d200930": "843",
            "d200929": "848",
            "d201002": "826",
            "d201003": "816",
            "d201001": "824"
        }
    }

    var dataset = get_dataset(result['data']);
    plot_result(dataset['data'], dataset['labels']);
}


function get_dataset(dictionary){
    var dataset = [];
    var labels = [];
    Object.keys(dictionary).sort().forEach(function(key){
        var year = '20' + key.substring(1,3);
        var month = key.substring(3,5);
        var day = key.substring(5,7);
        var date = new Date(year + '-' + month + '-' + day);
        labels.push('2020');
        var list_element = {};
        list_element['t'] = date;
        list_element['y'] = parseInt(dictionary[key]);
        dataset.push(list_element);
    })
    var output = {};
    output['data'] = dataset;
    output['labels'] = labels;
    return output
}

function plot_result(dataset, date_labels){
    var ctx = document.getElementById('myChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
          // labels : date_labels,
          datasets: [{
            label: 'Demo',
            data: dataset,
            borderWidth: 1,
            fill: false
          }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }],
                xAxes: [{
                    type: 'time',
                    time: {
                        unit: 'day',
                        tooltipFormat: 'lll',
                    }
                }]                    
            }
        }
      });
}
