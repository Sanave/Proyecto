// Cargar la tabla de productos
async function cargar_tabla(){
    const tabla = document.getElementById('tbody');
    try {
        const respuesta = await fetch('/get_productos');
        if (respuesta.ok){
            const productos = await respuesta.json();
            productos.forEach(producto => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${producto.id}</td>
                    <td>${producto.nombre}</td>
                    <td>${producto.precio}</td>
                    <td>${producto.codigo}</td>
                    <td>
                        <button class="btn btn-primary boton_info" value="${producto.id}">Info</button>
                    </td>
                `;
                tabla.appendChild(tr);
                info();
            });
        } else {
            console.log('depuración: respuesta no ok');
        }
    } catch (error) {
        console.log('depuración', error);
    }
};

// Guardar nuevo producto y recargar tabla
document.getElementById('guardar').addEventListener('click', async () => {
    const fnombre = document.getElementById('nombre').value;
    const fprecio = document.getElementById('precio').value;
    const fcodigo = document.getElementById('codigo').value;
    const tbody = document.getElementById('tbody');

    try {
        const respuesta = await fetch('/registrar_producto', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                nombre: fnombre,
                precio: fprecio,
                codigo: fcodigo
            })
        });

        if (respuesta.ok) {
            const resultado = await respuesta.json();
            alert(resultado.mensaje);
            document.querySelectorAll('form input').forEach(input => input.value = '');
            document.getElementById('subventana').style.display = 'none';
            tbody.innerHTML = '';
            cargar_tabla();
        } else {
            alert(resultado.mensaje);
        }
    } catch (error) {
        alert('Ha habido un error.');
        console.log('Ha habido un error.', error);
    }
});

// Mostrar información del producto en la ventana de actualizar
function info(){
    document.querySelectorAll('.boton_info').forEach(button => {
        button.addEventListener('click', async (e) => {
            const id = e.target.value;

            const nombre = document.getElementById('info_nombre');
            const precio = document.getElementById('info_precio');
            const codigo = document.getElementById('info_codigo');

            const n_nombre = document.getElementById('nuevo_nombre');
            const n_precio = document.getElementById('nuevo_precio');
            const n_codigo = document.getElementById('nuevo_codigo');

            try {
                const respuesta = await fetch(`/info_producto/${id}`);
                if (respuesta.ok) {
                    const datos = await respuesta.json();

                    nombre.setAttribute('data-id', datos.id);
                    nombre.innerHTML = datos.nombre;
                    precio.innerHTML = datos.precio;
                    codigo.innerHTML = datos.codigo;

                    n_nombre.value = datos.nombre;
                    n_precio.value = datos.precio;
                    n_codigo.value = datos.codigo;

                    document.getElementById('info_mensaje').style.display = 'none';
                    document.getElementById('info_contenido').style.display = 'block';
                }
            } catch (error) {
                console.log('depuración:', error);
                document.getElementById('info_mensaje').innerHTML = 'Ocurrió un error.';
            }
        });
    });
};

// Eliminar producto
document.getElementById('info_eliminar').addEventListener('click', async () => {
    const nombre = document.getElementById('info_nombre');
    const info_contenido = document.getElementById('info_contenido');
    const info_mensaje = document.getElementById('info_mensaje');
    const id = nombre.getAttribute('data-id');
    const tbody = document.getElementById('tbody');

    try {
        const respuesta = await fetch('/eliminar_producto', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ id: id })
        });

        if (respuesta.ok) {
            const datos = await respuesta.json();
            tbody.innerHTML = '';
            info_contenido.style.display = 'none';
            info_mensaje.style.display = 'block';
            cargar_tabla();
            alert(datos.mensaje);
        } else {
            console.log('depuración: hubo un error');
        }
    } catch (error) {
        console.log('depuración: hubo un error', error);
    }
});

// Actualizar producto
document.getElementById('actualizar_guardar').addEventListener('click', async () => {
    const ventana_actualizar = document.getElementById('subventana_actualizar');
    const nombre = document.getElementById('info_nombre');
    const id = nombre.getAttribute('data-id');
    const tbody = document.getElementById('tbody');
    const info_contenido = document.getElementById('info_contenido');
    const info_mensaje = document.getElementById('info_mensaje');

    const n_nombre = document.getElementById('nuevo_nombre').value;
    const n_precio = document.getElementById('nuevo_precio').value;
    const n_codigo = document.getElementById('nuevo_codigo').value;

    try {
        const respuesta = await fetch('/actualizar_producto', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                id: id,
                nombre: n_nombre,
                precio: n_precio,
                codigo: n_codigo
            })
        });

        if (respuesta.ok) {
            const datos = await respuesta.json();
            alert(datos.mensaje);
            ventana_actualizar.style.display = 'none';
            tbody.innerHTML = '';
            cargar_tabla();
            info_contenido.style.display = 'none';
            info_mensaje.style.display = 'block';
        } else {
            alert(datos.mensaje);
        }
    } catch (error) {
        console.log('depuración.', error);
    }
});

// --------------------------------
window.onload = () => { cargar_tabla() };



