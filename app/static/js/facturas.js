agregarEventos()

function agregarEventos(){
    const botones = document.querySelectorAll('.boton_info');
    botones.forEach(boton =>{
        boton.addEventListener('click', async ()=>{
            const idFactura = boton.getAttribute('value');
            const infoFactura = document.getElementById('informacion_factura');
            try{
                const respuesta = await fetch(`/get_factura?id=${idFactura}`);
                if (respuesta.ok){
                    const factura = await respuesta.json();

                    infoFactura.innerHTML = '';

                    pNumeroFactura = document.createElement('p');
                    pFecha = document.createElement('p');
                    pTotal = document.createElement('p');
                    pCliente = document.createElement('p');

                    pNumeroFactura.innerText ='Numero de factura: ' + factura.numero_factura;
                    pFecha.innerText = 'Fecha de facturación: ' + factura.fecha_emision;
                    pTotal.innerText = 'Total: ' + factura.total;
                    pCliente.innerText = 'Cliente: ' + factura.cliente.nombre;

                    infoFactura.append(pNumeroFactura, pFecha, pCliente, pTotal);
                    document.getElementById('pantallaNegra').style.display = 'block';
                    
                    const tabla = document.getElementById('tabla_detalles_factura');
                    tabla.innerHTML = '';
                    factura.productos.forEach(facturaProducto => {
                        const tr = document.createElement('tr');
                        const tdNombre = document.createElement('td');
                        const tdCodigo = document.createElement('td');
                        const tdPrecio = document.createElement('td');
                        const tdCantidad = document.createElement('td');
                        const tdTotal = document.createElement('td');

                        tdNombre.innerText = facturaProducto.producto.nombre;
                        tdCodigo.innerText = facturaProducto.producto.codigo;
                        tdPrecio.innerText = facturaProducto.producto.precio;
                        tdCantidad.innerText = facturaProducto.cantidad;
                        tdTotal.innerText = facturaProducto.producto.precio * facturaProducto.cantidad;

                        tr.append(tdNombre, tdCodigo, tdPrecio, tdCantidad, tdTotal);
                        tabla.append(tr);
                    });
                    

                }
                else{
                    console.log('Hubo un error.');
                }
            }
            catch(e){
                console.log(e);
            }
        })
    });

}

document.getElementById('boton_cancelar').addEventListener('click', ()=>{
    document.getElementById('pantallaNegra').style.display = 'none';
});