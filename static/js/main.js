const insert = document.getElementById('insert')
let url = 'http://127.0.0.1:8083/orders/get_orders'
let url_update = 'http://127.0.0.1:8083/orders/update_data'
async function sendRequest(url){
    await fetch(url_update)
    let test = await fetch(url)
    let response = await test.json()
    return response
}

sendRequest(url).then(response => {
    for (let i = 0; i<response.orders.length; i++){
        insert.insertAdjacentHTML("beforeend", `<div class="data" id="${response.orders[i].order_number}">
                    <div>
                        <span class="order_number">${response.orders[i].order_number}</span>
                    </div>
                    <div>
                        <span class="price_dollar">${response.orders[i].price_dollar}</span>
                    </div>
                    <div>
                        <span class="price_rur">${response.orders[i].price_rur}</span>
                    </div>
                    <div>
                        <span class="delivery_date">${response.orders[i].delivery_date}</span>
                    </div>
                </div>`)

    }
})

setInterval(() => {
    sendRequest(url).then(response => {
        const elemData = document.getElementsByClassName('data')
        const arrOrNum = new Array()
        for (let k=0; k<elemData.length; k++){
            arrOrNum.push(+elemData[k].id)
        }
        for (let j = 0; j<response.orders.length; j++){
            let arrIndex = arrOrNum.indexOf(response.orders[j].order_number)
            if (arrOrNum.includes(response.orders[j].order_number)) {
                let or_num = document.getElementById(response.orders[j].order_number)
                or_num.children[0].children[0].innerText = response.orders[j].order_number
                or_num.children[1].children[0].innerText = response.orders[j].price_dollar
                or_num.children[2].children[0].innerText = response.orders[j].price_rur
                or_num.children[3].children[0].innerText = response.orders[j].delivery_date
                if (arrIndex === 0)
                    arrOrNum.splice(arrIndex++, arrIndex++)
                else
                    arrOrNum.splice(arrIndex, arrIndex)
            } else {
                insert.insertAdjacentHTML("beforeend", `<div class="data" id="${response.orders[j].order_number}">
                    <div>
                        <span class="order_number">${response.orders[j].order_number}</span>
                    </div>
                    <div>
                        <span class="price_dollar">${response.orders[j].price_dollar}</span>
                    </div>
                    <div>
                        <span class="price_rur">${response.orders[j].price_rur}</span>
                    </div>
                    <div>
                        <span class="delivery_date">${response.orders[j].delivery_date}</span>
                    </div>
                </div>`)
            }
        }
        if (arrOrNum.length !== 0) {
            for (let q = 0; q<arrOrNum.length; q++) {
                document.getElementById(arrOrNum[q]).remove()
            }
        }
    })
}, 3000)
