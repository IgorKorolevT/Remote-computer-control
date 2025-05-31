const my_class = "my_message"
const not_my_class = "not_my_message"
const default_your = "You"
let my_id = NaN
let user_type = NaN

function create_message(data, sender, time, sender_type) {
    const div = document.createElement("div");
    div.className = "mb-2 p-2 border border-secondary text-dark message "
    let sender_name = sender;
    if (sender === my_id && sender_type === user_type) {
        div.className += my_class + " ms-auto "
        sender_name = default_your
    } else {
        div.className += not_my_class + " me-auto "
    }
    div.style.maxWidth = "70%";

    const strong = document.createElement('strong');
    const small = document.createElement('small');
    const br = document.createElement('br');

    strong.textContent = sender_name;
    small.textContent = time;
    small.className = 'text-muted';

    div.appendChild(strong);
    div.appendChild(document.createTextNode(`: ${data}`));
    div.appendChild(br);
    div.appendChild(small);

    document.querySelector("#id_chat_item_container").appendChild(div);
    div.scrollIntoView({behavior: "smooth"});
}