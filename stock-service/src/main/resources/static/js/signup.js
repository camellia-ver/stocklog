document.addEventListener('DOMContentLoaded', function () {
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirmPassword');
    const message = document.getElementById('message');
    const form = document.getElementById('userForm');
    const stockSearchInput = document.getElementById("stockSearch");
    const suggestions = document.getElementById("suggestions");
    const selectedList = document.getElementById("selectedList");

    let selectedStocks = [];
    let debounceTimer;

    const csrfTokenElement = document.querySelector('input[name="_csrf"]');
    const csrfToken = csrfTokenElement ? csrfTokenElement.value : null;

    if (!csrfToken) {
        console.error('CSRF 토큰을 찾을 수 없습니다.');
        return;
    }

    if (!stockSearchInput || !suggestions || !form || !selectedList) {
        console.error('DOM 요소를 찾을 수 없습니다.');
        return;
    }

    confirmPasswordInput.addEventListener("keyup", validatePassword);

    function validatePassword() {
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;
        const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

        if (!passwordRegex.test(password)) {
            showMessage("비밀번호는 최소 8자, 영문/숫자/특수문자를 포함해야 합니다.", "red");
            return false;
        } else if (password !== confirmPassword) {
            showMessage("비밀번호가 일치하지 않습니다.", "red");
            return false;
        } else {
            showMessage("비밀번호가 유효하고 일치합니다.", "green");
            return true;
        }
    }

    function showMessage(text, color) {
        message.style.color = color;
        message.innerText = text;
    }

    stockSearchInput.addEventListener("input", function () {
        clearTimeout(debounceTimer);

        const query = this.value;
        if (query.length < 2) {
            suggestions.innerHTML = "";
            return;
        }

        debounceTimer = setTimeout(() => {
            fetch(`/stocks/search?keyword=${query}`, {
                method: "GET",
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-TOKEN': csrfToken
                }
            })
                .then(response => response.json())
                .then(data => {
                    suggestions.innerHTML = "";
                    data.forEach(stock => {
                        const li = document.createElement("li");
                        li.className = "list-group-item list-group-item-action";
                        li.textContent = `${stock.name} (${stock.code})`;
                        li.onclick = () => selectStock(stock);
                        suggestions.appendChild(li);
                    });
                })
                .catch(error => console.error("❌ 자동완성 API 요청 실패:", error));
        }, 300);
    });

    function selectStock(stock) {
        if (selectedStocks.find(s => s.code === stock.code)) {
            alert('이미 선택한 종목입니다.');
            return;
        }

        selectedStocks.push(stock);
        updateSelectedStocks();

        stockSearchInput.value = '';
        suggestions.innerHTML = '';
    }

    function updateSelectedStocks() {
        selectedList.innerHTML = '';

        document.querySelectorAll("input[name^='interestStockList']").forEach(el => el.remove());

        selectedStocks.forEach((stock, index) => {
            const li = document.createElement("li");
            li.className = "list-group-item d-flex justify-content-between align-items-center";
            li.textContent = `${stock.name} (${stock.code})`;

            const removeBtn = document.createElement("button");
            removeBtn.className = "remove-btn btn btn-sm btn-outline-danger ms-2";
            removeBtn.type = "button";
            removeBtn.textContent = "❌";
            removeBtn.onclick = () => removeStock(stock.code);
            li.appendChild(removeBtn);

            selectedList.appendChild(li);

            const input = document.createElement("input");
            input.type = "hidden";
            input.name = `interestStockList[${index}].code`;
            input.value = stock.code;
            form.appendChild(input);
        });
    }

    function removeStock(code) {
        selectedStocks = selectedStocks.filter(stock => stock.code !== code);
        updateSelectedStocks();
    }
});
