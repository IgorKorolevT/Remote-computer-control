const my_class = "my_message"
const not_my_class = "not_my_message"
const default_your = "You"

function create_message(data, sender, time) {
    var div = document.createElement("div");
    div.className = "mb-2 p-2 border border-secondary text-dark message " + (sender === default_your ? my_class + " ms-auto " : not_my_class + " me-auto");
    div.style.maxWidth = "70%";
    div.innerHTML = `<strong>${sender}</strong>: ${data}<br><small class="text-muted">${time}</small>`;
    document.querySelector("#id_chat_item_container").appendChild(div);
    div.scrollIntoView({behavior: "smooth"});
}