
if (window.location.pathname === '/facturas') {
    
} else {
    
    document.getElementById('cancelar').addEventListener('click', () => document.getElementById('subventana').style.display = 'none');
    document.getElementById('registrar').addEventListener('click', () => document.getElementById('subventana').style.display = 'block');
    document.getElementById('actualizar_cancelar').addEventListener('click', () => document.getElementById('subventana_actualizar').style.display = 'none');
    document.getElementById('actualizar_info').addEventListener('click', () => document.getElementById('subventana_actualizar').style.display = 'block');
}