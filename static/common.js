if (document.getElementById('id_is_limited')) {
    let limited_checkbox = document.getElementById('id_is_limited');
    let hidden_elements = document.getElementsByClassName('hidden')
    let hidden_elements_array = Array.from(hidden_elements)
    limited_checkbox.addEventListener('change', function() {
        if (this.checked) {
            hidden_elements_array.forEach(function (element) {
                element.classList.remove('hidden');
            });
s
        }else{
            hidden_elements_array.forEach(function (element) {
                element.classList.add('hidden');
            });
        }
    })
}
