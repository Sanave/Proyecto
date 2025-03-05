// Agregar eventos
agregarEventos()

function agregarEventos(){
    const botones = document.querySelectorAll('.botonInfo');
    botones.forEach(boton => {
        boton.addEventListener('click', async () => {
            try{
                const idCompra = boton.getAttribute('valor');
                const respuesta = await fetch(`/get_compra?id=${idCompra}`)
                if(respuesta.ok){
                    const datosCompra = await respuesta.json();
                    console.log(datosCompra);
                    document.getElementById('fechaVenta').innerText = datosCompra.fecha_venta;
                    document.getElementById('nombreCliente').innerText = datosCompra.cliente.nombre;
                    document.getElementById('correoCliente').innerText = datosCompra.cliente.correo;
                    document.getElementById('telefonoCliente').innerText = datosCompra.cliente.telefono;
                    document.getElementById('direccionCliente').innerText = datosCompra.cliente.direccion;

                    const tabla = document.getElementById('tablaProductos');
                    tabla.innerHTML = '';
                    datosCompra.productos.forEach(producto =>{
                        const tr = document.createElement('tr');
                        const tdNombreProducto = document.createElement('td');
                        const tdPrecioProducto = document.createElement('td');
                        const tdCantidadProducto = document.createElement('td');
                        const tdTotal = document.createElement('td');

                        tdNombreProducto.innerText = producto.nombre;
                        tdPrecioProducto.innerText = producto.precio;
                        tdCantidadProducto.innerText = producto.cantidad;
                        tdTotal.innerText = producto.precio * producto.cantidad;

                        tr.append(tdNombreProducto, tdPrecioProducto, tdCantidadProducto, tdTotal);
                        tabla.append(tr);

                        document.getElementById('compra_total').innerText = datosCompra.total;

                    });
                    document.getElementById('seccion_detalles').style.display = 'block';
                }
            }
            catch(error){ console.log(error)}
        });
    });
};

//Boton de cerrar
document.getElementById('cerrar_ventana_detalles').addEventListener('click', ()=>{document.getElementById('seccion_detalles').style.display = 'none';});