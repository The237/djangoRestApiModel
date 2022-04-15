
$('#formData').on('submit', function(e){
    e.preventDefault();
    console.log('form submited');
    $.ajax({
        url : 'http://127.0.0.1:8000/predict',
        type : "POST",
        data : {
            pregnancies : parseInt($('#pregnancies').val(),10),
            glucose : parseInt($('#glucose').val(),10),
            bloodpressure : parseInt($('#bloodpressure').val(),10),
            skinthickness : parseInt($('#skinthickness').val(),10),
            insulin : parseFloat($('#insulin').val(),10),
            bmi : parseFloat($('#bmi').val(),10),
            diabetespedigreefunction : parseFloat($('#diabetespedigreefunction').val(),10),
            age : parseInt($('#age').val(),10),
        },
        success : function(json){
            $('#formData').trigger("reset");
            if(json.info == 'success'){
                if(json.patient_status === 0 ){
                    statut = 'Negative'
                }
                else{
                    statut = 'Positive'
                }
                $("#results").append('<div>' +
                    '<p> Test Status : ' +
                        json.info +
                    '</p><p> Patient Status : ' +
                        statut +
                    '</p> <p> Model confidence probability : ' +
                        json.model_confidence_proba+
                    '</p></div>')
            }
            else{
                $("#results").append('<div>' +
                    'An error occured'+
                    '</p></div>')
            }
        } 
    })
});