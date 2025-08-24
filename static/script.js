document.getElementById("send-btn").addEventListener("click", sendMessage);
document
  .getElementById("user-input")
  .addEventListener("keypress", function (e) {
    if (e.key === "Enter") sendMessage();
  });

function appendMessage(content, sender, typing = false) {
  const chatBox = document.getElementById("chat-box");
  const msg = document.createElement("div");
  msg.className = `chat-message ${sender}`;
  msg.innerHTML = `
        <div class="avatar">${sender === "bot" ? "🤖" : "👤"}</div>
        <div class="message-bubble"></div>
    `;

  const bubble = msg.querySelector(".message-bubble");
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;

  if (typing) {
    let index = 0;
    const htmlContent = marked.parse(content);
    const temp = document.createElement("div");
    temp.innerHTML = htmlContent;
    const textToType = temp.innerHTML;

    const typingInterval = setInterval(() => {
      bubble.innerHTML = textToType.slice(0, index);
      index++;
      chatBox.scrollTop = chatBox.scrollHeight;
      if (index > textToType.length) {
        clearInterval(typingInterval);
        msg.querySelectorAll("pre code").forEach((block) => {
          hljs.highlightElement(block);
        });
      }
    }, 10);
  } else {
    bubble.innerHTML = marked.parse(content);
    msg.querySelectorAll("pre code").forEach((block) => {
      hljs.highlightElement(block);
    });
  }
}

function sendMessage() {
  const input = document.getElementById("user-input");
  const text = input.value.trim();
  if (!text) return;

  appendMessage(text, "user");
  input.value = "";

  const typingIndicator = document.createElement("div");
  typingIndicator.className = "typing-indicator";
  typingIndicator.textContent = "Bot is typing...";
  document.getElementById("chat-box").appendChild(typingIndicator);
  document.getElementById("chat-box").scrollTop =
    document.getElementById("chat-box").scrollHeight;

  fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: text })
  })
    .then((res) => res.json())
    .then((data) => {
      typingIndicator.remove();
      appendMessage(data.reply, "bot", true);
    });
}
