const save = $(".save-btn")

const saveEvent = (evtID) => {
    let event = {"evtID" : evtID}
    $.post("/save-event", event, (res) => {
        console.log(res)
        $(res).attr("disabled", true)}
    )
};

save.on("click", (evt) => {
    console.log("I've been Clicked!")
    let evtButton = $(evt.target)
    let evtID = evtButton.attr("name")
    console.log(evtID)
    saveEvent(evtID)
});

