//Agregar productos a la lista de selección
let lista = [];
let total = 0;
document.getElementById('agregar_producto').addEventListener('click', async () =>{
    const tbody_seleccionados = document.getElementById('tbody_seleccionados');
    const productos_seleccion = document.getElementById('productos_seleccion').value;
    const total_venta = document.getElementById('total_venta');

    try {
        respuesta = await fetch(`get_producto?id=${productos_seleccion}`)
        if (respuesta.ok){
            const producto = await respuesta.json();
            const tr = document.createElement('tr');
            tr.innerHTML = `
            <td>${producto.nombre}</td>
            <td>${producto.codigo}</td>
            <td>${producto.precio}</td>
            `;
            lista.push(producto.id);
            tbody_seleccionados.appendChild(tr);
            total += parseInt(producto.precio);
            const formato = new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(total);
            total_venta.innerHTML = formato;

        };
    } catch (error) {
        console.log(error);
    }
});

//Registrar venta
document.getElementById('guardar').addEventListener('click', async () =>{
    const productos = lista;
    const cliente = document.getElementById('cliente').value;
    const total_venta = total;

    try {
        respuesta = await fetch('/registrar_venta', {
            method : "POST",
            headers : {'Content-Type': 'application/json'},
            body : JSON.stringify({
                productos : productos,
                id_cliente : cliente,
                total : total_venta
            })
        });

        if (respuesta.ok){
            const datos = await respuesta.json();
            console.log('depuracion. la venta se ha registrado');
            document.getElementById('subventana').style.display = 'none';
            window.location.href = '/compras';

            alert('La compra se ha registrado.')
        }else{
            console.log('depuracion: la venta no se pudo registrar');
            //alert(datos.mensaje);
        }
    } catch (error) {
        console.log('error: ', error);
    }
});