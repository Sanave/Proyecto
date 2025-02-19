// Display de formulario de registro
document.getElementById('registrar').addEventListener('click', ()=> {
    const formulario_registro = document.getElementById('formulario_registro');
    if (formulario_registro.style.display == 'block'){ formulario_registro.style.display = 'none'}
    else{formulario_registro.style.display = 'block'};
});

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
        const tcliente = document.getElementById('info_tcliente');

        try {
            const respuesta = await fetch(`/get_cliente?id=${id}`);
            if (respuesta.ok) {
                const cliente = await respuesta.json();
                id_readonly.value = id;
                nombre.value = cliente.nombre;
                correo.value = cliente.correo;
                telefono.value = cliente.telefono;
                direccion.value = cliente.direccion;
                tcliente.value = cliente.tipo_cliente;
            }
        } catch (error) {
            console.log(error);
        }
    });
});

document.getElementById('cancelar_info').addEventListener('click', ()=>{
    document.getElementById('formulario_actualizar').style.display = 'none';
});
