/**
 * RAG Chatbot JavaScript
 * 
 * Handles chatbot UI interactions and API communication
 */

(function () {
    'use strict';

    // Chatbot state
    const chatState = {
        isOpen: false,
        isProcessing: false,
        isListening: false,
        recognition: null,
        synth: null,
        currentUtterance: null
    };

    // Initialize on DOM ready
    document.addEventListener('DOMContentLoaded', function () {
        initializeChatbot();
    });

    function initializeChatbot() {
        // Create chatbot HTML if not exists
        if (!document.getElementById('chat-widget-container')) {
            createChatbotHTML();
        }

        // Initialize Web Speech API
        initializeSpeechRecognition();
        initializeSpeechSynthesis();

        // Bind events
        bindEvents();
    }

    function createChatbotHTML() {
        const container = document.createElement('div');
        container.id = 'chat-widget-container';
        container.innerHTML = `
            <button id="chat-toggle-btn" aria-label="Toggle Chatbot">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                </svg>
            </button>
            <div id="chat-window">
                <div id="chat-header">
                    <h3>US FoodScope Assistant</h3>
                    <button id="chat-close-btn" aria-label="Close Chat">×</button>
                </div>
                <div id="chat-messages"></div>
                <div id="chat-input-area">
                    <input type="text" id="chat-input" placeholder="Ask about food access, health outcomes, or food environment..." />
                    <button id="chat-mic-btn" aria-label="Voice Input" title="Voice Input">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
                            <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
                            <line x1="12" y1="19" x2="12" y2="23"></line>
                            <line x1="8" y1="23" x2="16" y2="23"></line>
                        </svg>
                    </button>
                    <button id="chat-send-btn" aria-label="Send Message">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <line x1="22" y1="2" x2="11" y2="13"></line>
                            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                        </svg>
                    </button>
                    <button id="chat-stop-speech-btn" aria-label="Stop Speaking" title="Stop Speaking" style="display: none;">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <rect x="6" y="6" width="12" height="12"></rect>
                        </svg>
                    </button>
                </div>
                <div id="chat-recording-indicator" style="display: none;">
                    <span class="recording-dot"></span>
                    <span class="recording-text">Listening...</span>
                </div>
            </div>
        `;
        document.body.appendChild(container);
    }

    function initializeSpeechRecognition() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            chatState.recognition = new SpeechRecognition();
            chatState.recognition.continuous = false;
            chatState.recognition.interimResults = false;
            chatState.recognition.lang = 'en-US';

            chatState.recognition.onresult = function (event) {
                const transcript = event.results[0][0].transcript;
                document.getElementById('chat-input').value = transcript;
                stopListening();
                sendMessage();
            };

            chatState.recognition.onerror = function (event) {
                console.error('Speech recognition error:', event.error);
                stopListening();
                addBotMessage('Sorry, I had trouble understanding your voice. Please try typing your question.');
            };

            chatState.recognition.onend = function () {
                stopListening();
            };
        }
    }

    function initializeSpeechSynthesis() {
        if ('speechSynthesis' in window) {
            chatState.synth = window.speechSynthesis;
        }
    }

    function bindEvents() {
        // Toggle chatbot
        const toggleBtn = document.getElementById('chat-toggle-btn');
        const closeBtn = document.getElementById('chat-close-btn');
        const chatWindow = document.getElementById('chat-window');
        const chatInput = document.getElementById('chat-input');
        const sendBtn = document.getElementById('chat-send-btn');
        const micBtn = document.getElementById('chat-mic-btn');

        toggleBtn?.addEventListener('click', toggleChatbot);
        closeBtn?.addEventListener('click', toggleChatbot);

        // Send message
        sendBtn?.addEventListener('click', sendMessage);
        chatInput?.addEventListener('keypress', function (e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });

        // Voice input
        micBtn?.addEventListener('click', toggleVoiceInput);

        // Stop speech
        const stopSpeechBtn = document.getElementById('chat-stop-speech-btn');
        stopSpeechBtn?.addEventListener('click', stopSpeaking);

        // Stop speech synthesis on close
        toggleBtn?.addEventListener('click', function () {
            if (!chatState.isOpen) {
                stopSpeaking();
            }
        });
    }

    function toggleChatbot() {
        chatState.isOpen = !chatState.isOpen;
        const chatWindow = document.getElementById('chat-window');
        if (chatWindow) {
            chatWindow.style.display = chatState.isOpen ? 'flex' : 'none';

            if (chatState.isOpen) {
                // Add welcome message if chat is empty
                const messages = document.getElementById('chat-messages');
                if (messages && messages.children.length === 0) {
                    addBotMessage('Hello! I\'m your FoodScope Assistant. I can help you analyze U.S. food quality, food access, and food environment data. Ask me anything about counties, food insecurity, health outcomes, or food accessibility!');
                }
                // Focus input
                const input = document.getElementById('chat-input');
                if (input) input.focus();
            }
        }
    }

    function toggleVoiceInput() {
        if (!chatState.recognition) {
            addBotMessage('Voice input is not supported in your browser.');
            return;
        }

        if (chatState.isListening) {
            stopListening();
        } else {
            startListening();
        }
    }

    function startListening() {
        if (chatState.recognition && !chatState.isListening) {
            chatState.isListening = true;
            const micBtn = document.getElementById('chat-mic-btn');
            const indicator = document.getElementById('chat-recording-indicator');

            if (micBtn) micBtn.classList.add('listening');
            if (indicator) indicator.style.display = 'flex';

            try {
                chatState.recognition.start();
            } catch (e) {
                console.error('Error starting recognition:', e);
                stopListening();
            }
        }
    }

    function stopListening() {
        chatState.isListening = false;
        const micBtn = document.getElementById('chat-mic-btn');
        const indicator = document.getElementById('chat-recording-indicator');

        if (micBtn) micBtn.classList.remove('listening');
        if (indicator) indicator.style.display = 'none';

        if (chatState.recognition) {
            try {
                chatState.recognition.stop();
            } catch (e) {
                // Ignore errors when stopping
            }
        }
    }

    async function sendMessage() {
        const input = document.getElementById('chat-input');
        const query = input?.value.trim();

        if (!query || chatState.isProcessing) {
            return;
        }

        // Add user message
        addUserMessage(query);
        input.value = '';

        // Show typing indicator
        showTypingIndicator();

        // Disable input and buttons
        setProcessingState(true);

        try {
            // Call API
            const response = await fetch('/rag/api/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({ query: query })
            });

            const data = await response.json();

            // Remove typing indicator
            hideTypingIndicator();

            if (data.error) {
                addBotMessage(`Error: ${data.error}`);
            } else {
                // Add bot response
                addBotMessage(data.response, data.sources);

                // Speak response (optional)
                speakResponse(data.response);
            }

        } catch (error) {
            hideTypingIndicator();
            addBotMessage('Sorry, I encountered an error. Please try again.');
            console.error('Chat API error:', error);
        } finally {
            setProcessingState(false);
        }
    }

    function addUserMessage(text) {
        const messages = document.getElementById('chat-messages');
        if (!messages) return;

        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user';
        messageDiv.textContent = text;
        messages.appendChild(messageDiv);
        scrollToBottom();
    }

    function addBotMessage(text, sources = null) {
        const messages = document.getElementById('chat-messages');
        if (!messages) return;

        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot';

        // Add response text as Markdown
        const textDiv = document.createElement('div');
        textDiv.className = 'markdown-body';
        textDiv.innerHTML = typeof marked !== 'undefined' ? marked.parse(text) : text;
        messageDiv.appendChild(textDiv);


        messages.appendChild(messageDiv);
        scrollToBottom();
    }

    function showTypingIndicator() {
        const messages = document.getElementById('chat-messages');
        if (!messages) return;

        const indicator = document.createElement('div');
        indicator.id = 'typing-indicator';
        indicator.className = 'typing-indicator';
        indicator.innerHTML = `
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
        `;
        messages.appendChild(indicator);
        scrollToBottom();
    }

    function hideTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) indicator.remove();
    }

    function setProcessingState(processing) {
        chatState.isProcessing = processing;
        const input = document.getElementById('chat-input');
        const sendBtn = document.getElementById('chat-send-btn');
        const micBtn = document.getElementById('chat-mic-btn');

        if (input) input.disabled = processing;
        if (sendBtn) sendBtn.disabled = processing;
        if (micBtn) micBtn.disabled = processing;
    }

    function scrollToBottom() {
        const messages = document.getElementById('chat-messages');
        if (messages) {
            messages.scrollTop = messages.scrollHeight;
        }
    }

    function speakResponse(text) {
        if (chatState.synth && chatState.synth.speaking) {
            chatState.synth.cancel();
        }

        if (chatState.synth) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 0.9;
            utterance.pitch = 1.0;

            utterance.onstart = () => showStopBtn(true);
            utterance.onend = () => showStopBtn(false);
            utterance.onerror = () => showStopBtn(false);

            chatState.currentUtterance = utterance;
            chatState.synth.speak(utterance);
        }
    }

    function showStopBtn(show) {
        const stopBtn = document.getElementById('chat-stop-speech-btn');
        if (stopBtn) {
            stopBtn.style.display = show ? 'flex' : 'none';
        }
    }

    function stopSpeaking() {
        if (chatState.synth) {
            chatState.synth.cancel();
            showStopBtn(false);
        }
    }

    function getCsrfToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        // Fallback: try to get from meta tag
        const meta = document.querySelector('meta[name="csrf-token"]');
        return meta ? meta.getAttribute('content') : '';
    }

})();

