$(document).ready(function() 
{
    $('#select-btn').click(function(event) { event.preventDefault(); });

    $('#select-btn').on('click', function() 
    {
        $('#file').click();
    });

    $('#file').on('change', function(event) 
    {
        const selectedFile = event.target.files[0];
        if(selectedFile) 
        { $("#form").submit(); }
    });
});

function editEvent(eventID)
{
    $("#event-" + eventID).attr("hidden", true); // Hide the single event
    $("#event-form-" + eventID).attr("hidden", false); // Show the form
}

function cancelEdit(eventID)
{
    $("#event-" + eventID).attr("hidden", false); // Show the single event
    $("#event-form-" + eventID).attr("hidden", true); // Hide the form
}

function showList(loopIndex)
{
    // Open the modal when the button is clicked
    $("#" + loopIndex).css("display", "block");

    // Close the modal when the close button or outside the modal is clicked
    $(".close").click(function() {
        $("#" + loopIndex).css("display", "none");
    });

    $(window).click(function(event) {
        if (event.target === document.getElementById(loopIndex)) {
            $("#" + loopIndex).css("display", "none");
        }
    });
}