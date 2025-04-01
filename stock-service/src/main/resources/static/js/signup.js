document.addEventListener('DOMContentLoaded', function() {
    document.getElementById("confirmPassword").addEventListener("keyup", validatePassword);

    function validatePassword(){
        let password = document.getElementById('password').value;
        let confirmPassword = document.getElementById('confirmPassword').value;
        let message = document.getElementById("message");

        let passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

        if (!passwordRegex.test(password)){
            message.style.color = "red";
            message.innerText = "비밀번호는 최소 8자, 영문/숫자/특수문자를 포함해야 합니다.";
            return false;
        }else if(password != confirmPassword){
            message.style.color = "red";
            message.innerText = "비밀번호가 일치하지 않습니다.";
            return false;
        }else{
            message.style.color = "green";
            message.innerText = "비밀번호가 유효하고 일치합니다.";
            return true;
        }
    }

    let selectedStocks = []
    let debounceTimer;

    const csrfTokenElement = document.querySelector('input[name="_csrf"]');
    const csrfToken = csrfTokenElement ? csrfTokenElement.value : null;

    if (!csrfToken) {
        console.error('CSRF 토큰을 찾을 수 없습니다.');
        return;
    }

    let stockSearchInput = document.getElementById("stockSearch");
    if (!stockSearchInput) {
        console.error("❌ 검색 입력 필드를 찾을 수 없습니다.");
        return;
    }

    stockSearchInput.addEventListener("input", function() {
        clearTimeout(debounceTimer);

        let query = this.value;
        if (query.length < 2) {
            document.getElementById("suggestions").innerHTML = "";
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
            .then(response => {
                return response.json();
            })
            .then(data => {
                let suggestions = document.getElementById("suggestions");
                if (!suggestions) {
                    console.error("❌ 자동완성 목록을 표시할 요소가 없습니다.");
                    return;
                }

                suggestions.innerHTML = "";
                data.forEach(stock => {
                let li = document.createElement("li");
                li.className = "list-group-item list-group-item-action";
                li.textContent = `${stock.itmsNm} (${stock.srtnCd})`;
                li.onclick = () => selectStock(stock);
                suggestions.appendChild(li);
                });
            })
            .catch(error => console.error("❌ 자동완성 API 요청 실패:", error));
        }, 300);
    });


    function selectStock(stock){
        if (selectedStocks.length >= 5) {
            alert("최대 5개까지 선택할 수 있습니다.");
            return;
        }

        if (selectedStocks.find(s => s.srtnCd === stock.srtnCd)){
            alert('이미 선택한 종목입니다.');
            return;
        }

        selectedStocks.push(stock);
        updateSelectedStocks();

        document.getElementById("stockSearch").value = '';
        document.getElementById("suggestions").innerHTML = '';
    }

    function updateSelectedStocks(){
        let selectedList = document.getElementById("selectedList");
        selectedList.innerHTML = '';

        selectedStocks.forEach(stock => {
            let li = document.createElement("li");
            li.className = "list-group-item d-flex justify-content-between";
            li.textContent = `${stock.itmsNm} (${stock.srtnCd})`;

            let removeBtn = document.createElement("button");
            removeBtn.className = "remove-btn";
            removeBtn.textContent = "❌";
            removeBtn.onclick = () => removeStock(stock.srtnCd);
            li.appendChild(removeBtn);

            selectedList.appendChild(li);
        });
    }

    function removeStock(srtnCd) {
        selectedStocks = selectedStocks.filter(stock => stock.srtnCd !== srtnCd);
        updateSelectedStocks();
    }
});
