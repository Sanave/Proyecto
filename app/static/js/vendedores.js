// Display de formulario de registro
document.getElementById('registrar').addEventListener('click', ()=> {
    const formulario_registro = document.getElementById('formulario_registro');
    if (formulario_registro.style.display == 'block'){ formulario_registro.style.display = 'none'}
    else{formulario_registro.style.display = 'block'};
});
// Cerrar formulario de registro
document.getElementById('cancelar').addEventListener('click', () => {
    document.getElementById('formulario_registro').style.display = 'none';
});

// Boton de Información de los clientes
const botonesInfo = document.querySelectorAll('.boton_info');
botonesInfo.forEach(boton => {
    boton.addEventListener('click', async (event) => {
        const botonClickeado = event.currentTarget;
        const formulario_actualizar = document.getElementById('formulario_actualizar');
        if (formulario_actualizar.style.display === 'none') {
            formulario_actualizar.style.display = 'block';
        }; 
        const id = botonClickeado.value;
        const id_readonly = document.getElementById('id_readonly');
        const nombre = document.getElementById('info_nombre');
        const correo = document.getElementById('info_correo');
        const telefono = document.getElementById('info_telefono');
        const direccion = document.getElementById('info_direccion');

        try {
            const respuesta = await fetch(`/get_vendedor?id=${id}`);
            if (respuesta.ok) {
                const vendedor = await respuesta.json();
                id_readonly.value = vendedor.id;
                nombre.value = vendedor.nombre;
                correo.value = vendedor.correo;
                telefono.value = vendedor.telefono;
                direccion.value = vendedor.direccion;
            }
            else{
                const vendedor = await respuesta.json();
                console.log(vendedor.mensaje);
            }
        } catch (error) {
            console.log(error);
        }
    });
});
// Bloqueo de ReadOnly
document.getElementById('cancelar_info').addEventListener('click', ()=>{
    document.getElementById('info_nombre').readOnly = true;
    document.getElementById('info_correo').readOnly = true;
    document.getElementById('info_telefono').readOnly = true;
    document.getElementById('info_direccion').readOnly = true;
    document.getElementById('formulario_actualizar').style.display = 'none';
});

document.getElementById('readonly_block').addEventListener('click', () => {
    document.getElementById('info_nombre').readOnly = false;
    document.getElementById('info_correo').readOnly = false;
    document.getElementById('info_telefono').readOnly = false;
    document.getElementById('info_direccion').readOnly = false;
});
