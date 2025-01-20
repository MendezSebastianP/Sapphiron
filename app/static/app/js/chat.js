document.getElementById('send-message').addEventListener('click', function() {
    const userInput = document.getElementById('user-input').value;

    if (userInput.trim()) {
        // Create and display the user message
        const userMessage = document.createElement('div');
        userMessage.classList.add('chat-message', 'user-message');
        userMessage.innerHTML = `
            <span class="message-text">${userInput}</span>
            <span class="timestamp">${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
        `;

        const chatBox = document.getElementById('chat-box');
        chatBox.appendChild(userMessage);
        document.getElementById('user-input').value = '';
        chatBox.scrollTop = chatBox.scrollHeight;

        // Send user message to server
        fetch('/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token
            },
            body: JSON.stringify({ message: userInput })
        })
        .then(response => response.json())
        .then(data => {
            // Display the server's response
            const systemMessage = document.createElement('div');
            systemMessage.classList.add('chat-message', 'system-message');
            systemMessage.innerHTML = `
                <span class="message-text">${data.response}</span>
            `;
            chatBox.appendChild(systemMessage);
            chatBox.scrollTop = chatBox.scrollHeight;
        })
        .catch(error => console.error('Error:', error));
    }
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
