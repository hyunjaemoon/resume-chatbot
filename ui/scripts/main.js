// State management
let chatHistory = [];
let currentFile = null;

// DOM Elements
const typingIndicator = document.getElementById('typing-indicator');
const fileNameDisplay = document.getElementById('file-name');
const messageInput = document.getElementById('message-input');
const chatContainer = document.getElementById('chat-container');

// File input handling
document.getElementById('file-input').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            currentFile = e.target.result;
            fileNameDisplay.textContent = `Selected file: ${file.name}`;
            fileNameDisplay.style.color = '#2196f3';
        };
        reader.readAsDataURL(file);
    }
});

// Message handling
function addMessage(message, isUser) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    messageDiv.textContent = message;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Typing indicator
function showTypingIndicator() {
    typingIndicator.style.display = 'block';
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function hideTypingIndicator() {
    typingIndicator.style.display = 'none';
}

// Message sending
async function sendMessage() {
    const message = messageInput.value.trim();
    
    if (!message) return;
    if (!currentFile) {
        alert('Please upload a resume first!');
        return;
    }

    addMessage(message, true);
    messageInput.value = '';
    showTypingIndicator();

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                data_url: currentFile,
                history: chatHistory
            })
        });

        const data = await response.json();
        hideTypingIndicator();
        addMessage(data.response, false);
        chatHistory.push(['user', message]);
        chatHistory.push(['assistant', data.response]);
    } catch (error) {
        console.error('Error:', error);
        hideTypingIndicator();
        addMessage('Error: Could not send message', false);
    }
}

// Event Listeners
messageInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Input focus effects
messageInput.addEventListener('focus', function() {
    this.parentElement.style.boxShadow = '0 4px 20px rgba(33, 150, 243, 0.15)';
});

messageInput.addEventListener('blur', function() {
    this.parentElement.style.boxShadow = 'var(--shadow)';
}); 