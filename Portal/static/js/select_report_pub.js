$(document).ready(function(){
$('#optionSelector').on('change', function() {
      if ( this.value == "report")
      {
        console.log("Report!")
        $("#reportSubmission").show();
      }
      else
      {
        $("#reportSubmission").hide();
      }
    });
});

$(document).ready(function(){
$('#optionSelector').on('change', function() {
      if ( this.value == "pub")
      {
        console.log("Publication!")
        $("#publicationInfo").show();
      }
      else
      {
        $("#publicationInfo").hide();
      }
    });
});