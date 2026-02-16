let cart = {}; // เก็บสินค้าที่สแกน

document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ JavaScript Loaded");

    // ตรวจจับ Enter เพื่อสแกนบาร์โค้ด
    document.getElementById("barcode-input").addEventListener("keydown", function (event) {
        scanBarcode(event);
    });
});

// ฟังก์ชันตรวจจับการกด Enter และสแกนบาร์โค้ด
function scanBarcode(event) {
    if (event.key === "Enter") {
        let barcode = document.getElementById("barcode-input").value.trim();
        
        if (!barcode) {
            return;  
        }

        console.log("🔍 บาร์โค้ดที่สแกน:", barcode);
        fetchProduct(barcode);
    }
}

// ฟังก์ชันปุ่มกดเพื่อกรอกบาร์โค้ดเอง
function manualScan() {
    let barcode = document.getElementById("barcode-input").value.trim();
    
    if (!barcode) {
        return;  
    }

    console.log("🔍 กรอกบาร์โค้ดด้วยมือ:", barcode);
    fetchProduct(barcode);
}

// ฟังก์ชันเรียก API เพื่อดึงข้อมูลสินค้า
function fetchProduct(barcode) {
    let url = `/shopsales/get_product_by_barcode/${barcode}/`;  // ✅ แก้ให้ตรงกับเส้นทางที่ใช้
    console.log("📡 เรียก API:", url);

    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log("📦 ผลลัพธ์จาก API:", data);
            if (data.success) {
                addToCart(data.product);
            } else {
                alert("❌ ไม่พบสินค้าในระบบ");
            }
        })
        .catch(error => {
            console.error("⚠️ เกิดข้อผิดพลาด:", error);
            alert("เกิดข้อผิดพลาดในการโหลดข้อมูลสินค้า");
        });

    document.getElementById("barcode-input").value = "";
}

// ฟังก์ชันเพิ่มสินค้าเข้าตะกร้า
function addToCart(product) {
    console.log("🛒 เพิ่มสินค้า:", product);

    if (cart[product.code]) {
        cart[product.code].quantity++;
    } else {
        cart[product.code] = {
            name: product.name,
            price: product.price,
            quantity: 1
        };
    }
    updateCartDisplay();
}

// ฟังก์ชันลบสินค้าออกจากตะกร้า
function removeItem(code) {
    delete cart[code];
    updateCartDisplay();
}

// ฟังก์ชันอัปเดตการแสดงตะกร้าสินค้า
function updateCartDisplay() {
    let tbody = document.querySelector("#cart tbody");
    tbody.innerHTML = "";
    let total = 0;

    console.log("🛒 ตะกร้าสินค้า:", cart);

    for (let code in cart) {
        let item = cart[code];
        let row = `<tr>
            <td>${code}</td>
            <td>${item.name}</td>
            <td>${item.price.toFixed(2)}</td>
            <td>
                <button onclick="decreaseQuantity('${code}')">➖</button>
                <span id="qty-${code}">${item.quantity}</span>
                <button onclick="increaseQuantity('${code}')">➕</button>
            </td>
            <td>${(item.price * item.quantity).toFixed(2)}</td>
            <td><button onclick="removeItem('${code}')">❌</button></td>
        </tr>`;
        tbody.innerHTML += row;
        total += item.price * item.quantity;
    }

    document.getElementById("total-price").innerText = total.toFixed(2);
    document.getElementById("item-count").innerText = Object.keys(cart).length;
}

// เพิ่มจำนวนสินค้า
function increaseQuantity(code) {
    if (cart[code]) {
        cart[code].quantity++;
        document.getElementById(`qty-${code}`).innerText = cart[code].quantity;
        updateCartDisplay();
    }
}

// ลดจำนวนสินค้า
function decreaseQuantity(code) {
    if (cart[code] && cart[code].quantity > 1) {
        cart[code].quantity--;
    } else {
        delete cart[code]; // ถ้าจำนวนเป็น 0 ให้ลบออกจากตะกร้า
    }
    updateCartDisplay();
}

// ฟังก์ชันล้างตะกร้าทั้งหมด
function clearCart() {
    cart = {};
    updateCartDisplay();
}

// ฟังก์ชันคิดเงิน
function getCSRFToken() {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1]; // ✅ ดึงค่า CSRF Token จาก Cookie
}

function checkout() {
    if (Object.keys(cart).length === 0) {
        alert("⚠️ ตะกร้าว่าง กรุณาเพิ่มสินค้าก่อนคิดเงิน");
        return;
    }

    // ✅ แปลง cart ให้เป็น Array และเพิ่ม "code"
    let cartArray = Object.entries(cart).map(([code, item]) => ({
        code: code,  // ✅ เพิ่ม "code" เข้าไปใน Object
        name: item.name,
        price: item.price,
        quantity: item.quantity
    }));

    console.log("🛒 JSON ที่ส่งไป:", JSON.stringify(cartArray)); // ✅ Debug JSON

    fetch('/checkout/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ cart: cartArray })  // ✅ ส่งไปเป็น Array ที่ถูกต้อง
    })
    .then(response => response.json())
    .then(data => {
        console.log("📦 ผลลัพธ์จาก API:", data);
        if (data.success) {
            alert(`🎉 การขายสำเร็จ เลขที่การขาย: ${data.sale_id}`);
            clearCart();
        } else {
            alert(`❌ ${data.message}`);
        }
    })
    .catch(error => {
        console.error('⚠️ Error:', error);
        alert("เกิดข้อผิดพลาดในการทำรายการ");
    });
}

function openPaymentModal() {
    let modal = document.getElementById("payment-modal");
    let tbody = document.querySelector("#payment-summary tbody");
    let total = 0;

    tbody.innerHTML = ""; // ล้างข้อมูลเก่าก่อนแสดงใหม่

    for (let code in cart) {
        let item = cart[code];
        let row = `<tr>
            <td>${item.name}</td>
            <td>${item.quantity}</td>
            <td>${item.price.toFixed(2)}</td>
            <td>${(item.price * item.quantity).toFixed(2)}</td>
        </tr>`;
        tbody.innerHTML += row;
        total += item.price * item.quantity;
    }

    document.getElementById("payment-total").innerText = total.toFixed(2);
    document.getElementById("received-amount").value = "";
    document.getElementById("change-amount").innerText = "0";

    modal.style.display = "block";
}

function closePaymentModal() {
    document.getElementById("payment-modal").style.display = "none";
}

function calculateChange() {
    let total = parseFloat(document.getElementById("payment-total").innerText);
    let received = parseFloat(document.getElementById("received-amount").value) || 0;
    let change = received - total;
    document.getElementById("change-amount").innerText = change >= 0 ? change.toFixed(2) : "0";
}

function confirmCheckout() {
    let received = parseFloat(document.getElementById("received-amount").value) || 0;
    let total = parseFloat(document.getElementById("payment-total").innerText);
    let change = received - total;

    if (received < total) {
        alert("⚠️ เงินที่ได้รับไม่เพียงพอ!");
        return;
    }

    // ✅ แปลง cart ให้เป็น Array และเพิ่ม "code"
    let cartArray = Object.entries(cart).map(([code, item]) => ({
        code: code,  
        name: item.name,
        price: item.price,
        quantity: item.quantity
    }));

    console.log("🛒 JSON ที่ส่งไป:", JSON.stringify({
        cart: cartArray,
        amount_received: received,
        change_amount: change
    })); // ✅ Debug JSON ที่ส่งไป

    fetch('/checkout/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            cart: cartArray,
            amount_received: received,  // ✅ ส่งค่าจำนวนเงินที่ลูกค้าจ่าย
            change_amount: change  // ✅ ส่งค่าเงินทอน
        })  
    })
    .then(response => response.json())
    .then(data => {
        console.log("📦 ผลลัพธ์จาก API:", data);
        if (data.success) {
            alert(`🎉 การขายสำเร็จ! เงินทอน: ${change.toFixed(2)} บาท`);
            closePaymentModal();
            clearCart();
        } else {
            alert(`❌ ${data.message}`);
        }
    })
    .catch(error => {
        console.error('⚠️ Error:', error);
        alert("เกิดข้อผิดพลาดในการทำรายการ");
    });
}

