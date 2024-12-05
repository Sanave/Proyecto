//Mostrar facturas
async function cargar_tabla(){
    const tbody = document.getElementById('tbody');
    try {
        respuesta = await fetch('/get_facturas');
        if (respuesta.ok){
            const facturas = await respuesta.json();
            facturas.forEach(factura => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                <td>${factura.id}</td>
                <td>${factura.numero_factura}</td>
                <td>${factura.fecha_emision}</td>
                <td>${factura.id_cliente}</td>
                <td>${factura.total}</td>
                <td><button class="btn btn-primary factura_info" value="${factura.id}">Info</button></td>
                `;
                tbody.appendChild(tr);
                
            });
            agregarEventosInfo();
        }
    } catch (error) {
        console.log(error);
    }
};

// Botones info factura
function agregarEventosInfo() {
    document.querySelectorAll('.factura_info').forEach(button => {
        button.addEventListener('click', async (e) => {
            const id = e.target.value;
            const codigo = document.getElementById('info_codigo');
            const fecha = document.getElementById('info_fecha');
            const cliente = document.getElementById('info_cliente');
            const compra = document.getElementById('info_id_compra');
            const total = document.getElementById('info_total');

            try {
                const respuesta = await fetch(`/info_factura?id=${id}`);
                if (respuesta.ok) {
                    const factura = await respuesta.json();
                    codigo.innerHTML = factura.numero_factura;
                    fecha.innerHTML = factura.fecha_emision;
                    cliente.innerHTML = factura.id_cliente;
                    compra.innerHTML = factura.id_compra;
                    total.innerHTML = factura.total;

                    document.getElementById('info_mensaje').style.display = 'none';
                    document.getElementById('info_contenido').style.display = 'block';
                } else {
                    console.log('depuracion: respuesta no ok');
                }
            } catch (error) {
                console.log('depuracion:', error);
                document.getElementById('info_mensaje').innerHTML = 'Ocurrió un error.';
            }
        });
    });
}

//-----------------------------
window.onload = () => {cargar_tabla()};