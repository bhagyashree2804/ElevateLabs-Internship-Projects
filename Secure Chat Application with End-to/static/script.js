alert("script.js loaded! ✅");

let socket;
let username = "";
let privateKeyPEM = "";
let publicKeyPEM = "";

function join() {
  username = document.getElementById("username").value;
  if (!username) {
    alert("Enter username first!");
    return;
  }

  socket = io();
  socket.on("connect", () => {
    console.log("Connected as", username);
    alert("Joined as " + username);
  });

  socket.on("receive_message", (data) => {
    const li = document.createElement("li");
    li.textContent = `${data.from}: ${data.message}`;
    document.getElementById("messages").appendChild(li);
  });
}

// ✅ Load Private Key
function loadPrivateKey() {
  const file = document.getElementById("privateKeyFile").files[0];
  if (!file) {
    alert("Please choose a private key file first!");
    return;
  }
  const reader = new FileReader();
  reader.onload = (e) => {
    privateKeyPEM = e.target.result;
    alert("Private key loaded successfully!");
    console.log("Private key starts with:", privateKeyPEM.substring(0, 40));
  };
  reader.readAsText(file);
}

// ✅ Load Public Key
function loadPublicKey() {
  const file = document.getElementById("publicKeyFile").files[0];
  if (!file) {
    alert("Please choose a public key file first!");
    return;
  }
  const reader = new FileReader();
  reader.onload = (e) => {
    publicKeyPEM = e.target.result;
    alert("Public key loaded successfully!");
    console.log("Public key starts with:", publicKeyPEM.substring(0, 40));
  };
  reader.readAsText(file);
}

// ✅ Send a message
function sendMessage() {
  const msg = document.getElementById("message").value;
  if (!msg) return;
  if (!socket) {
    alert("Join first!");
    return;
  }

  socket.emit("send_message", { from: username, message: msg });
  document.getElementById("message").value = "";
}
