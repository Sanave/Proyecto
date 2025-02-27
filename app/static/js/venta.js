
let carrito = {};
let total = 0;

// Evento de botones y tabla de resumen de compra
let formularios = document.getElementsByClassName('formulario_agregar');
for ( let formulario of formularios){
    formulario.querySelector('.boton_agregar').addEventListener('click', async (evento) =>{
        const idProducto = formulario.querySelector('.id_producto').value;
        const cantidadProducto = formulario.querySelector('.cantidad').value;
        const resumen = document.getElementById('resumen');
        if (cantidadProducto == 0){return};

        try{
            const respuesta = await fetch(`/get_producto?id=${idProducto}`);
            if(respuesta.ok){

                const producto = await respuesta.json();
                if (producto.id in carrito){
                    carrito[Number(producto.id)] += Number(cantidadProducto);
                    console.log(carrito);
                }
                else{
                    carrito[producto.id] = Number(cantidadProducto);
                    console.log(carrito);
                    let tr = document.createElement('tr');
                    let tdNombre = document.createElement('td');
                    let tdPrecio = document.createElement('td');
                    let tdCantidad = document.createElement('td');
                    tdCantidad.cantidad = cantidadProducto;
                    tdNombre.innerText = producto.nombre;
                    tdPrecio.innerText = producto.precio;
                    tdCantidad.innerText = cantidadProducto;
                    tr.appendChild(tdNombre);
                    tr.appendChild(tdPrecio);
                    tr.appendChild(tdCantidad);
                    document.getElementById('tabla_seleccionados').appendChild(tr);

                    
                }

                total += producto.precio * cantidadProducto;
                document.getElementById('total').innerText = total + ' $';

                

            }
        }
        catch (error){
            console.log(error);
        }
    });
};