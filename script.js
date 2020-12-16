
//Accessing AWS API GW REST API -> AWS Lambda -> AWS Comprehend for Sentiment Analysis
const getResp = function() {

    //user input in text area
    var requestData = document.getElementById("textInput").value;
    console.log(requestData);
    fetch('https://c24ge3u77j.execute-api.us-east-1.amazonaws.com/prod/helloworld',{
        method: 'POST',
        body: JSON.stringify
        ({text: requestData}),
        headers: {
            'Content-type': 'application/json; charset=UTF-8'
        }
    }).then(function(response){
        console.log(response);
        //alert(response);
        return response.json();
    }).then(function(data){
        //console.log(data.body);
        var outputRes = data.body;
        console.log(outputRes);

        //Extracting different sentiments from object
        var positiveSent = outputRes.Positive;
        //console.log(positiveSent);
        var negativeSent = outputRes.Negative;
        var neutralSent = outputRes.Neutral;
        var mixedSent = outputRes.Mixed;
    }).catch(function(error) {
        console.warn('Something went wrong', error);
    })
};



//For plotting sentiment values
function plotSentiment() {
    var data = [{
        values: [19, 26, 55],
        labels: ['Residential', 'Non-Residential', 'Utility'],
        type: 'pie'
        }];

    var layout = {
        height: 400,
        width: 500
    };
    Plotly.newPlot('myDiv', data, layout);
}