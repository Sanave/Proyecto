// Display de formulario de registro
document.getElementById('registrar').addEventListener('click', ()=> {
   // document.getElementById('formulario_registro').style.display = 'block';
    const formulario_registro = document.getElementById('formulario_registro');
    if (formulario_registro.style.display == 'block'){ formulario_registro.style.display = 'none'}
    else{formulario_registro.style.display = 'block'};
});

document.getElementById('cancelar').addEventListener('click', () => {
    document.getElementById('formulario_registro').style.display = 'none';
});



// CARGAR TABLAS
/*async function cargar_tabla(){
    const tabla = document.getElementById('tbody');
    try {
        respuesta = await fetch('/get_clientes');
        if (respuesta.ok){
            const clientes = await respuesta.json();
            clientes.forEach(cliente =>{
                const tr = document.createElement('tr');
                tr.innerHTML = `
                <td>${cliente.id}</td>
                <td>${cliente.nombre}</td>
                <td>${cliente.correo}</td>
                <td>${cliente.telefono}</td>
                <td>${cliente.direccion}</td>
                <td>${cliente.estado}</td>
                <td><form action="${eliminarClienteUrl}" method="post">
                        <td><button class="btn btn-danger" name="id" value="${cliente.id}">X</button></td>
                    </form></td>
                `;
                tabla.appendChild(tr);

            });
        }else{
            console.log('No se cargaron las tablas');
        }
    } catch (error) {
        console.log('depuracion', error);
    }
};*/


// GUARDAR CLIENTE Y RECARGAR PÁGINA
/*document.getElementById('guardarr').addEventListener('click', async () => {
    const fnombre = document.getElementById('nombre').value;
    const fcorreo = document.getElementById('correo').value;
    const ftelefono = document.getElementById('telefono').value;
    const fdireccion = document.getElementById('direccion').value;
    const ftipo_cliente = document.getElementById('tcliente').value;
    const tbody = document.getElementById('tbody');

    try{
        respuesta = await fetch('/registrar_cliente', {
            method : 'POST', 
            headers : {'Content-Type': 'application/json'},
            body : JSON.stringify({
                nombre : fnombre,
                correo : fcorreo,
                telefono : ftelefono,
                direccion : fdireccion,
                tipo_cliente : ftipo_cliente
            })
        });

        
        if (respuesta.ok){
            const resultado = await respuesta.json();
            alert(resultado.mensaje);
            const inputs = document.querySelectorAll('form input');
            inputs.forEach(input => input.value = '');
            document.getElementById('formulario_registro').style.display = 'none';
            tbody.innerHTML = '';
            location.reload();
        }else{
            alert(resultado.mensaje);
        }
    }catch(error){
        alert('Ha habido un error.');
        console.log('Ha habido un error.', error);
    }
});
*/

// MOSTRAR INFORMACIÓN DEL CLIENTE Y DATOS EN LA VENTANA DE ACTUALIZAR DATOS
/*function info(){
    document.querySelectorAll('.boton_info').forEach(button =>{button.addEventListener('click', async (e) =>{
        const id = e.target.value;
        
        const nombre = document.getElementById('info_nombre');
        const direccion = document.getElementById('info_direccion');
        const correo = document.getElementById('info_correo');
        const telefono = document.getElementById('info_telefono');
        const tipo_cliente = document.getElementById('info_tipo_cliente');

        const n_nombre = document.getElementById('nuevo_nombre');
        const n_direccion = document.getElementById('nuevo_direccion');
        const n_correo = document.getElementById('nuevo_correo');
        const n_telefono = document.getElementById('nuevo_telefono');
        const n_tipo_cliente = document.getElementById('nuevo_tcliente');
    
        try {
            const respuesta = await fetch(`/info_cliente/${id}`);
            if (respuesta.ok){
                const datos = await respuesta.json();
    
                nombre.setAttribute('data-id', datos.id);
                nombre.innerHTML = datos.nombre;
                direccion.innerHTML = datos.direccion;
                correo.innerHTML = datos.correo;
                telefono.innerHTML = datos.telefono;
                tipo_cliente.innerHTML = datos.tipo_cliente;

                n_nombre.value = datos.nombre;
                n_direccion.value = datos.direccion;
                n_correo.value = datos.correo;
                n_telefono.value = datos.telefono;
                n_tipo_cliente.value = datos.tipo_cliente;

    
                document.getElementById('info_mensaje').style.display = 'none';
                document.getElementById('info_contenido').style.display = 'block'
    
            }
            
        } catch (error) {
            console.log('depuracion:', error)
            document.getElementById('info_mensaje').innerHTML = 'Ocurrió un error.';
        }
        });
    });
};


// ELIMIINAR CLIENTE
document.getElementById('info_eliminar').addEventListener('click', async () =>{
    const nombre = document.getElementById('info_nombre');
    const info_contenido = document.getElementById('info_contenido');
    const info_mensaje = document.getElementById('info_mensaje');
    const id = nombre.getAttribute('data-id');
    const tbody = document.getElementById('tbody');

    try {
        const respuesta = await fetch('eliminar_cliente', {
            method : 'POST', 
            headers : {'Content-Type': 'application/json'},
            body : JSON.stringify({
                id : id
            })

        });

        if (respuesta.ok){
            const datos = await respuesta.json();
            tbody.innerHTML = '';
            info_contenido.style.display = 'none'
            info_mensaje.style.display = 'block';

            cargar_tabla();
            alert(datos.mensaje)
            console.log('depuracion: cliente eliminado')
        }else{
            console.log('depuracion: hubo un error')
        }
    } catch (error) {
        console.log('depuracion: hubo un error', error)
    }
});

// ACTUALIZAR INFORMACIÓN DEL CLIENTE
document.getElementById('actualizar_guardar').addEventListener('click', async () =>{
    const ventana_actualizar = document.getElementById('subventana_actualizar')
    const nombre = document.getElementById('info_nombre');
    const id = nombre.getAttribute('data-id');
    const tbody = document.getElementById('tbody');
    const info_contenido = document.getElementById('info_contenido');
    const info_mensaje = document.getElementById('info_mensaje');

    const n_nombre = document.getElementById('nuevo_nombre').value;
    const n_direccion = document.getElementById('nuevo_direccion').value;
    const n_correo = document.getElementById('nuevo_correo').value;
    const n_telefono = document.getElementById('nuevo_telefono').value;
    const n_tipo_cliente = document.getElementById('nuevo_tcliente').value;

    try {
        respuesta = await fetch('/actualizar_cliente', {
            method : "POST",
            headers : {'Content-Type': 'application/json'},
            body : JSON.stringify({
                id : id,
                nombre : n_nombre,
                direccion : n_direccion,
                correo : n_correo,
                telefono : n_telefono,
                tipo_cliente : n_tipo_cliente
            })
        });
        if (respuesta.ok){
            const datos = await respuesta.json();
            alert(datos.mensaje);
            ventana_actualizar.style.display = 'none';
            tbody.innerHTML = '';
            cargar_tabla();
            info_contenido.style.display = 'none';
            info_mensaje.style.display = 'block';

        }else{
            alert(datos.mensaje);
        }
    } catch (error) {
        console.log('depuracion.', error)
    }
});
// ------------------------
window.onload = () => {cargar_tabla()};
*/