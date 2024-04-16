const chatSocket = new WebSocket(
    'ws://'
    + '127.0.0.1:8010'
    + '/ws/chat/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log('receive message', data)
    if ( data.action === 'chat_created' ) {
        const full_name = data.init_user.full_name
        alert(`Пользователь ${full_name} Создал с вами чат!`)
    }
};