console.log('search.js loaded')
const shop = document.getElementById('select_shop')
const category = document.getElementById('select_category')
const brand = document.getElementById('select_brand')
shop?.addEventListener('change', (e) => {
    fetch(`/categories?shop_id=${e.target.value}`).then((res) => {
        res.json().then((data) => {
            console.log(data)
            category.innerHTML = `<option value="">--Please choose an option--</option>`
            data.forEach((element) => {
                category.innerHTML += `<option value="${element.id}">${element.categoryName}</option>`
            })
            category.disabled = false
        })
    })
})

category?.addEventListener('change', (e) => {
    fetch(`/brands?category_id=${e.target.value}`).then((res) => {
        res.json().then((data) => {
            console.log(data)
            brand.innerHTML = ''
            data.forEach((element) => {
                brand.innerHTML += `<option value="${element.id}">${element.brandName}</option>`
            })
            brand.disabled = false
        })
    })
})

function changeArrowButton() {
    const detailSearch = document.getElementById('detail_search')
    const arrowButton = document.getElementById('i_search_filter')
    if (arrowButton.classList.contains('ti-arrow-big-down')) {
        arrowButton.classList.remove('ti-arrow-big-down')
        arrowButton.classList.add('ti-arrow-big-up')
        detailSearch?.classList.remove('hidden')
    } else {
        arrowButton.classList.remove('ti-arrow-big-up')
        arrowButton.classList.add('ti-arrow-big-down')
        detailSearch?.classList.add('hidden')
    }
}
