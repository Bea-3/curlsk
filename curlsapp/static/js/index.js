// External JS file for Index

//show and hide the registration forms
$(document).ready(function(){
    $('#cust_reg').hide()
    $('#ven_reg').hide()

    $('[name="register"]').click(function(){
        if ($(this).val() == 'new_cust'){
            $('#cust_reg').show()
            $('#ven_reg').hide()
        }else{
            $('#ven_reg').show()
            $('#cust_reg').hide()
        }
    })
})

// Bootstrap Vendor Dashboard JS
// /* global bootstrap: false */
// (function () {
//     'use strict'
//     var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
//     tooltipTriggerList.forEach(function (tooltipTriggerEl) {
//       new bootstrap.Tooltip(tooltipTriggerEl)
//     })
//   })()
  