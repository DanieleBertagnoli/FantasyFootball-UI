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

    var starID = sessionStorage.getItem("starID");
    if (starID)
    { selectStar(starID); }
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

function editPartecipant(loopIndex)
{
    $("#partecipant-" + loopIndex).attr("hidden", true); // Hide the single event
    $("#partecipant-" + loopIndex + "-form").attr("hidden", false); // Show the form
}

function cancelEditPartecipant(loopIndex)
{
    $("#partecipant-" + loopIndex).attr("hidden", false); // Show the single event
    $("#partecipant-" + loopIndex + "-form").attr("hidden", true); // Hide the form
}

function selectStar(starID)
{
    $(".star").css("color", "white");
    $("#" + starID).css("color", "darkorange");

    $(".star-list").attr("hidden", true); // Hide all the lists
    $("#" + starID + "-list").attr("hidden", false); // Show the starred list

    sessionStorage.setItem("starID", starID);
}

function checkEditEvent(formID)
{
    var isValid = true;

    if($("#new-player-edit-" + formID).val() === "")
    { 
        $("#new-player-edit-" + formID).css("border-color", "red"); 
        isValid = false;
    }

    if($("#new-cost-edit-" + formID).val() === "")
    { 
        $("#new-cost-edit-" + formID).css("border-color", "red"); 
        isValid = false;
    }

    if(isValid)
    { 
        // Open a confirmation popup
        var confirmResult = confirm("Are you sure?");
        if(confirmResult)
        { $("#event-form-" + formID).submit(); } 
    }
}

function checkNewPlayer()
{
    var isValid = true;

    if($("#new-player").val() === "")
    { 
        $("#new-player").css("border-color", "red"); 
        isValid = false;
    }

    if($("#cost").val() === "")
    { 
        $("#cost").css("border-color", "red"); 
        isValid = false;
    }

    return isValid;
}

function checkEditPartecipant(formID)
{
    var isValid = true;
    if($("#new-partecipant-edit-" + formID).val() === "")
    { 
        $("#new-partecipant-edit-" + formID).css("border-color", "red"); 
        isValid = false;
    }
    
    if(isValid)
    { $("#partecipant-" + formID + "-form").submit(); }
}

function checkEventDelete(formID)
{
    // Open a confirmation popup
    var confirmResult = confirm("Are you sure?");
    if(confirmResult)
    { $("#" + formID).submit(); }
}