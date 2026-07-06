let products = JSON.parse(localStorage.getItem("products")) || [];

function saveProduct() {
    const url = document.getElementById("productUrl").value.trim();
    const targetPrice = document.getElementById("targetPrice").value.trim();

    if (url === "" || targetPrice === "") {
        alert("Fill all fields!");
        return;
    }

    products.push({
        url: url,
        targetPrice: targetPrice
    });

    localStorage.setItem("products", JSON.stringify(products));

    document.getElementById("productUrl").value = "";
    document.getElementById("targetPrice").value = "";

    renderProducts();
}

function deleteProduct(index) {
    products.splice(index, 1);
    localStorage.setItem("products", JSON.stringify(products));
    renderProducts();
}

function renderProducts() {
    const list = document.getElementById("products");
    list.innerHTML = "";

    if (products.length === 0) {
        list.innerHTML = "<p>No products saved.</p>";
        return;
    }

    products.forEach((product, index) => {
        list.innerHTML += `
            <div class="card">
                <p><b>🎯 Target:</b> ₹${product.targetPrice}</p>
                <a href="${product.url}" target="_blank">Open Product</a><br><br>
                <button onclick="deleteProduct(${index})">Delete</button>
            </div>
        `;
    });
}

renderProducts();