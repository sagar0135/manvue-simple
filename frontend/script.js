import { products } from "./products.js";

const API_URL = "http://localhost:5000";

async function register() {
  try {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    
    if (!email || !password) {
      alert("Please fill in both email and password");
      return;
    }
    
    const res = await fetch(`${API_URL}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });
    
    if (res.ok) {
      alert("Registration successful!");
    } else {
      const error = await res.text();
      alert(`Registration failed: ${error}`);
    }
  } catch (error) {
    alert(`Error: ${error.message}`);
  }
}

async function login() {
  try {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    
    if (!email || !password) {
      alert("Please fill in both email and password");
      return;
    }
    
    const res = await fetch(`${API_URL}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });
    
    if (res.ok) {
      const data = await res.json();
      if (data.access_token) {
        localStorage.setItem("token", data.access_token);
        alert("Login successful!");
        loadProducts();
      } else {
        alert("Login failed: No token received");
      }
    } else {
      const error = await res.text();
      alert(`Login failed: ${error}`);
    }
  } catch (error) {
    alert(`Error: ${error.message}`);
  }
}

async function loadProducts() {
  try {
    const res = await fetch(`${API_URL}/products`);
    if (res.ok) {
      const products = await res.json();
      renderProducts(products);
    } else {
      console.log("Backend not available, using demo products");
      renderProducts(products); // fallback to demo products
    }
  } catch (error) {
    console.log("Backend not available, using demo products");
    renderProducts(products); // fallback to demo products
  }
}

function renderProducts(products) {
  const container = document.getElementById("products");
  container.innerHTML = "";
  products.forEach(p => {
    const div = document.createElement("div");
    div.className = "product";
    div.innerHTML = `
      <img src="${p.image_url}" alt="${p.title}">
      <h3>${p.title}</h3>
      <p>$${p.price}</p>
    `;
    container.appendChild(div);
  });
}

// Make functions globally available for onclick handlers
window.register = register;
window.login = login;

window.onload = () => {
  renderProducts(products); // fallback demo products
};
