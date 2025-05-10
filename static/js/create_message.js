const my_class = "bg-light border border-secondary text-dark"
const not_my_class = "bg-light border border-secondary text-dark"


function create_message(data, sender, time) {
    var div = document.createElement("div");
    div.className = "mb-2 p-2 rounded " + (isNaN(sender) ? my_class + " ms-auto " : not_my_class + " me-auto");
    div.style.maxWidth = "70%";
    const sender_name = isNaN(sender) ? "You" : sender;
    div.innerHTML = `<strong>${sender_name}</strong>: ${data}<br><small class="text-muted">${time}</small>`;
    document.querySelector("#id_chat_item_container").appendChild(div);
    div.scrollIntoView({behavior: "smooth"});
}