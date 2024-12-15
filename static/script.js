document.addEventListener('DOMContentLoaded', () => {
    const sendButton = document.getElementById('send');
    const userInput = document.getElementById('user-input');
    const chat = document.getElementById('chat');

    function sendQuery() {
        const query = userInput.value;
        if (query) {
            fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: query }),
            })
            .then(response => response.json())
            .then(data => {
                chat.innerHTML += `<p class="from-me">${query}</p>`;
                chat.innerHTML += `<p class="from-them">${data.response}</p>`;
                userInput.value = '';
                chat.scrollTop = chat.scrollHeight;
            });
        }
    }

    sendButton.addEventListener('click', sendQuery);
    
    userInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            sendQuery();
        }
    });
});