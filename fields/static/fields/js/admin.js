document.addEventListener("DOMContentLoaded", function(event) {
    var data_type = document.getElementById('id_data_type');
    data_type.addEventListener('change', hideOrShowOptions);

    function hideOrShowOptions(ele) {
        if (ele.target.value === 'OPTION') {
            document.getElementsByClassName('field-options')[0].style.display = 'block';
        } else {
            document.getElementsByClassName('field-options')[0].style.display = 'none';
        }
    }


    hideOrShowOptions({target: data_type});
});
