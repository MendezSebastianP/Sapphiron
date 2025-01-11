// Function to format timestamp to HH:mm (24-hour format)
function formatTimestamp() {
    const now = new Date();
    let hours = now.getHours();
    let minutes = now.getMinutes();
    // Pad single digits with leading zero
    if (minutes < 10) minutes = '0' + minutes;
    if (hours < 10) hours = '0' + hours;
    return `${hours}:${minutes}`;
}

document.getElementById('send-message').addEventListener('click', function() {
    const userInput = document.getElementById('user-input').value;

    if (userInput.trim()) {
        // Create a user message
        const userMessage = document.createElement('div');
        userMessage.classList.add('chat-message', 'user-message');  // Add 'user-message' class
        userMessage.innerHTML = `
            <span class="message-text">${userInput}</span>
            <span class="timestamp">${formatTimestamp()}</span>  <!-- Timestamp outside message -->
        `;

        // Append user message to chat box
        const chatBox = document.getElementById('chat-box');
        chatBox.appendChild(userMessage);

        // Clear the input field
        document.getElementById('user-input').value = '';

        // Scroll to the bottom of the chat box (after the new message is added)
        chatBox.scrollTop = chatBox.scrollHeight;

        // Simulate a fixed response from the system
        setTimeout(() => {
            const systemMessage = document.createElement('div');
            systemMessage.classList.add('chat-message', 'system-message');  // Add 'system-message' class
            systemMessage.innerHTML = `
                <span class="message-text">Aún no puedo hacer esto.</span>
                <!-- No timestamp for system messages -->
            `;

            // Append system response to chat box
            chatBox.appendChild(systemMessage);

            // Scroll to the bottom after the system message is added
            chatBox.scrollTop = chatBox.scrollHeight;
        }, 1000);
    }
});
