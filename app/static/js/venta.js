
let carrito = {};
let total = 0;

agregarEvento();

// Nuevo código de prueba
function agregarEvento(){
    //Seleccionar formularios
    const formularios = document.getElementsByClassName('formulario_agregar');
    //Agregar evento a cada boton de cada formulario
    for ( let formulario of formularios){
        formulario.querySelector('.boton_agregar').addEventListener('click', async ()=>{
            //id y cantidad del producto
            const idProducto = formulario.querySelector('.id_producto').value;
            const cantidadProducto = formulario.querySelector('.cantidad').value;
            //return si la cantidad es 0
            if (cantidadProducto == 0){return};
            //fetch
            try{
                const respuesta = await fetch(`/get_producto?id=${idProducto}`);
                if(respuesta.ok){
                    const producto = await respuesta.json();
                    //carrito
                    if(producto.id in carrito){
                        carrito[Number(producto.id)] += Number(cantidadProducto);
                        document.getElementById(`c${producto.id}`).innerText = carrito[producto.id];
                    }
                    else{
                        carrito[producto.id] = Number(cantidadProducto);
                        
                        
                        let tr = document.createElement('tr');
                        let tdNombre = document.createElement('td');
                        let tdPrecio = document.createElement('td');
                        let tdCantidad = document.createElement('td');
                        tdNombre.innerText = producto.nombre;
                        tdPrecio.innerText = producto.precio;
                        tdCantidad.innerText = cantidadProducto;
                        tdCantidad.id = `c${producto.id}`;
                        tr.appendChild(tdNombre);
                        tr.appendChild(tdPrecio);
                        tr.appendChild(tdCantidad);
                        document.getElementById('tabla_seleccionados').appendChild(tr);

                    }
                    total += producto.precio * cantidadProducto;
                    document.getElementById('total').innerText = total + ' $';
                }
            }catch(error){console.log(error)};
        });
    };
};



// Tabla de busqueda
document.getElementById('boton_buscar').addEventListener('click', async () => {
    let formulario = document.getElementById('formulario_busqueda');

    try{
        const opcion_busqueda = formulario.opcion_busqueda.value;
        const producto_busqueda = formulario.producto.value;

        const respuesta = await fetch(`/get_producto_busqueda?producto=${producto_busqueda}&opcion_busqueda=${opcion_busqueda}`);
        if (respuesta.ok){
            const producto = await respuesta.json();
            const tabla = document.getElementById('tabla_busqueda');
            tabla.innerHTML = '';
            const tr = document.createElement('tr');
            const td = document.createElement('td');
            //Crear los campos de la tabla
            const tdNombre = document.createElement('td');
            const tdCodigo = document.createElement('td');
            const tdPrecio = document.createElement('td');
            const tdFormulario = document.createElement('td');
            //Asignar valores a la tabla
            tdNombre.innerText = producto.nombre;
            tdCodigo.innerText = producto.codigo;
            tdPrecio.innerText = producto.precio;
            //Crear formulario e inputs
            const form = document.createElement('form');
            const inputId = document.createElement('input');
            const inputCantidad = document.createElement('input');
            const boton = document.createElement('button');
            boton.innerText = 'Agregar';
            form.className = 'formulario_agregar'
            //Asignar atributos
            inputId.type = 'text';
            inputId.className = 'id_producto';
            inputId.value = producto.id;
            inputId.name = 'id_producto';
            inputId.readOnly = 'true';
            inputId.style.display = 'none';

            inputCantidad.type = 'number';
            inputCantidad.min = '0';
            inputCantidad.max = '100';
            inputCantidad.className = 'cantidad';

            boton.type = 'button';
            boton.className = 'btn btn-success boton_agregar';
            //Agregar todo a la tabla
            form.append(inputId, inputCantidad, boton);
            tdFormulario.appendChild(form);
            tr.append(tdNombre, tdCodigo, tdPrecio, tdFormulario);
            tabla.appendChild(tr);

            agregarEvento();

            

        }
        else{
            console.log('Hubo un error.');
        }
    }catch (error){
        console.log(error);
    };
});

// Pantalla de confirmación de pedido
document.getElementById('boton_guardar').addEventListener('click', async ()=> {
    const cliente = document.getElementById('cliente_id').getAttribute('cliente');
    const pantalla = document.getElementById('pantallaNegra');
    try{
        const respuesta = await fetch(`/venta_confirmacion?cliente=${cliente}&carrito=${JSON.stringify(carrito)}`);
        if (respuesta.ok){
            // Datos del cliente
            const datos = await respuesta.json();
            console.log(datos.productos.length);
            const datosCliente = document.getElementById('confirmacion_cliente_datos');
            datosCliente.innerHTML = '';
            const titulo = document.createElement('h3');
            titulo.innerText = 'Datos de compra'
            const pNombre = document.createElement('p');
            const pTelefono = document.createElement('p');
            const pDireccion = document.createElement('p');
            pNombre.innerText = `Nombre del cliente: ${datos.cliente.nombre}`;
            pDireccion.innerText = `Dirección de envío: ${datos.cliente.direccion}`;
            pTelefono.innerText = `Teléfono: ${datos.cliente.telefono}`;

            datosCliente.append(titulo, pNombre, pDireccion, pTelefono);
            // Datos de productos
            const tabla_confirmacion = document.getElementById('tabla_confirmacion');
            for (key in datos.productos){
                if (datos.productos.hasOwnProperty(key)){
                    const producto = datos.productos[key];
                    const tr = document.createElement('tr');
                    const tdNombreProducto = document.createElement('td');
                    const tdCodigoProducto = document.createElement('td');
                    const tdPrecioProducto = document.createElement('td');
                    const tdCantidad = document.createElement('td');
                    const tdPrecioTotalProducto = document.createElement('td');
                    tdNombreProducto.innerText = producto.nombre;
                    tdCodigoProducto.innerText = producto.codigo;
                    tdPrecioProducto.innerText = producto.precio + ' $';
                    tdCantidad.innerText = producto.cantidad;
                    tdPrecioTotalProducto.innerText = producto.cantidad_total;
    
                    tr.append(tdNombreProducto, tdCodigoProducto, tdPrecioProducto, tdCantidad, tdPrecioTotalProducto);
                    tabla_confirmacion.append(tr);
                    document.getElementById('confirmacion_total').innerText = `Total : ${datos.total} $`;
                }
               

            }

            pantalla.style.display = 'flex';
        }
        
    }
    catch(error){console.log(error)};

    
    
});

document.getElementById('boton_cancelar_confirmacion').addEventListener('click', ()=> {
    const pantalla = document.getElementById('pantallaNegra');
    document.getElementById('tabla_confirmacion').innerHTML = '';
    if (pantalla.style.display = 'flex'){
        pantalla.style.display = 'none';
    };
});

// Finalizar confirmacion
document.getElementById('boton_finalizar_confirmacion').addEventListener('click', async ()=>{
    const clienteId = document.getElementById('cliente_id').getAttribute('cliente');
    try{
        const respuesta = await fetch('/registrar_venta', {
            method : 'POST',
            headers : {'Content-Type': 'application/json'},
            body : JSON.stringify({
                id_cliente : clienteId,
                productos : carrito
            })
        })

        if (respuesta.ok){
            const mensaje = await respuesta.json()
            console.log(mensaje)
        }
        else{
            const mensaje = await respuesta.json()
            console.log(mensaje)
        }
    }
    catch(error){
        console.log(error)
    }
});
