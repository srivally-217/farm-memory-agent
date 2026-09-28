// Backend URL
const API_URL = "http://127.0.0.1:8000";


// ================================
// CHAT ELEMENTS
// ================================

const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const chatMessages = document.getElementById("chatMessages");


// ================================
// SEND MESSAGE
// ================================

async function sendMessage() {

    const message = messageInput.value.trim();

    if (!message) {
        return;
    }

    // Show farmer's message
    addUserMessage(message);

    // Clear input
    messageInput.value = "";

    // Disable button while waiting
    sendButton.disabled = true;
    sendButton.innerHTML = "Thinking...";

    // Show loading message
    const loadingMessage = addAgentMessage("🌱 Remembering your farm history...");

    try {

        const response = await fetch(`${API_URL}/farm-response`, {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })
        });


        if (!response.ok) {
            throw new Error("Server returned an error");
        }


        const data = await response.json();


        // Remove loading message
        loadingMessage.remove();


        // Show actual agent response
        addAgentMessage(data.response);

    } catch (error) {

        loadingMessage.remove();

        addAgentMessage(
            "Sorry, I couldn't connect to the Farm Memory Agent. " +
            "Please make sure the FastAPI server is running."
        );

        console.error(error);

    } finally {

        sendButton.disabled = false;
        sendButton.innerHTML = "<span>Ask Agent</span> ➤";
    }
}


// ================================
// ADD USER MESSAGE
// ================================

function addUserMessage(message) {

    const wrapper = document.createElement("div");

    wrapper.className = "user-message-wrapper";

    wrapper.innerHTML = `
        <div class="message user-message">
            ${escapeHtml(message)}
        </div>
    `;

    chatMessages.appendChild(wrapper);

    scrollToBottom();
}


// ================================
// ADD AGENT MESSAGE
// ================================

function addAgentMessage(message) {

    const wrapper = document.createElement("div");

    wrapper.className = "agent-response-wrapper";

    wrapper.innerHTML = `
        <div class="agent-icon">
            🌱
        </div>

        <div class="message agent-response">
            ${formatAgentResponse(message)}
        </div>
    `;

    chatMessages.appendChild(wrapper);

    scrollToBottom();

    return wrapper;
}


// ================================
// SAVE FARM EVENT
// ================================

const eventInput = document.getElementById("eventInput");
const eventButton = document.getElementById("eventButton");
const eventStatus = document.getElementById("eventStatus");


eventButton.addEventListener("click", async function () {

    const event = eventInput.value.trim();

    if (!event) {

        eventStatus.textContent =
            "Please describe what happened on your farm.";

        return;
    }


    eventButton.disabled = true;
    eventButton.textContent = "Saving...";

    eventStatus.textContent = "";


    try {

        const response = await fetch(`${API_URL}/farm-event`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                event: event
            })
        });


        if (!response.ok) {
            throw new Error("Could not save event");
        }


        const data = await response.json();


        eventStatus.textContent =
            "✅ " + data.message;

        eventInput.value = "";


    } catch (error) {

        eventStatus.textContent =
            "❌ Could not save the farm experience.";

        console.error(error);

    } finally {

        eventButton.disabled = false;
        eventButton.textContent = "💾 Save Farm Experience";
    }

});


// ================================
// SEND MESSAGE WITH ENTER
// ================================

messageInput.addEventListener("keydown", function (event) {

    if (event.key === "Enter" && !event.shiftKey) {

        event.preventDefault();

        sendMessage();
    }

});


// ================================
// BUTTON EVENT
// ================================

sendButton.addEventListener("click", sendMessage);


// ================================
// SCROLL CHAT
// ================================

function scrollToBottom() {

    chatMessages.parentElement.scrollTop =
        chatMessages.parentElement.scrollHeight;
}


// ================================
// BASIC HTML ESCAPING
// ================================

function escapeHtml(text) {

    const div = document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}


// ================================
// FORMAT AGENT RESPONSE
// ================================

function formatAgentResponse(text) {

    // Convert basic Markdown-style formatting
    // into readable HTML.

    let formatted = escapeHtml(text);

    formatted = formatted.replace(
        /\*\*(.*?)\*\*/g,
        "<strong>$1</strong>"
    );

    formatted = formatted.replace(
        /^- (.*)$/gm,
        "• $1"
    );

    formatted = formatted.replace(
        /\n/g,
        "<br>"
    );

    return formatted;
}