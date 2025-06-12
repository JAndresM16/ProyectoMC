const btnDelete= document.querySelectorAll('.btn-delete');
if(btnDelete){
    const btnArray=Array.from(btnDelete);
    btnArray.forEach((btn) => {
        btn.addEventListener('click', (e) => {
            if(!confirm('esta seguro de eliminar?')){
                e.preventDefault();
            }
        });
    });
}

const checkbox = document.getElementById('exampleCheck1');
const passwordField = document.getElementById('exampleInputPassword1');

checkbox.addEventListener('change', function() {
    if (checkbox.checked) {
        passwordField.type = 'text';
    } else {
        passwordField.type = 'password';
    }
});

function confirmarRenta() {
    return confirm("¿Estás seguro de que quieres rentar este DVD?");
}