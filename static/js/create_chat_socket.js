function create_socket(url, receiver) {
    const chatSocket = new WebSocket("ws://" + window.location.host + url);
    chatSocket.onopen = function (e) {
        console.log('The connection was setup successfully !');
    };
    chatSocket.onclose = function (e) {
        console.log("Something unexpected happened !");
    };
    const input = document.querySelector("#id_message_send_input");
    input.focus();
    input.onkeyup = function (e) {
        if (e.key === "Enter") {
            document.querySelector("#id_message_send_button").click();
        }
    };
    document.querySelector("#id_message_send_button").onclick = function (e) {
        const messageInput = input.value;
        if (messageInput.trim() === "") return;
        input.value = "";
        const current_date = new Date();
        chatSocket.send(JSON.stringify({
            message: messageInput,
            receiver: receiver,
            date: current_date
        }));
        create_message(messageInput, NaN, current_date);
    };
    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        create_message(data.message, data.sender, data.date);
    };
    chatSocket.onerror = function (error) {
        console.error("WebSocket Error:", error);
    };
    return chatSocket
}